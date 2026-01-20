API Reference
=============

Complete API reference for psj-lib.


Quick Navigation
----------------

**Core Components**

* `Devices`_ - Device and channel classes
* `Base Capabilities`_ - Common capabilities across all devices
* `d-Drive Specific Capabilities`_ - d-Drive enhanced features
* `Exceptions`_ - Error handling
* `Type Definitions`_ - Type aliases and enums

**Base Capabilities by Category**

* `Status and Monitoring`_ - Status register, temperature, actuator info
* `Position Control`_ - Setpoint, position, closed-loop control, slew rate
* `Control System`_ - PID controller, pre-control factor
* `Filters`_ - Notch filter, low-pass filters, error filtering
* `Signal Generation`_ - Modulation source, monitor output, waveform generation
* `Data Acquisition`_ - Data recorder, trigger output
* `Configuration`_ - Units, factory reset, fan control

**Usage Patterns**

* `Common Patterns`_ - Quick reference for typical operations
* `Async Patterns`_ - Async/await usage examples
* `Type Hints`_ - Type annotation support


Package Structure
-----------------

.. code-block:: text

    psj_lib/
    ├── devices/
    │   ├── base/                    # Base device classes (public: PiezoDevice, PiezoChannel)
    │   │   ├── piezo_device.py
    │   │   ├── piezo_channel.py
    │   │   ├── exceptions.py
    │   │   └── capabilities/        # Base capabilities (all public)
   │   ├── d_drive_family/          # d-Drive family (d-Drive + 30DV series)
   │   │   ├── d_drive/             # d-Drive modular system
   │   │   │   ├── d_drive_device.py
   │   │   │   └── d_drive_channel.py
   │   │   ├── psj_30dv/             # PSJ 30DV single-channel device
   │   │   │   ├── psj_30dv_device.py
   │   │   │   └── psj_30dv_channel.py
   │   │   └── capabilities/        # d-Drive family capabilities (all public)
   │   │       ├── d_drive_status_register.py
   │   │       ├── d_drive_waveform_generator.py
   │   │       └── ...
    │   └── transport_protocol/      # Internal (only TransportType, DiscoverFlags, TransportProtocolInfo exported)
    └── _internal/                   # Internal utilities

**Note**: Only classes and types exported in ``psj_lib.__init__.py`` are part of the public API.
Internal modules like ``device_factory`` and ``transport_protocol`` implementation details should not be accessed directly by end users.


Quick Reference
---------------

Main Classes
^^^^^^^^^^^^

.. code-block:: python

    from psj_lib import DDriveDevice, TransportType, DiscoverFlags


Core Modules
------------

Devices
^^^^^^^

.. automodule:: psj_lib.devices
   :members:
   :undoc-members:
   :show-inheritance:


Base Device Classes
^^^^^^^^^^^^^^^^^^^

.. automodule:: psj_lib.devices.base.piezo_device
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.piezo_channel
   :members:
   :undoc-members:
   :show-inheritance:


d-Drive Device
^^^^^^^^^^^^^^^

.. automodule:: psj_lib.devices.d_drive_family.d_drive.d_drive_device
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.d_drive_family.d_drive.d_drive_channel
   :members:
   :undoc-members:
   :show-inheritance:

PSJ 30DV Device
^^^^^^^^^^^^^^^^

.. automodule:: psj_lib.devices.d_drive_family.psj_30dv.psj_30dv_device
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.d_drive_family.psj_30dv.psj_30dv_channel
   :members:
   :undoc-members:
   :show-inheritance:


Base Capabilities
^^^^^^^^^^^^^^^^^

Status and Monitoring
"""""""""""""""""""""

.. automodule:: psj_lib.devices.base.capabilities.status
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.temperature
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.actuator_description
   :members:
   :undoc-members:
   :show-inheritance:

Position Control
""""""""""""""""

.. automodule:: psj_lib.devices.base.capabilities.position
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.setpoint
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.closed_loop_controller
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.slew_rate
   :members:
   :undoc-members:
   :show-inheritance:

Control System
""""""""""""""

.. automodule:: psj_lib.devices.base.capabilities.pid_controller
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.pcf
   :members:
   :undoc-members:
   :show-inheritance:

Filters
"""""""

