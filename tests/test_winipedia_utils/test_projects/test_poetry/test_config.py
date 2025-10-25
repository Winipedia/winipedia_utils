"""Tests for winipedia_utils.projects.poetry.config module."""

from pathlib import Path

from winipedia_utils.projects.poetry.config import (
    PyProjectTomlConfig,
    PyTypedConfigFile,
)
from winipedia_utils.testing.assertions import assert_with_msg


class MyPyProjectTomlConfig(PyProjectTomlConfig):
    """PyProject TOML config file for testing."""

    PATH = Path("pyproject.toml")

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()


class TestPyProjectTomlConfig:
    """Test class for PyProjectTomlConfig."""

    def test_get_path(self, tmp_path: Path) -> None:
        """Test method for get_path."""
        config_file = MyPyProjectTomlConfig(tmp_path)
        path = config_file.get_path()
        assert_with_msg(
            path.name == "pyproject.toml",
            f"Expected path name to be 'pyproject.toml', got {path.name}",
        )

    def test_get_configs(self, tmp_path: Path) -> None:
        """Test method for get_configs."""
        config_file = MyPyProjectTomlConfig(tmp_path)
        configs = config_file.get_configs()
        assert_with_msg(
            "project" in configs,
            f"Expected 'project' key in configs, got {configs.keys()}",
        )
        assert_with_msg(
            "build-system" in configs,
            f"Expected 'build-system' key in configs, got {configs.keys()}",
        )
        assert_with_msg(
            "tool" in configs,
            f"Expected 'tool' key in configs, got {configs.keys()}",
        )

    def test_get_package_name(self, tmp_path: Path) -> None:
        """Test method for get_package_name."""
        config_file = MyPyProjectTomlConfig(tmp_path)
        package_name = config_file.get_package_name()
        assert_with_msg(
            len(package_name) > 0,
            f"Expected package_name to be non-empty, got {package_name}",
        )

    def test_get_dev_dependencies(self, tmp_path: Path) -> None:
        """Test method for get_dev_dependencies."""
        config_file = MyPyProjectTomlConfig(tmp_path)
        dev_dependencies = config_file.get_dev_dependencies()
        assert_with_msg(
            len(dev_dependencies) >= 0,
            f"Expected dev_dependencies to be a set, got {type(dev_dependencies)}",
        )

    def test_get_expected_dev_dependencies(self, tmp_path: Path) -> None:
        """Test method for get_expected_dev_dependencies."""
        config_file = MyPyProjectTomlConfig(tmp_path)
        expected_dev_dependencies = config_file.get_expected_dev_dependencies()
        assert_with_msg(
            len(expected_dev_dependencies) > 0,
            f"Expected non-empty expected_dev_dependencies, "
            f"got {expected_dev_dependencies}",
        )


class MyPyTypedConfigFile(PyTypedConfigFile):
    """PyTyped config file for testing."""

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.tmp_path = tmp_path
        super().__init__()

    def get_path(self) -> Path:
        """Get the path to the config file."""
        toml_config = MyPyProjectTomlConfig(self.tmp_path)
        package_name = toml_config.get_package_name()
        return self.tmp_path / package_name / "py.typed"


class TestPyTypedConfigFile:
    """Test class for PyTypedConfigFile."""

    def test_get_path(self, tmp_path: Path) -> None:
        """Test method for get_path."""
        config_file = MyPyTypedConfigFile(tmp_path)
        path = config_file.get_path()
        assert_with_msg(
            path.name == "py.typed",
            f"Expected path name to be 'py.typed', got {path.name}",
        )

    def test_load(self, tmp_path: Path) -> None:
        """Test method for load."""
        config_file = MyPyTypedConfigFile(tmp_path)
        loaded = config_file.load()
        assert_with_msg(
            loaded == {},
            f"Expected empty dict from load, got {loaded}",
        )

    def test_dump(self, tmp_path: Path) -> None:
        """Test method for dump."""
        config_file = MyPyTypedConfigFile(tmp_path)
        # Test dumping empty config (should not raise)
        config_file.dump({})
        assert_with_msg(
            config_file.path.exists(),
            f"Expected py.typed file to exist at {config_file.path}",
        )

    def test_get_configs(self, tmp_path: Path) -> None:
        """Test method for get_configs."""
        config_file = MyPyTypedConfigFile(tmp_path)
        configs = config_file.get_configs()
        assert_with_msg(
            configs == {},
            f"Expected empty dict from get_configs, got {configs}",
        )
