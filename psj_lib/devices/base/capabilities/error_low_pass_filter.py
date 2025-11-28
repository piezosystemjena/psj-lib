from .piezo_capability import PiezoCapability


class ErrorLowPassFilter(PiezoCapability):
    CMD_CUTOFF_FREQUENCY = "ERROR_LOW_PASS_FILTER_CUTOFF_FREQUENCY"
    CMD_ORDER = "ERROR_LOW_PASS_FILTER_ORDER"

    async def set(
        self,
        cutoff_frequency: float | None = None,
        order: int | None = None,
    ) -> None:
        if cutoff_frequency is not None:
            await self._write(self.CMD_CUTOFF_FREQUENCY, [cutoff_frequency])

        if order is not None:
            await self._write(self.CMD_ORDER, [order])

    async def get_cutoff_frequency(self) -> float:
        result = await self._write(self.CMD_CUTOFF_FREQUENCY)
        return float(result[0])

    async def get_order(self) -> int:
        result = await self._write(self.CMD_ORDER)
        return int(result[0])