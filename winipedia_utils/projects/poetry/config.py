"""Config utilities for poetry and pyproject.toml."""

from pathlib import Path
from typing import Any, cast

from packaging.specifiers import SpecifierSet
from packaging.version import Version

from winipedia_utils.modules.package import get_src_package, make_name_from_package
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
                "bandit": {},
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
        spec = constraint.strip().strip('"').strip("'")
        sset = SpecifierSet(spec)
        # find upper bound specifiers
        uppers = [Version(sp.version) for sp in sset if sp.operator in ("<", "<=")]
        if uppers:
            top = max(uppers)
            # if strict "<", we might treat it as “one less” in minor
            if any(sp.operator == "<" and Version(sp.version) == top for sp in sset):
                # subtract one minor
                return f"{top.major}.{top.minor - 1}"
            return f"{top.major}.{top.minor}"
        # no upper bound → “3.x”
        return "3.x"


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
