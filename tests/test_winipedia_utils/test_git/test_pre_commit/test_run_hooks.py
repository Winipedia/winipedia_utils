"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_git.test_pre_commit.test_run_hooks
"""

import sys
from subprocess import CompletedProcess  # nosec: B404

import pytest
from pytest_mock import MockFixture

from winipedia_utils.git.pre_commit import hooks
from winipedia_utils.git.pre_commit.run_hooks import run_all
from winipedia_utils.modules.function import get_all_functions_from_module
from winipedia_utils.os.os import run_subprocess
from winipedia_utils.testing.assertions import assert_with_msg


def test_run_all(caplog: pytest.LogCaptureFixture, mocker: MockFixture) -> None:
    """Test func for _run_all_hooks with both success and failure cases."""
    # patch sys.exit to prevent the test from exiting
    mocker.patch(f"{sys.__name__}.exit")

    # patch run_subprocess to simulate some hooks passing and some failing
    mock_run_subprocess = mocker.patch(
        f"{run_all.__module__}.{run_subprocess.__name__}"
    )

    # create a list of CompletedProcess objects with mixed results
    hook_functions = get_all_functions_from_module(hooks)
    mock_results = [
        CompletedProcess(
            args=hook_func(),
            returncode=0,
            stdout="Success output",
            stderr="",
        )
        for hook_func in hook_functions
    ]
    # make every second fail
    for i in range(1, len(mock_results), 2):
        mock_results[i].returncode = 1
        mock_results[i].stdout = "Failure output"

    # set the side effect of mock_run_subprocess to return the mock results
    mock_run_subprocess.side_effect = mock_results

    # call the function with caplog at info and error level
    with caplog.at_level("INFO"):
        run_all()

    # verify the results
    for hook_func in hook_functions:
        mock_run_subprocess.assert_any_call(
            hook_func(),
            check=False,
            capture_output=True,
            text=True,
        )
    # Verify that we have the expected number of log records for failing hooks
    assert_with_msg(
        len(caplog.records) == len(hook_functions),
        (
            f"Expected {len(hook_functions)} failing hook logs, "
            f"got {len(caplog.records)}"
        ),
    )

    # Verify the format of the logs we do have
    for i, record in enumerate(caplog.records):
        assert_with_msg(
            "Hook" in record.message,
            f"Expected log record {i} to contain 'Hook', got {record.message}",
        )
        assert_with_msg(
            "-" in record.message,
            f"Expected log record {i} to contain '-', got {record.message}",
        )
        assert_with_msg(
            "FAILED" in record.message or "PASSED" in record.message,
            f"Expected log record {i} to contain "
            f"'FAILED' or 'PASSED', got {record.message}",
        )
