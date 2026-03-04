from ...base.capabilities import CapabilityDescriptor
from ..capabilties.nv_knob import NVKnob
from ..nv_family_device import NVFamilyDevice
from .nv120_channel import NV120Channel

class NV120Device(NVFamilyDevice):
    DEVICE_ID = "NV120/1"
    
    NV_FAMILY_IDENTIFIER = "NV120"
    NV_CHANNEL_TYPE = NV120Channel

    MAX_CHANNEL_COUNT = 1

    @property
    def channels(self) -> dict[int, NV120Channel]:
        return self._channels

    knob: NVKnob = CapabilityDescriptor(
        NVKnob, {
            NVKnob.CMD_MODET: "encmode",
            NVKnob.CMD_SAMPLE_TIME: "enctime",
            NVKnob.CMD_STEP_LIMIT: "enclim",
            NVKnob.CMD_ACCEL_EXPONENT: "encexp",
            NVKnob.CMD_STEP_OPEN_LOOP: "encstol",
        }
    )