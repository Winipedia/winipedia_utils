"""Contains base utilities for git workflows."""

from typing import Any


def _get_checkout_step(fetch_depth: int | None = None) -> dict[str, Any]:
    """Get the checkout step."""
    step: dict[str, Any] = {
        "name": "Checkout repository",
        "uses": "actions/checkout@v5",
    }
    if fetch_depth is not None:
        step["with"] = {"fetch-depth": fetch_depth}
    return step


def _get_poetry_setup_steps(
    *,
    install_dependencies: bool = False,
    fetch_depth: int | None = None,
    configure_pipy_token: bool = False,
) -> list[dict[str, Any]]:
    """Get the poetry steps."""
    steps = [_get_checkout_step(fetch_depth)]
    steps.append(
        {
            "name": "Setup Python",
            "uses": "actions/setup-python@v6",
            "with": {"python-version": "3.x"},
        }
    )
    steps.append(
        {
            "name": "Install Poetry",
            "run": "curl -sSL https://install.python-poetry.org | python3 -",
        }
    )
    if configure_pipy_token:
        steps.append(
            {
                "name": "Configure Poetry",
                "run": "poetry config pypi-token.pypi ${{ secrets.PYPI_TOKEN }}",
            }
        )
    if install_dependencies:
        steps.append({"name": "Install Dependencies", "run": "poetry install"})
    return steps
