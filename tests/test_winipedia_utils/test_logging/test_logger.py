"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_logging.test_logger
"""

import logging

import pytest
from pytest_mock import MockFixture

from winipedia_utils.logging.config import LOGGING_CONFIG
from winipedia_utils.logging.logger import get_logger
from winipedia_utils.testing.assertions import assert_with_msg


def test_get_logger(caplog: pytest.LogCaptureFixture, mocker: MockFixture) -> None:
    """Test func for get_logger.

    This test verifies that the get_logger function returns a properly configured
    logger with the specified name and that it works as expected.
    """
    # Test 1: Basic functionality - get a logger with a specific name
    logger_name = "test_logger"
    logger = get_logger(logger_name)

    # Verify the logger has the correct name and type
    assert_with_msg(
        logger.name == logger_name,
        f"Expected logger name to be '{logger_name}', got '{logger.name}'",
    )
    assert_with_msg(
        type(logger) is logging.Logger,
        f"Expected logger to be a logging.Logger, got {type(logger)}",
    )

    # Test 2: Logger caching - same name returns same instance
    same_logger = get_logger(logger_name)
    assert_with_msg(
        logger is same_logger,
        "Expected get_logger to return the same logger instance for the same name",
    )

    # Test 3: Logger configuration - verify the logger uses the root logger's level
    # Note: Loggers with level=0 (NOTSET) inherit from parent
    root_logger = logging.getLogger()
    root_level_name = logging.getLevelName(root_logger.level)
    expected_level = LOGGING_CONFIG["root"]["level"]

    # Either the logger has the expected level directly, or it inherits from root
    level_is_correct = logger.level == getattr(logging, expected_level) or (
        logger.level == logging.NOTSET and root_level_name == expected_level
    )

    assert_with_msg(
        level_is_correct,
        (
            f"Expected logger to use level {expected_level} (directly or inherited), "
            f"but logger.level={logging.getLevelName(logger.level)} and "
            f"root_level={root_level_name}"
        ),
    )

    # Test 4: Logging functionality - log a message and verify it's captured correctly
    test_message = "Test log message"
    with caplog.at_level(logging.INFO):
        logger.info(test_message)

    # Verify the log record properties
    assert_with_msg(len(caplog.records) == 1, "Expected 1 log record")
    record = caplog.records[0]
    assert_with_msg(record.levelname == "INFO", "Expected INFO level")
    assert_with_msg(record.message == test_message, "Expected correct message")
    assert_with_msg(record.name == logger_name, "Expected correct logger name")

    # Test 5: Verify the log output contains the expected message
    # Note: The exact format can vary between pytest's caplog and direct console output
    log_text = caplog.text.strip()
    assert_with_msg(
        test_message in log_text,
        f"Expected message '{test_message}' not found in log: {log_text}",
    )

    # Test 6: dictConfig call - verify dictConfig was called with LOGGING_CONFIG
    mock_dict_config = mocker.patch("logging.config.dictConfig")

    # Force a reload of the module to trigger the dictConfig call
    import importlib

    import winipedia_utils.logging.logger

    importlib.reload(winipedia_utils.logging.logger)
    mock_dict_config.assert_called_once_with(LOGGING_CONFIG)
