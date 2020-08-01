from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import serial

from compas_rcf.fab_data import fab_conf


def readline_serial(port, baudrate):
    """Read line from serial bus.

    Parameters
    ----------
    port : :obj:`str`
        Serial port. Name convention in Windows systems is COM* while *nix
        family systems use /dev/tty*
    baudrate : :obj:`int`
        Symbols (signal changes) per second. One of the components that
        determines speed of communication over a data channel.

    Returns
    -------
    obj:bytes:

    Raises
    ------
    Exception
        ???
    """

    with serial.Serial(port, baudrate) as ser:
        while True:
            try:
                time.sleep(0.01)
                line = ser.readline()
            except Exception as e:
                print(e)
                raise

    return line.decode("ascii").strip()


def get_distance_measurement():
    """Read distance from distance sensors.

    Parameters specified in fab_conf (either from command line arguments or
    config file).

    Returns
    -------
    :obj:`float`
        Distance in millimeter.
    """
    address = fab_conf["tool"]["dist_sensor"]["port"].get()
    baudrate = fab_conf["tool"]["dist_sensor"]["baudrate"].get()
    return float(readline_serial(address, baudrate))


if __name__ == "__main__":
    print(get_distance_measurement("COM4", 115200))
