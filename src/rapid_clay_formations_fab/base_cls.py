from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from compas.utilities import DataDecoder
from compas.utilities import DataEncoder

try:
    import typing

    if typing.TYPE_CHECKING:
        import os
except ImportError:
    pass


class BaseCls(object):
    @property
    def dtype(self):  # type: () -> str
        """Type in the form of a "2-level" import and a class name."""
        return "{}/{}".format(
            ".".join(self.__class__.__module__.split(".")[:2]), self.__class__.__name__
        )

    @property
    def data(self):  # type: () -> dict
        """Representation of the object as native Python data.

        The structure of the data is described by the data schema.
        """
        raise NotImplementedError

    @data.setter
    def data(self, data):  # type: (dict) -> None
        pass

    @classmethod
    def from_data(cls, data):  # type: (dict) -> BaseCls
        """Construct an object of this type from the provided data."""
        raise NotImplementedError

    def to_data(self):  # type: () -> dict
        """Convert an object to its native data representation."""
        raise NotImplementedError

    @classmethod
    def from_json(cls, filepath):  # type: (os.PathLike) -> BaseCls
        """Construct an object from serialised data contained in a JSON file.

        Parameters
        ----------
        filepath
            The path to the file for serialisation.
        """
        with open(filepath, mode="r") as fp:
            data = json.load(fp, cls=DataDecoder)

        return cls.from_data(data)

    def to_json(self, filepath):  # type: (os.PathLike) -> None
        """Serialize the data representation of an object to a JSON file.

        Parameters
        ----------
        filepath
            The path to the file containing the data.
        """
        with open(filepath, mode="w") as fp:
            json.dump(self, fp, cls=DataEncoder)
