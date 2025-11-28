from .piezo_capability import PiezoCapability


class Setpoint(PiezoCapability):
    CMD_SETPOINT = "SETPOINT"

    async def set(self, setpoint: float) -> None:
        await self._write(self.CMD_SETPOINT, [setpoint])

    async def get(self) -> float:
        result = await self._write(self.CMD_SETPOINT)
        return float(result[0])