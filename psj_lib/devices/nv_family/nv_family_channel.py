"""NV family channel model and capability mapping.

This module defines the shared channel-level capabilities for supported
NV-series amplifiers.
"""

from typing import Awaitable

from ..base.piezo_channel import PiezoChannel
from ..base.capabilities import *
from .capabilities.nv_setpoint import NVSetpoint
from .capabilities.nv_modulation_source import NVModulationSource, NVModulationSourceTypes
from .capabilities.nv_monitor_output import NVMonitorOutputSource, NVMonitorOutput
from .capabilities.nv_status_register import NVStatusRegister

class NVFamilyChannel(PiezoChannel):
    """Base channel for NV-series amplifiers.

    This class provides common channel capabilities across open-loop and
    closed-loop NV variants.

    Common capabilities include:
    - Setpoint and position control/readback
    - Status register access with NV-specific flag decoding
    - Modulation source selection
    - Monitor output routing
    - Open-loop unit and limit queries

    Example:
        >>> channel = device.channels[0]
        >>> await channel.setpoint.set(25.0)
        >>> pos = await channel.position.get()
        >>> status = await channel.status.get()
        >>> print(pos, status.over_temperature)
    """

    BACKUP_COMMANDS: set[str] = {
        "monwpa",
        "setk",
        "cloop"
    }
    """NV channel commands included in backup/restore operations."""

    GLOBAL_COMMANDS: set[str] = {
        "ERROR",
        "dspvmin",
        "dspvmax",
    }
    """
    Commands that should belong to a channel, but the device expects them without a channel ID prefix. 
    Handled specially in the _write method.
    """

    # Capability descriptors
    setpoint: NVSetpoint = CapabilityDescriptor(
        NVSetpoint, {
            NVSetpoint.CMD_SETPOINT: "set",
        }
    )
    """Channel setpoint capability.

    Readback value is always the last set value, due to the lack of direct readback for this value in NV devices. 

    Example:
        >>> await channel.setpoint.set(40.0)
        >>> target = await channel.setpoint.get()
    """

    position: Position = CapabilityDescriptor(
        Position, {
            Position.CMD_POSITION: "rk"
        }
    )
    """Channel position readback capability.

    Example:
        >>> actual = await channel.position.get()
    """

    modulation_source: NVModulationSource = CapabilityDescriptor(
        NVModulationSource, {
            NVModulationSource.CMD_SOURCE: "setk"
        },
        sources=NVModulationSourceTypes
    )
    """Channel modulation source selection.

    Expects :class:`~psj_lib.devices.nv_family.capabilities.nv_modulation_source.NVModulationSourceTypes` values.
    Readback value is always the last set value, due to the lack of direct readback for this value in NV devices. 
    """

    monitor_output: NVMonitorOutput = CapabilityDescriptor(
        NVMonitorOutput, {
            NVMonitorOutput.CMD_OUTPUT_SRC: "monwpa"
        },
        sources=NVMonitorOutputSource
    )
    """Analog monitor output source routing.

    Expects :class:`~psj_lib.devices.nv_family.capabilities.nv_monitor_output.NVMonitorOutputSource` values.
    Readback value is always the last set value, due to the lack of direct readback for this value in NV devices. 
    """

    openloop_unit: Unit = CapabilityDescriptor(
        Unit, {
            Unit.CMD_UNIT: "unitol"
        }
    )
    """Open-loop unit readback capability.

    Example:
        >>> unit = await channel.openloop_unit.get()
    """

    openloop_limits: Limits = CapabilityDescriptor(
        Limits, {
            Limits.CMD_LOWER_LIMIT: "dspvmin",
            Limits.CMD_UPPER_LIMIT: "dspvmax"
        }
    )
    """Open-loop lower and upper limit queries.

    Example:
        >>> lower, upper = await channel.openloop_limits.get_range()
    """

    status: Status = CapabilityDescriptor(
        Status, {
            Status.CMD_STATUS: "ERROR"
        },
        register_type=NVStatusRegister,
    )
    """NV status register access.

    Returns :class:`~psj_lib.devices.nv_family.capabilities.nv_status_register.NVStatusRegister` for interpreted per-channel flags.
    """
    
    async def _write(self, cmd: str, params: list[PiezoChannel.Param] | None) -> Awaitable[list[str]]:
        """Send channel command, with special handling for global NV status command."""
        if not self._write_cb:
            raise RuntimeError("No write callback defined for this channel.")

        # Do not send channel ID for some commands
        if cmd in self.GLOBAL_COMMANDS:
            return await self._write_cb(None, cmd, params)

        return await self._write_cb(self._channel_id, cmd, params)
