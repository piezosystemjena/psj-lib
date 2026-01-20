from ..d_drive_family_device import DDriveFamilyDevice
from .psj_30dv_channel import PSJ30DVChannel

class PSJ30DVDevice(DDriveFamilyDevice):
    DEVICE_ID = "30DV"
    """Device type identifier used for device discovery and type checking."""

    D_DRIVE_IDENTIFIER = "AP"
    """Internal identifier string used to recognize different d-Drive family devices."""

    async def _discover_channels(self):
        self._channels = {}
        self._channels[0] = PSJ30DVChannel(
            0, self._write_channel
        )
    
    async def _write_channel(self, channel_id, cmd, params = None):
        return await super()._write_channel(None, cmd, params)

    # Override to provide typed channels
    @property
    def channels(self) -> dict[int, PSJ30DVChannel]:
        return self._channels