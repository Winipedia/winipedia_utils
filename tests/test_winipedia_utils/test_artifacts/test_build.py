"""module."""

import pytest


@pytest.mark.skip(reason="Can not test a test")
def test_build_project() -> None:
    """Test func for build_project."""
    raise NotImplementedError
