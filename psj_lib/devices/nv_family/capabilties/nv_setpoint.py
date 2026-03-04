"""NV setpoint capability with client-side readback cache."""

from ...base.capabilities import Setpoint

class NVSetpoint(Setpoint):
    """Setpoint capability for NV devices.

    NV devices do not support direct setpoint readback, so the last written
    value is cached and returned by :meth:`get`.
    """

    _setpoint_cache: float = 0.0

    async def set(self, value: float) -> None:
        """Write channel setpoint.

        Args:
            value: Target setpoint value in the currently active domain
                (open-loop voltage or closed-loop position).

        Returns:
            None
        """
        await super().set(value)
        self._setpoint_cache = value

    async def get(self) -> float:
        """Get channel setpoint.

        NV hardware does not provide direct setpoint readback. This returns the
        last value written via :meth:`set`.

        Returns:
            Last configured setpoint value.
        """
        return self._setpoint_cache
    