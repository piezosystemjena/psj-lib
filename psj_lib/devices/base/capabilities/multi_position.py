from .piezo_capability import PiezoCapability

class MultiPosition(PiezoCapability):
    CMD_POSITIONS = "POSITIONS"

    async def get(self) -> list[float]:
        result = await self._write(self.CMD_POSITIONS)
        return [float(value) for value in result]
    