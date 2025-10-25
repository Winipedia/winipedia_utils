"""Has utils towards skipping tests."""

import functools

import pytest

skip_fixture_test: pytest.MarkDecorator = functools.partial(
    pytest.mark.skip,
    reason="Fixtures are not testable bc they cannot be called directly.",
)()
