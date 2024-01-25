def get_files(tree):
    # Get the root element
    root = tree.getroot()

    # Get the Files element
    files = root.find("Files")
    if files is None:
        raise ValueError("Files element not found")

    # Get the File elements
    files = files.findall("File")

    return files


def get_version(name, platform):
    # Check if the file is a library
    if not name.startswith("Engine/Source/Runtime/OodleDataCompression/Sdks/"):
        raise ValueError("File is not a library")

    # Split the file name
    splitted = name.split("/")

    # Check if the file is for the target platform
    platform_map = {
        "windows": "Win64",
        "linux": "Linux",
        "mac": "Mac",
    }
    if splitted[7] != platform_map[platform]:
        raise ValueError("File is not for the target platform")

    return tuple(map(int, splitted[5].split(".")))


def get_libraries(files, platform) -> dict[str, dict[str, str]]:
    libraries = {}
    version = (0, 0, 0)

    # Get the libraries
    for file in files:
        # Get the version from the file
        try:
            _version = get_version(file.attrib["Name"], platform)
        except ValueError:
            continue

        # Check if the version is newer than the current version
        if _version > version:
            version = _version

        # Check if the version is the same as the current version
        if _version == version:
            # Add the library to the libraries list
            libraries[file.attrib["Name"]] = {"hash": str(file.attrib["Hash"])}

    # Clean up the libraries list
    libraries = {
        library: values
        for library, values in libraries.items()
        if get_version(library, platform) == version
    }

    return libraries
