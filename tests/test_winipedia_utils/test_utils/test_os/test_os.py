"""Tests for winipedia_utils.os.os module."""

import subprocess  # nosec: B404
from typing import Any

import pytest
from pytest_mock import MockFixture

from winipedia_utils.utils.os.os import run_subprocess, which_with_raise
from winipedia_utils.utils.testing.assertions import assert_with_msg


def test_which_with_raise(mocker: MockFixture) -> None:
    """Test func for which_with_raise."""
    # Test 1: Command found successfully
    expected_path = "/usr/bin/python"
    mock_which = mocker.patch("shutil.which", return_value=expected_path)

    result = which_with_raise("python")

    assert_with_msg(
        result == expected_path,
        f"Expected {expected_path}, got {result}",
    )
    mock_which.assert_called_with("python")

    # Test 2: Command not found
    mock_which.return_value = None

    with pytest.raises(FileNotFoundError, match="Command nonexistent_cmd not found"):
        which_with_raise("nonexistent_cmd")

    # Test 3: Empty command string
    with pytest.raises(FileNotFoundError, match="Command  not found"):
        which_with_raise("")

    # Test 4: Command with path separators
    expected_path_custom = "/usr/local/bin/custom-tool"
    mock_which.return_value = expected_path_custom

    result = which_with_raise("custom-tool")

    assert_with_msg(
        result == expected_path_custom,
        f"Expected {expected_path_custom}, got {result}",
    )


def test_run_subprocess(mocker: MockFixture) -> None:
    """Test func for run_subprocess."""
    # Setup common mock
    mock_result = mocker.MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "success output"
    mock_result.stderr = ""
    mock_run = mocker.patch("subprocess.run", return_value=mock_result)

    # Test basic execution
    args: list[str] = ["echo", "hello"]
    result = run_subprocess(args)
    assert_with_msg(result is mock_result, "Expected to return the mock result")
    mock_run.assert_called_with(
        args, check=True, input=None, capture_output=True, timeout=None
    )

    # Test with string input
    mock_run.reset_mock()
    result = run_subprocess(["cat"], input_="test input")
    assert_with_msg(result is mock_result, "Expected to return the mock result")
    mock_run.assert_called_with(
        ["cat"], check=True, input="test input", capture_output=True, timeout=None
    )

    # Test with bytes input
    mock_run.reset_mock()
    result = run_subprocess(["cat"], input_=b"test bytes")
    assert_with_msg(result is mock_result, "Expected to return the mock result")
    mock_run.assert_called_with(
        ["cat"], check=True, input=b"test bytes", capture_output=True, timeout=None
    )

    # Test no capture output
    mock_run.reset_mock()
    result = run_subprocess(args, capture_output=False)
    assert_with_msg(result is mock_result, "Expected to return the mock result")
    mock_run.assert_called_with(
        args, check=True, input=None, capture_output=False, timeout=None
    )

    # Test with timeout
    mock_run.reset_mock()
    result = run_subprocess(["sleep", "1"], timeout=30)
    assert_with_msg(result is mock_result, "Expected to return the mock result")
    mock_run.assert_called_with(
        ["sleep", "1"], check=True, input=None, capture_output=True, timeout=30
    )

    # Test no check
    mock_run.reset_mock()
    mock_result.returncode = 1
    result = run_subprocess(["false"], check=False)
    assert_with_msg(result is mock_result, "Expected to return the mock result")
    mock_run.assert_called_with(
        ["false"], check=False, input=None, capture_output=True, timeout=None
    )

    # Test with kwargs
    mock_run.reset_mock()
    extra_kwargs: dict[str, Any] = {
        "cwd": "/home/user",
        "env": {"PATH": "/usr/bin"},
        "shell": False,
    }
    result = run_subprocess(args, **extra_kwargs)
    assert_with_msg(result is mock_result, "Expected to return the mock result")
    mock_run.assert_called_with(
        args, check=True, input=None, capture_output=True, timeout=None, **extra_kwargs
    )

    # Test exception propagation
    mock_run.side_effect = subprocess.CalledProcessError(1, ["false"])
    with pytest.raises(subprocess.CalledProcessError):
        run_subprocess(["false"])

    # Test timeout exception
    mock_run.side_effect = subprocess.TimeoutExpired(["sleep", "10"], 1)
    with pytest.raises(subprocess.TimeoutExpired):
        run_subprocess(["sleep", "10"], timeout=1)
