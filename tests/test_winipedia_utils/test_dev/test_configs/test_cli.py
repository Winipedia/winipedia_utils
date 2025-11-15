"""module."""

from pathlib import Path

from winipedia_utils.dev.configs.cli import CliConfigFile
from winipedia_utils.utils.testing.assertions import assert_with_msg


class TestCliConfigFile:
    """Test class for CliConfigFile."""

    def test_get_parent_path(self) -> None:
        """Test method for get_parent_path."""
        # just assert it returns a path
        assert_with_msg(
            isinstance(CliConfigFile.get_parent_path(), Path),
            "Expected Path",
        )

    def test_get_content_str(self) -> None:
        """Test method for get_content_str."""
        content_str = CliConfigFile.get_content_str()
        assert_with_msg(
            len(content_str) > 0,
            "Expected non-empty string",
        )
