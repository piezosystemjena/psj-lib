"""Example 8: NV403CLE Capabilities Overview

This example demonstrates how to:
- Connect to an NV403CLE device
- Backup current configuration at start
- Set modulation source to SERIAL at startup
- Toggle closed-loop control
- Read open-loop and closed-loop units and limits
- Set and read display brightness
- Print actuator connected status for all channels
- Use multi_setpoint and multi_position for all channels
- Restore original configuration at end

Adjust the COM port to match your setup.
"""

import asyncio

from psj_lib import NV403CLEDevice, NVModulationSourceTypes, TransportType


async def main() -> None:
    print("=" * 72)
    print("NV403CLE capabilities overview")
    print("=" * 72)

    device = NV403CLEDevice(TransportType.SERIAL, "COM10")
    backup_data = None

    try:
        print("\n[1] Connecting to NV403CLE...")
        await device.connect()
        print("✓ Connected")

        print("\n[2] Backing up current configuration...")
        backup_data = await device.backup()
        print("✓ Backup created")

        channel = device.channels[0]

        print("\n[3] Setting modulation source to SERIAL for all channels...")
        
        for ch in device.channels.values():
            await ch.modulation_source.set_source(NVModulationSourceTypes.SERIAL)
        
        current_source = await channel.modulation_source.get_source()
        print(f"✓ Modulation source: {current_source.name}")

        print("\n[4] Reading and setting display brightness...")
        before_brightness = await device.display.get_brightness()
        print(f"Current brightness: {before_brightness:.1f}%")
        await device.display.set(brightness=40.0)
        after_brightness = await device.display.get_brightness()
        print(f"Updated brightness: {after_brightness:.1f}%")

        print("\n[5] Toggling closed-loop control...")
        closed_loop_before = await channel.closed_loop_controller.get_enabled()
        print(f"Closed-loop before: {closed_loop_before}")
        await channel.closed_loop_controller.set(not closed_loop_before)
        closed_loop_after = await channel.closed_loop_controller.get_enabled()
        print(f"Closed-loop after:  {closed_loop_after}")

        print("\n[6] Reading units and limits...")
        openloop_unit = await channel.openloop_unit.get()
        openloop_limits = await channel.openloop_limits.get_range()
        print(f"Open-loop unit: {openloop_unit}")
        print(f"Open-loop limits: {openloop_limits[0]} .. {openloop_limits[1]}")

        closedloop_unit = await channel.closedloop_unit.get()
        closedloop_limits = await channel.closedloop_limits.get_range()
        print(f"Closed-loop unit: {closedloop_unit}")
        print(f"Closed-loop limits: {closedloop_limits[0]} .. {closedloop_limits[1]}")

        print("\n[7] Reading actuator connected status for all channels...")
        for channel_id, current_channel in device.channels.items():
            status = await current_channel.status.get()
            print(f"Channel {channel_id}: actuator connected = {status.actuator_plugged}")

        print("\n[8] Using multi_setpoint and multi_position...")

        # Note: Using multi_setpoint requires all channels to have an actuator connected
        # and modulation mode set to SERIAL. Otherwise, the amplifier will ignore the command.
        setpoints = [10.0, 20.0, 30.0]
        await device.multi_setpoint.set(setpoints)
        positions = await device.multi_position.get()
        print(f"Setpoints written: {setpoints}")
        print(f"Positions read:    {positions}")

    except Exception as exc:
        print(f"\n❌ Error: {exc}")
        import traceback
        traceback.print_exc()
    finally:
        if backup_data is not None:
            print("\n[9] Restoring original configuration...")
            try:
                await device.restore(backup_data)
                print("✓ Configuration restored")
            except Exception as restore_exc:
                print(f"⚠ Restore failed: {restore_exc}")

        print("\n[10] Disconnecting...")
        await device.close()
        print("✓ Disconnected")

    print("\n" + "=" * 72)
    print("Example completed")
    print("=" * 72)


if __name__ == "__main__":
    asyncio.run(main())
