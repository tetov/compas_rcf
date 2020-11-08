"""Tools for fab data."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
import json
from collections import OrderedDict

from compas.utilities import DataDecoder


try:
    from pathlib import Path
except ImportError:
    pass


def csv_reports(args):
    """Convert fabrication data json files to CSV files.

    Use by running ``python -m rapid_clay_formations_fab.fab_data.csv_report``
    """
    json_files = []

    for file_path in args.json_files:

        pathobj = Path(file_path)

        if pathobj.is_dir():
            for child in pathobj.iterdir():
                if child.suffix == ".json":
                    json_files.append(child)
        elif pathobj.suffix == ".json":
            json_files.append(pathobj)
        else:
            raise ValueError(
                "File needs to be a json file and have .json as the extension."
            )

    for json_file in json_files:

        csv_file = json_file.with_suffix(".csv")

        if csv_file.exists() and not args.clobber:
            print("{} already exists, skipping.".format(csv_file))
            continue

        with json_file.open(mode="r") as fp:
            run_data = json.load(fp, cls=DataDecoder)
        elements = run_data["fab_data"]

        headers_attrs = OrderedDict(
            (
                ("id", "id_"),
                ("radius (mm)", "radius"),
                ("height (mm)", "height"),
                ("compression-height-ratio", "compression_ratio"),
                ("density (kg/l)", "density"),
                ("cycle time (s)", "cycle_time"),
                ("time placed (from epoch)", "placed"),
                ("location frame", "location"),
            )
        )

        with csv_file.open(mode="w", encoding="utf8", newline="") as out_file:
            csv_w = csv.writer(out_file)
            csv_w.writerow(headers_attrs.keys())

            for elem in elements:
                row = []
                for attr in headers_attrs.values():
                    row.append(getattr(elem, attr, None))


def get_average_cycle_time(elements):
    sum_ = 0
    count = 0
    for elem in elements:
        if elem.cycle_time:
            count += 1
            sum_ += elem.cycle_time

    return sum_ / count


def mark_placed(path, from_=None, to=None):
    """Mark fabrication elemenets as placed in JSON file.

    Parameters
    ----------
    path : :class:`os.PathLike`
    from_ : :obj:`int`, optional
        Defines lower bound of element index to mark (inclusive).
    to : :obj:`int`, optional
        Defines upper bound of element index to mark (exclusive).
    """
    update_fabdata_attrs(path, {"id_": 1}, from_=from_, to=to)


def renumber_fab_elements(path, prefix=None):
    with open(path, mode="r") as fp:
        run_data = json.load(fp, cls=DataDecoder)
    fab_elems = run_data["fab_data"]

    for i, fab_elem in enumerate(fab_elems):
        if prefix:
            fab_elem.id_ = "{}{:03d}".format(prefix, i)
        else:
            fab_elem.id_ = i

    with open(path, mode="w") as fp:
        json.dump(run_data, fp, cls=DataDecoder)


def update_fabdata_attrs(
    path, updated_attrs, from_=None, to=None, reset_ids=False, overwrite=False
):
    """Update fabrication element's attributes in JSON file.

    Parameters
    ----------
    path : :class:`os.PathLike`
    updated_attrs : :obj:`dict`
        Dictionary of attribute names and new values.
    from_ : :obj:`int`, optional
        Defines lower bound of element index to mark (inclusive).
    to : :obj:`int`, optional
        Defines upper bound of element index to mark (exclusive).
    reset_ids : :obj:`bool`, optional
        If true will change the `id_` attribute to be the same as the
        element's index in list. Defaults to ``False``.
    overwrite : :obj:`bool`, optional
        Overwrite attributes. Defaults to ``False``.
    """
    with open(path, mode="r") as fp:
        run_data = json.load(fp, cls=DataDecoder)
    elements = run_data["fab_data"]

    if not from_:
        from_ = 0
    if not to:
        to = len(elements)

    for i, elem in enumerate(elements):
        modified = False
        if reset_ids:
            print("Changing id from {} to {}".format(elem.id_, i))
            elem.id_ = i

        if from_ <= i < to:
            for key, value in updated_attrs.items():
                if getattr(elem, key, None) is None or overwrite:
                    setattr(elem, key, value)
                    modified |= True  # a fun OR gate

        if modified:
            print("Element with index {} and id {} updated.".format(i, elem.id_))
        else:
            print("Element with index {} and id {} not updated.".format(i, elem.id_))

    with open(path, mode="w") as fp:
        json.dump(run_data, fp, cls=DataDecoder)
