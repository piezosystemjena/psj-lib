from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional


class ProtocolException(Exception):
    """Exception raised for errors in the transport protocol communication."""

    pass


class DeviceUnavailableException(ProtocolException):
    """Exception raised when a device is unavailable or cannot be accessed."""

    pass


class TimeoutException(ProtocolException):
    """Exception raised when a communication timeout occurs."""

    pass


class TransportType(str, Enum):
    """
    Enumeration of supported transport types for device communication.

    Attributes:
        TELNET: Represents the Telnet protocol for network communication.
        SERIAL: Represents serial communication (e.g., RS-232).
    """
    TELNET = "telnet"
    SERIAL = "serial"

    def __str__(self):
        """
        Returns a string representation of the transport type, capitalized.
        """
        return self.name.capitalize()


@dataclass
class TransportProtocolInfo:
    """
    Represents the protocol information for a transport type.
    """
    transport: TransportType
    identifier: str  # e.g., IP or serial port
    mac: Optional[str] = None

    def __str__(self):
        """
        Returns a string representation of the TransportProtocolInfo.
        """
        return f"{self.transport} @ {self.identifier}"


@dataclass
class DetectedDevice:
    """
    Represents a device detected on the network or via serial connection

    Attributes:
        transport (TransportType): The transport type used to communicate with the device (e.g., Ethernet, Serial).
        identifier (str): A unique identifier for the device, such as an IP address or serial port name.
        mac (Optional[str]): The MAC address of the device, if available.
        device_id (Optional[str]): A unique identifier for the device, if available. such as NV200/D_NET
        device_info: Dictionary with additional information about the device, such as actuator name and serial number.
    """
    transport: TransportType
    identifier: str  # e.g., IP or serial port
    mac: Optional[str] = None
    device_id: Optional[str] = None  # Unique identifier for the device, if available
    device_info: Dict[str, str] = field(default_factory=dict)

    def __str__(self):
        """
        Returns a string representation of the transport type, capitalized.
        """
        result = f"{self.transport} @ {self.identifier}"
        if self.mac:
            result += f" (MAC: {self.mac})"

        if self.device_id:
            result += f" - {self.device_id}"

        if self.device_info:
            return f"{result} - {self.device_info}"

        return result