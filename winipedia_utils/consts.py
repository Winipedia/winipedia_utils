"""Constants used throughout the winipedia_utils package.

This module contains package-wide constants that are used by various
modules within the package. These constants define core configuration
values and identifiers for the package.
"""

import tomllib
from pathlib import Path

toml = tomllib.loads(Path("pyproject.toml").read_text())

PACKAGE_NAME = toml["project"]["name"].replace("-", "_")
