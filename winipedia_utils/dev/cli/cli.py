"""This module contains the CLI entrypoint."""

import logging

import typer
from logdecorator import log_on_error  # type: ignore[import-untyped]

from winipedia_utils.dev.configs.subcommands import SubcommandsConfigFile
from winipedia_utils.utils.modules.function import get_all_functions_from_module
from winipedia_utils.utils.modules.module import import_module_from_file

app = typer.Typer()

subcommands_module = import_module_from_file(SubcommandsConfigFile().get_path())

sub_cmds = get_all_functions_from_module(subcommands_module)

for sub_cmd in sub_cmds:
    app.command()(sub_cmd)


@log_on_error(log_level=logging.ERROR, message="Error in CLI")  # type: ignore[misc]
def main() -> None:
    """Entry point for the CLI."""
    if sub_cmds:
        app()
