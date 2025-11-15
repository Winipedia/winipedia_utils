"""module."""

from collections.abc import Callable

import pytest

from winipedia_utils.dev.configs.cli_test import CliTestConfigFile
from winipedia_utils.utils.testing.assertions import assert_with_msg


@pytest.fixture
def my_test_cli_test_config_file(
    config_file_factory: Callable[[type[CliTestConfigFile]], type[CliTestConfigFile]],
) -> type[CliTestConfigFile]:
    """Create a test zero test config file class with tmp_path."""

    class MyTestCliTestConfigFile(config_file_factory(CliTestConfigFile)):  # type: ignore [misc]
        """Test zero test config file with tmp_path override."""

    return MyTestCliTestConfigFile


class TestCliTestConfigFile:
    """Test class for CliTestConfigFile."""

    def test_get_filename(
        self, my_test_cli_test_config_file: type[CliTestConfigFile]
    ) -> None:
        """Test method for get_filename."""
        filename = my_test_cli_test_config_file.get_filename()
        # ZeroTestConfigFile reverses the filename
        assert_with_msg(
            filename.startswith("test_"),
            f"Expected filename to start with 'test_', got {filename}",
        )

    def test_get_content_str(
        self, my_test_cli_test_config_file: type[CliTestConfigFile]
    ) -> None:
        """Test method for get_content_str."""
        content_str = my_test_cli_test_config_file.get_content_str()
        assert_with_msg(
            "test" in content_str,
            "Expected 'test_zero' in content",
        )

    def test_get_parent_path(
        self, my_test_cli_test_config_file: type[CliTestConfigFile]
    ) -> None:
        """Test method for get_parent_path."""
        parent_path = my_test_cli_test_config_file.get_parent_path()
        assert_with_msg(
            parent_path.name == "test_cli",
            f"Expected parent_path to end with 'test_dev', got {parent_path}",
        )
