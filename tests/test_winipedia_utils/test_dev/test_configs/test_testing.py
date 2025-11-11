"""module."""

from collections.abc import Callable
from pathlib import Path

import pytest
from pytest_mock import MockFixture

from winipedia_utils.dev.configs import testing
from winipedia_utils.dev.configs.testing import (
    ConftestConfigFile,
    ExperimentConfigFile,
    PythonTestsConfigFile,
    ZeroTestConfigFile,
)
from winipedia_utils.dev.testing.convention import TESTS_PACKAGE_NAME
from winipedia_utils.utils.modules.module import make_obj_importpath
from winipedia_utils.utils.testing.assertions import assert_with_msg


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

    def test_run_tests(
        self,
        my_test_conftest_config_file: type[ConftestConfigFile],
        mocker: MockFixture,
    ) -> None:
        """Test method for run_tests."""
        mock_run = mocker.patch(
            make_obj_importpath(testing) + ".run_subprocess",
            return_value=0,
        )
        my_test_conftest_config_file.run_tests()
        mock_run.assert_called_once_with(["pytest"])


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
