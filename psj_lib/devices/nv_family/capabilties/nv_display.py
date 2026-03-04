from ...base.capabilities import Display

class NVDisplay(Display):
    _cached_brightness: float = 0.0
    """NV does not support querying brightness, so we cache the last set value for retrieval."""

    async def set(
        self,
        brightness: float | None = None,
    ) -> None:
        if brightness is not None:
            if not (0.0 <= brightness <= 100.0):
                raise ValueError("Brightness must be between 0 and 100")
            
            nv_brightness = self._convert_brightness(brightness)
            await self._write(self.CMD_BRIGHTNESS, [nv_brightness])
            self._cached_brightness = brightness

    async def get_brightness(self) -> float:
        return self._cached_brightness
    
    def _convert_brightness(self, brightness: float) -> int:
        """Convert 0-100% brightness to NV's expected 0-255 range."""
        return int((brightness / 100.0) * 255)
    