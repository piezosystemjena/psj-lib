from .transport_protocol import TRANSPORT_REGISTRY, TransportProtocol
from .transport_types import DetectedDevice

class TransportFactory:
    @staticmethod
    def from_detected_device(detected_device: DetectedDevice) -> "TransportProtocol":
        """
        Creates and returns a transport protocol instance based on the detected device's transport type.
        """

        if detected_device.transport not in TRANSPORT_REGISTRY:
            raise ValueError(f"Unsupported transport type: {detected_device.transport}")

        return TRANSPORT_REGISTRY[detected_device.transport](detected_device.identifier)
    

    @staticmethod
    def from_transport_type(transport_type: str, identifier: str) -> "TransportProtocol":
        """
        Creates and returns a transport protocol instance based on the specified transport type.
        """

        if transport_type not in TRANSPORT_REGISTRY:
            raise ValueError(f"Unsupported transport type: {transport_type}")

        return TRANSPORT_REGISTRY[transport_type](identifier)