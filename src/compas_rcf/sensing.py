from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import serial


def get_distance_measurement(address):
    with serial.Serial(address, 115200) as ser:
        while True:
            try:
                time.sleep(0.01)
                reading = ser.readline()
            except Exception as e:
                print(e)

        reading = float(reading.strip().partition(":")[-1])
        return reading
