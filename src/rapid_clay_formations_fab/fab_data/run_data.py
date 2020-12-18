from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from rapid_clay_formations_fab.base_cls import BaseCls


class RunData(BaseCls):
    def __init__(self, fab_data, fab_conf, filepath=None):
        self.fab_data = fab_data
        self.fab_conf = fab_conf
        self.filepath = None

    @property
    def data(self):
        return {
            "fab_data": self.fab_data,
            "fab_conf": self.fab_conf,
            "filepath": self.filepath,
        }

    @data.setter
    def data(self, data):
        self.fab_data = data.get("fab_data")
        self.fab_conf = data.get("fab_conf")
        self.filepath = data.get("filepath")

    def to_data(self):
        data = self.data
        data["filepath"] = str(data["filepath"])
        data["fab_conf"] = confuse_conf_to_data(data["fab_conf"])
        return data

    @classmethod
    def from_data(cls, data):
        return cls(data["fab_data"], data["fab_conf"], filepath=data["filepath"])

    def to_json(self, path=None):
        _path = path or self.file_path

        if not _path:
            raise ValueError("No explicit or implict path has been given.")

        super(self, RunData).to_json(_path)


class FabData(BaseCls):
    def __init__(self, elements):
        self.elements = elements

    @property
    def data(self):
        return {"elements": self.elemenets}

    @data.setter
    def data(self, data):
        self.elements = data["elements"]

    def interactive_edit_sequence(self):
        pass
