import gzip
import urllib.request
import xml.etree.ElementTree as etree

from get_oodle_lib.common import args
from get_oodle_lib.parse import (
    get_blobs,
    get_files,
    get_libraries,
    get_packs,
    match_blobs,
    match_packs,
)

# Read the file and parse it
with open(args.gitdeps, "r") as f:
    tree = etree.parse(f)

base_url = tree.getroot().attrib["BaseUrl"]

# Get the files
files = get_files(tree)
libraries = get_libraries(files)

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
