from ...base.capabilities import Setpoint

class NVSetpoint(Setpoint):
    _setpoint_cache: float = 0.0

    async def set(self, value: float) -> None:
        await super().set(value)
        self._setpoint_cache = value

    async def get(self) -> float:
        return self._setpoint_cache
    