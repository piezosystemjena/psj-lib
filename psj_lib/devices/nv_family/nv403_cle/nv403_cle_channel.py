from ..nv_family_channel import NVFamilyChannel
from ...base.capabilities import *

class NV403CLEChannel(NVFamilyChannel):
    """Closed-loop channel model used by NV40/3CLE devices.

    Extends :class:`NVFamilyChannel` with closed-loop specific capabilities
    for each of the three channels.

    Example:
        >>> ch2 = device.channels[2]
        >>> await ch2.closed_loop_controller.set(True)
        >>> await ch2.setpoint.set(9.0)
        >>> limits = await ch2.closedloop_limits.get_range()
    """

    closed_loop_controller: ClosedLoopController = CapabilityDescriptor(
        ClosedLoopController, {
            ClosedLoopController.CMD_ENABLE: "cloop",
        },
        sample_period=0
    )
    """Closed-loop feedback control enable/disable."""

    closedloop_unit: Unit = CapabilityDescriptor(
        Unit, {
            Unit.CMD_UNIT: "unitcl"
        }
    )
    """Closed-loop unit readback capability."""

    closedloop_limits: Limits = CapabilityDescriptor(
        Limits, {
            Limits.CMD_LOWER_LIMIT: "dspclmin",
            Limits.CMD_UPPER_LIMIT: "dspclmax"
        }
    )
    """Closed-loop lower and upper limit queries."""
