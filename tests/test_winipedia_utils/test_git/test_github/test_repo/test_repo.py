"""module."""

from github.Repository import Repository

import winipedia_utils
from winipedia_utils.git.github.repo.protect import get_default_ruleset_params
from winipedia_utils.git.github.repo.repo import (
    DEFAULT_RULESET_NAME,
    create_or_update_ruleset,
    get_all_rulesets,
    get_repo,
    get_rules_payload,
    ruleset_exists,
)
from winipedia_utils.projects.poetry.config import PyprojectConfigFile
from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.testing.tests.base.utils.utils import get_github_repo_token

OWNER = PyprojectConfigFile.get_main_author_name()
TOKEN = get_github_repo_token()


def test_get_rules_payload() -> None:
    """Test func for get_rules_payload."""
    # Test with no rules
    rules = get_rules_payload()
    assert_with_msg(
        rules == [],
        "Expected empty list when no rules provided",
    )

    # Test with single rule
    rules = get_rules_payload(deletion={})
    assert_with_msg(
        len(rules) == 1,
        "Expected one rule",
    )
    assert_with_msg(
        rules[0]["type"] == "deletion",
        f"Expected type 'deletion', got {rules[0]['type']}",
    )

    # Test with rule that has parameters
    rules = get_rules_payload(pull_request={"required_approving_review_count": 1})
    assert_with_msg(
        len(rules) == 1,
        "Expected one rule",
    )
    assert_with_msg(
        "parameters" in rules[0],
        "Expected 'parameters' key in rule",
    )
    assert_with_msg(
        rules[0]["parameters"]["required_approving_review_count"] == 1,
        "Expected parameter value to be 1",
    )

    # Test with multiple rules
    rules = get_rules_payload(
        deletion={},
        creation={},
        pull_request={"required_approving_review_count": 1},
    )
    expected_multiple_rules = 3
    assert_with_msg(
        len(rules) == expected_multiple_rules,
        f"Expected {expected_multiple_rules} rules, got {len(rules)}",
    )


def test_get_repo() -> None:
    """Test func for get_repo."""
    repo = get_repo(TOKEN, OWNER, winipedia_utils.__name__)
    assert_with_msg(
        isinstance(repo, Repository),
        "Expected Repository object",
    )
    assert_with_msg(
        repo.name == winipedia_utils.__name__,
        f"Expected repo name {winipedia_utils.__name__}, got {repo.name}",
    )


def test_get_all_rulesets() -> None:
    """Test func for get_all_rulesets."""
    rulesets = get_all_rulesets(TOKEN, OWNER, winipedia_utils.__name__)
    assert_with_msg(
        isinstance(rulesets, list),
        "Expected rulesets to be a list",
    )


def test_ruleset_exists() -> None:
    """Test func for ruleset_exists."""
    ruleset_id = ruleset_exists(
        TOKEN, OWNER, winipedia_utils.__name__, DEFAULT_RULESET_NAME
    )
    assert_with_msg(
        ruleset_id > 0,
        f"Expected ruleset id > 0, got {ruleset_id}",
    )


def test_create_or_update_ruleset() -> None:
    """Test func for create_or_update_ruleset."""
    create_or_update_ruleset(
        **get_default_ruleset_params(),
    )
