from enum import Enum

from .piezo_capability import PiezoCapability, ProgressCallback


class DataRecorderChannel(Enum):
    CHANNEL_1 = 1
    CHANNEL_2 = 2


class DataRecorder(PiezoCapability):
    CMD_MEMORY_LENGTH = "DATA_RECORDER_MEMORY_LENGTH"
    CMD_STRIDE = "DATA_RECORDER_RECORD_STRIDE"
    CMD_START_RECORDING = "DATA_RECORDER_START_RECORDING"
    CMD_PTR = "DATA_RECORDER_POINTER"
    CMD_GET_DATA_1 = "DATA_RECORDER_GET_DATA_1"
    CMD_GET_DATA_2 = "DATA_RECORDER_GET_DATA_2"


    async def set(
        self,
        memory_length: int | None = None,
        stride: int | None = None,
    ) -> None:
        if memory_length is not None:
            await self._write(self.CMD_MEMORY_LENGTH, [memory_length])

        if stride is not None:
            await self._write(self.CMD_STRIDE, [stride])

    async def get_memory_length(self) -> int:
        result = await self._write(self.CMD_MEMORY_LENGTH)
        return int(result[0])

    async def get_stride(self) -> int:
        result = await self._write(self.CMD_STRIDE)
        return int(result[0])

    async def start(self) -> None:
        await self._write(self.CMD_START_RECORDING, None)

    async def get_single_data(
        self,
        channel: DataRecorderChannel,
        index: int | None = None
    ) -> float:
        # Check if index pointer needs to be set
        if index is not None:
            await self._write(self.CMD_PTR, [index])

        cmd = self.CMD_GET_DATA_1 if channel == DataRecorderChannel.CHANNEL_1 else self.CMD_GET_DATA_2
        return await self._write(cmd)[0]

    async def get_all_data(
        self,
        channel: DataRecorderChannel,
        callback: ProgressCallback | None = None
    ) -> list[float]:
        # Get total length of recorded data
        length = await self.get_memory_length()
        data = []

        # Retrieve all data points for the specified channel
        for i in range(length):
            data.append(await self.get_single_data(channel, 0 if i == 0 else None))

            # Call progress callback if provided
            if callback is not None:
                callback(i + 1, length)

        return data