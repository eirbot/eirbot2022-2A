import logging
import struct

import serial


class SerialManager():
    def __init__(self, port="/dev/ttyACM0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate)
        self.type: dict[str, bin] = {"int_16": 0,
                                     "int_32": 1}

    def serial_read(self):
        data = self.ser.read()
        logging.info("Reading from serial: {}".format(data))
        return data

    def serial_write(self, op, int_type, param_array):
        header = op << 4 | int_type << 3 | len(param_array)
        data = []

        for param in param_array:
            if int_type == self.type["int_16"]:
                if param < -32768 or param > 32767:
                    raise ValueError
                data += struct.pack("!h", param)
            elif int_type == self.type["int_32"]:
                if param < -2147483648 or param > 2147483647:
                    raise ValueError
                data += struct.pack("!i", param)

        cmd = [header] + data
        logging.info("Writing to serial: {}".format(cmd))

        self.ser.write(cmd)

    def kms_is_dead(self, output):
        """
        This function check if the output on serial is KMS, if not count the number of time and reset nucleo if
        necessary.
        """
        if output != self.return_codes["KMS"]:
            self.kms_dead_count += 1
            if self.kms_dead_count >= 10:
                self.kms_dead_count = 0
                self.reset_soft_count += 1
                self.reset()
                if self.reset_soft_count >= 3:
                    self.reset_soft_count = 0
                    GPIO.output(self.gpio.GPIO["reset"]["pin"], GPIO.HIGH)
            return False
        else:
            self.kms_dead_count = 0
            self.reset_soft_count = 0
            return True
