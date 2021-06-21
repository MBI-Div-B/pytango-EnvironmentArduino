#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tango import AttrWriteType, DevState, DebugIt, DispLevel
from tango.server import Device, attribute, command, device_property
import serial

class EnvironmentArduino(Device):
    Port = device_property(dtype=str, default_value='/dev/ttyArduino')
    Baudrate = device_property(dtype=int, default_value=115200)

# ------ Attributes ------ #

    humidity = attribute(label='Humidity',
                         dtype=float,
                         access=AttrWriteType.READ,
                         unit='%',
                         format='6.2f')

    # optionally use fget/fset to point to read and write functions.
    # Default is "read_temperature"/"write_temperature".
    # Added some optional attribute properties.
    temperature = attribute(label='Temperature',
                            dtype=float,
                            access=AttrWriteType.READ_WRITE,
                            unit='C',
                            format="6.2f",)

    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.INIT)

        try:
            self.info_stream('Connection to port {:s} with baudrate {:d}'.format(self.Port, self.Baudrate))
            self.serial = serial.Serial(port=self.Port, baudrate=self.Baudrate)
            if self.serial.is_open:
                self.serial.close()
            self.serial.open()
            self.set_state(DevState.ON)
        except:
            self.error_stream('Cannot connect to port {:s}!'.format(self.Port))
            self.set_state(DevState.OFF)

    def delete_device(self):
        if self.serial.is_open:
            self.serial.close()
            self.info_stream('Connection closed on port {:s}'.format(self.Port))
        self.set_state(DevState.OFF)

    def read_humidity(self):
        return 1

    def read_temperature(self):
        return 2


# start the server
if __name__ == "__main__":
    EnvironmentArduino.run_server()
