"""Tools for fab data."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
import json
from collections import OrderedDict

from compas_rcf.fab_data import ClayBullet

try:
    from pathlib import Path
except ImportError:
    pass


def csv_reports(args):
    """Convert fabrication data json files to CSV files.

    Use by running ``python -m compas_rcf.fab_data.csv_report``
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


def load_bullets(file_path):
    """Load fabrication data from JSON file.

    Parameters
    ----------
    file_path : :class:`os.PathLike` or :class:`str`
        JSON file to load data from.

    Returns
    -------
    :class:`list` of :class:`ClayBullet`
    """
    with open(str(file_path), mode="r") as fp:
        run_data = json.load(fp)

    # Accept either run_data file or fab_data file
    fab_data = run_data.get("fab_data") or run_data

    clay_cylinders = []
    for data in fab_data:
        clay_cylinders.append(ClayBullet.from_data(data))

    return clay_cylinders
