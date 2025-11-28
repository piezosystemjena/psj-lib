from ...base.capabilities import DataRecorderChannel


class DDriveDataRecorderChannel(DataRecorderChannel):
    POSITION = DataRecorderChannel.CHANNEL_1
    VOLTAGE = DataRecorderChannel.CHANNEL_2