.. automodule:: psj_lib.devices.base.capabilities.notch_filter
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.low_pass_filter
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.error_low_pass_filter
   :members:
   :undoc-members:
   :show-inheritance:

Signal Generation
"""""""""""""""""

.. automodule:: psj_lib.devices.base.capabilities.modulation_source
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.monitor_output
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.static_waveform_generator
   :members:
   :undoc-members:
   :show-inheritance:

Data Acquisition
""""""""""""""""

.. automodule:: psj_lib.devices.base.capabilities.data_recorder
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.trigger_out
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
"""""""""""""

.. automodule:: psj_lib.devices.base.capabilities.units
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.factory_reset
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.base.capabilities.fan
   :members:
   :undoc-members:
   :show-inheritance:


d-Drive Specific Capabilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: psj_lib.devices.d_drive_family.capabilities.d_drive_status_register
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.d_drive_family.capabilities.d_drive_waveform_generator
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.d_drive_family.capabilities.d_drive_data_recorder
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.d_drive_family.capabilities.d_drive_trigger_out
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.d_drive_family.capabilities.d_drive_modulation_source
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.d_drive_family.capabilities.d_drive_monitor_output
   :members:
   :undoc-members:
   :show-inheritance:


Exceptions
^^^^^^^^^^

.. automodule:: psj_lib.devices.base.exceptions
   :members:
   :undoc-members:
   :show-inheritance:


Type Definitions
^^^^^^^^^^^^^^^^

.. automodule:: psj_lib.devices.base.piezo_types
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: psj_lib.devices.transport_protocol.transport_types
   :members:
   :undoc-members:
   :show-inheritance:

**Note**: ``TransportType``, ``DiscoverFlags``, and ``TransportProtocolInfo`` are exported 
from the main ``psj_lib`` module, not from ``transport_protocol`` directly.


Common Patterns
---------------

Device Creation
^^^^^^^^^^^^^^^

.. code-block:: python

    # Direct instantiation (recommended)
    device = DDriveDevice(TransportType.SERIAL, "COM3")
    
    # From discovery (devices are already instantiated)
    devices = await DDriveDevice.discover_devices()
    device = devices[0]  # Already a DDriveDevice instance


Connection Management
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Context manager (recommended)
    async with device:
        # Use device
        pass
    
    # Manual
    await device.open()
    try:
        # Use device
        pass
    finally:
        await device.close()


Channel Access
^^^^^^^^^^^^^^

.. code-block:: python

    # Get all channels
    channels = device.channels
    
    # Access by index
    channel = device.channels[0]
    
    # Iterate
    for channel in device.channels:
        # Use channel
        pass


Capability Access
^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Capabilities are channel attributes
    position = channel.position
    setpoint = channel.setpoint
    pid = channel.pid_controller
    recorder = channel.data_recorder
    
    # Use capabilities
    await setpoint.set(50.0)
    await pid.set(p=0.5, i=0.1, d=0.05)
    await recorder.start()


Error Handling
^^^^^^^^^^^^^^

.. code-block:: python

    from psj_lib import DeviceError, DeviceUnavailableException
    
    try:
        async with device:
            await channel.setpoint.set(50.0)
    
    except DeviceUnavailableException as e:
        print(f"Connection failed: {e}")
    
    except DeviceError as e:
        print(f"Device error: {e}")


Type Hints
----------

psj-lib includes comprehensive type hints for IDE autocomplete:

.. code-block:: python

    from psj_lib import DDriveDevice, TransportType, Position, PIDController
    
    async def typed_function(device: DDriveDevice) -> float:
        channel = device.channels[0]
        
        # IDE provides autocomplete for all methods
        position: Position = channel.position
        value: float = await position.get()
        
        return value


Async Patterns
--------------

Sequential Operations
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Operations execute one after another
    await channel.setpoint.set(30.0)
    await channel.setpoint.set(50.0)
    await channel.setpoint.set(70.0)


Parallel Operations
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Operations execute concurrently
    await asyncio.gather(
        channel1.setpoint.set(30.0),
        channel2.setpoint.set(60.0),
        channel3.setpoint.set(90.0)
    )


Timeouts
^^^^^^^^

.. code-block:: python

    # With timeout
    async with asyncio.timeout(5.0):
        await channel.setpoint.set(50.0)


Index
-----

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
