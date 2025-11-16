"""This module contains the CLI entrypoint."""

import logging

import typer
from logdecorator import log_on_error  # type: ignore[import-untyped]

from winipedia_utils.dev.cli import subcommands
from winipedia_utils.utils.modules.function import get_all_functions_from_module

app = typer.Typer()


sub_cmds = get_all_functions_from_module(subcommands)

for sub_cmd in sub_cmds:
    app.command()(sub_cmd)


@log_on_error(log_level=logging.ERROR, message="Error in CLI")  # type: ignore[misc]
def main() -> None:
    """Entry point for the CLI."""
    if sub_cmds:
        app()
