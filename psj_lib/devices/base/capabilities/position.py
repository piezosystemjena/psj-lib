from .piezo_capability import PiezoCapability


class Position(PiezoCapability):
    CMD_POSITION = "POSITION"

    async def get(self) -> float:
        result = await self._write(self.CMD_POSITION)
        return float(result[0])