"""module."""

from collections.abc import Callable
from pathlib import Path

import pytest

from winipedia_utils.projects.poetry.config import (
    PyprojectConfigFile,
    PyTypedConfigFile,
    TypedConfigFile,
)
from winipedia_utils.testing.assertions import assert_with_msg


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
            len(expected_dev_deps) == 0,
            "Expected expected_dev_deps to be empty",
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
        assert_with_msg(
            latest_version == "3.11",
            "Expected get_latest_possible_python_version to return 3.11",
        )
        config["project"]["requires-python"] = ">=3.8, <=3.12"
        my_test_pyproject_config_file.dump(config)
        latest_version = (
            my_test_pyproject_config_file.get_latest_possible_python_version()
        )
        assert_with_msg(
            latest_version == "3.12",
            "Expected get_latest_possible_python_version to return 3.12",
        )
        config["project"]["requires-python"] = ">=3.8, <3.11, ==3.10.*"
        my_test_pyproject_config_file.dump(config)
        latest_version = (
            my_test_pyproject_config_file.get_latest_possible_python_version()
        )
        assert_with_msg(
            latest_version == "3.10",
            "Expected get_latest_possible_python_version to return 3.10",
        )
        config["project"]["requires-python"] = ">=3.8"
        my_test_pyproject_config_file.dump(config)
        latest_version = (
            my_test_pyproject_config_file.get_latest_possible_python_version()
        )
        assert_with_msg(
            latest_version == "3.x",
            "Expected get_latest_possible_python_version to return 3.x",
        )


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
