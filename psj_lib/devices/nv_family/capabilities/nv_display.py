"""NV-specific display capability implementation."""

from ...base.capabilities import Display

class NVDisplay(Display):
    """Display capability for NV devices.

    Internally scale brightness to NV's expected 0-255 range.
    """

    async def set(
        self,
        brightness: float | None = None,
    ) -> None:
        """Set display brightness.

        Args:
            brightness: Target brightness in percent from 0.0 to 100.0.
                If ``None``, no command is sent.

        Returns:
            None

        Raises:
            ValueError: If ``brightness`` is outside the range 0..100.
        """
        if brightness is not None:
            if not (0.0 <= brightness <= 100.0):
                raise ValueError("Brightness must be between 0 and 100")
            
            nv_brightness = self._convert_brightness(brightness)
            await self._write(self.CMD_BRIGHTNESS, [nv_brightness])

    async def get_brightness(self) -> float:
        """Read current display brightness.

        Returns:
            Brightness in percent from 0.0 to 100.0.
        """
        response = await self._write(self.CMD_BRIGHTNESS)
        return self._parse_brightness(int(response[0]))
    
    def _convert_brightness(self, brightness: float) -> int:
        """Convert percentage brightness to NV register scale.

        Args:
            brightness: Brightness in percent from 0.0 to 100.0.

        Returns:
            Brightness value mapped to NV range 0..255.
        """
        return int((brightness / 100.0) * 255)
    
    def _parse_brightness(self, nv_brightness: int) -> float:
        """Convert NV register brightness to percentage.

        Args:
            nv_brightness: Raw NV brightness value in range 0..255.

        Returns:
            Brightness in percent from 0.0 to 100.0.
        """
        return (nv_brightness / 255.0) * 100.0
    