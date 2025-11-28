import logging
from abc import ABC, abstractmethod
from typing import Awaitable, Callable

from .transport_types import DetectedDevice, TransportProtocolInfo, TransportType

# Global module locker
logger = logging.getLogger(__name__)

# Async function to enrich discovered device with device information
type DiscoveryCallback = Callable[
    [TransportProtocol, DetectedDevice],
    Awaitable[bool]
]

# Registry for transport protocol implementations
TRANSPORT_REGISTRY: dict[TransportType, type["TransportProtocol"]] = {}


class TransportProtocol(ABC):
    """
    Abstract base class representing a transport protocol interface for a device.
    """
    XON = b'\x11'
    XOFF = b'\x13'
    LF = b'\x0A'
    CR = b'\x0D'
    CRLF = b'\x0D\x0A'
    DEFAULT_TIMEOUT_SECS = 0.6

    TRANSPORT_TYPE: TransportType | None = None  # To be set in subclasses

    def __init__(
        self,
        identifier: str
    ):
        """
        Initializes the TransportProtocol base class.
        Subclasses may extend this constructor to initialize protocol-specific state.
        """
        self.rx_delimiter = TransportProtocol.XON  # Default delimiter for reading messages

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.TRANSPORT_TYPE:
            TRANSPORT_REGISTRY[cls.TRANSPORT_TYPE] = cls

    @abstractmethod
    async def discover_devices(self, discovery_cb: DiscoveryCallback) -> list[DetectedDevice]:
        """
        Asynchronously discovers devices available via this transport protocol.

        Returns:
            list[DetectedDevice]: A list of detected devices.
        """

    @abstractmethod
    async def connect(self, auto_adjust_comm_params: bool = True):
        """
        Establishes an asynchronous connection to the NV200 device.

        This method is intended to handle the initialization of a connection
        to the NV200 device. The implementation should include the necessary
        steps to ensure the connection is successfully established.

        Raises:
            Exception: If the connection fails or encounters an error.
        """

    async def read_message(self, timeout: float = DEFAULT_TIMEOUT_SECS) -> str:
        """
        Asynchronously reads a complete delimited message from the device

        Returns:
            str: The response read from the source.
        """
        return await self.read_until(self.rx_delimiter, timeout)

    @abstractmethod
    async def read_until(self, expected: bytes = XON, timeout: float = DEFAULT_TIMEOUT_SECS) -> str:
        """
        Asynchronously reads data from the connection until the specified expected byte sequence is encountered.

        Args:
            expected (bytes, optional): The byte sequence to read until. Defaults to serial.XON.

        Returns:
            str: The data read from the serial connection, decoded as a string, .
        """

    @abstractmethod
    def get_info(self) -> TransportProtocolInfo:
        """
        Returns metadata about the transport protocol, such as type and identifier.
        """

    @abstractmethod
    async def flush_input(self):
        """
        Asynchronously flushes or clears the input buffer of the transport protocol.

        This method is intended to remove any pending or unread data from the input stream,
        ensuring that subsequent read operations start with a clean buffer. It is typically
        used to prevent processing of stale or unwanted data.
        """

    @abstractmethod
    async def write(self, cmd: str):
        """
        Sends a command to the NV200 device asynchronously.

        Args:
            cmd (str): The command string to be sent to the device.

        Raises:
            Exception: If there is an error while sending the command.
        """

    @abstractmethod
    async def close(self):
        """
        Asynchronously closes the connection or resource associated with this instance.

        This method should be used to release any resources or connections
        that were opened during the lifetime of the instance. Ensure that this
        method is called to avoid resource leaks.

        Raises:
            Exception: If an error occurs while attempting to close the resource.
        """

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Checks if the transport protocol is currently connected.

        Returns:
            bool: True if connected, False otherwise.
        """
