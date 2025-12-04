Examples
========

This page demonstrates common use cases with complete, working examples.


Example Scripts
---------------

All examples are available in the ``examples/`` directory of the repository.


01 - Device Discovery and Connection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Demonstrates device discovery, connection, and basic information retrieval.

**What You'll Learn:**

* How to discover devices on Serial and Telnet
* Connecting to a device
* Displaying device information
* Listing available channels

**Code:** ``examples/01_device_discovery_and_connection.py``

.. code-block:: python

    from psj_lib import PiezoDevice, DDriveDevice, DiscoverFlags
    
    # Discover devices on all interfaces
    devices = await DDriveDevice.discover_devices(
        flags=DiscoverFlags.ALL_INTERFACES
    )
    
    # Display discovered devices
    for i, device in enumerate(devices):
        print(f"{i}: {device.device_id} on {device.address}")
    
    # Connect to first device
    if devices:
        device = devices[0]  # Already a DDriveDevice instance
        await device.connect()
        
        # Display channels
        for channel in device.channels:
            print(f"Channel {channel.channel_id}")


02 - Simple Position Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Basic position control with open-loop and closed-loop modes.

**What You'll Learn:**

* Reading current position
* Setting target positions
* Open-loop vs closed-loop control
* Position error checking

**Code:** ``examples/02_simple_position_control.py``

.. code-block:: python

    # Enable closed-loop control
    await channel.closed_loop_controller.set(True)
    
    # Move to target positions
    targets = [30.0, 50.0, 70.0]
    
    for target in targets:
        await channel.position.set(target)
        await asyncio.sleep(0.2)  # Settling time
        
        actual = await channel.position.get()
        error = abs(actual - target)
        print(f"Target: {target:.1f} µm, Actual: {actual:.2f} µm, "
              f"Error: {error:.3f} µm")


03 - PID Tuning
^^^^^^^^^^^^^^^^

Configure and test PID controller parameters.

**What You'll Learn:**

* Setting P, I, D parameters
* Reading current PID configuration
* Testing step response

**Code:** ``examples/03_pid_tuning.py``

.. code-block:: python

    # Set PID parameters
    await channel.pid_controller.set_p(0.5)
    await channel.pid_controller.set_i(0.1)
    await channel.pid_controller.set_d(0.05)
    
    # Read back settings
    p = await channel.pid_controller.get_p()
    i = await channel.pid_controller.get_i()
    d = await channel.pid_controller.get_d()
    
    print(f"PID Parameters: P={p:.3f}, I={i:.3f}, D={d:.3f}")


04 - Data Recorder Capture
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Record position and voltage data at high sample rates.

**What You'll Learn:**

* Configuring sample rate and buffer
* Starting and stopping recording
* Retrieving and saving data
* Optional plotting with matplotlib

**Code:** ``examples/04_data_recorder_capture.py``

.. code-block:: python

    # Configure recorder
    await channel.data_recorder.set_sample_rate(10000)  # 10 kHz
    await channel.data_recorder.set_num_samples(5000)   # 0.5 seconds
    
    # Start recording
    await channel.data_recorder.start()
    
    # Perform movement
    await channel.position.set(50.0)
    
    # Wait for recording
    await asyncio.sleep(0.6)
    
    # Get data
    data = await channel.data_recorder.get_data()
    
    # Export to CSV
    with open('recording.csv', 'w') as f:
        f.write('Time,Position,Voltage\n')
        for i in range(len(data['position'])):
            t = i / 10000
            f.write(f"{t:.6f},{data['position'][i]:.4f},"
                    f"{data['voltage'][i]:.4f}\n")


05 - Waveform Generation Basics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate periodic waveforms for scanning and testing.

**What You'll Learn:**

* Configuring different waveform types
* Setting frequency and amplitude
* Starting and stopping waveforms

**Code:** ``examples/05_waveform_generation_basics.py``

.. code-block:: python

    # Sine wave
    await channel.waveform_generator.sine.set_frequency(100.0)
    await channel.waveform_generator.sine.set_amplitude(20.0)
    await channel.waveform_generator.sine.set_offset(50.0)
    await channel.waveform_generator.enable()
    
    # Triangle wave (for scanning)
    await channel.waveform_generator.triangle.set_frequency(10.0)
    await channel.waveform_generator.triangle.set_amplitude(30.0)
    await channel.waveform_generator.enable()
    
    # Sweep (frequency response)
    await channel.waveform_generator.sweep.set_start_frequency(10)
    await channel.waveform_generator.sweep.set_stop_frequency(5000)
    await channel.waveform_generator.sweep.set_duration(10.0)
    await channel.waveform_generator.enable()


06 - Filter Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

Configure notch filter, LPF, and error LPF for optimal performance.

**What You'll Learn:**

* Enabling and configuring notch filter
* Setting low-pass filter cutoff
* Error low-pass filter setup

**Code:** ``examples/06_filter_configuration.py``

.. code-block:: python

    # Notch filter (suppress resonance)
    await channel.notch.set(frequency=2500.0, bandwidth=250.0, enabled=True)
    
    # Low-pass filter (reduce noise)
    await channel.lpf.set(cutoff_frequency=1000.0, enabled=True)
    
    # Error low-pass filter (PID stability)
    await channel.error_lpf.set(cutoff_frequency=200.0, enabled=True)


07 - Backup and Restore Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Save and restore device configuration to/from files.

**What You'll Learn:**

* Backing up channel configuration
* Saving to JSON file
* Restoring configuration from file

**Code:** ``examples/07_backup_and_restore_configuration.py``

