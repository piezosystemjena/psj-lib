from .piezo_capability import PiezoCapability


class PreControlFactor(PiezoCapability):
    CMD_VALUE = "PCF_VALUE"

    async def set(self, value: float) -> None:
        await self._write(self.CMD_VALUE, [value])

    async def get(self) -> None:
        return await self._write(self.CMD_VALUE)