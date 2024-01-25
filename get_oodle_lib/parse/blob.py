def get_blobs(tree):
    # Get the root element
    root = tree.getroot()

    # Get the Blobs element
    blobs = root.find("Blobs")
    if blobs is None:
        raise ValueError("Blobs element not found")

    # Get the Blob elements
    blobs = blobs.findall("Blob")

    return blobs


def match_blobs(files, blobs) -> dict[str, dict[str, str | int]]:
    # Get the blobs hashes
    blob_hashes = [data["hash"] for data in files.values()]

    # Get the matched blobs
    matched_blobs = {}

    for blob in blobs:
        if blob.attrib["Hash"] not in blob_hashes:
            continue

        matched_blobs[blob.attrib["Hash"]] = {
            "size": int(blob.attrib["Size"]),
            "pack_hash": str(blob.attrib["PackHash"]),
            "pack_offset": int(blob.attrib["PackOffset"]),
        }

    return matched_blobs
