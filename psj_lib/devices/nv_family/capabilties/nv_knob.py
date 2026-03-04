from enum import Enum

from ...base.capabilities import PiezoCapability

class NVKnobMode(Enum):
    UNKNOWN = -1
    ACCELERATION = 0
    INTERVAL = 1
    INTERVAL_ACCELERATION = 2

class NVKnob(PiezoCapability):
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
            step_closed_loop: Step size for closed loop control (um)
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
        if step_closed_loop is not None:
            await self._write(self.CMD_STEP_CLOSED_LOOP, [step_closed_loop])

    async def get_mode(self) -> NVKnobMode:
        result = await self._write(self.CMD_MODE)
        
        try:
            mode_value = int(result[0])
            return NVKnobMode(mode_value)
        except Exception:
            return NVKnobMode.UNKNOWN
    
    async def get_sample_time(self) -> float:
        result = await self._write(self.CMD_SAMPLE_TIME)
        return int(result[0]) * 0.02  # Convert back to seconds
    
    async def get_accel_exponent(self) -> int:
        result = await self._write(self.CMD_ACCEL_EXPONENT)
        return int(result[0])
    
    async def get_step_limit(self) -> int:
        result = await self._write(self.CMD_STEP_LIMIT)
        return int(result[0])
    
    async def get_step_open_loop(self) -> float:
        result = await self._write(self.CMD_STEP_OPEN_LOOP)
        return float(result[0])
    
class NVCLEKnob(NVKnob):
    CMD_STEP_CLOSED_LOOP = "KNOB_STEP_CLOSED_LOOP"
    
    async def get_step_closed_loop(self) -> float:
        result = await self._write(self.CMD_STEP_CLOSED_LOOP)
        return float(result[0])
    