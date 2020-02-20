"""Convert JSON file to CSV file.

Adapted from https://stackoverflow.com/a/28246154

Does not handle more than one level of nesting
"""
import argparse
import csv
import json
from pathlib import Path


def flattenjson(b, delim):
    val = {}
    for i in b.keys():
        if isinstance(b[i], dict):
            get = flattenjson(b[i], delim)
            for j in get.keys():
                val[i + delim + j] = get[j]
        else:
            val[i] = b[i]

    return val


def main(args):
    json_file = Path(args.json_file)
    with json_file.open(mode="r") as fp:
        json_ = fp.read()
    json_obj = json.loads(json_)

    flat_json = list(map(lambda x: flattenjson(x, "__"), json_obj))

    columns = [x for row in flat_json for x in row.keys()]
    columns = list(set(columns))

    csv_file = json_file.with_suffix(".csv")

    with csv_file.open(mode="w", encoding="utf8") as out_file:
        csv_w = csv.writer(out_file)
        csv_w.writerow(columns)

        for i_r in flat_json:
            csv_w.writerow(map(lambda x: i_r.get(x, ""), columns))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert json to CSV file")
    parser.add_argument("json_file", action="store", help="JSON file to convert")

    args = parser.parse_args()

    main(args)
