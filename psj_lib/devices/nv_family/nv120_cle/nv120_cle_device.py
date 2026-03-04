from ...base.capabilities import CapabilityDescriptor
from ..nv_family_device import NVFamilyDevice
from ..capabilties.nv_knob import NVCLEKnob
from .nv120_cle_channel import NV120CLEChannel

class NV120CLEDevice(NVFamilyDevice):
    DEVICE_ID = "NV120CLE"
    
    NV_FAMILY_IDENTIFIER = "NV120CLE"
    NV_CHANNEL_TYPE = NV120CLEChannel
    
    MAX_CHANNEL_COUNT = 1

    @property
    def channels(self) -> dict[int, NV120CLEChannel]:
        return self._channels

    knob: NVCLEKnob = CapabilityDescriptor(
        NVCLEKnob, {
            NVCLEKnob.CMD_MODE: "encmode",
            NVCLEKnob.CMD_SAMPLE_TIME: "enctime",
            NVCLEKnob.CMD_STEP_LIMIT: "enclim",
            NVCLEKnob.CMD_ACCEL_EXPONENT: "encexp",
            NVCLEKnob.CMD_STEP_OPEN_LOOP: "encstol",
            NVCLEKnob.CMD_STEP_CLOSED_LOOP: "encstcl",
        }
    )
