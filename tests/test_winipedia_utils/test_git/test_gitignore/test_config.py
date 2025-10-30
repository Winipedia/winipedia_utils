"""module."""

from collections.abc import Callable
from pathlib import Path

import pytest
from pytest_mock import MockFixture

from winipedia_utils.git.gitignore.config import GitIgnoreConfigFile
from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.text.config import ConfigFile, DotEnvConfigFile


@pytest.fixture
def my_test_gitignore_config_file(
    config_file_factory: Callable[[type[ConfigFile]], type[ConfigFile]],
) -> type[GitIgnoreConfigFile]:
    """Create a test gitignore config file class with tmp_path."""

    class MyTestGitIgnoreConfigFile(
        config_file_factory(GitIgnoreConfigFile)  # type: ignore [misc]
    ):
        """Test gitignore config file with tmp_path override."""

    return MyTestGitIgnoreConfigFile


class TestGitIgnoreConfigFile:
    """Test class for GitIgnoreConfigFile."""

    def test_get_filename(
        self, my_test_gitignore_config_file: type[GitIgnoreConfigFile]
    ) -> None:
        """Test method for get_filename."""
        filename = my_test_gitignore_config_file.get_filename()
        assert_with_msg(
            filename == "",
            f"Expected empty string, got {filename}",
        )

    def test_get_parent_path(
        self, my_test_gitignore_config_file: type[GitIgnoreConfigFile]
    ) -> None:
        """Test method for get_parent_path."""
        parent_path = my_test_gitignore_config_file.get_parent_path()
        assert_with_msg(
            parent_path == Path(),
            f"Expected Path(), got {parent_path}",
        )

    def test_get_file_extension(
        self, my_test_gitignore_config_file: type[GitIgnoreConfigFile]
    ) -> None:
        """Test method for get_file_extension."""
        extension = my_test_gitignore_config_file.get_file_extension()
        assert_with_msg(
            extension == "gitignore",
            f"Expected 'gitignore', got {extension}",
        )

    def test_load(
        self, my_test_gitignore_config_file: type[GitIgnoreConfigFile]
    ) -> None:
        """Test method for load."""
        # Initialize the config file first
        my_test_gitignore_config_file()
        loaded = my_test_gitignore_config_file.load()
        assert_with_msg(
            len(loaded) > 0,
            "Expected loaded config to be non-empty",
        )
        # assert .env is in loaded config
        assert_with_msg(
            any(DotEnvConfigFile.get_path().as_posix() in item for item in loaded),
            "Expected .env pattern in loaded config",
        )

    def test_dump(
        self, my_test_gitignore_config_file: type[GitIgnoreConfigFile]
    ) -> None:
        """Test method for dump."""
        test_config = ["__pycache__/", ".idea/", ".pytest_cache/"]
        my_test_gitignore_config_file.dump(test_config)
        loaded = my_test_gitignore_config_file.load()
        assert_with_msg(
            loaded == test_config,
            f"Expected {test_config}, got {loaded}",
        )
        # Test error handling for non-list
        with pytest.raises(TypeError, match="Cannot dump"):
            my_test_gitignore_config_file.dump({"key": "value"})

    def test_get_configs(
        self,
        my_test_gitignore_config_file: type[GitIgnoreConfigFile],
        mocker: MockFixture,
    ) -> None:
        """Test method for get_configs."""
        # Mock the load method to return a minimal list
        mocker.patch.object(
            my_test_gitignore_config_file,
            "load",
            return_value=["__pycache__/"],
        )
        configs = my_test_gitignore_config_file.get_configs()
        assert_with_msg(
            len(configs) > 0,
            "Expected configs to be non-empty",
        )
        # Verify it contains expected patterns
        assert_with_msg(
            any("__pycache__" in item for item in configs),
            "Expected __pycache__ pattern in configs",
        )

    def test_get_github_python_gitignore(
        self, my_test_gitignore_config_file: type[GitIgnoreConfigFile]
    ) -> None:
        """Test method for get_github_python_gitignore."""
        patterns = my_test_gitignore_config_file.get_github_python_gitignore()
        assert_with_msg(
            len(patterns) > 0,
            "Expected patterns to be non-empty",
        )
