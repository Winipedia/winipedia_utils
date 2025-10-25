"""Base class for config files."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import tomlkit
import yaml

import winipedia_utils
from winipedia_utils.iterating.iterate import nested_structure_is_subset
from winipedia_utils.modules.class_ import init_all_nonabstract_subclasses
from winipedia_utils.projects.poetry.poetry import get_poetry_run_module_script


class ConfigFile(ABC):
    """Base class for config files."""

    @abstractmethod
    def get_path(self) -> Path:
        """Get the path to the config file."""

    @abstractmethod
    def load(self) -> dict[str, Any]:
        """Load the config file."""

    @abstractmethod
    def dump(self, config: dict[str, Any]) -> None:
        """Dump the config file."""

    @abstractmethod
    def get_configs(self) -> dict[str, Any]:
        """Get the config."""

    def __init__(self) -> None:
        """Initialize the config file."""
        self.path = self.get_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()
            self.dump(self.get_configs())

        if not self.is_correct():
            config = self.add_missing_configs()
            self.dump(config)

        self.config = self.load()
        if not self.is_correct():
            msg = f"Config file {self.path} is not correct."
            raise ValueError(msg)

    def add_missing_configs(self) -> dict[str, Any]:
        """Add any missing configs to the config file."""
        current_config = self.load()
        expected_config = self.get_configs()
        nested_structure_is_subset(
            expected_config,
            current_config,
            self.add_missing_dict_val,
            self.insert_missing_list_val,
        )
        return current_config

    @staticmethod
    def add_missing_dict_val(
        expected_dict: dict[str, Any], actual_dict: dict[str, Any], key: str
    ) -> None:
        """Add a missing dict value."""
        actual_dict[key] = expected_dict[key]

    @staticmethod
    def insert_missing_list_val(
        expected_list: list[Any], actual_list: list[Any], index: int
    ) -> None:
        """Append a missing list value."""
        actual_list.insert(index, expected_list[index])

    def is_correct(self) -> bool:
        """Check if the config is correct.

        If the file is empty, it is considered correct.
        This is so bc if a user does not want a specific config file,
        they can just make it empty and the tests will not fail.
        """
        return self.is_unwanted() or self.is_correct_recursively(
            self.get_configs(), self.load()
        )

    def is_unwanted(self) -> bool:
        """Check if the config file is unwanted.

        If the file is empty, it is considered unwanted.
        """
        return self.path.exists() and self.path.read_text() == ""

    @staticmethod
    def is_correct_recursively(
        expected_config: Any,
        actual_config: Any,
    ) -> bool:
        """Check if the config is correct.

        Checks if expected is a subset recursively of actual.
        If a value is Any, it is considered correct.

        Args:
            expected_config: The expected config
            actual_config: The actual config

        Returns:
            True if the config is correct, False otherwise
        """
        return nested_structure_is_subset(expected_config, actual_config)

    @classmethod
    def init_config_files(cls) -> None:
        """Initialize all subclasses."""
        init_all_nonabstract_subclasses(cls, load_package_before=winipedia_utils)


class YamlConfigFile(ConfigFile):
    """Base class for yaml config files."""

    def load(self) -> dict[str, Any]:
        """Load the config file."""
        return yaml.safe_load(self.path.read_text()) or {}

    def dump(self, config: dict[str, Any]) -> None:
        """Dump the config file."""
        with self.path.open("w") as f:
            yaml.safe_dump(config, f, sort_keys=False)

    @staticmethod
    def get_poetry_run_setup_script() -> str:
        """Get the poetry run setup script."""
        from winipedia_utils import setup  # noqa: PLC0415  # avoid circular import

        return get_poetry_run_module_script(setup)


class TomlConfigFile(ConfigFile):
    """Base class for toml config files."""

    def load(self) -> dict[str, Any]:
        """Load the config file."""
        return tomlkit.parse(self.path.read_text())

    def dump(self, config: dict[str, Any]) -> None:
        """Dump the config file."""
        with self.path.open("w") as f:
            tomlkit.dump(config, f)
