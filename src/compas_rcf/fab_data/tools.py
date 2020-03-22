"""Tools for fab data."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
import datetime
import json

import compas.geometry as cg

from compas_rcf.fab_data.clay_objs import ClayBullet

try:
    from pathlib import Path
except ImportError:
    try:
        from pathlib2 import Path
    except ImportError:
        pass

__all__ = ["csv_reports", "ClayBulletEncoder", "load_bullets"]


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

        columns = [
            "id",
            "radius (mm)",
            "height (mm)",
            "compression-height-ratio",
            "density (kg/l)",
            "cycle_time (s)",
            "time placed (in UTC)",
            "location (xyz in mm)",
            "tool",
            "weight (kg)",
        ]

        with csv_file.open(mode="w", encoding="utf8", newline="") as out_file:
            csv_w = csv.writer(out_file)
            csv_w.writerow(columns)

            for bullet in clay_bullets:
                row = []

                # get bullet_id or id
                try:
                    row.append(bullet.bullet_id)
                except AttributeError:
                    row.append(bullet.id)

                row.append(bullet.radius)
                row.append(bullet.height)
                row.append(bullet.compression_ratio)

                try:
                    if bullet.density:
                        row.append(bullet.density)
                except AttributeError:
                    try:
                        row.append(bullet.attributes["density"])
                    except (AttributeError, KeyError):
                        row.append(None)

                row.append(bullet.cycle_time)

                if bullet.placed:
                    time_obj = datetime.datetime.fromtimestamp(bullet.placed)
                    time_str = time_obj.isoformat()
                    row.append(time_str)
                else:
                    row.append(None)

                pt_fmt = ",".join(["{:.3f}"] * 3)
                row.append(pt_fmt.format(*bullet.location.point))

                row.append(bullet.tool)

                try:
                    row.append(bullet.weight_kg)
                except AttributeError:
                    row.append(None)

                csv_w.writerow(row)


class ClayBulletEncoder(json.JSONEncoder):
    """JSON encoder for :class:`ClayBullet`.

    Implemented from https://docs.python.org/3/library/json.html#json.JSONEncoder
    """

    def default(self, obj):
        if isinstance(obj, ClayBullet):
            return obj.__dict__
        if isinstance(obj, cg.Primitive):
            return obj.to_data()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


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
        json_string = json.load(fp)

    clay_bullets = []
    for dict_ in json_string:
        clay_bullets.append(ClayBullet.from_data(dict_))

    return clay_bullets
