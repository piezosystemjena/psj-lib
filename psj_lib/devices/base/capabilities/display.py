from .piezo_capability import PiezoCapability

class Display(PiezoCapability):
    CMD_BRIGHTNESS = "DISPLAY_BRIGHTNESS"

    async def set(
        self,
        brightness: float | None = None,
    ) -> None:
        if brightness is not None:
            if not (0.0 <= brightness <= 100.0):
                raise ValueError("Brightness must be between 0 and 100")
            await self._write(self.CMD_BRIGHTNESS, [brightness])

    async def get_brightness(self) -> float:
        result = await self._write(self.CMD_BRIGHTNESS)
        return float(result[0])
    