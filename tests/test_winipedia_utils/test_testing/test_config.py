"""module."""

from collections.abc import Callable
from pathlib import Path

import pytest

from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.testing.config import (
    ConftestConfigFile,
    ExperimentConfigFile,
    PythonConfigFile,
    PythonTestsConfigFile,
    ZeroTestConfigFile,
)
from winipedia_utils.testing.convention import TESTS_PACKAGE_NAME


@pytest.fixture
def my_test_python_config_file(
    config_file_factory: Callable[[type[PythonConfigFile]], type[PythonConfigFile]],
) -> type[PythonConfigFile]:
    """Create a test python config file class with tmp_path."""

    class MyTestPythonConfigFile(config_file_factory(PythonConfigFile)):  # type: ignore [misc]
        """Test python config file with tmp_path override."""

        @classmethod
        def get_parent_path(cls) -> Path:
            """Get the parent path."""
            return Path()

        @classmethod
        def get_content_str(cls) -> str:
            """Get the content string."""
            return '"""Test content."""\n'

    return MyTestPythonConfigFile


class TestPythonConfigFile:
    """Test class for PythonConfigFile."""

    def test_load(self, my_test_python_config_file: type[PythonConfigFile]) -> None:
        """Test method for load."""
        my_test_python_config_file()
        loaded = my_test_python_config_file.load()
        assert_with_msg(
            PythonConfigFile.CONTENT_KEY in loaded,
            f"Expected '{PythonConfigFile.CONTENT_KEY}' key in loaded config",
        )

    def test_dump(self, my_test_python_config_file: type[PythonConfigFile]) -> None:
        """Test method for dump."""
        my_test_python_config_file()
        # Test successful dump
        content = '"""New content."""\n'
        my_test_python_config_file.dump({PythonConfigFile.CONTENT_KEY: content})
        loaded = my_test_python_config_file.load()
        assert_with_msg(
            loaded[PythonConfigFile.CONTENT_KEY] == content,
            "Expected dumped content to match loaded content",
        )
        # Test error when dumping non-dict
        with pytest.raises(TypeError, match=r"Cannot dump .* to python file"):
            my_test_python_config_file.dump([])

    def test_get_file_extension(
        self, my_test_python_config_file: type[PythonConfigFile]
    ) -> None:
        """Test method for get_file_extension."""
        expected = "py"
        actual = my_test_python_config_file.get_file_extension()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_get_configs(
        self, my_test_python_config_file: type[PythonConfigFile]
    ) -> None:
        """Test method for get_configs."""
        configs = my_test_python_config_file.get_configs()
        assert_with_msg(
            PythonConfigFile.CONTENT_KEY in configs,
            f"Expected '{PythonConfigFile.CONTENT_KEY}' key in configs",
        )

    def test_get_file_content(
        self, my_test_python_config_file: type[PythonConfigFile]
    ) -> None:
        """Test method for get_file_content."""
        my_test_python_config_file()
        content = my_test_python_config_file.get_file_content()
        assert_with_msg(
            len(content) > 0,
            "Expected file content to be non-empty",
        )

    def test_get_content_str(
        self, my_test_python_config_file: type[PythonConfigFile]
    ) -> None:
        """Test method for get_content_str."""
        content_str = my_test_python_config_file.get_content_str()
        assert_with_msg(
            len(content_str) > 0,
            "Expected content string to be non-empty",
        )

    def test_is_correct(
        self, my_test_python_config_file: type[PythonConfigFile]
    ) -> None:
        """Test method for is_correct."""
        my_test_python_config_file()
        is_correct = my_test_python_config_file.is_correct()
        assert_with_msg(
            is_correct,
            "Expected config to be correct after initialization",
        )


