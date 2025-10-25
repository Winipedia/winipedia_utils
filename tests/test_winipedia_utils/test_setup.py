"""Tests for winipedia_utils.setup module."""

from typing import Any

from pytest_mock import MockFixture

from winipedia_utils.modules.module import make_obj_importpath
from winipedia_utils.setup import SETUP_STEPS, get_setup_steps, setup
from winipedia_utils.testing.assertions import assert_with_msg


def test_get_setup_steps() -> None:
    """Test func for _get_setup_steps."""
    setup_steps = get_setup_steps()
    assert_with_msg(
        setup_steps == SETUP_STEPS,
        f"Expected {SETUP_STEPS}, got {setup_steps}",
    )


def test_setup(mocker: MockFixture) -> None:
    """Test func for _setup."""
    # patch _get_setup_steps to return a list of mock functions
    # which we assert are called once
    mock_setup_steps: list[Any] = []
    for i, step in enumerate(SETUP_STEPS):
        mock_step = mocker.MagicMock()
        mock_step.__name__ = f"mock_step_{step.__name__}_{i}"
        mock_setup_steps.append(mock_step)

    mocker.patch(
        make_obj_importpath(get_setup_steps),
        return_value=mock_setup_steps,
    )

    # assert all mock setup steps are called once
    setup()
    for mock_setup_step in mock_setup_steps:
        assert_with_msg(
            mock_setup_step.call_count == 1,
            f"Expected {mock_setup_step} to be called exactly once",
        )
