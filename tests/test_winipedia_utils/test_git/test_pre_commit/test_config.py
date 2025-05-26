"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_git.test_pre_commit.test_config
"""

import io
from pathlib import Path
from typing import Any

import yaml
from pytest_mock import MockFixture

from winipedia_utils.git.pre_commit.config import (
    _add_package_hook_to_pre_commit_config,
    _get_pre_commit_config_dict,
    _pre_commit_config_is_correct,
    dump_pre_commit_config,
    load_pre_commit_config,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_load_pre_commit_config(mocker: MockFixture) -> None:
    """Test func for load_pre_commit_config."""
    # Test case 1: File exists with content
    mock_yaml_content: dict[str, list[dict[str, Any]]] = {
        "repos": [{"repo": "local", "hooks": [{"id": "test-hook"}]}]
    }
    mock_yaml_str = yaml.safe_dump(mock_yaml_content)

    # Setup mocks for first test case
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "read_text", return_value=mock_yaml_str)

    # Execute function and verify result
    result = load_pre_commit_config()
    assert_with_msg(
        result == mock_yaml_content,
        f"Expected {mock_yaml_content}, got {result}",
    )

    # Test case 2: File doesn't exist (should create empty file)
    # Reset mocks
    mocker.resetall()

    # Setup mocks for second test case
    mocker.patch.object(Path, "exists", return_value=False)
    mock_touch = mocker.patch.object(Path, "touch")
    mocker.patch.object(Path, "read_text", return_value="")

    # Execute function and verify result
    result = load_pre_commit_config()

    # Verify touch was called
    mock_touch.assert_called_once()

    # Verify result is empty dict
    assert_with_msg(
        result == {},
        f"Expected empty dict, got {result}",
    )


def test_dump_pre_commit_config(mocker: MockFixture) -> None:
    """Test func for dump_pre_commit_config."""
    test_config: dict[str, list[dict[str, Any]]] = {
        "repos": [{"repo": "local", "hooks": [{"id": "test-hook"}]}]
    }
    file_content = io.StringIO()

    # Create a context manager mock that returns our StringIO
    mock_file = mocker.MagicMock()
    mock_file.__enter__.return_value = file_content
    mock_file.__exit__.return_value = None

    # Mock Path.open to return our context manager
    mock_open = mocker.patch.object(Path, "open", return_value=mock_file)

    # Verify the mode parameter when called
    def verify_mode(mode: str) -> None:
        assert_with_msg(
            mode == "w",
            f"Expected mode 'w', got '{mode}'",
        )

    # Add side effect to verify the mode parameter
    def side_effect(mode_param: str) -> Any:
        verify_mode(mode_param)
        return mock_file

    mock_open.side_effect = side_effect

    # Call the function
    dump_pre_commit_config(test_config)

    # Get the written content and parse it
    written_content = file_content.getvalue()
    written_dict = yaml.safe_load(written_content)

    assert_with_msg(
        written_dict == test_config,
        f"Expected {test_config}, got {written_dict}",
    )


def test__get_pre_commit_config_dict() -> None:
    """Test func for _get_pre_commit_config_dict."""
    result = _get_pre_commit_config_dict()

    # The type system already ensures result is a dict, so we'll skip that check

    # Check that the dictionary has the expected keys
    expected_keys = ["repo", "hooks"]
    for key in expected_keys:
        assert_with_msg(
            key in result,
            f"Expected key '{key}' in result, but it was not found",
        )

    # Check that the repo value is "local"
    assert_with_msg(
        result["repo"] == "local",
        f"Expected repo to be 'local', got {result['repo']}",
    )

    # Check that hooks is a list with one item
    assert_with_msg(
        isinstance(result["hooks"], list) and len(result["hooks"]) == 1,
        f"Expected hooks to be a list with one item, got {result['hooks']}",
    )

    # Check that the hook has the expected keys
    hook = result["hooks"][0]
    expected_hook_keys = [
        "id",
        "name",
        "entry",
        "language",
        "always_run",
        "pass_filenames",
    ]
    for key in expected_hook_keys:
        assert_with_msg(
            key in hook,
            f"Expected key '{key}' in hook, but it was not found",
        )

    # Check that the hook id and name are "winipedia-utils"
    assert_with_msg(
        hook["id"] == "winipedia-utils",
        f"Expected hook id to be 'winipedia-utils', got {hook['id']}",
    )
    assert_with_msg(
        hook["name"] == "winipedia-utils",
        f"Expected hook name to be 'winipedia-utils', got {hook['name']}",
    )


def test__pre_commit_config_is_correct(mocker: MockFixture) -> None:
    """Test func for _pre_commit_config_is_correct."""
    # Test case 1: Config is correct
    expected_config = _get_pre_commit_config_dict()
    mock_config = {"repos": [expected_config]}

    mocker.patch(
        "winipedia_utils.git.pre_commit.config.load_pre_commit_config",
        return_value=mock_config,
    )
    result = _pre_commit_config_is_correct()
    assert_with_msg(
        result is True,
        f"Expected True, got {result}",
    )

    # Test case 2: Config is incorrect (empty)
    mocker.patch(
        "winipedia_utils.git.pre_commit.config.load_pre_commit_config",
        return_value={},
    )
    result = _pre_commit_config_is_correct()
    assert_with_msg(
        result is False,
        f"Expected False, got {result}",
    )

    # Test case 3: Config is incorrect (wrong hook)
    wrong_hook = {"repo": "local", "hooks": [{"id": "wrong-hook"}]}
    mock_config = {"repos": [wrong_hook]}

    mocker.patch(
        "winipedia_utils.git.pre_commit.config.load_pre_commit_config",
        return_value=mock_config,
    )
    result = _pre_commit_config_is_correct()
    assert_with_msg(
        result is False,
        f"Expected False, got {result}",
    )


def test__add_package_hook_to_pre_commit_config(mocker: MockFixture) -> None:
    """Test func for _add_package_hook_to_pre_commit_config."""
    # Test case 1: Config is already correct
    mocker.patch(
        "winipedia_utils.git.pre_commit.config._pre_commit_config_is_correct",
        return_value=True,
    )
    mock_load = mocker.patch(
        "winipedia_utils.git.pre_commit.config.load_pre_commit_config"
    )
    mock_dump = mocker.patch(
        "winipedia_utils.git.pre_commit.config.dump_pre_commit_config"
    )

    _add_package_hook_to_pre_commit_config()

    # Check that load was called but dump was not
    mock_load.assert_called_once()
    mock_dump.assert_not_called()

    # Test case 2: Config needs to be updated
    expected_config = _get_pre_commit_config_dict()
    existing_config = {
        "repos": [{"repo": "other-repo", "hooks": [{"id": "other-hook"}]}]
    }
    expected_updated_config = {
        "repos": [
            expected_config,
            {"repo": "other-repo", "hooks": [{"id": "other-hook"}]},
        ]
    }

    # Reset mocks for the second test case
    mocker.resetall()

    # Setup mocks for the second test case
    mocker.patch(
        "winipedia_utils.git.pre_commit.config._pre_commit_config_is_correct",
        return_value=False,
    )
    mock_load = mocker.patch(
        "winipedia_utils.git.pre_commit.config.load_pre_commit_config",
        return_value=existing_config,
    )
    mock_dump = mocker.patch(
        "winipedia_utils.git.pre_commit.config.dump_pre_commit_config"
    )
    mock_logger = mocker.patch("winipedia_utils.git.pre_commit.config.logger")

    _add_package_hook_to_pre_commit_config()

    # Check that load and dump were called
    mock_load.assert_called_once()
    mock_dump.assert_called_once()

    # Check that dump was called with the expected config
    dump_arg = mock_dump.call_args[0][0]
    assert_with_msg(
        dump_arg == expected_updated_config,
        f"Expected {expected_updated_config}, got {dump_arg}",
    )

    # Check that logger.info was called
    mock_logger.info.assert_called_once()
