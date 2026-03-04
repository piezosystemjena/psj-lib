from ..nv_family_channel import NVFamilyChannel

class NV120Channel(NVFamilyChannel):
    """Single-channel open-loop channel for NV120 devices.

    Inherits all common NV channel capabilities from
    :class:`~psj_lib.devices.nv_family.nv_family_channel.NVFamilyChannel`.

    Example:
        >>> channel = device.channels[0]
        >>> await channel.setpoint.set(12.0)
        >>> print(await channel.position.get())
    """

    pass 