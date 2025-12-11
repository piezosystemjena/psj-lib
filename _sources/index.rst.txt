psj-lib: Piezosystem Jena Device Library
=========================================

.. image:: images/psj-lib-header.png

**psj-lib** is a comprehensive Python library for controlling piezoelectric amplifiers and control 
devices manufactured by `piezosystem jena GmbH <https://www.piezosystem.com>`_. The library provides 
an intuitive, asynchronous interface for precision position control, waveform generation, data 
acquisition, and advanced control system configuration.

**Key Features:**

* **Asynchronous Architecture**: Built on Python's asyncio for efficient, non-blocking device communication
* **Multi-Device Support**: Extensible framework supporting multiple device families (currently d-Drive)
* **Comprehensive Capabilities**: Full access to position control, PID tuning, waveform generation, data recording, and filtering
* **Multiple Transport Protocols**: Connect via Serial (USB) or Telnet (Ethernet)
* **Type-Safe API**: Complete type hints for excellent IDE autocomplete and type checking
* **Extensive Documentation**: Comprehensive docstrings, examples, and developer guides

**Currently Supported Devices:**

* **d-Drive**: Modular piezo amplifiers with 20-bit resolution, 50 kHz sampling, and advanced control features

**Quick Start:**

.. code-block:: python

    import asyncio
    from psj_lib import DDriveDevice, TransportType
    
    async def main():
        device = DDriveDevice(TransportType.SERIAL, "COM3")
        
        async with device:
            channel = device.channels[0]
            await channel.closed_loop_controller.set(True)
            await channel.setpoint.set(50.0)
            print(f"Position: {await channel.position.get():.2f} µm")
    
    asyncio.run(main())

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   intro
   installation
   connecting
   getting_started

.. toctree::
   :maxdepth: 2
   :caption: Device Documentation:

   d_drive
   base_capabilities

.. toctree::
   :maxdepth: 2
   :caption: Reference:

   api
   examples
   developer_guide

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
