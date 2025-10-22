"""module."""

from winipedia_utils.git.workflows.base.base import (
    _get_checkout_step,
    _get_poetry_setup_steps,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test__get_checkout_step() -> None:
    """Test func for _get_checkout_step."""
    step = _get_checkout_step()
    # check is not empyt dict
    assert_with_msg(
        bool(step) and isinstance(step, dict),
        f"Expected non-empty dict, got {step}",
    )


def test__get_poetry_setup_steps() -> None:
    """Test func for _get_poetry_setup_steps."""
    steps = _get_poetry_setup_steps()
    # check is not empyt list
    assert_with_msg(
        bool(steps) and isinstance(steps, list),
        f"Expected non-empty list, got {steps}",
    )
