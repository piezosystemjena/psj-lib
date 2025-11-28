from enum import Enum

from .piezo_capability import PiezoCapability


class TriggerDataSource(Enum):
    POSITION = 0
    SETPOINT = 1


class TriggerEdge(Enum):
    DISABLED = 0
    RISING = 1
    FALLING = 2
    BOTH = 3


class TriggerOut(PiezoCapability):
    CMD_START = "TRIGGER_OUT_START"
    CMD_STOP = "TRIGGER_OUT_STOP"
    CMD_INTERVAL = "TRIGGER_OUT_INTERVAL"
    CMD_LENGTH = "TRIGGER_OUT_LENGTH"
    CMD_EDGE = "TRIGGER_OUT_EDGE"
    CMD_SRC = "TRIGGER_OUT_SRC"
    async def set(
        self,
        start_value: float | None = None,
        stop_value: float | None = None,
        interval: float | None = None,
        length: int | None = None,
        edge: TriggerEdge | None = None,
        src: TriggerDataSource | None = None
    ) -> None:
        if start_value is not None:
            await self._write(self.CMD_START, [start_value])

        if stop_value is not None:
            await self._write(self.CMD_STOP, [stop_value])

        if interval is not None:
            await self._write(self.CMD_INTERVAL, [interval])

        if length is not None:
            await self._write(self.CMD_LENGTH, [length])

        if edge is not None:
            await self._write(self.CMD_EDGE, [edge])

        if src is not None:
            await self._write(self.CMD_SRC, [src])

    async def get_start_value(self) -> float:
        result = await self._write(self.CMD_START)
        return float(result[0])

    async def get_stop_value(self) -> float:
        result = await self._write(self.CMD_STOP)
        return float(result[0])

    async def get_interval(self) -> float:
        result = await self._write(self.CMD_INTERVAL)
        return float(result[0])

    async def get_length(self) -> int:
        result = await self._write(self.CMD_LENGTH)
        return int(result[0])

    async def get_edge(self) -> TriggerEdge:
        result = await self._write(self.CMD_EDGE)
        return TriggerEdge(int(result[0]))

    async def get_src(self) -> TriggerDataSource:
        result = await self._write(self.CMD_SRC)
        return TriggerDataSource(int(result[0]))