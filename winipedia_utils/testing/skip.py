"""Has utils towards skipping tests."""

import functools

import pytest

from winipedia_utils.git.github.github import running_in_github_action

skip_fixture_test: pytest.MarkDecorator = functools.partial(
    pytest.mark.skip,
    reason="Fixtures are not testable bc they cannot be called directly.",
)()


skip_in_github_actions: pytest.MarkDecorator = functools.partial(
    pytest.mark.skipif,
    running_in_github_action(),
    reason="Test cannot run in GitHub action.",
)()
