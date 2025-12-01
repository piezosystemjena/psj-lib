from ...base.capabilities import DataRecorderChannel


class DDriveDataRecorderChannel(DataRecorderChannel):
    """d-Drive data recorder channel aliases with semantic names.
    
    Provides meaningful names for the two hardware data recorder channels
    in d-Drive amplifiers. The d-Drive always records position on channel 1
    and actuator voltage on channel 2.
    
    Attributes:
        POSITION: Position sensor signal (alias for CHANNEL_1).
            Records actual measured position from the sensor.
        VOLTAGE: Actuator voltage signal (alias for CHANNEL_2).
            Records the output voltage applied to the piezo actuator.
    
    Example:
        >>> from psj_lib import DDriveDataRecorderChannel
        >>> # Configure recorder
        >>> await channel.data_recorder.set(
        ...     memory_length=50000,  # 1 second at 50 kHz
        ...     stride=1
        ... )
        >>> await channel.data_recorder.start()
        >>> # ... perform motion ...
        >>> # Retrieve position data using semantic name
        >>> pos_data = await channel.data_recorder.get_all_data(
        ...     DDriveDataRecorderChannel.POSITION
        ... )
        >>> # Retrieve voltage data
        >>> vol_data = await channel.data_recorder.get_all_data(
        ...     DDriveDataRecorderChannel.VOLTAGE
        ... )
        >>> print(f\"Recorded {len(pos_data)} position samples\")\n        >>> print(f\"Recorded {len(vol_data)} voltage samples\")
    
    Note:
        - Both channels always record simultaneously
        - Sample rate: 50 kHz (20 µs period) maximum
        - Maximum 500,000 samples per channel
        - POSITION and VOLTAGE are semantic aliases for hardware channels
    """
    POSITION = DataRecorderChannel.CHANNEL_1
    VOLTAGE = DataRecorderChannel.CHANNEL_2