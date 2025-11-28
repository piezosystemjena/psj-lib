from .piezo_capability import PiezoCapability


class SlewRate(PiezoCapability):
    CMD_RATE = "SLEW_RATE"

    async def set(self, rate: float) -> None:
        await self._write(self.CMD_RATE, [rate])

    async def get(self) -> float:
        result = await self._write(self.CMD_RATE)
        return float(result[0])