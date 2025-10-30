"""Config utilities for poetry and pyproject.toml."""

from pathlib import Path
from typing import Any, cast

from winipedia_utils.modules.package import get_src_package, make_name_from_package
from winipedia_utils.projects.poetry.poetry import VersionConstraint
from winipedia_utils.testing.config import ExperimentConfigFile
from winipedia_utils.testing.convention import TESTS_PACKAGE_NAME
from winipedia_utils.text.config import ConfigFile, TomlConfigFile


class PyprojectConfigFile(TomlConfigFile):
    """Config file for pyproject.toml."""

    @classmethod
    def get_parent_path(cls) -> Path:
        """Get the path to the config file."""
        return Path()

    @classmethod
    def get_configs(cls) -> dict[str, Any]:
        """Get the config."""
        return {
            "project": {
                "name": make_name_from_package(get_src_package(), capitalize=False),
                "readme": "README.md",
                "dynamic": ["dependencies"],
            },
            "build-system": {
                "requires": ["poetry-core>=2.0.0,<3.0.0"],
                "build-backend": "poetry.core.masonry.api",
            },
            "tool": {
                "poetry": {
                    "packages": [{"include": get_src_package().__name__}],
                    "dependencies": dict.fromkeys(
                        cls.get_dependencies(),
                        "*",
                    ),
                    "group": {
                        "dev": {
                            "dependencies": dict.fromkeys(
                                cls.get_dev_dependencies(),
                                "*",
                            )
                        }
                    },
                },
                "ruff": {
                    "exclude": [".*", "**/migrations/*.py"],
                    "lint": {
                        "select": ["ALL"],
                        "ignore": ["D203", "D213", "COM812", "ANN401"],
                        "fixable": ["ALL"],
                        "pydocstyle": {"convention": "google"},
                    },
                },
                "mypy": {
                    "strict": True,
                    "warn_unreachable": True,
                    "show_error_codes": True,
                    "files": ".",
                },
                "pytest": {"ini_options": {"testpaths": [TESTS_PACKAGE_NAME]}},
                "bandit": {
                    "exclude_dirs": [ExperimentConfigFile.get_path().as_posix()],
                },
            },
        }

    @classmethod
    def get_package_name(cls) -> str:
        """Get the package name."""
        project_dict = cls.load().get("project", {})
        package_name = str(project_dict.get("name", ""))
        return package_name.replace("-", "_")

    @classmethod
    def get_all_dependencies(cls) -> set[str]:
        """Get all dependencies."""
        return cls.get_dependencies() | cls.get_dev_dependencies()

    @classmethod
    def get_dev_dependencies(cls) -> set[str]:
        """Get the dev dependencies."""
        dev_dependencies = set(
            cls.load()
            .get("tool", {})
            .get("poetry", {})
            .get("group", {})
            .get("dev", {})
            .get("dependencies", {})
            .keys()
        )
        if not dev_dependencies:
            dev_dependencies = set(
                cls.load().get("dependency-groups", {}).get("dev", [])
            )
            dev_dependencies = {d.split("(")[0].strip() for d in dev_dependencies}
        return dev_dependencies

    @classmethod
    def get_dependencies(cls) -> set[str]:
        """Get the dependencies."""
        return set(
            cls.load().get("tool", {}).get("poetry", {}).get("dependencies", {}).keys()
        )

    @classmethod
    def get_expected_dev_dependencies(cls) -> set[str]:
        """Get the expected dev dependencies."""
        return set(
            cls.get_configs()["tool"]["poetry"]["group"]["dev"]["dependencies"].keys()
        )

    @classmethod
    def get_authors(cls) -> list[dict[str, str]]:
        """Get the authors."""
        return cast(
            "list[dict[str, str]]", cls.load().get("project", {}).get("authors", [])
        )

    @classmethod
    def get_main_author(cls) -> dict[str, str]:
        """Get the main author.

        Assumes the main author is the first author.
        """
        return cls.get_authors()[0]

    @classmethod
    def get_main_author_name(cls) -> str:
        """Get the main author name."""
        return cls.get_main_author()["name"]

    @classmethod
    def get_latest_possible_python_version(cls) -> str:
        """Get the latest possible python version."""
        constraint = cls.load()["project"]["requires-python"]
        version_constraint = VersionConstraint(constraint)
        upper = version_constraint.get_upper_exclusive()
        if upper is None:
            return "3.x"

        # convert to inclusive
        if upper.micro != 0:
            micro = upper.micro - 1
            return f"{upper.major}.{upper.minor}" + (f".{micro}" if micro != 0 else "")
        if upper.minor != 0:
            minor = upper.minor - 1
            return f"{upper.major}" + (f".{minor}" if minor != 0 else "")
        return f"{upper.major - 1}.x"

    @classmethod
    def get_first_supported_python_version(cls) -> str:
        """Get the first supported python version."""
        constraint = cls.load()["project"]["requires-python"]
        version_constraint = VersionConstraint(constraint)
        lower = version_constraint.get_lower_inclusive()
        if lower is None:
            msg = "Need a lower bound for python version"
            raise ValueError(msg)
        return str(lower)


class TypedConfigFile(ConfigFile):
    """Config file for py.typed."""

    @classmethod
    def get_file_extension(cls) -> str:
        """Get the file extension of the config file."""
        return "typed"

    @classmethod
    def load(cls) -> dict[str, Any] | list[Any]:
        """Load the config file."""
        return {}

    @classmethod
    def dump(cls, config: dict[str, Any] | list[Any]) -> None:
        """Dump the config file."""
        if config:
            msg = "Cannot dump to py.typed file."
            raise ValueError(msg)

    @classmethod
    def get_configs(cls) -> dict[str, Any] | list[Any]:
        """Get the config."""
        return {}


class PyTypedConfigFile(ConfigFile):
    """Config file for py.typed."""

    @classmethod
    def get_parent_path(cls) -> Path:
        """Get the path to the config file."""
        return Path(PyprojectConfigFile.get_package_name())


class DotPythonVersionConfigFile(ConfigFile):
    """Config file for .python-version."""

    VERSION_KEY = "version"

    @classmethod
    def get_filename(cls) -> str:
        """Get the filename of the config file."""
        return ""  # so it builds the path .python-version

    @classmethod
    def get_file_extension(cls) -> str:
        """Get the file extension of the config file."""
        return "python-version"

    @classmethod
    def get_parent_path(cls) -> Path:
        """Get the path to the config file."""
        return Path()

    @classmethod
    def get_configs(cls) -> dict[str, Any]:
        """Get the config."""
        return {
            cls.VERSION_KEY: PyprojectConfigFile.get_first_supported_python_version()
        }

    @classmethod
    def load(cls) -> dict[str, Any]:
        """Load the config file."""
        return {cls.VERSION_KEY: cls.get_path().read_text()}

    @classmethod
    def dump(cls, config: dict[str, Any] | list[Any]) -> None:
        """Dump the config file."""
        if not isinstance(config, dict):
            msg = f"Cannot dump {config} to .python-version file."
            raise TypeError(msg)
        cls.get_path().write_text(config[cls.VERSION_KEY])
