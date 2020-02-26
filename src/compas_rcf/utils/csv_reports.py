"""Format CSV reports from JSON files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import csv
import datetime
import json
from pathlib import Path


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

    for json_file in json_files:

        csv_file = json_file.with_suffix(".csv")

        if csv_file.exists() and not args.clobber:
            print("{} already exists, skipping.".format(csv_file))
            continue

        with json_file.open(mode="r") as fp:
            json_obj = json.load(fp)

        columns = [
            "id",
            "radius",
            "height",
            "density",
            "cycle_time",
            "placed",
            "location",
            "tool",
        ]

        with csv_file.open(mode="w", encoding="utf8", newline="") as out_file:
            csv_w = csv.writer(out_file)
            csv_w.writerow(columns)

            for bullet in json_obj:
                row = []

                # get bullet_id or id
                try:
                    row.append(bullet["bullet_id"])
                except KeyError:
                    row.append(bullet["id"])

                row.append(bullet["radius"])
                row.append(bullet["height"])

                if "density" in bullet.keys():
                    row.append(bullet["density"])
                else:
                    try:
                        row.append(bullet["attributes"]["density"])
                    except KeyError:
                        row.append("")

                if "cycle_time" in bullet.keys():
                    row.append(bullet["cycle_time"])
                else:
                    row.append("")

                if "placed" in bullet.keys():
                    time_obj = datetime.datetime.fromtimestamp(bullet["placed"])
                    time_str = time_obj.isoformat()
                    row.append(time_str)
                else:
                    row.append("")

                pt_fmt = ",".join(["{:.3f}"] * 3)
                row.append(pt_fmt.format(*bullet["_location"]["point"]))

                if "tool" in bullet.keys():
                    row.append(bullet["tool"])

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
