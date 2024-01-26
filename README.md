# get-oodle-lib
A library for getting the oodle library from Unreal Engine source code.

## Dependencies
- `Commit.gitdeps.xml` file from Unreal Engine source code (found [here](https://github.com/EpicGames/UnrealEngine/blob/release/Engine/Build/Commit.gitdeps.xml)) which access can be granted by following the instructions at https://github.com/EpicGames/Signup.

## Usage
```bash
python get_oodle_lib <path to Commit.gitdeps.xml> --platform <platform> --output <output directory>
```

For more information, run `python get_oodle_lib --help`.

You can also install the package with `pipx install git+https://github.com/sehnryr/get-oodle-lib` and run it with `get-oodle-lib`.
