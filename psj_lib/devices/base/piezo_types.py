from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional

from ..transport_protocol import TransportProtocolInfo


class SensorType(Enum):
    NONE = 0
    STRAIN_GAUGE = 1
    CAPACITIVE = 2
    INDUCTIVE = 3
    UNKNOWN = 99


class ActorType(Enum):
    NANOX = 0
    PSH = 1
    PARALLEL = 2
    UNKNOWN = 99


@dataclass
class DeviceInfo:
    """
    Represents information about a device, including its transport type, identifier, and optional metadata.

    Attributes:
        transport (TransportType): The type of transport used to communicate with the device.
        identifier (str): The primary identifier for the device (e.g., IP address or serial port).
        mac (Optional[str]): The MAC address of the device, if available.
        device_id (Optional[str]): A unique identifier for the device, if available.
    """
    transport_info: TransportProtocolInfo
    device_id: Optional[str] = None  # Unique identifier for the device, if available
    extended_info: Dict[str, str] = field(default_factory=dict)

    def __str__(self):
        """
        Returns a string representation of the transport type, capitalized.
        """
        device_info = f"{self.transport_info}"
        if self.device_id:
            device_info += f" - {self.device_id}"
        if self.extended_info:
            return f"{device_info} - {self.extended_info}"
        else:
            return device_info