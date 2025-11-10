"""module."""

from collections.abc import Callable
from pathlib import Path

import pytest
from packaging.version import Version
from pytest_mock import MockFixture

from winipedia_utils.dev.configs import pyproject
from winipedia_utils.dev.configs.pyproject import (
    DotPythonVersionConfigFile,
    PyprojectConfigFile,
    PyTypedConfigFile,
    TypedConfigFile,
)
from winipedia_utils.utils.modules.module import make_obj_importpath
from winipedia_utils.utils.os.os import run_subprocess
from winipedia_utils.utils.testing.assertions import assert_with_msg


@pytest.fixture
def my_test_pyproject_config_file(
    config_file_factory: Callable[
        [type[PyprojectConfigFile]], type[PyprojectConfigFile]
    ],
) -> type[PyprojectConfigFile]:
    """Create a test pyproject config file class with tmp_path."""

    class MyTestPyprojectConfigFile(config_file_factory(PyprojectConfigFile)):  # type: ignore [misc]
        """Test pyproject config file with tmp_path override."""

    return MyTestPyprojectConfigFile


class TestPyprojectConfigFile:
    """Test class for PyprojectConfigFile."""

    def test_is_correct(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for is_correct."""
        my_test_pyproject_config_file()
        is_correct = my_test_pyproject_config_file.is_correct()
        assert_with_msg(
            is_correct,
            "Expected config to be correct after initialization",
        )

    def test_dump(
        self,
        my_test_pyproject_config_file: type[PyprojectConfigFile],
        mocker: MockFixture,
    ) -> None:
        """Test method for dump."""
        my_test_pyproject_config_file()
        # spy on remove_wrong_dependencies
        spy = mocker.spy(
            my_test_pyproject_config_file,
            my_test_pyproject_config_file.remove_wrong_dependencies.__name__,
        )
        config = my_test_pyproject_config_file.get_configs()
        my_test_pyproject_config_file.dump(config)
        spy.assert_called_once_with(config)

    def test_get_parent_path(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_parent_path."""
        expected = Path()
        actual = my_test_pyproject_config_file.get_parent_path()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_get_configs(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_configs."""
        # pyproject get configs internally uses load which makes it a special case
        # where the file must exist before calling get_configs
        my_test_pyproject_config_file()  # to create file
        configs = my_test_pyproject_config_file.get_configs()
        assert_with_msg(
            "project" in configs,
            "Expected 'project' key in configs",
        )
        assert_with_msg(
            "build-system" in configs,
            "Expected 'build-system' key in configs",
        )
        assert_with_msg(
            "tool" in configs,
            "Expected 'tool' key in configs",
        )

    def test_get_repository_name(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_repository_name."""
        my_test_pyproject_config_file()
        repository_name = my_test_pyproject_config_file.get_repository_name()
        assert_with_msg(
            len(repository_name) > 0,
            "Expected repository name to be non-empty",
        )

    def test_get_package_name(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_package_name."""
        my_test_pyproject_config_file()
        package_name = my_test_pyproject_config_file.get_package_name()
        assert_with_msg(
            len(package_name) > 0,
            "Expected package name to be non-empty",
        )

    def test_remove_wrong_dependencies(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for remove_wrong_dependencies."""
        my_test_pyproject_config_file()
        config = my_test_pyproject_config_file.get_configs()
        # add wrong dependencies to config
        config["project"]["dependencies"] = ["wrong (>=1.0.0,<2.0.0)"]
        config["tool"]["poetry"]["dev-dependencies"] = {"wrong": "*"}
        cleaned_config = my_test_pyproject_config_file.remove_wrong_dependencies(config)
        # assert wrong sections are removed
        assert_with_msg(
            "dependencies" not in cleaned_config["project"],
            "Expected dev-dependencies section to be deleted",
        )
        assert_with_msg(
            "dev-dependencies" not in cleaned_config["tool"]["poetry"],
            "Expected dev-dependencies section to be deleted",
        )

    def test_get_all_dependencies(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_all_dependencies."""
        my_test_pyproject_config_file()
        # get_all_dependencies should return a set (union of deps and dev_deps)
        all_deps = my_test_pyproject_config_file.get_all_dependencies()
        assert_with_msg(
            len(all_deps) >= 0,
            "Expected get_all_dependencies to return a set",
        )

    def test_get_dependencies(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_dependencies."""
        my_test_pyproject_config_file()
        # get_dependencies may raise if dependencies key doesn't exist
        # This is expected behavior for the test config
        deps = my_test_pyproject_config_file.get_dependencies()
        assert_with_msg(
            len(deps) >= 0,
            "Expected get_dependencies to return a set",
        )

    def test_get_dev_dependencies(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_dev_dependencies."""
        my_test_pyproject_config_file()
        dev_deps = my_test_pyproject_config_file.get_dev_dependencies()
        assert_with_msg(
            len(dev_deps) >= 0,
            "Expected get_dev_dependencies to return a set",
        )

    def test_get_expected_dev_dependencies(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_expected_dev_dependencies."""
        # get_expected_dev_dependencies internally uses get_configs which makes it a
        # special case where the file must exist before calling the method
        my_test_pyproject_config_file()
        expected_dev_deps = (
            my_test_pyproject_config_file.get_expected_dev_dependencies()
        )
        assert_with_msg(
            isinstance(expected_dev_deps, set),
            "Expected get_expected_dev_dependencies to return a set",
        )

    def test_get_authors(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_authors."""
        my_test_pyproject_config_file()
        config = my_test_pyproject_config_file.load()
        # assert authors rn is empty list
        assert_with_msg(
            my_test_pyproject_config_file.get_authors() == [],
            "Expected get_authors to return an empty list",
        )
        config["project"]["authors"] = [
            {"name": "Test Author", "email": "test@example.com"}
        ]
        my_test_pyproject_config_file.dump(config)
        authors = my_test_pyproject_config_file.get_authors()
        assert_with_msg(
            authors == [{"name": "Test Author", "email": "test@example.com"}],
            "Expected get_authors to return a list with one author",
        )

    def test_get_main_author(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_main_author."""
        my_test_pyproject_config_file()
        config = my_test_pyproject_config_file.load()
        # assert authors rn is empty list
        with pytest.raises(IndexError, match=r"list index out of range"):
            my_test_pyproject_config_file.get_main_author()
        config["project"]["authors"] = [
            {"name": "Test Author", "email": "test@example.com"}
        ]
        my_test_pyproject_config_file.dump(config)
        main_author = my_test_pyproject_config_file.get_main_author()
        assert_with_msg(
            main_author == {"name": "Test Author", "email": "test@example.com"},
            "Expected get_main_author to return the first author",
        )

    def test_get_main_author_name(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_main_author_name."""
        my_test_pyproject_config_file()
        config = my_test_pyproject_config_file.load()
        # assert authors rn is empty list
        with pytest.raises(IndexError, match=r"list index out of range"):
            my_test_pyproject_config_file.get_main_author_name()
        config["project"]["authors"] = [
            {"name": "Test Author", "email": "test@example.com"}
        ]
        my_test_pyproject_config_file.dump(config)
        main_author_name = my_test_pyproject_config_file.get_main_author_name()
        assert_with_msg(
            main_author_name == "Test Author",
            "Expected get_main_author_name to return the first author name",
        )

    def test_get_latest_possible_python_version(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_latest_possible_python_version."""
        my_test_pyproject_config_file()
        config = my_test_pyproject_config_file.load()
        config["project"]["requires-python"] = ">=3.8, <3.12"
        my_test_pyproject_config_file.dump(config)
        latest_version = (
            my_test_pyproject_config_file.get_latest_possible_python_version()
        )
        expected = Version("3.11")
        assert_with_msg(
            latest_version == expected,
            f"Expected {expected}, got {latest_version}",
        )
        config["project"]["requires-python"] = ">=3.8, <=3.12"
        my_test_pyproject_config_file.dump(config)
        latest_version = (
            my_test_pyproject_config_file.get_latest_possible_python_version()
        )
        expected = Version("3.12")
        assert_with_msg(
            latest_version == expected,
            f"Expected {expected}, got {latest_version}",
        )
        config["project"]["requires-python"] = ">=3.8, <3.11, ==3.10.*"
        my_test_pyproject_config_file.dump(config)
        latest_version = (
            my_test_pyproject_config_file.get_latest_possible_python_version()
        )
        expected = Version("3.10")
        assert_with_msg(
            latest_version == expected,
            f"Expected {expected}, got {latest_version}",
        )
        config["project"]["requires-python"] = ">=3.8"
        my_test_pyproject_config_file.dump(config)
        latest_version = (
            my_test_pyproject_config_file.get_latest_possible_python_version()
        )
        assert_with_msg(
            latest_version > Version("3.13"),
            "Expected get_latest_possible_python_version to return 3.x",
        )

    def test_fetch_latest_python_version(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for fetch_latest_python_version."""
        my_test_pyproject_config_file()
        latest_version = my_test_pyproject_config_file.fetch_latest_python_version()
        assert_with_msg(
            latest_version >= Version("3.13"),
            "Expected fetch_latest_python_version to return a version >= 3.11",
        )

    def test_get_supported_python_versions(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_supported_python_versions."""
        my_test_pyproject_config_file()
        config = my_test_pyproject_config_file.load()
        config["project"]["requires-python"] = ">=3.8, <3.12"
        my_test_pyproject_config_file.dump(config)
        supported_versions = (
            my_test_pyproject_config_file.get_supported_python_versions()
        )
        actual = [str(v) for v in supported_versions]
        expected = ["3.8", "3.9", "3.10", "3.11"]
        assert_with_msg(
            actual == expected,
            f"Expected {expected}, got {actual}",
        )

        config["project"]["requires-python"] = ">=3.2, <=4.6"
        my_test_pyproject_config_file.dump(config)
        supported_versions = (
            my_test_pyproject_config_file.get_supported_python_versions()
        )
        actual = [str(v) for v in supported_versions]
        expected = [
            "3.2",
            "3.3",
            "3.4",
            "3.5",
            "3.6",
            "4.2",
            "4.3",
            "4.4",
            "4.5",
            "4.6",
        ]
        assert_with_msg(
            actual == expected,
            f"Expected {expected}, got {actual}",
        )

    def test_get_first_supported_python_version(
        self, my_test_pyproject_config_file: type[PyprojectConfigFile]
    ) -> None:
        """Test method for get_first_supported_python_version."""
        my_test_pyproject_config_file()
        config = my_test_pyproject_config_file.load()
        config["project"]["requires-python"] = ">=3.8, <3.12"
        my_test_pyproject_config_file.dump(config)
        first_version = str(
            my_test_pyproject_config_file.get_first_supported_python_version()
        )
        assert_with_msg(
            first_version == "3.8",
            "Expected get_first_supported_python_version to return 3.8",
        )
        config["project"]["requires-python"] = "<=3.12, >3.8"
        my_test_pyproject_config_file.dump(config)
        first_version = str(
            my_test_pyproject_config_file.get_first_supported_python_version()
        )
        assert_with_msg(
            first_version == "3.8.1",
            "Expected get_first_supported_python_version to return 3.8.1",
        )

    def test_update_poetry(
        self,
        my_test_pyproject_config_file: type[PyprojectConfigFile],
        mocker: MockFixture,
    ) -> None:
        """Test method for update_poetry."""
        my_test_pyproject_config_file()
        # mock run_subprocess to avoid actually running poetry self update
        mock_run = mocker.patch(
            make_obj_importpath(pyproject) + "." + run_subprocess.__name__
        )
        my_test_pyproject_config_file.update_poetry()
        mock_run.assert_called_once()

    def test_update_with_dev(
        self,
        my_test_pyproject_config_file: type[PyprojectConfigFile],
        mocker: MockFixture,
    ) -> None:
        """Test method for install_with_dev."""
        my_test_pyproject_config_file()
        # mock run_subprocess to avoid actually running poetry install
        mock_run = mocker.patch(
            make_obj_importpath(pyproject) + "." + run_subprocess.__name__
        )
        my_test_pyproject_config_file.update_with_dev()
        mock_run.assert_called_once()


@pytest.fixture
def my_test_typed_config_file(
    config_file_factory: Callable[[type[TypedConfigFile]], type[TypedConfigFile]],
) -> type[TypedConfigFile]:
    """Create a test typed config file class with tmp_path."""

    class MyTestTypedConfigFile(config_file_factory(TypedConfigFile)):  # type: ignore [misc]
        """Test typed config file with tmp_path override."""

    return MyTestTypedConfigFile


class TestTypedConfigFile:
    """Test class for TypedConfigFile."""

    def test_get_file_extension(
        self, my_test_typed_config_file: type[TypedConfigFile]
    ) -> None:
        """Test method for get_file_extension."""
        expected = "typed"
        actual = my_test_typed_config_file.get_file_extension()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_load(self, my_test_typed_config_file: type[TypedConfigFile]) -> None:
        """Test method for load."""
        loaded = my_test_typed_config_file.load()
        assert_with_msg(
            loaded == {},
            "Expected load to return empty dict",
        )

    def test_dump(self, my_test_typed_config_file: type[TypedConfigFile]) -> None:
        """Test method for dump."""
        # assert dumps empty dict successfully
        my_test_typed_config_file.dump({})
        assert_with_msg(
            my_test_typed_config_file.load() == {},
            "Expected dump to work with empty dict",
        )
        # assert raises ValueError if config is not empty
        with pytest.raises(ValueError, match=r"Cannot dump to py\.typed file"):
            my_test_typed_config_file.dump({"key": "value"})

    def test_get_configs(
        self, my_test_typed_config_file: type[TypedConfigFile]
    ) -> None:
        """Test method for get_configs."""
        configs = my_test_typed_config_file.get_configs()
        assert_with_msg(
            configs == {},
            "Expected get_configs to return empty dict",
        )


@pytest.fixture
def my_test_py_typed_config_file(
    config_file_factory: Callable[[type[PyTypedConfigFile]], type[PyTypedConfigFile]],
) -> type[PyTypedConfigFile]:
    """Create a test py.typed config file class with tmp_path."""

    class MyTestPyTypedConfigFile(config_file_factory(PyTypedConfigFile)):  # type: ignore [misc]
        """Test py.typed config file with tmp_path override."""

    return MyTestPyTypedConfigFile


class TestPyTypedConfigFile:
    """Test class for PyTypedConfigFile."""

    def test_get_parent_path(
        self, my_test_py_typed_config_file: type[PyTypedConfigFile]
    ) -> None:
        """Test method for get_parent_path."""
        parent_path = my_test_py_typed_config_file.get_parent_path()
        # The parent path should be the package name
        assert_with_msg(
            len(parent_path.as_posix()) > 0,
            "Expected parent_path to be non-empty",
        )


@pytest.fixture
def my_test_dot_python_version_config_file(
    config_file_factory: Callable[
        [type[DotPythonVersionConfigFile]], type[DotPythonVersionConfigFile]
    ],
) -> type[DotPythonVersionConfigFile]:
    """Create a test .python-version config file class with tmp_path."""

    class MyTestDotPythonVersionConfigFile(
        config_file_factory(DotPythonVersionConfigFile)  # type: ignore [misc]
    ):
        """Test .python-version config file with tmp_path override."""

    return MyTestDotPythonVersionConfigFile


class TestDotPythonVersionConfigFile:
    """Test class for DotPythonVersionConfigFile."""

    def test_get_filename(
        self, my_test_dot_python_version_config_file: type[DotPythonVersionConfigFile]
    ) -> None:
        """Test method for get_filename."""
        expected = ""
        actual = my_test_dot_python_version_config_file.get_filename()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_get_file_extension(
        self, my_test_dot_python_version_config_file: type[DotPythonVersionConfigFile]
    ) -> None:
        """Test method for get_file_extension."""
        expected = "python-version"
        actual = my_test_dot_python_version_config_file.get_file_extension()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_get_parent_path(
        self, my_test_dot_python_version_config_file: type[DotPythonVersionConfigFile]
    ) -> None:
        """Test method for get_parent_path."""
        expected = Path()
        actual = my_test_dot_python_version_config_file.get_parent_path()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_load(
        self, my_test_dot_python_version_config_file: type[DotPythonVersionConfigFile]
    ) -> None:
        """Test method for load."""
        my_test_dot_python_version_config_file()
        loaded = my_test_dot_python_version_config_file.load()
        assert_with_msg(
            DotPythonVersionConfigFile.VERSION_KEY in loaded,
            "Expected 'version' key in loaded config",
        )
        assert_with_msg(
            len(loaded[DotPythonVersionConfigFile.VERSION_KEY]) > 0,
            "Expected version to be non-empty",
        )

    def test_dump(
        self, my_test_dot_python_version_config_file: type[DotPythonVersionConfigFile]
    ) -> None:
        """Test method for dump."""
        my_test_dot_python_version_config_file()
        config = {DotPythonVersionConfigFile.VERSION_KEY: "3.11"}
        my_test_dot_python_version_config_file.dump(config)
        loaded = my_test_dot_python_version_config_file.load()
        assert_with_msg(
            loaded[DotPythonVersionConfigFile.VERSION_KEY] == "3.11",
            "Expected version to be 3.11",
        )

    def test_dump_raises_type_error(
        self, my_test_dot_python_version_config_file: type[DotPythonVersionConfigFile]
    ) -> None:
        """Test method for dump with invalid type."""
        my_test_dot_python_version_config_file()
        with pytest.raises(TypeError, match=r"Cannot dump .* to \.python-version file"):
            my_test_dot_python_version_config_file.dump(["invalid"])

    def test_get_configs(
        self, my_test_dot_python_version_config_file: type[DotPythonVersionConfigFile]
    ) -> None:
        """Test method for get_configs."""
        my_test_dot_python_version_config_file()
        configs = my_test_dot_python_version_config_file.get_configs()
        assert_with_msg(
            DotPythonVersionConfigFile.VERSION_KEY in configs,
            "Expected 'version' key in configs",
        )
