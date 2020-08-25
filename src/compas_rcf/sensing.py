from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

log = logging.getLogger(__name__)


def serial_readline_to_str(port, baudrate):
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
    :obj:`bytes`

    Raises
    ------
    Exception
        ???
    """
    import serial

    log.debug(
        "Reading serial input from port: {} and baudrate: {}".format(port, baudrate)
    )
    with serial.Serial(port=port, baudrate=baudrate, timeout=10) as ser:
        line = ser.readline()

    line = line.decode("ascii").strip()
    log.debug("Line read: {}".format(line))

    return line


class ClayCylinderMeasurement(object):
    SEPARATOR = ":"
    DUMMY_MSG = "9999" + SEPARATOR + "9999"

    def __init__(self, frame=None, expected_dist=None, raw_reading=None):

        self.frame = frame
        self.expected_reading = expected_dist

        self.raw_reading = raw_reading

    def __str__(self):
        return "Measurement at {}. Expected reading: {}. Measured distance: {}.".format(
            self.frame, self.expected_reading, self.dist
        )

    @property
    def dist(self):
        """:obj:`float` : Distance in millimeter given by distance sensor."""
        return self.parse_raw_reading()["dist"]

    @property
    def at_milli(self):
        """:obj:`int` : Milliseconds from power on from arduino with distance sensor."""
        return self.parse_raw_reading()["at_milli"]

    def measure(self, port, baudrate, use_dummy=False):
        if use_dummy:
            self.raw_reading = self.DUMMY_MSG
        else:
            self.raw_reading = serial_readline_to_str(port, baudrate)

    def parse_raw_reading(self):
        if not self.raw_reading:
            raise RuntimeError("No raw reading recorded.")

        at_milli, dist = self.raw_reading.split(self.SEPARATOR)

        return {"at_milli": at_milli, "dist": dist}

    def get_dist_diff(self):
        if not self.raw_reading:
            raise RuntimeError("Distance not measured (yet).")
        if not self.expected_dist:
            raise ValueError("No expected dist set.")

        return self.dist - self.expected_dist

    def to_data(self):
        """Get :obj:`dict` representation of :class:`ClayBullet`."""
        data = {}

        for key, value in self.__dict__.items():
            if hasattr(value, "to_data"):
                data[key] = value.to_data()
            else:
                data[key] = value

        return data

    @classmethod
    def from_data(cls, data):
        for key, value in data.items():
            if hasattr(value, "from_data"):
                data[key] = value.from_data()

        return cls(**data)


if __name__ == "__main__":
    pass
