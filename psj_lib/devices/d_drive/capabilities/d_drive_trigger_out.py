from ...base.capabilities import TriggerDataSource, TriggerEdge, TriggerOut


class DDriveTriggerOut(TriggerOut):
    """
    Represents the Trigger Out capability of a D-Drive amplifier channel.
    """

    CMD_OFFSET = "TRIGGER_OUT_OFFSET"

    async def set(
        self,
        start_value: float | None = None,
        stop_value: float | None = None,
        interval: float | None = None,
        length: int | None = None,
        edge: TriggerEdge | None = None,
        src: TriggerDataSource | None = None,
        offset: float | None = None
    ) -> None:
        await super().set(
            start_value=start_value,
            stop_value=stop_value,
            interval=interval,
            length=length,
            edge=edge,
            src=src
        )

        if offset is not None:
            await self._write(self.CMD_OFFSET, [offset])

    async def get_offset(self) -> float:
        result = await self._write(self.CMD_OFFSET)
        return float(result[0])