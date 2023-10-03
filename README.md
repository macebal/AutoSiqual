# AutoSiqual

A standalone application to input data into from Excel workbooks and into Siqual. The robot automatically clicks all the relevant buttons and navigates through all the menus.

## Usage

After cloning the repository, create python virtual environment and activate it:

```
python -m venv .venv
source .venv/Scripts/activate
```

Then run

```
make install
```

If make commands are not available run `python -m pip install poetry==1.6.1` and `poetry install`.

Once all the dependencies are installed, simply run

```
make run-dev
```

Or, if make commands are not available: `python -m main`

## Building standalone executables

This section requires a virtual environment running with all the dependecies installed.

To build the project into a standalone executable, run:

```
make build
```

The resulting zip file can be found in the dist/ folder

**Note:** The build script attempts to use the `zip` command to zip the executable and related config files and images. If the `zip` command is not available, for example in windows using Git Bash, [these instructions](https://stackoverflow.com/a/55749636) must be followed first. Orsimply zip all the files and folders inside the dist/ folder manually.

## Bumping the version

To bump the version, use the following command:

```
make version-bump version_bump_type=<VERSION BUMP TYPE>
```

where `<VERSION BUMP TYPE>` can be for example "major", "minor", "patch", etc. For more information see: https://python-poetry.org/docs/cli/#version
