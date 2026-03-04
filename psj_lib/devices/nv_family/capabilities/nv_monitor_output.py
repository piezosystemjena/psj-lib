"""NV-specific monitor output capability and source enum."""

from ...base.capabilities import MonitorOutput, MonitorOutputSource

class NVMonitorOutputSource(MonitorOutputSource):
    """NV analog monitor output routing.

    Defines internal signals that can be routed to the analog monitor output
    connector for live observation.

    Attributes:
        ACTUATOR_VOLTAGE: Actuator drive voltage signal.
        POSITION_VOLTAGE: Position-proportional voltage signal.
        MODE_DEPENDENT: Source selected by current operation mode.

    Example:
        >>> from psj_lib import NVMonitorOutputSource
        >>> await channel.monitor_output.set_source(NVMonitorOutputSource.POSITION_VOLTAGE)
        >>> source = await channel.monitor_output.get_source()
        >>> print(source.name)
    """

    ACTUATOR_VOLTAGE = 0
    POSITION_VOLTAGE = 1
    MODE_DEPENDENT = 2

class NVMonitorOutput(MonitorOutput):
    """Monitor output capability with cached readback behavior."""

    _source_cache: NVMonitorOutputSource = NVMonitorOutputSource.ACTUATOR_VOLTAGE

    async def set_source(self, source: NVMonitorOutputSource) -> None:
        """Set monitor output source.

        Args:
            source: Desired monitor output source.

        Returns:
            None

        Raises:
            ValueError: If ``source`` is not an :class:`NVMonitorOutputSource`.
        """
        if type(source) is not NVMonitorOutputSource:
            raise ValueError(f"Invalid monitor source type: {type(source)} (Expected: NVMonitorOutputSource)")

        await self._write(self.CMD_OUTPUT_SRC, [source.value])
        self._source_cache = source

    async def get_source(self) -> NVMonitorOutputSource:
        """Get monitor output source.

        NV hardware does not provide source readback. This returns the last
        value set via :meth:`set_source`.

        Returns:
            Last configured :class:`NVMonitorOutputSource` value.
        """
        return self._source_cache
