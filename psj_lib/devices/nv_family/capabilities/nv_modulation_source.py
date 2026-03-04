"""NV-specific modulation source capability and source enum."""

from ...base.capabilities import ModulationSource, ModulationSourceTypes

class NVModulationSourceTypes(ModulationSourceTypes):
    """NV modulation source selection.

    Defines available control sources for setpoint modulation on NV devices.

    Attributes:
        ENCODER_ANALOG: Front-panel encoder + analog control path.
        SERIAL: Serial command path.

    Example:
        >>> from psj_lib import NVModulationSourceTypes
        >>> await channel.modulation_source.set_source(NVModulationSourceTypes.SERIAL)
        >>> source = await channel.modulation_source.get_source()
        >>> print(source.name)
    """

    ENCODER_ANALOG = 0
    SERIAL = 1

class NVModulationSource(ModulationSource):
    """Modulation source capability with client-side readback cache.

    NV devices do not expose readback for modulation source, therefore the last
    written value is returned by :meth:`get_source`.
    """

    def __init__(self, *args, **kwargs):
        """Initialize modulation source capability.

        Args:
            *args: Positional arguments forwarded to :class:`ModulationSource`.
            **kwargs: Keyword arguments forwarded to :class:`ModulationSource`.
        """
        super().__init__(*args, **kwargs)
        self._source_cache: NVModulationSourceTypes = NVModulationSourceTypes.ENCODER_ANALOG

    async def set_source(self, source: NVModulationSourceTypes) -> None:
        """Set modulation source.

        Args:
            source: Desired NV modulation source.

        Returns:
            None
        """
        await super().set_source(source)
        self._source_cache = source

    async def get_source(self) -> NVModulationSourceTypes:
        """Get current modulation source.

        NV hardware does not provide source readback. This returns the last
        value set via :meth:`set_source`.

        Returns:
            Last configured :class:`NVModulationSourceTypes` value.
        """
        return self._source_cache
