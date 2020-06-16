"""Format CSV reports from JSON files."""
import argparse

from compas_rcf.fab_data.tools import csv_reports

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

    csv_reports(args)
