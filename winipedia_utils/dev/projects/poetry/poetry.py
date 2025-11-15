"""Project utilities for introspection and manipulation.

This module provides utility functions for working with Python projects
"""

from collections.abc import Callable, Iterable
from types import ModuleType
from typing import Any

import winipedia_utils
from winipedia_utils.dev.configs.pyproject import PyprojectConfigFile
from winipedia_utils.utils.data.structures.text.string import make_name_from_obj
from winipedia_utils.utils.logging.logger import get_logger

logger = get_logger(__name__)


POETRY_ARG = "poetry"

POETRY_RUN_ARGS = [POETRY_ARG, "run"]

RUN_PYTHON_MODULE_ARGS = ["python", "-m"]


def get_script_from_args(args: Iterable[str]) -> str:
    """Get the script from args."""
    return " ".join(args)


def get_run_python_module_args(module: ModuleType) -> list[str]:
    """Get the args to run a module."""
    from winipedia_utils.utils.modules.module import (  # noqa: PLC0415  # avoid circular import
        make_obj_importpath,
    )

    return [*RUN_PYTHON_MODULE_ARGS, make_obj_importpath(module)]


def get_poetry_run_module_args(module: ModuleType) -> list[str]:
    """Get the args to run a module."""
    return [*POETRY_RUN_ARGS, *get_run_python_module_args(module)]


def get_poetry_run_cli_cmd_args(cmd: Callable[[], Any]) -> list[str]:
    """Get the args to run winipedia_utils."""
    name = make_name_from_obj(cmd, capitalize=False)
    src_pkg_name = PyprojectConfigFile.get_project_name()
    return [*POETRY_RUN_ARGS, src_pkg_name, name]


def get_poetry_run_winipedia_utils_cli_cmd_args(cmd: Callable[[], Any]) -> list[str]:
    """Get the args to run winipedia_utils."""
    name = make_name_from_obj(cmd, capitalize=False)
    winipedia_utils_name = PyprojectConfigFile.get_project_name_from_pkg_name(
        winipedia_utils.__name__
    )
    return [*POETRY_RUN_ARGS, winipedia_utils_name, name]


def get_poetry_run_cli_cmd_script(cmd: Callable[[], Any]) -> str:
    """Get the script to run winipedia_utils."""
    return get_script_from_args(get_poetry_run_cli_cmd_args(cmd))


def get_poetry_run_winipedia_utils_cli_cmd_script(cmd: Callable[[], Any]) -> str:
    """Get the script to run winipedia_utils."""
    return get_script_from_args(get_poetry_run_winipedia_utils_cli_cmd_args(cmd))


def get_python_module_script(module: ModuleType) -> str:
    """Get the script to run a module."""
    return get_script_from_args(get_run_python_module_args(module))


def get_poetry_run_module_script(module: ModuleType) -> str:
    """Get the script to run a module."""
    return get_script_from_args(get_poetry_run_module_args(module))
