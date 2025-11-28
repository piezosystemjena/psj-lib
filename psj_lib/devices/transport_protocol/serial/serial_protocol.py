import asyncio
import logging
from typing import List

import aioserial
import serial.tools.list_ports

from ..transport_protocol import DiscoveryCallback, TransportProtocol
from ..transport_types import (
    DetectedDevice,
    DeviceUnavailableException,
    TransportProtocolInfo,
    TransportType,
)


# Global module locker
logger = logging.getLogger(__name__)

class SerialProtocol(TransportProtocol):
    """
    A class to handle serial communication with an NV200 device using the AioSerial library.
    Attributes:
        port (str): The serial port to connect to. Defaults to None. If port is None, the class
        will try to auto detect the port.
        baudrate (int): The baud rate for the serial connection. Defaults to 115200.
        serial (AioSerial): The AioSerial instance for asynchronous serial communication.
    """   

    TRANSPORT_TYPE = TransportType.SERIAL

    def __init__(
        self,
        identifier: str,
        baudrate: int = 115200
    ):
        """
        Initializes the NV200 driver with the specified serial port settings.

        Args:
            port (str, optional): The serial port to connect to. Defaults to None.
                                  If port is None, the class will try to auto detect the port.
            baudrate (int, optional): The baud rate for the serial connection. Defaults to 115200.
        """
        super().__init__(identifier)
        self.__serial: aioserial.AioSerial | None = None
        self.__port: str | None = identifier
        self.__baudrate: int = baudrate

    @property
    def serial(self) -> aioserial.AioSerial | None:
        """
        Provides access to the internal AioSerial interface.
        Returns:
            AioSerial: The internal AioSerial instance.
        """
        return self.__serial

    @staticmethod
    async def discover_devices(discovery_cb: DiscoveryCallback) -> List[DetectedDevice]:
        """
        Asynchronously discovers all devices connected via serial interface.

        Returns:
            list: A list of serial port strings where a device has been detected.
        """
        ports = serial.tools.list_ports.comports()
        valid_ports = [p.device for p in ports if p.manufacturer == "FTDI"]

        async def detect_on_port(port_name: str) -> DetectedDevice | None:
            protocol = SerialProtocol(port_name)
            try:
                detected_device = DetectedDevice(
                    transport=TransportType.SERIAL,
                    identifier=port_name
                )
                await protocol.connect()
                is_type = await discovery_cb(protocol, detected_device)

                if not is_type:
                    return None
                
                return detected_device
            except Exception as e:
                # We do ignore the exception - if it is not possible to connect to the device, we just return None
                logger.info(f"Error on port {port_name}: {e.__class__.__name__} {e}")
                return None
            finally:
                await protocol.close()

        # Run all detections concurrently
        tasks = [detect_on_port(port) for port in valid_ports]
        results = await asyncio.gather(*tasks)
        # Filter out Nones
        return [dev for dev in results if dev]

    async def connect(self, auto_adjust_comm_params: bool = True):
        """
        Establishes an asynchronous connection to the NV200 device using the specified serial port settings.

        This method initializes the serial connection with the given port, baud rate, and flow control settings.
        If the port is not specified, it attempts to automatically detect the NV200 device's port. If the device
        cannot be found, a RuntimeError is raised.

        Raises:
            RuntimeError: If the NV200 device cannot be detected or connected to.
        """
        if self.__port is None:
            raise DeviceUnavailableException("No serial port specified for connection.")

        self.__serial = aioserial.AioSerial(port=self.__port, xonxoff=False, baudrate=self.__baudrate)

    async def flush_input(self):
        """
        Discard all available input within a short timeout window.
        """
        self.__serial.reset_input_buffer()


    async def write(self, cmd: str):
        await self.flush_input()
        await self.__serial.write_async(cmd.encode('latin1'))

    async def read_until(self, expected: bytes = TransportProtocol.XON, timeout: float = TransportProtocol.DEFAULT_TIMEOUT_SECS) -> str:
        data = await asyncio.wait_for(self.__serial.read_until_async(expected), timeout)
        # return data.replace(TransportProtocol.XON, b'').replace(TransportProtocol.XOFF, b'') # strip XON and XOFF characters
        return data.decode('latin1').strip("\x11\x13")  # strip XON and XOFF characters

    async def close(self):
        if self.__serial:
            self.__serial.close()

    @property
    def port(self) -> str:
        """
        Returns the serial port the device is connected to
        """
        return self.__port

    @property
    def is_connected(self) -> bool:
        """
        Returns whether the serial connection is established.
        """
        return self.__serial is not None and self.__serial.is_open

    def get_info(self) -> TransportProtocolInfo:
        """
        Returns metadata about the transport protocol, such as type and identifier.
        """
        return TransportProtocolInfo(
            transport=TransportType.SERIAL,
            identifier=self.__port,
        )