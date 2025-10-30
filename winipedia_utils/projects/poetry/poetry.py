"""Project utilities for introspection and manipulation.

This module provides utility functions for working with Python projects
"""

from collections.abc import Iterable
from types import ModuleType

from packaging.specifiers import SpecifierSet
from packaging.version import Version

from winipedia_utils.logging.logger import get_logger

logger = get_logger(__name__)


POETRY_ARG = "poetry"

POETRY_RUN_ARGS = [POETRY_ARG, "run"]

RUN_PYTHON_MODULE_ARGS = ["python", "-m"]


def get_script_from_args(args: Iterable[str]) -> str:
    """Get the script from args."""
    return " ".join(args)


def get_run_python_module_args(module: ModuleType) -> list[str]:
    """Get the args to run a module."""
    from winipedia_utils.modules.module import (  # noqa: PLC0415  # avoid circular import
        make_obj_importpath,
    )

    return [*RUN_PYTHON_MODULE_ARGS, make_obj_importpath(module)]


def get_python_module_script(module: ModuleType) -> str:
    """Get the script to run a module."""
    return get_script_from_args(get_run_python_module_args(module))


def get_poetry_run_module_script(module: ModuleType) -> str:
    """Get the script to run a module."""
    return get_script_from_args([*POETRY_RUN_ARGS, *get_run_python_module_args(module)])


class VersionConstraint:
    """Version class."""

    def __init__(self, constraint: str) -> None:
        """Initialize the version."""
        self.constraint = constraint
        self.spec = self.constraint.strip().strip('"').strip("'")
        self.sset = SpecifierSet(self.spec)

        self.lowers_inclusive = [
            Version(s.version) for s in self.sset if s.operator == ">="
        ]
        self.lowers_exclusive = [
            Version(s.version) for s in self.sset if s.operator == ">"
        ]
        # increment the last number of exclusive, so
        # >3.4.1 to >=3.4.2; <3.4.0 to <=3.4.1; 3.0.0 to <=3.0.1
        self.lowers_exclusive_to_inclusive = [
            Version(f"{v.major}.{v.minor}.{v.micro + 1}") for v in self.lowers_exclusive
        ]
        self.lowers_inclusive = (
            self.lowers_inclusive + self.lowers_exclusive_to_inclusive
        )

        self.uppers_inclusive = [
            Version(s.version) for s in self.sset if s.operator == "<="
        ]
        self.uppers_exclusive = [
            Version(s.version) for s in self.sset if s.operator == "<"
        ]

        # increment the last number of inclusive, so
        # <=3.4.1 to <3.4.2; >=3.4.0 to >3.4.1; 3.0.0 to >3.0.1
        self.uppers_inclusive_to_exclusive = [
            Version(f"{v.major}.{v.minor}.{v.micro + 1}") for v in self.uppers_inclusive
        ]
        self.uppers_exclusive = (
            self.uppers_inclusive_to_exclusive + self.uppers_exclusive
        )

        self.upper_exclusive = (
            min(self.uppers_exclusive) if self.uppers_exclusive else None
        )
        self.lower_inclusive = (
            max(self.lowers_inclusive) if self.lowers_inclusive else None
        )

    def get_lower_inclusive(self, default: str | None = None) -> Version | None:
        """Get the minimum version.

        Is given inclusive. E.g. >=3.8, <3.12 -> 3.8
        if >3.7, <3.12 -> 3.7.1

        E.g. >=3.8, <3.12 -> 3.8

        Args:
            default: The default value to return if there is no minimum version

        Returns:
            The minimum version
        """
        if self.lower_inclusive is None:
            return Version(default) if default else None

        return self.lower_inclusive

    def get_upper_exclusive(self, default: str | None = None) -> Version | None:
        """Get the maximum version.

        Is given exclusive. E.g. >=3.8, <3.12 -> 3.12
        if >=3.8, <=3.12 -> 3.12.1

        Args:
            default: The default value to return if there is no maximum version

        Returns:
            The maximum version
        """
        if self.upper_exclusive is None:
            return Version(default) if default else None

        return self.upper_exclusive
