from .piezo_capability import PiezoCapability


class PIDController(PiezoCapability):
    CMD_P = "PID_CONTROLLER_P"
    CMD_I = "PID_CONTROLLER_I"
    CMD_D = "PID_CONTROLLER_D"
    CMD_TF = "PID_CONTROLLER_TF"

    async def set(
        self,
        p: float | None = None,
        i: float | None = None,
        d: float | None = None,
        diff_filter: float | None = None
    ) -> None:
        if p is not None:
            await self._write(self.CMD_P, [p])

        if i is not None:
            await self._write(self.CMD_I, [i])

        if d is not None:
            await self._write(self.CMD_D, [d])

        if diff_filter is not None:
            await self._write(self.CMD_TF, [diff_filter])

    async def get_p(self) -> float:
        result = await self._write(self.CMD_P)
        return float(result[0])

    async def get_i(self) -> float:
        result = await self._write(self.CMD_I)
        return float(result[0])

    async def get_d(self) -> float:
        result = await self._write(self.CMD_D)
        return float(result[0])

    async def get_diff_filter(self) -> float:
        result = await self._write(self.CMD_TF)
        return float(result[0])