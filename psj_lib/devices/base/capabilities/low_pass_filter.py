from .piezo_capability import PiezoCapability


class LowPassFilter(PiezoCapability):
    CMD_ENABLE = "LOW_PASS_FILTER_ENABLE"
    CMD_CUTOFF_FREQUENCY = "LOW_PASS_FILTER_CUTOFF_FREQUENCY"

    async def set(
        self,
        enabled: bool | None = None,
        cutoff_frequency: float | None = None,
    ) -> None:
        if enabled is not None:
            await self._write(self.CMD_ENABLE, [enabled])

        if cutoff_frequency is not None:
            await self._write(self.CMD_CUTOFF_FREQUENCY, [cutoff_frequency])

    async def get_enabled(self) -> bool:
        result = await self._write(self.CMD_ENABLE)
        return bool(result[0])

    async def get_cutoff_frequency(self) -> float:
        result = await self._write(self.CMD_CUTOFF_FREQUENCY)
        return float(result[0])