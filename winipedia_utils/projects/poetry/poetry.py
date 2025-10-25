"""Project utilities for introspection and manipulation.

This module provides utility functions for working with Python projects
"""

from collections.abc import Iterable
from types import ModuleType

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


def get_run_python_module_script(module: ModuleType) -> str:
    """Get the script to run a module."""
    return get_script_from_args(get_run_python_module_args(module))


def get_poetry_run_module_script(module: ModuleType) -> str:
    """Get the script to run a module."""
    return get_script_from_args([*POETRY_RUN_ARGS, *get_run_python_module_args(module)])
