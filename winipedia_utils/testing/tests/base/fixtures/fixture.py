"""Fixtures for testing.

This module provides custom fixtures for pytest that can be used to
automate common testing tasks and provide consistent setup and teardown
for tests.
"""

from collections.abc import Callable
from pathlib import Path

import pytest

from winipedia_utils.text.config import ConfigFile


@pytest.fixture
def config_file_factory[T: ConfigFile](
    tmp_path: Path,
) -> Callable[[type[T]], type[T]]:
    """Factory fixture for creating config file classes with tmp_path.

    This factory wraps any ConfigFile subclass to use tmp_path for get_path().
    Define tmp_path once here, then all test config classes inherit it.
    """

    def _make_test_config(
        base_class: type[T],
    ) -> type[T]:
        """Create a test config class that uses tmp_path."""

        class TestConfigFile(base_class):  # type: ignore [misc, valid-type]
            """Test config file with tmp_path override."""

            @classmethod
            def get_path(cls) -> Path:
                """Get the path to the config file in tmp_path."""
                path = super().get_path()
                return Path(tmp_path / path)

        return TestConfigFile

    return _make_test_config
