"""Contains an empty test."""

import pytest


@pytest.mark.skip(reason="Can not test a test")
def test_0() -> None:
    """Empty test.

    Exists so that when no tests are written yet the base fixtures are executed.
    """
