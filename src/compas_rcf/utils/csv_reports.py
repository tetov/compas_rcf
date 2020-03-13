"""Format CSV reports from JSON files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import csv
import datetime
from pathlib import Path

from compas_rcf.utils.json_ import load_bullets


def main(args):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format CSV reports from JSON files")
    parser.add_argument(
        "json_files",
        action="append",
        help="JSON files or directory containing JSON files to convert",
    )
    parser.add_argument(
        "--clobber", action="store_true", help="Overwrite existing files"
    )

    args = parser.parse_args()

    main(args)
