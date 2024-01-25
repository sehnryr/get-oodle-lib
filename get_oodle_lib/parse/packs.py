def get_packs(tree):
    # Get the root element
    root = tree.getroot()

    # Get the Packs element
    packs = root.find("Packs")
    if packs is None:
        raise ValueError("Packs element not found")

    # Get the Pack elements
    packs = packs.findall("Pack")

    return packs


def match_packs(blobs, packs) -> dict[str, dict[str, str | int]]:
    # Get the packs hashes
    pack_hashes = [data["pack_hash"] for data in blobs.values()]

    # Get the matched packs
    matched_packs = {}

    for pack in packs:
        if pack.attrib["Hash"] not in pack_hashes:
            continue

        matched_packs[pack.attrib["Hash"]] = {
            "size": int(pack.attrib["Size"]),
            "compressed_size": int(pack.attrib["CompressedSize"]),
            "remote_path": str(pack.attrib["RemotePath"]),
        }

    return matched_packs
