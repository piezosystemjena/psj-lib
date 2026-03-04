"""NV-series encoder knob capabilities."""

from enum import Enum

from ...base.capabilities import PiezoCapability

class NVKnobMode(Enum):
    """NV encoder knob operating modes.

    Defines the operating behavior of the front-panel encoder knob for
    setpoint adjustment.

    Attributes:
        UNKNOWN: Unrecognized mode (fallback when parsing fails).
        ACCELERATION: Step size scales with rotation speed.
        INTERVAL: Fixed step interval mode.
        INTERVAL_ACCELERATION: Interval mode with acceleration behavior.

    Example:
        >>> from psj_lib import NVKnobMode
        >>> await device.knob.set(mode=NVKnobMode.INTERVAL)
        >>> mode = await device.knob.get_mode()
        >>> print(mode.name)
    """

    UNKNOWN = -1
    ACCELERATION = 0
    INTERVAL = 1
    INTERVAL_ACCELERATION = 2

class NVKnob(PiezoCapability):
    """Encoder knob configuration for open-loop and shared settings."""

    CMD_MODE = "KNOB_MODE"
    CMD_SAMPLE_TIME = "KNOB_SAMPLE_TIME"
    CMD_ACCEL_EXPONENT = "KNOB_ACCEL_EXPONENT"
    CMD_STEP_LIMIT = "KNOB_STEP_LIMIT"
    CMD_STEP_OPEN_LOOP = "KNOB_STEP_OPEN_LOOP"
    
    async def set(
        self,
        mode: NVKnobMode | None = None,
        sample_time: float | None = None,
        accel_exponent: int | None = None,
        step_limit: int | None = None,
        step_open_loop: float | None = None,
    ) -> None:
        """
        Set encoder knob parameters. Only parameters that are not None will be updated.

        Args:
            mode: Encoder knob mode (acceleration, interval, or interval with acceleration)
            sample_time: Sample time in seconds (NV expects multiples of 20ms)
            accel_exponent: Exponent for acceleration mode (higher = more aggressive)
            step_limit: Maximum step size for interval mode
            step_open_loop: Step size for open loop control (V)

        Returns:
            None
        """
        if mode is not None:
            await self._write(self.CMD_MODE, [mode.value])
        if sample_time is not None:
            output = int(sample_time / 0.02)  # NV expects sample time in units of 20ms
            await self._write(self.CMD_SAMPLE_TIME, [output])
        if accel_exponent is not None:
            await self._write(self.CMD_ACCEL_EXPONENT, [accel_exponent])
        if step_limit is not None:
            await self._write(self.CMD_STEP_LIMIT, [step_limit])
        if step_open_loop is not None:
            await self._write(self.CMD_STEP_OPEN_LOOP, [step_open_loop])

    async def get_mode(self) -> NVKnobMode:
        """Read the currently configured knob mode.

        Returns:
            Current :class:`NVKnobMode`. Returns ``NVKnobMode.UNKNOWN`` if
            parsing fails.
        """
        result = await self._write(self.CMD_MODE)
        
        try:
            mode_value = int(result[0])
            return NVKnobMode(mode_value)
        except Exception:
            return NVKnobMode.UNKNOWN
    
    async def get_sample_time(self) -> float:
        """Read encoder sampling period.

        Returns:
            Sampling period in seconds.
        """
        result = await self._write(self.CMD_SAMPLE_TIME)
        return int(result[0]) * 0.02  # Convert back to seconds
    
    async def get_accel_exponent(self) -> int:
        """Read acceleration exponent.

        Returns:
            Configured acceleration exponent.
        """
        result = await self._write(self.CMD_ACCEL_EXPONENT)
        return int(result[0])
    
    async def get_step_limit(self) -> int:
        """Read configured knob step limit.

        Returns:
            Maximum step limit value.
        """
        result = await self._write(self.CMD_STEP_LIMIT)
        return int(result[0])
    
    async def get_step_open_loop(self) -> float:
        """Read open-loop knob step value.

        Returns:
            Open-loop step size (typically in volts).
        """
        result = await self._write(self.CMD_STEP_OPEN_LOOP)
        return float(result[0])
    
class NVCLEKnob(NVKnob):
    """Encoder knob capability variant with closed-loop step settings."""

    CMD_STEP_CLOSED_LOOP = "KNOB_STEP_CLOSED_LOOP"
    
    async def set(
        self,
        mode: NVKnobMode | None = None,
        sample_time: float | None = None,
        accel_exponent: int | None = None,
        step_limit: int | None = None,
        step_open_loop: float | None = None,
        step_closed_loop: float | None = None,
    ) -> None:
        """
        Set encoder knob parameters. Only parameters that are not None will be updated.

        Args:
            mode: Encoder knob mode (acceleration, interval, or interval with acceleration)
            sample_time: Sample time in seconds (NV expects multiples of 20ms)
            accel_exponent: Exponent for acceleration mode (higher = more aggressive)
            step_limit: Maximum step size for interval mode
            step_open_loop: Step size for open loop control (V)
            step_closed_loop: Step size for closed loop control (µm)

        Returns:
            None
        """
        await super().set(mode, sample_time, accel_exponent, step_limit, step_open_loop)

        if step_closed_loop is not None:
            await self._write(self.CMD_STEP_CLOSED_LOOP, [step_closed_loop])
    
    async def get_step_closed_loop(self) -> float:
        """Read closed-loop knob step value.

        Returns:
            Closed-loop step size (typically in µm).
        """
        result = await self._write(self.CMD_STEP_CLOSED_LOOP)
        return float(result[0])
    