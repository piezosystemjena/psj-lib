from .piezo_capability import PiezoCapability

class MultiSetpoint(PiezoCapability):
    """Capability for devices with multiple independent setpoints.
    
    Some devices allow synchronous control of multiple channel setpoints.
    This capability provides a unified interface for setting these setpoints together, 
    ensuring coordinated updates and consistent timing.
    """

    CMD_SETPOINTS = "SETPOINTS"

    _channel_count = 0

    def __init__(
        self, 
        *args,
        channel_count: int,
        **kwargs
    ) -> None:
        """Initialize multi-setpoint capability.

        Args:
            channel_count: Expected number of setpoint values for ``set()``.
        """
        super().__init__(*args, **kwargs)
        self._channel_count = channel_count

    async def set(self, setpoints: list[float]) -> None:
        """Set multiple channel setpoints simultaneously.
        
        Args:
            setpoints: List of setpoint values for each channel. Length must match device's channel count.
        
        Example:
            >>> await multi_setpoint.set([1.0, 2.0, 3.0])  # Set 3 channels at once
        """
        if len(setpoints) != self._channel_count:
            raise ValueError(f"Expected {self._channel_count} setpoints, got {len(setpoints)}")
        
        await self._write(self.CMD_SETPOINTS, setpoints)
