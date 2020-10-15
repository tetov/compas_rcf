"""Tools for fab data."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
import json
from collections import OrderedDict

from rapid_clay_formations_fab.fab_data import ClayBullet
from rapid_clay_formations_fab.utils import CompasObjEncoder

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

        clay_bullets = load_bullets(json_file)

        headers_attrs = OrderedDict(
            (
                ("id", "bullet_id"),
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

            for bullet in clay_bullets:
                row = []
                for attr in headers_attrs.values():
                    row.append(getattr(bullet, attr, None))


def _load_run_data(file_path):
    with open(str(file_path), mode="r") as fp:
        run_data = json.load(fp)

    return run_data


def _get_fab_data(path_or_dict):
    if type(path_or_dict) == dict:
        dict_ = path_or_dict
    else:
        dict_ = _load_run_data(path_or_dict)

    return dict_["fab_data"]


def load_fabrication_elements(path_or_dict):
    """Load fabrication data from JSON file.

    Parameters
    ----------
    path_or_dict : :class:`os.PathLike` or :obj:`dict`
        Path to JSON representation or dictionary representation of fabrication
        element.

    Returns
    -------
    :obj:`list` of :class:`ClayBullet`
    """
    fab_data = _get_fab_data(path_or_dict)

    return [ClayBullet.from_data(data) for data in fab_data]


def load_bullets(path_or_dict):
    print("load_bullets will be removed in the future.")
    return load_fabrication_elements(path_or_dict)


def get_average_cycle_time(path_or_dict):
    cylinders = load_fabrication_elements(path_or_dict)

    sum_ = 0
    count = 0
    for cylinder in cylinders:
        if cylinder.cycle_time:
            count += 1
            sum_ += cylinder.cycle_time

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
    update_fabdata_attrs(path, {"bullet_id": 1}, from_=from_, to=None)


def renumber_fab_elements(path, prefix=None):
    run_data = _load_run_data(path)
    fab_elems = load_fabrication_elements(run_data)

    for i, fab_elem in enumerate(fab_elems):
        if prefix:
            fab_elem.bullet_id = "{}{:03d}".format(prefix, i)
        else:
            fab_elem.bullet_id = i

    run_data["fab_data"] = fab_elems
    with open(path, mode="w") as fp:
        json.dump(run_data, fp, cls=CompasObjEncoder)


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
        If true will change the `bullet_id` attribute to be the same as the
        element's index in list. Defaults to ``False``.
    overwrite : :obj:`bool`, optional
        Overwrite attributes. Defaults to ``False``.
    """
    run_data = _load_run_data(path)
    cylinders = load_fabrication_elements(run_data)

    if not from_:
        from_ = 0
    if not to:
        to = len(cylinders)

    for i, cylinder in enumerate(cylinders):
        modified = False
        if reset_ids:
            print("Changing id from {} to {}".format(cylinder.bullet_id, i))
            cylinder.bullet_id = i

        if from_ <= i < to:
            for key, value in updated_attrs.items():
                if getattr(cylinder, key, None) is None or overwrite:
                    setattr(cylinder, key, value)
                    modified |= True  # a fun OR gate

        if modified:
            print(
                "Cylinder with index {} and id {} updated.".format(
                    i, cylinder.bullet_id
                )
            )
        else:
            print(
                "Cylinder with index {} and id {} not updated.".format(
                    i, cylinder.bullet_id
                )
            )

    run_data["fab_data"] = cylinders
    with open(path, mode="w") as fp:
        json.dump(run_data, fp, cls=CompasObjEncoder)
