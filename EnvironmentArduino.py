#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tango import AttrWriteType, DevState, DebugIt, DispLevel
from tango.server import Device, attribute, command, device_property
import serial
from time import sleep

class EnvironmentArduino(Device):
    Port = device_property(dtype=str, default_value='/dev/ttyArduino')
    Baudrate = device_property(dtype=int, default_value=115200)

    humidity = attribute(label='Humidity',
                         dtype=float,
                         access=AttrWriteType.READ,
                         unit='%',
                         format='4.1f')

    temperature = attribute(label='Temperature',
                            dtype=float,
                            access=AttrWriteType.READ,
                            unit='C',
                            format="4.1f",)

    rate = attribute(label='Rate',
                            dtype=float,
                            access=AttrWriteType.READ,
                            unit='Hz',
                            format="4.1f",)

    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.INIT)

        try:
            self.info_stream('Connection to port {:s} with baudrate {:d}'.format(self.Port, self.Baudrate))
            self.serial = serial.Serial(port=self.Port, baudrate=self.Baudrate, timeout=0)
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
        return float(self.query('h'))

    def read_temperature(self):
        return float(self.query('t'))

    def read_rate(self):
        return float(self.query('r'))

    def query(self, cmd):
        cmd_str = '{:s}\r\n'.format(cmd)
        self.debug_stream('Sending command: {:s}'.format(cmd_str))
        self.serial.write(cmd_str.encode('utf-8'))
        self.serial.flush()
        sleep(1)
        res = self.serial.readline().decode('utf-8')
        self.debug_stream('Receiving result: {:s}'.format(res))
        return res

# start the server
if __name__ == "__main__":
    EnvironmentArduino.run_server()