.. code-block:: python

    import json
    
    # Backup configuration
    config = {}
    
    # PID parameters
    config['pid'] = {
        'p': await channel.pid_controller.get_p(),
        'i': await channel.pid_controller.get_i(),
        'd': await channel.pid_controller.get_d()
    }
    
    # Filter settings
    config['notch_freq'] = await channel.notch.get_frequency()
    config['lpf_cutoff'] = await channel.lpf.get_cutoff_frequency()
    
    # Save to file
    with open('device_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # Restore from file
    with open('device_config.json', 'r') as f:
        config = json.load(f)
    
    await channel.pid_controller.set_p(config['pid']['p'])
    await channel.pid_controller.set_i(config['pid']['i'])
    await channel.pid_controller.set_d(config['pid']['d'])


Common Patterns
---------------

Connection Pattern
^^^^^^^^^^^^^^^^^^

All examples follow this pattern:

.. code-block:: python

    import asyncio
    from psj_lib import DDriveDevice, TransportType
    
    async def main():
        # Create device instance
        device = DDriveDevice(TransportType.SERIAL, 'COM3')
        
        # Connect
        await device.connect()
        
        try:
            # Use device
            channel = device.channels[0]
            # ... operations ...
        
        finally:
            # Always disconnect
            await device.disconnect()
    
    if __name__ == "__main__":
        asyncio.run(main())


Error Handling Pattern
^^^^^^^^^^^^^^^^^^^^^^^

Robust error handling:

.. code-block:: python

    from psj_lib import DeviceError
    
    try:
        device = DDriveDevice(TransportType.SERIAL, 'COM3')
        await device.connect()
        
        # Operations...
        
    except DeviceError as e:
        print(f"Device error: {e}")
    
    finally:
        if device.is_connected:
            await device.disconnect()


Running Examples
----------------

Prerequisites
^^^^^^^^^^^^^

1. Install psj-lib:

   .. code-block:: bash

       pip install psj-lib

2. Connect your d-Drive device via USB or Ethernet

3. Note the connection details (COM port or IP address)


Running an Example
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Navigate to examples directory
    cd examples
    
    # Run example
    python 01_device_discovery_and_connection.py

**Note**: Adjust the COM port or IP address in each example to match your setup.


Modifying Examples
^^^^^^^^^^^^^^^^^^

Each example is self-contained and can be modified:

1. Open example file in your editor
2. Adjust connection parameters (port, IP address)
3. Modify parameters (positions, PID values, etc.)
4. Run and observe results


Integration Examples
--------------------

Multi-Channel Scanning
^^^^^^^^^^^^^^^^^^^^^^

Using two channels for 2D scanning:

.. code-block:: python

    async def raster_scan_2d(device):
        """2D raster scan with X and Y channels."""
        x_channel = device.channels[0]
        y_channel = device.channels[1]
        
        # Enable closed-loop on both
        await x_channel.closed_loop_controller.set(True)
        await y_channel.closed_loop_controller.set(True)
        
        # Scan parameters
        x_range = np.linspace(0, 100, 256)
        y_range = np.linspace(0, 100, 256)
        
        for y in y_range:
            await y_channel.position.set(y)
            
            for x in x_range:
                await x_channel.position.set(x)
                await asyncio.sleep(0.01)  # Dwell time
                
                # Acquire data here


Automated System Characterization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete characterization workflow:

.. code-block:: python

    async def characterize_system(channel):
        """Comprehensive system characterization."""
        results = {}
        
        # 1. Step response
        await channel.position.set(0.0)
        await asyncio.sleep(0.5)
        
        await channel.data_recorder.set_sample_rate(10000)
        await channel.data_recorder.set_num_samples(5000)
        await channel.data_recorder.start()
        
        await channel.position.set(50.0)
        await asyncio.sleep(0.6)
        
        data = await channel.data_recorder.get_data()
        results['step_response'] = analyze_step(data)
        
        # 2. Frequency response
        await channel.waveform_generator.sweep.set_start_frequency(10)
        await channel.waveform_generator.sweep.set_stop_frequency(5000)
        # ... configure and analyze
        
        # 3. Noise floor
        await channel.position.set(50.0)
        await asyncio.sleep(5.0)
        
        await channel.data_recorder.start()
        await asyncio.sleep(0.6)
        
        data = await channel.data_recorder.get_data()
        results['noise_rms'] = np.std(data['position'])
        
        return results


Real-Time Monitoring
^^^^^^^^^^^^^^^^^^^^

Continuous monitoring application:

.. code-block:: python

    async def monitor_position(channel, duration=60.0):
        """Monitor position for specified duration."""
        import csv
        
        start_time = asyncio.get_event_loop().time()
        
        with open('position_log.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Time', 'Position', 'Temperature'])
            
            while asyncio.get_event_loop().time() - start_time < duration:
                pos = await channel.position.get()
                temp = await channel.temperature.get()
                elapsed = asyncio.get_event_loop().time() - start_time
                
                writer.writerow([f'{elapsed:.3f}', f'{pos:.4f}', f'{temp:.2f}'])
                print(f"t={elapsed:.1f}s: {pos:.3f} µm, {temp:.1f}°C")
                
                await asyncio.sleep(0.1)


Best Practices from Examples
-----------------------------

1. **Always Disconnect**: Use try/finally to ensure disconnection
2. **Check Status**: Read status register before operations
3. **Wait for Settling**: Add delays after position changes
4. **Data Export**: Save data for later analysis
5. **Configuration Backup**: Save working configurations
6. **Gradual Changes**: Ramp parameters, don't make sudden changes


Next Steps
----------

* Review full API documentation: :doc:`api`
* Learn about advanced features: :doc:`advanced_topics`
* Read developer guide: :doc:`developer_guide`
* Explore device-specific docs: :doc:`d_drive`
