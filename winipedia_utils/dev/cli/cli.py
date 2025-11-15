"""This module contains the CLI entrypoint."""

import sys

import typer

import winipedia_utils
from winipedia_utils.dev.cli import subcommands
from winipedia_utils.dev.configs.pyproject import PyprojectConfigFile
from winipedia_utils.dev.configs.subcommands import SubcommandsConfigFile
from winipedia_utils.utils.modules.function import get_all_functions_from_module
from winipedia_utils.utils.modules.module import import_module_from_path

app = typer.Typer()

# if winipedia-utils is the caller subcommands_module = subcommands
if (
    PyprojectConfigFile.get_project_name_from_pkg_name(winipedia_utils.__name__)
    in sys.argv
):
    subcommands_module = subcommands
else:
    subcommands_module = import_module_from_path(SubcommandsConfigFile().get_path())


sub_cmds = get_all_functions_from_module(subcommands_module)

for sub_cmd in sub_cmds:
    app.command()(sub_cmd)


def main() -> None:
    """Entry point for the CLI."""
    if sub_cmds:
        app()
