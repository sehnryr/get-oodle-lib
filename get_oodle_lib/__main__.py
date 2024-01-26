import gzip
import os
import urllib.request
import xml.etree.ElementTree as etree
from pathlib import Path

from get_oodle_lib.common import parser
from get_oodle_lib.parse import (
    get_blobs,
    get_files,
    get_libraries,
    get_packs,
    match_blobs,
    match_packs,
)


def main():
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

    # Read the file and parse it
    with open(args.gitdeps, "r") as f:
        tree = etree.parse(f)

    base_url = tree.getroot().attrib["BaseUrl"]

    # Get the files
    files = get_files(tree)
    libraries = get_libraries(files, args.platform)

    # Get the blobs
    blobs = get_blobs(tree)
    blobs = match_blobs(libraries, blobs)

    # Get the packs
    packs = get_packs(tree)
    packs = match_packs(blobs, packs)

    # Download the libraries
    for library_path, library_data in libraries.items():
        file_name = library_path.rsplit("/", 1)[-1]

        blob_hash = library_data["hash"]
        blob = blobs[blob_hash]

        size = int(blob["size"])

        pack_offset = int(blob["pack_offset"])
        pack_hash = str(blob["pack_hash"])
        pack = packs[pack_hash]

        remote_path = pack["remote_path"]
        url = f"{base_url}/{remote_path}/{pack_hash}"

        # Download the pack
        response = urllib.request.urlopen(url)
        compressed = response.read()

        # Decompress the pack
        decompressed = gzip.decompress(compressed)

        # Write the library
        with open(f"{args.output}/{file_name}", "wb") as f:
            print(f"Writing {file_name}...")
            f.write(decompressed[pack_offset : pack_offset + size])


if __name__ == "__main__":
    main()
