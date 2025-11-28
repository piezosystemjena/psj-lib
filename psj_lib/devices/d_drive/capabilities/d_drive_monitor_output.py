from ...base.capabilities import MonitorOutputSource


class DDriveMonitorOutputSource(MonitorOutputSource):
    CLOSED_LOOP_POSITION = 0
    SETPOINT = 1
    CONTROLLER_VOLTAGE = 2
    POSITION_ERROR = 3
    POSITION_ERROR_ABS = 4
    ACTUATOR_VOLTAGE = 5
    OPEN_LOOP_POSITION = 6