@pytest.fixture
def my_test_python_tests_config_file(
    config_file_factory: Callable[
        [type[PythonTestsConfigFile]], type[PythonTestsConfigFile]
    ],
) -> type[PythonTestsConfigFile]:
    """Create a test python tests config file class with tmp_path."""

    class MyTestPythonTestsConfigFile(config_file_factory(PythonTestsConfigFile)):  # type: ignore [misc]
        """Test python tests config file with tmp_path override."""

        @classmethod
        def get_content_str(cls) -> str:
            """Get the content string."""
            return '"""Test content."""\n'

    return MyTestPythonTestsConfigFile


class TestPythonTestsConfigFile:
    """Test class for PythonTestsConfigFile."""

    def test_get_parent_path(
        self, my_test_python_tests_config_file: type[PythonTestsConfigFile]
    ) -> None:
        """Test method for get_parent_path."""
        expected = Path(TESTS_PACKAGE_NAME)
        actual = my_test_python_tests_config_file.get_parent_path()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")


@pytest.fixture
def my_test_conftest_config_file(
    config_file_factory: Callable[[type[ConftestConfigFile]], type[ConftestConfigFile]],
) -> type[ConftestConfigFile]:
    """Create a test conftest config file class with tmp_path."""

    class MyTestConftestConfigFile(config_file_factory(ConftestConfigFile)):  # type: ignore [misc]
        """Test conftest config file with tmp_path override."""

    return MyTestConftestConfigFile


class TestConftestConfigFile:
    """Test class for ConftestConfigFile."""

    def test_get_content_str(
        self, my_test_conftest_config_file: type[ConftestConfigFile]
    ) -> None:
        """Test method for get_content_str."""
        content_str = my_test_conftest_config_file.get_content_str()
        assert_with_msg(
            "pytest_plugins" in content_str,
            "Expected 'pytest_plugins' in conftest content",
        )


@pytest.fixture
def my_test_zero_test_config_file(
    config_file_factory: Callable[[type[ZeroTestConfigFile]], type[ZeroTestConfigFile]],
) -> type[ZeroTestConfigFile]:
    """Create a test zero test config file class with tmp_path."""

    class MyTestZeroTestConfigFile(config_file_factory(ZeroTestConfigFile)):  # type: ignore [misc]
        """Test zero test config file with tmp_path override."""

    return MyTestZeroTestConfigFile


class TestZeroTestConfigFile:
    """Test class for ZeroTestConfigFile."""

    def test_get_filename(
        self, my_test_zero_test_config_file: type[ZeroTestConfigFile]
    ) -> None:
        """Test method for get_filename."""
        filename = my_test_zero_test_config_file.get_filename()
        # ZeroTestConfigFile reverses the filename
        assert_with_msg(
            filename.startswith("test_"),
            f"Expected filename to start with 'test_', got {filename}",
        )

    def test_get_content_str(
        self, my_test_zero_test_config_file: type[ZeroTestConfigFile]
    ) -> None:
        """Test method for get_content_str."""
        content_str = my_test_zero_test_config_file.get_content_str()
        assert_with_msg(
            "test_zero" in content_str,
            "Expected 'test_zero' in content",
        )


@pytest.fixture
def my_test_experiment_config_file(
    config_file_factory: Callable[
        [type[ExperimentConfigFile]], type[ExperimentConfigFile]
    ],
) -> type[ExperimentConfigFile]:
    """Create a test experiment config file class with tmp_path."""

    class MyTestExperimentConfigFile(config_file_factory(ExperimentConfigFile)):  # type: ignore [misc]
        """Test experiment config file with tmp_path override."""

    return MyTestExperimentConfigFile


class TestExperimentConfigFile:
    """Test class for ExperimentConfigFile."""

    def test_get_parent_path(
        self, my_test_experiment_config_file: type[ExperimentConfigFile]
    ) -> None:
        """Test method for get_parent_path."""
        expected = Path()
        actual = my_test_experiment_config_file.get_parent_path()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_get_content_str(
        self, my_test_experiment_config_file: type[ExperimentConfigFile]
    ) -> None:
        """Test method for get_content_str."""
        content_str = my_test_experiment_config_file.get_content_str()
        assert_with_msg(
            "experimentation" in content_str,
            "Expected 'experimentation' in content",
        )
