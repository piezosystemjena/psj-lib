NV40/3(CLE)
===========

This page covers the currently supported NV-series amplifiers and their psj-lib integration.

Overview
--------

NV series support follows the same three-layer architecture as other devices:

.. code-block:: text

    NVFamilyDevice
    ├── Global capabilities (display, knob)
    └── NVFamilyChannel / derived channel types
        └── Channel capabilities (setpoint, position, status, monitor output, ...)

Shared behavior is implemented in :class:`~psj_lib.NVFamilyDevice` and :class:`~psj_lib.NVFamilyChannel`,
while model-specific classes define channel count and available closed-loop features.


Device Variants
---------------

Open-loop variants
^^^^^^^^^^^^^^^^^^

* :class:`~psj_lib.devices.nv_family.nv403.nv403_device.NV403Device` (three channels)

Closed-loop variants
^^^^^^^^^^^^^^^^^^^^

* :class:`~psj_lib.devices.nv_family.nv403_cle.nv403_cle_device.NV403CLEDevice` (three channels)


Device Capabilities
-------------------

NV devices provide global (device-level) capabilities that are not tied to a specific channel:

User Interface
^^^^^^^^^^^^^^

* **Display**: Front-panel brightness control
* **Knob Configuration**: Encoder mode, timing, acceleration, and step behavior

Multi-Channel Coordination
^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Multi Setpoint**: Set all channel setpoints in one command (NV40/3 variants)
* **Multi Position**: Read all channel positions in one command (NV40/3 variants)


Channel Capabilities
--------------------

Each NV channel provides a set of capabilities for command/control and diagnostics:

Status and Monitoring
^^^^^^^^^^^^^^^^^^^^^

* **Status Register**: NV-specific fault and actuator state flags
* **Position**: Actual position readback (voltage for open-loop, sensor readback for closed-loop devices)

Open-Loop Control
^^^^^^^^^^^^^^^^^

* **Setpoint**: Open-loop/closed-loop target setting
* **Open-Loop Unit**: Unit readback for open-loop operation
* **Open-Loop Limits**: Lower and upper admissible range

Signal Routing
^^^^^^^^^^^^^^

* **Modulation Source**: Select control source (encoder/analog or serial)
* **Monitor Output**: Route internal signals to analog monitor output

Closed-Loop Additions (CLE Variants)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Closed-Loop Controller**: Enable/disable closed-loop feedback
* **Closed-Loop Unit**: Unit readback for closed-loop operation
* **Closed-Loop Limits**: Lower and upper admissible range

Accessing Capabilities
----------------------

All capabilities are accessed as device or channel attributes. The NV family provides both standard piezo capabilities
and device-specific implementations.

.. code-block:: python

    from psj_lib import NV403CLEDevice, TransportType

    device = NV403CLEDevice(TransportType.SERIAL, "COM10")
    async with device:
        channel = device.channels[0]

        # Device-level capability
        await device.display.set(brightness=40.0)

        # Access channel capabilities
        status = await channel.status.get()
        position = await channel.position.get()
        await channel.setpoint.set(25.0)


Device Capabilities Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All NV-family device capabilities with API references:

.. list-table::
   :widths: 25 35 40
   :header-rows: 1

   * - Property
     - API Reference
     - Description
   * - ``display``
     - :class:`~psj_lib.devices.nv_family.capabilities.nv_display.NVDisplay`
     - Device display brightness control
   * - ``knob``
     - :class:`~psj_lib.devices.nv_family.capabilities.nv_knob.NVKnob`/ :class:`~psj_lib.devices.nv_family.capabilities.nv_knob.NVCLEKnob` (CLE variants)
     - Encoder knob configuration
   * - ``multi_setpoint``
     - :class:`~psj_lib.devices.base.capabilities.multi_setpoint.MultiSetpoint`
     - Set all channel setpoints synchronously (NV40/3 and NV40/3CLE)
   * - ``multi_position``
     - :class:`~psj_lib.devices.base.capabilities.multi_position.MultiPosition`
     - Read all channel positions synchronously (NV40/3 and NV40/3CLE)


Channel Capabilities Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All NV-family channel capabilities with API references:

.. note::
    Some capability readbacks (e.g. setpoint) are cached by the library, as NV devices do not provide native readback for these values. 
    Cached values are updated on set operations.


.. list-table::
   :widths: 25 35 40
   :header-rows: 1

   * - Property
     - API Reference
     - Description
   * - ``setpoint``
     - :class:`~psj_lib.devices.nv_family.capabilities.nv_setpoint.NVSetpoint`
     - | Target open-loop/closed-loop setpoint
       **Cached readback**
   * - ``position``
     - :class:`~psj_lib.devices.base.capabilities.position.Position`
     - Actual channel position readback
   * - ``modulation_source``
     - :class:`~psj_lib.devices.nv_family.capabilities.nv_modulation_source.NVModulationSource`
     - | Modulation source selection (expects :class:`~psj_lib.devices.nv_family.capabilities.nv_modulation_source.NVModulationSourceTypes` enum)
       **Cached readback**
   * - ``monitor_output``
     - :class:`~psj_lib.devices.nv_family.capabilities.nv_monitor_output.NVMonitorOutput`
     - | Analog monitor output routing (expects :class:`~psj_lib.devices.nv_family.capabilities.nv_monitor_output.NVMonitorOutputSource` enum)
       **Cached readback**
   * - ``openloop_unit``
     - :class:`~psj_lib.devices.base.capabilities.unit.Unit`
     - Unit of the open-loop command domain
   * - ``openloop_limits``
     - :class:`~psj_lib.devices.base.capabilities.limits.Limits`
     - Open-loop lower and upper limits
   * - ``status``
     - :class:`~psj_lib.devices.base.capabilities.status.Status`
     - Status access using :class:`~psj_lib.devices.nv_family.capabilities.nv_status_register.NVStatusRegister`
   * - ``closed_loop_controller``
     - :class:`~psj_lib.devices.base.capabilities.closed_loop_controller.ClosedLoopController`
     - Closed-loop feedback control enable/disable (CLE variants only)
   * - ``closedloop_unit``
     - :class:`~psj_lib.devices.base.capabilities.unit.Unit`
     - Unit of the closed-loop command domain (CLE variants only)
   * - ``closedloop_limits``
     - :class:`~psj_lib.devices.base.capabilities.limits.Limits`
     - Closed-loop lower and upper limits (CLE variants only)


Usage Example
-------------

.. code-block:: python

    import asyncio
    from psj_lib import NV403CLEDevice, TransportType

    async def main():
        device = NV403CLEDevice(TransportType.SERIAL, "COM10")

        async with device:
            await device.display.set(brightness=50.0)

            ch0 = device.channels[0]
            await ch0.closed_loop_controller.set(enabled=True)
            await ch0.setpoint.set(25.0)
            print(await ch0.position.get())

            await device.multi_setpoint.set([10.0, 20.0, 30.0])
            print(await device.multi_position.get())

    asyncio.run(main())
