from ..base.piezo_channel import PiezoChannel
from ..base.capabilities import *
from .capabilities.d_drive_modulation_source import DDriveModulationSourceTypes
from .capabilities.d_drive_status_register import DDriveStatusRegister
from .capabilities.d_drive_trigger_out import DDriveTriggerOut
from .capabilities.d_drive_waveform_generator import DDriveWaveformGenerator


class DDriveChannel(PiezoChannel):
    """
    Represents a channel of a D-Drive amplifier.
    """

    BACKUP_COMMANDS = {
        "fan",
        "modon",
        "monsrc",
        "cl",
        "sr",
        "pcf",
        "errlpf",
        "elpor",
        "kp",
        "ki",
        "kd",
        "tf",
        "notchon",
        "notchf",
        "notchb",
        "lpon",
        "lpf",
        "gfkt",
        "gasin",
        "gosin",
        "gfsin",
        "gatri",
        "gotri",
        "gftri",
        "gstri",
        "garec",
        "gorec",
        "gfrec",
        "gsrec",
        "ganoi",
        "gonoi",
        "gaswe",
        "goswe",
        "gtswe",
        "sct",
        "trgss",
        "trgse",
        "trgsi",
        "trglen",
        "trgedge",
        "trgsrc",
        "trgoffs",
        "recstride",
        "reclen",
        "bright",
    }
    
    # Capability descriptors
    status_register = CapabilityDescriptor(
        Status, {
            Status.CMD_STATUS: "stat"
        },
        DDriveStatusRegister
    )

    actuator_description = CapabilityDescriptor(
        ActuatorDescription, {
            ActuatorDescription.CMD_DESCRIPTION: "acdescr"
        }
    )

    setpoint = CapabilityDescriptor(
        Setpoint, {
            Setpoint.CMD_SETPOINT: "set"
        }
    )

    position = CapabilityDescriptor(
        Position, {
            Position.CMD_POSITION: "mess"
        }
    )

    temperature = CapabilityDescriptor(
        Temperature, {
            Temperature.CMD_TEMPERATURE: "ktemp"
        }
    )

    fan = CapabilityDescriptor(
        Fan, {
            Fan.CMD_ENABLE: "fan"
        }
    )

    modulation_source = CapabilityDescriptor(
        ModulationSource, {
            ModulationSource.CMD_SOURCE: "modon"
        },
        DDriveModulationSourceTypes
    )

    monitor_output = CapabilityDescriptor(
        MonitorOutput, {
            MonitorOutput.CMD_OUTPUT_SRC: "monsrc"
        }
    )

    closed_loop_controller = CapabilityDescriptor(
        ClosedLoopController, {
            ClosedLoopController.CMD_ENABLE: "cloop"
        }
    )

    slew_rate = CapabilityDescriptor(
        SlewRate, {
            SlewRate.CMD_RATE: "sr"
        }
    )

    pcf = CapabilityDescriptor(
        PreControlFactor, {
            PreControlFactor.CMD_VALUE: "pcf"
        }
    )

    error_lpf = CapabilityDescriptor(
        ErrorLowPassFilter, {
            ErrorLowPassFilter.CMD_CUTOFF_FREQUENCY: "errlpf",
            ErrorLowPassFilter.CMD_ORDER: "elpor"
        }
    )

    pid_controller = CapabilityDescriptor(
        PIDController, {
            PIDController.CMD_P: "kp",
            PIDController.CMD_I: "ki",
            PIDController.CMD_D: "kd",
            PIDController.CMD_TF: "tf"
        }
    )

    notch = CapabilityDescriptor(
        NotchFilter, {
            NotchFilter.CMD_ENABLE: "notchon",
            NotchFilter.CMD_FREQUENCY: "notchf",
            NotchFilter.CMD_BANDWIDTH: "notchb"
        }
    )

    lpf = CapabilityDescriptor(
        LowPassFilter, {
            LowPassFilter.CMD_ENABLE: "lpon",
            LowPassFilter.CMD_CUTOFF_FREQUENCY: "lpf"
        }
    )

    trigger_out = CapabilityDescriptor(
        DDriveTriggerOut, {
            DDriveTriggerOut.CMD_START: "trigstart",
            DDriveTriggerOut.CMD_STOP: "trigstop",
            DDriveTriggerOut.CMD_INTERVAL: "trigint",
            DDriveTriggerOut.CMD_LENGTH: "triglen",
            DDriveTriggerOut.CMD_EDGE: "trigedge",
            DDriveTriggerOut.CMD_SRC: "trigsrc",
            DDriveTriggerOut.CMD_OFFSET: "trigoffset"
        }
    )

    data_recorder = CapabilityDescriptor(
        DataRecorder, {
            DataRecorder.CMD_START_RECORDING: "recstart",
            DataRecorder.CMD_STRIDE: "recstride",
            DataRecorder.CMD_MEMORY_LENGTH: "reclen",
            DataRecorder.CMD_PTR: "recrdptr",
            DataRecorder.CMD_GET_DATA_1: "m",
            DataRecorder.CMD_GET_DATA_2: "u"
        }
    )

    units = CapabilityDescriptor(
        Units, {
            Units.CMD_UNIT_POSITION: "acclmas",
            Units.CMD_UNIT_VOLTAGE: "acolmas"
        }
    )

    waveform_generator = CapabilityDescriptor(
        DDriveWaveformGenerator, {
            DDriveWaveformGenerator.CMD_WFG_TYPE: "gfkt",
            DDriveWaveformGenerator.CMD_SINE_AMPLITUDE: "gasin",
            DDriveWaveformGenerator.CMD_SINE_OFFSET: "gosin",
            DDriveWaveformGenerator.CMD_SINE_FREQUENCY: "gfsin",
            DDriveWaveformGenerator.CMD_TRI_AMPLITUDE: "gatri",
            DDriveWaveformGenerator.CMD_TRI_OFFSET: "gotri",
            DDriveWaveformGenerator.CMD_TRI_FREQUENCY: "gftri",
            DDriveWaveformGenerator.CMD_TRI_DUTY_CYCLE: "gstri",
            DDriveWaveformGenerator.CMD_REC_AMPLITUDE: "garec",
            DDriveWaveformGenerator.CMD_REC_OFFSET: "gorec",
            DDriveWaveformGenerator.CMD_REC_FREQUENCY: "gfrec",
            DDriveWaveformGenerator.CMD_REC_DUTY_CYCLE: "gsrec",
            DDriveWaveformGenerator.CMD_NOISE_AMPLITUDE: "ganoi",
            DDriveWaveformGenerator.CMD_NOISE_OFFSET: "gonoi",
            DDriveWaveformGenerator.CMD_SWEEP_AMPLITUDE: "gaswe",
            DDriveWaveformGenerator.CMD_SWEEP_OFFSET: "goswe",
            DDriveWaveformGenerator.CMD_SWEEP_TIME: "gtswe",
            DDriveWaveformGenerator.CMD_SCAN_START: "ss",
            DDriveWaveformGenerator.CMD_SCAN_TYPE: "sct"
        }
    )