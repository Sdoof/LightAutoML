import argparse
import fileinput
from pathlib import Path
import sys
import re
from typing import Optional


PYPROJECT_TOML = Path("pyproject.toml")
DEFAULT_PYTHON_DEPS = ">=3.6.1, <3.10"
PYTHON_DEPS = {
    6: "~3.6.1",
    7: "~3.7.1",
    8: "~3.8.0",
    9: "~3.9.0"
}
PYTHON_DEPS_PATTERN = "^python = \".*\"$"


def _set_version(py_version: Optional[int] = None):
    for line in fileinput.input(PYPROJECT_TOML, inplace=1):
        if re.search(PYTHON_DEPS_PATTERN, line):
            if py_version is None:
                version = DEFAULT_PYTHON_DEPS
            else:
                version = PYTHON_DEPS[py_version]
            line = "python = \"{}\"\n".format(version)

        sys.stdout.write(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "version",
        nargs='?',
        const=1,
        type=int,
        choices=list(PYTHON_DEPS.keys()),
        default=None,
        help="Set python restriction in `pyproject.toml`"
    )

    args = parser.parse_args()

    _set_version(args.version)


if __name__ == "__main__":
    main()