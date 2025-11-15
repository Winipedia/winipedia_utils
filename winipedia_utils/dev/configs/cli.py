"""Config utilities for cli.py."""

from pathlib import Path

import winipedia_utils
from winipedia_utils.dev import cli
from winipedia_utils.dev.cli import subcommands
from winipedia_utils.dev.configs.base.base import ConfigFile, PythonConfigFile
from winipedia_utils.dev.configs.pyproject import PyprojectConfigFile
from winipedia_utils.utils.modules.function import get_all_functions_from_module
from winipedia_utils.utils.modules.module import (
    get_isolated_obj_name,
    get_module_of_obj,
    make_obj_importpath,
    to_path,
)


class CliConfigFile(PythonConfigFile):
    """Config file for cli.py."""

    @classmethod
    def get_parent_path(cls) -> Path:
        """Get the path to the config file."""
        src_package = PyprojectConfigFile.get_package_name()
        builds_package = cls.get_module_name_replacing_start_module(cli, src_package)
        return to_path(builds_package, is_package=True)

    @classmethod
    def get_content_str(cls) -> str:
        """Get the config."""
        subcomand_module_isolated_name = get_isolated_obj_name(subcommands)
        cli_import_path = ConfigFile.get_module_name_replacing_start_module(
            cli, PyprojectConfigFile.get_package_name()
        )
        functions_module_import_path = make_obj_importpath(
            get_module_of_obj(get_all_functions_from_module)
        )
        from_functions_import_get_all_functions_from_module = f"from {functions_module_import_path} import {get_all_functions_from_module.__name__}"  # noqa: E501
        from_cli_import_subcommands = (
            f"from {cli_import_path} import {subcomand_module_isolated_name}"
        )
        package_name = PyprojectConfigFile.get_package_name()
        content = '''"""This module contains the CLI entrypoint."""

import typer
'''

        if package_name == winipedia_utils.__name__:
            content += f"""
{from_cli_import_subcommands}
"""

        content += from_functions_import_get_all_functions_from_module

        if package_name != winipedia_utils.__name__:
            content += f"""

{from_cli_import_subcommands}"""

        content += f'''

app = typer.Typer()

sub_cmds = {get_all_functions_from_module.__name__}({subcomand_module_isolated_name})

for sub_cmd in sub_cmds:
    app.command()(sub_cmd)


def main() -> None:
    """Entry point for the CLI."""
    app()
'''
        return content
