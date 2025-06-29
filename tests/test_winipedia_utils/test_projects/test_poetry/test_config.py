"""Tests for winipedia_utils.projects.poetry.config module."""

from pathlib import Path

import pytest
import tomlkit
from pytest_mock import MockFixture

from winipedia_utils.projects.poetry.config import (
    _add_configurations_to_pyproject_toml,
    _get_pyproject_toml_tool_configs,
    _pyproject_tool_configs_are_correct,
    _tool_config_is_correct,
    dump_pyproject_toml,
    get_poetry_package_name,
    laod_pyproject_toml,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_laod_pyproject_toml(mocker: MockFixture) -> None:
    """Test func for laod_pyproject_toml."""
    # Test successful loading
    mock_toml_content = """
[project]
name = "test-project"
version = "1.0.0"

[tool.ruff]
exclude = [".*"]
"""
    # Mock Path.read_text to return our test content
    mock_read_text = mocker.patch.object(
        Path, "read_text", return_value=mock_toml_content
    )

    result = laod_pyproject_toml()

    # Verify Path.read_text was called with correct file
    mock_read_text.assert_called_once()

    # Verify the result is a TOMLDocument with expected content
    project_name = result.get("project", {}).get("name")
    assert_with_msg(
        project_name == "test-project",
        f"Expected project name 'test-project', got {project_name}",
    )

    # Test file not found error
    mock_read_text.side_effect = FileNotFoundError("File not found")

    with pytest.raises(FileNotFoundError):
        laod_pyproject_toml()


def test_dump_pyproject_toml(mocker: MockFixture) -> None:
    """Test func for dump_pyproject_toml."""
    # Create test TOML document
    test_doc = tomlkit.document()
    test_doc["project"] = {"name": "test-project", "version": "1.0.0"}

    # Mock file operations
    mock_open_context = mocker.patch("builtins.open", mocker.mock_open())
    mock_path_open = mocker.patch.object(
        Path, "open", return_value=mock_open_context.return_value
    )

    # Mock tomlkit.dump
    mock_dump = mocker.patch("tomlkit.dump")

    # Call the function
    dump_pyproject_toml(test_doc)

    # Verify Path.open was called with correct parameters
    mock_path_open.assert_called_once_with("w")

    # Verify tomlkit.dump was called with correct parameters
    mock_dump.assert_called_once_with(
        test_doc, mock_open_context.return_value.__enter__.return_value
    )


def test_get_poetry_package_name(mocker: MockFixture) -> None:
    """Test func for get_poetry_package_name."""
    # Test case 1: Normal project name with hyphens
    mock_doc = tomlkit.document()
    mock_doc["project"] = {"name": "test-project-name"}

    mock_load = mocker.patch(
        "winipedia_utils.projects.poetry.config.laod_pyproject_toml",
        return_value=mock_doc,
    )

    result = get_poetry_package_name()

    assert_with_msg(
        result == "test_project_name",
        f"Expected 'test_project_name', got '{result}'",
    )
    mock_load.assert_called_once()

    # Test case 2: Project name without hyphens
    mock_load.reset_mock()
    mock_doc_no_hyphens = tomlkit.document()
    mock_doc_no_hyphens["project"] = {"name": "testproject"}
    mock_load.return_value = mock_doc_no_hyphens

    result = get_poetry_package_name()

    assert_with_msg(
        result == "testproject",
        f"Expected 'testproject', got '{result}'",
    )

    # Test case 3: No project section
    mock_load.reset_mock()
    mock_doc_empty = tomlkit.document()
    mock_load.return_value = mock_doc_empty

    result = get_poetry_package_name()

    assert_with_msg(
        result == "",
        f"Expected empty string, got '{result}'",
    )

    # Test case 4: Project section without name
    mock_load.reset_mock()
    mock_doc_no_name = tomlkit.document()
    mock_doc_no_name["project"] = {}
    mock_load.return_value = mock_doc_no_name

    result = get_poetry_package_name()

    assert_with_msg(
        result == "",
        f"Expected empty string, got '{result}'",
    )


def test__get_pyproject_toml_tool_configs() -> None:
    """Test func for _get_pyproject_toml_tool_configs."""
    result = _get_pyproject_toml_tool_configs()

    # Verify expected tools are present
    expected_tools = ["ruff", "mypy", "pytest", "bandit"]
    for tool in expected_tools:
        assert_with_msg(
            tool in result,
            f"Expected tool '{tool}' in result, but it was not found",
        )

    # Verify ruff configuration
    ruff_config = result["ruff"]
    assert_with_msg(
        "exclude" in ruff_config
        and ruff_config["exclude"] == [".*", "**/migrations/*.py"],
        f"Expected ruff exclude to be ['.*', '**/migrations/*.py'], "
        f"got {ruff_config.get('exclude')}",
    )
    assert_with_msg(
        "lint" in ruff_config,
        "Expected 'lint' section in ruff config",
    )

    # Verify mypy configuration
    mypy_config = result["mypy"]
    assert_with_msg(
        mypy_config.get("strict") is True,
        f"Expected mypy strict to be True, got {mypy_config.get('strict')}",
    )
    assert_with_msg(
        mypy_config.get("files") == ".",
        f"Expected mypy files to be '.', got {mypy_config.get('files')}",
    )

    # Verify pytest configuration
    pytest_config = result["pytest"]
    assert_with_msg(
        "ini_options" in pytest_config,
        "Expected 'ini_options' in pytest config",
    )

    # Verify bandit configuration (should be empty)
    bandit_config = result["bandit"]
    assert_with_msg(
        bandit_config == {},
        f"Expected empty bandit config, got {bandit_config}",
    )


def test__tool_config_is_correct(mocker: MockFixture) -> None:
    """Test func for _tool_config_is_correct."""
    # Test case 1: Tool config is correct
    mock_doc = tomlkit.document()
    mock_doc["tool"] = {
        "ruff": {
            "exclude": [".*"],
            "lint": {"select": ["ALL"]},
        }
    }

    mock_load = mocker.patch(
        "winipedia_utils.projects.poetry.config.laod_pyproject_toml",
        return_value=mock_doc,
    )

    test_config = {
        "exclude": [".*"],
        "lint": {"select": ["ALL"]},
    }

    result = _tool_config_is_correct("ruff", test_config)

    assert_with_msg(
        result is True,
        f"Expected True, got {result}",
    )
    mock_load.assert_called_once()

    # Test case 2: Tool config is incorrect
    mock_load.reset_mock()
    wrong_config = {"exclude": ["different"]}

    result = _tool_config_is_correct("ruff", wrong_config)

    assert_with_msg(
        result is False,
        f"Expected False, got {result}",
    )

    # Test case 3: Tool doesn't exist
    mock_load.reset_mock()

    result = _tool_config_is_correct("nonexistent", test_config)

    assert_with_msg(
        result is False,
        f"Expected False, got {result}",
    )

    # Test case 4: No tool section
    mock_load.reset_mock()
    mock_doc_no_tool = tomlkit.document()
    mock_load.return_value = mock_doc_no_tool

    result = _tool_config_is_correct("ruff", test_config)

    assert_with_msg(
        result is False,
        f"Expected False, got {result}",
    )


def test__pyproject_tool_configs_are_correct(mocker: MockFixture) -> None:
    """Test func for _pyproject_tool_configs_are_correct."""
    # Test case 1: All configs are correct
    mock_tool_config_correct = mocker.patch(
        "winipedia_utils.projects.poetry.config._tool_config_is_correct",
        return_value=True,
    )

    result = _pyproject_tool_configs_are_correct()

    assert_with_msg(
        result is True,
        f"Expected True, got {result}",
    )

    # Verify _tool_config_is_correct was called for each expected tool
    expected_tools = ["ruff", "mypy", "pytest", "bandit"]
    expected_call_count = len(expected_tools)
    actual_call_count = mock_tool_config_correct.call_count
    assert_with_msg(
        actual_call_count == expected_call_count,
        f"Expected {expected_call_count} calls, got {actual_call_count}",
    )

    # Test case 2: One config is incorrect
    mock_tool_config_correct.reset_mock()
    mock_tool_config_correct.side_effect = [
        True,
        False,
        True,
        True,
    ]  # mypy is incorrect

    result = _pyproject_tool_configs_are_correct()

    assert_with_msg(
        result is False,
        f"Expected False, got {result}",
    )

    # Test case 3: All configs are incorrect
    mock_tool_config_correct.reset_mock()
    mock_tool_config_correct.side_effect = None  # Reset side_effect
    mock_tool_config_correct.return_value = False

    result = _pyproject_tool_configs_are_correct()

    assert_with_msg(
        result is False,
        f"Expected False, got {result}",
    )


def test__add_configurations_to_pyproject_toml(mocker: MockFixture) -> None:
    """Test func for _add_tool_configurations_to_pyproject_toml."""
    # Setup mocks
    mock_doc = tomlkit.document()
    mock_doc["tool"] = {}

    mock_load = mocker.patch(
        "winipedia_utils.projects.poetry.config.laod_pyproject_toml",
        return_value=mock_doc,
    )
    mock_dump = mocker.patch(
        "winipedia_utils.projects.poetry.config.dump_pyproject_toml"
    )
    mock_tool_config_correct = mocker.patch(
        "winipedia_utils.projects.poetry.config._tool_config_is_correct",
        return_value=False,  # All configs need to be added
    )
    mock_logger = mocker.patch("winipedia_utils.projects.poetry.config.logger")

    # Call the function
    _add_configurations_to_pyproject_toml()

    # Verify load and dump were called
    mock_load.assert_called_once()
    mock_dump.assert_called_once_with(mock_doc)

    # Verify logger.info was called for each tool
    expected_tools = ["ruff", "mypy", "pytest", "bandit"]
    assert_with_msg(
        mock_logger.info.call_count == len(expected_tools),
        f"Expected {len(expected_tools)} log calls, got {mock_logger.info.call_count}",
    )

    # Verify the tool section was updated
    assert_with_msg(
        "tool" in mock_doc,
        "Expected 'tool' section in document",
    )

    # Test case 2: Some configs already correct
    mock_load.reset_mock()
    mock_dump.reset_mock()
    mock_logger.reset_mock()
    mock_tool_config_correct.reset_mock()

    # Mock that ruff and mypy are correct, pytest and bandit need updates
    mock_tool_config_correct.side_effect = [True, True, False, False]

    _add_configurations_to_pyproject_toml()

    # Should only log for pytest and bandit
    expected_log_calls = 2  # pytest and bandit
    assert_with_msg(
        mock_logger.info.call_count == expected_log_calls,
        f"Expected {expected_log_calls} log calls, got {mock_logger.info.call_count}",
    )

    # Test case 3: All configs already correct
    mock_load.reset_mock()
    mock_dump.reset_mock()
    mock_logger.reset_mock()
    mock_tool_config_correct.reset_mock()
    mock_tool_config_correct.side_effect = None  # Reset side_effect
    mock_tool_config_correct.return_value = True

    _add_configurations_to_pyproject_toml()

    # Should not log anything
    assert_with_msg(
        mock_logger.info.call_count == 0,
        f"Expected 0 log calls, got {mock_logger.info.call_count}",
    )
