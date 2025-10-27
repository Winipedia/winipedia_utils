"""module."""

from winipedia_utils.git.github.repo.protect import (
    create_or_update_default_branch_ruleset,
    get_default_ruleset_params,
    protect_repository,
    set_secure_repo_settings,
)
from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.testing.tests.base.utils.utils import get_github_token

TOKEN = get_github_token()


def test_protect_repository() -> None:
    """Test func for protect_repository."""
    protect_repository(TOKEN)


def test_set_secure_repo_settings() -> None:
    """Test func for set_secure_repo_settings."""
    set_secure_repo_settings(TOKEN)


def test_create_or_update_default_branch_ruleset() -> None:
    """Test func for create_or_update_default_branch_ruleset."""
    create_or_update_default_branch_ruleset(TOKEN)


def test_get_default_ruleset_params() -> None:
    """Test func for get_default_ruleset_params."""
    params = get_default_ruleset_params(TOKEN)
    assert_with_msg(
        "owner" in params,
        "Expected 'owner' in params",
    )
    assert_with_msg(
        "token" in params,
        "Expected 'token' in params",
    )
