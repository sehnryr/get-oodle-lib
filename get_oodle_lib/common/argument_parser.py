import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser(
    prog="get_oodle_lib",
    description="Get Oodle library for Unreal Engine",
)
parser.add_argument(
    "-p",
    "--platform",
    type=str,
    choices=["windows", "linux", "mac"],
    help="Target platform to download the Oodle library for",
    required=True,
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Path to output directory",
    default=".",
)
parser.add_argument(
    "gitdeps",
    type=str,
    help="Path to Commit.gitdeps.xml",
)

args = parser.parse_args()

# Check if the gitdeps's path is valid and exists
if not os.path.isfile(args.gitdeps):
    print("Invalid path to Commit.gitdeps.xml")
    exit(1)

# Check if the output path is valid and exists else create it
if not os.path.isdir(args.output):
    try:
        path = Path(args.output)
        path.mkdir(parents=True)
    except OSError:
        print("Invalid path to output directory")
        exit(1)
