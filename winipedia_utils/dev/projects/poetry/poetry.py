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
from winipedia_utils.utils.modules.package import get_src_package

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


def get_poetry_run_cli_cmd_args(
    cmd: Callable[[], Any] | None = None, extra_args: list[str] | None = None
) -> list[str]:
    """Get the args to run the cli of the current project."""
    args = [
        *POETRY_RUN_ARGS,
        PyprojectConfigFile.get_project_name_from_pkg_name(get_src_package().__name__),
    ]
    if cmd is not None:
        name = make_name_from_obj(cmd, capitalize=False)
        args.append(name)
    if extra_args is not None:
        args.extend(extra_args)
    return args


def get_poetry_run_winipedia_utils_cli_cmd_args(
    cmd: Callable[[], Any] | None = None,
    extra_args: list[str] | None = None,
) -> list[str]:
    """Get the args to run winipedia_utils."""
    args = get_poetry_run_cli_cmd_args(cmd, extra_args)
    args[len(POETRY_RUN_ARGS)] = PyprojectConfigFile.get_project_name_from_pkg_name(
        winipedia_utils.__name__
    )
    return args


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
