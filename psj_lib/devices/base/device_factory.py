from ..transport_protocol import DetectedDevice
from .piezo_device import PiezoDevice

# Device model registry
DEVICE_MODEL_REGISTRY = {}


class DeviceFactory:
    @staticmethod
    def from_id(device_id: str, *args, **kwargs) -> PiezoDevice:
        """
        Creates and returns an instance of a device class corresponding to the given device ID.

        Args:
            device_id (str): The identifier for the device model to instantiate.
            *args: Positional arguments to pass to the device class constructor.
            **kwargs: Keyword arguments to pass to the device class constructor.

        Returns:
            PiezoDevice: An instance of the device class associated with the given device ID.

        Raises:
            ValueError: If the provided device_id is not supported or not found in the registry.
        """
        cls = DEVICE_MODEL_REGISTRY.get(device_id)

        if cls is None:
            raise ValueError(f"Unsupported device ID: {device_id}")

        return cls(*args, **kwargs)

    @staticmethod
    def from_detected_device(detected_device: DetectedDevice) -> PiezoDevice:
        """
        Creates a device object from the given DetectedDevice parameters.
        """
        if not detected_device:
            raise ValueError("No detected device provided.")

        return DeviceFactory.from_id(
            detected_device.device_id,
            transport_type=detected_device.transport,
            identifier=detected_device.identifier
        )