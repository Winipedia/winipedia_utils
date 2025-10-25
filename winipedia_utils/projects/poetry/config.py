"""Config utilities for poetry and pyproject.toml."""

from pathlib import Path
from typing import Any

from winipedia_utils.modules.package import get_src_package
from winipedia_utils.projects.project import make_name_from_package
from winipedia_utils.testing.convention import TESTS_PACKAGE_NAME
from winipedia_utils.text.config import ConfigFile, TomlConfigFile


class PyProjectTomlConfig(TomlConfigFile):
    """Config file for pyproject.toml."""

    PATH = Path("pyproject.toml")

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def get_configs(self) -> dict[str, Any]:
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
                    "group": {
                        "dev": {
                            "dependencies": dict.fromkeys(
                                [
                                    "ruff",
                                    "pre-commit",
                                    "mypy",
                                    "pytest",
                                    "bandit",
                                    "types-setuptools",
                                    "types-tqdm",
                                    "types-defusedxml",
                                    "types-pyyaml",
                                    "pytest-mock",
                                ],
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

    def get_package_name(self) -> str:
        """Get the package name."""
        project_dict = self.load().get("project", {})
        package_name = str(project_dict.get("name", ""))
        return package_name.replace("-", "_")

    def get_dev_dependencies(self) -> set[str]:
        """Get the dev dependencies."""
        dev_dependencies = set(
            self.load()
            .get("tool", {})
            .get("poetry", {})
            .get("group", {})
            .get("dev", {})
            .get("dependencies", {})
            .keys()
        )
        if not dev_dependencies:
            dev_dependencies = set(
                self.load().get("dependency-groups", {}).get("dev", [])
            )
            dev_dependencies = {d.split("(")[0].strip() for d in dev_dependencies}
        return dev_dependencies

    def get_expected_dev_dependencies(self) -> set[str]:
        """Get the expected dev dependencies."""
        return set(
            self.get_configs()["tool"]["poetry"]["group"]["dev"]["dependencies"].keys()
        )


class PyTypedConfigFile(ConfigFile):
    """Config file for py.typed."""

    def get_path(self) -> Path:
        """Get the path to the config file."""
        toml_config = PyProjectTomlConfig()
        package_name = toml_config.get_package_name()
        return Path(package_name) / "py.typed"

    def load(self) -> dict[str, Any]:
        """Load the config file."""
        return {}

    def dump(self, config: dict[str, Any]) -> None:
        """Dump the config file."""
        if config:
            msg = "Cannot dump to py.typed file."
            raise ValueError(msg)
        self.path.touch()

    def get_configs(self) -> dict[str, Any]:
        """Get the config."""
        return {}
