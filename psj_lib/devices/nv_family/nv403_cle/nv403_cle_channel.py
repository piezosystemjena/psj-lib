from ..nv_family_channel import NVFamilyChannel
from ...base.capabilities import *

class NV403CLEChannel(NVFamilyChannel):
    closed_loop_controller: ClosedLoopController = CapabilityDescriptor(
        ClosedLoopController, {
            ClosedLoopController.CMD_ENABLE: "cloop",
        },
        sample_period=0
    )

    position_unit: Unit = CapabilityDescriptor(
        Unit, {
            Unit.CMD_UNIT: "unitcl"
        }
    )

    position_limits: Limits = CapabilityDescriptor(
        Limits, {
            Limits.CMD_LOWER_LIMIT: "dspclmin",
            Limits.CMD_UPPER_LIMIT: "dspclmax"
        }
    )
