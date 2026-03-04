"""Display capabilities for PSJ devices."""

from .piezo_capability import PiezoCapability

class Display(PiezoCapability):
    """Display settings capability.

    Provides access to the device display brightness in percent.
    """

    CMD_BRIGHTNESS = "DISPLAY_BRIGHTNESS"

    async def set(
        self,
        brightness: float | None = None,
    ) -> None:
        """Set display brightness.
        Only parameters that are not None will be updated.

        Args:
            brightness: Brightness in percent in range 0.0..100.0.

        Raises:
            ValueError: If brightness is outside 0..100.
        """
        if brightness is not None:
            if not (0.0 <= brightness <= 100.0):
                raise ValueError("Brightness must be between 0 and 100")
            await self._write(self.CMD_BRIGHTNESS, [brightness])

    async def get_brightness(self) -> float:
        """Read display brightness as percent.
        
        Returns:
            Brightness in percent in range 0.0..100.0.
        """
        result = await self._write(self.CMD_BRIGHTNESS)
        return float(result[0])
    