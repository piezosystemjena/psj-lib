from .piezo_capability import PiezoCapability


class Fan(PiezoCapability):
    CMD_ENABLE = "FAN_ENABLE"

    async def set(self, enabled: bool) -> None:
        await self._write(self.CMD_ENABLE, [enabled])

    async def get_enabled(self) -> bool:
        result = await self._write(self.CMD_ENABLE)
        return bool(int(result[0]))