from .piezo_capability import PiezoCapability

class MultiPosition(PiezoCapability):
    """Capability for reading multiple channel positions synchronously."""

    CMD_POSITIONS = "POSITIONS"

    async def get(self) -> list[float]:
        """Return current position values for all channels."""
        result = await self._write(self.CMD_POSITIONS)
        return [float(value) for value in result]
    