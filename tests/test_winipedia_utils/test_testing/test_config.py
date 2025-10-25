"""module."""

from pathlib import Path

from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.testing.config import (
    ConftestConfigFile,
    ExperimentConfigFile,
    PythonConfigFile,
    ZeroTestConfigFile,
)


class MyPythonConfigFile(PythonConfigFile):
    """Python config file for testing."""

    PATH = Path("my_temp_file.py")

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def get_content(self) -> str:
        """Get the content."""
        return '"""Test content."""\n'

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()


class TestPythonConfigFile:
    """Test class for PythonConfigFile."""

    def test_get_configs(self, tmp_path: Path) -> None:
        """Test method for get_configs."""
        config_file = MyPythonConfigFile(tmp_path)
        expected = config_file.get_content()
        actual = config_file.get_configs()
        assert_with_msg(
            actual["content"] == expected,
            f"Expected {expected}, got {actual['content']}",
        )

    def test_get_content(self, tmp_path: Path) -> None:
        """Test method for get_content."""
        config_file = MyPythonConfigFile(tmp_path)
        content = config_file.get_content()
        assert_with_msg(
            content == '"""Test content."""\n',
            f'Expected \'"""Test content."""\\n\', got {content}',
        )

    def test_load(self, tmp_path: Path) -> None:
        """Test method for load."""
        config_file = MyPythonConfigFile(tmp_path)
        loaded = config_file.load()
        assert_with_msg(
            "content" in loaded,
            f"Expected 'content' key in loaded config, got {loaded}",
        )
        assert_with_msg(
            loaded["content"] == '"""Test content."""\n',
            f'Expected \'"""Test content."""\\n\', got {loaded["content"]}',
        )

    def test_dump(self, tmp_path: Path) -> None:
        """Test method for dump."""
        config_file = MyPythonConfigFile(tmp_path)
        new_content = '"""New content."""\n'
        config_file.dump({"content": new_content})
        assert_with_msg(
            config_file.path.read_text() == new_content,
            f"Expected {new_content}, got {config_file.path.read_text()}",
        )


class MyConftestConfigFile(ConftestConfigFile):
    """Conftest config file for testing."""

    PATH = Path("conftest.py")

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()


class TestConftestConfigFile:
    """Test class for ConftestConfigFile."""

    def test_get_content(self, tmp_path: Path) -> None:
        """Test method for get_content."""
        config_file = MyConftestConfigFile(tmp_path)
        content = config_file.get_content()
        assert_with_msg(
            "pytest_plugins" in content,
            f"Expected 'pytest_plugins' in content, got {content}",
        )

    def test_get_path(self, tmp_path: Path) -> None:
        """Test method for get_path."""
        config_file = MyConftestConfigFile(tmp_path)
        path = config_file.get_path()
        assert_with_msg(
            path.name == "conftest.py",
            f"Expected path name to be 'conftest.py', got {path.name}",
        )

    def test_get_configs(self, tmp_path: Path) -> None:
        """Test method for get_configs."""
        config_file = MyConftestConfigFile(tmp_path)
        configs = config_file.get_configs()
        assert_with_msg(
            "content" in configs,
            f"Expected 'content' key in configs, got {configs}",
        )
        assert_with_msg(
            "pytest_plugins" in configs["content"],
            f"Expected 'pytest_plugins' in content, got {configs['content']}",
        )


class MyZeroTestConfigFile(ZeroTestConfigFile):
    """Zero test config file for testing."""

    PATH = Path("test_0.py")

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()


class TestZeroTestConfigFile:
    """Test class for Test0ConfigFile."""

    def test_get_content(self, tmp_path: Path) -> None:
        """Test method for get_content."""
        config_file = MyZeroTestConfigFile(tmp_path)
        content = config_file.get_content()
        assert_with_msg(
            "test_0" in content,
            f"Expected 'test_0' in content, got {content}",
        )

    def test_get_path(self, tmp_path: Path) -> None:
        """Test method for get_path."""
        config_file = MyZeroTestConfigFile(tmp_path)
        path = config_file.get_path()
        assert_with_msg(
            path.name == "test_0.py",
            f"Expected path name to be 'test_0.py', got {path.name}",
        )

    def test_get_configs(self, tmp_path: Path) -> None:
        """Test method for get_configs."""
        config_file = MyZeroTestConfigFile(tmp_path)
        configs = config_file.get_configs()
        assert_with_msg(
            "content" in configs,
            f"Expected 'content' key in configs, got {configs}",
        )
        assert_with_msg(
            "test_0" in configs["content"],
            f"Expected 'test_0' in content, got {configs['content']}",
        )


class MyExperimentConfigFile(ExperimentConfigFile):
    """Experiment config file for testing."""

    PATH = Path("experiment.py")

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()


class TestExperimentConfigFile:
    """Test class for ExperimentConfigFile."""

    def test_get_path(self, tmp_path: Path) -> None:
        """Test method for get_path."""
        config_file = MyExperimentConfigFile(tmp_path)
        path = config_file.get_path()
        assert_with_msg(
            path.name == "experiment.py",
            f"Expected path name to be 'experiment.py', got {path.name}",
        )

    def test_get_content(self, tmp_path: Path) -> None:
        """Test method for get_content."""
        config_file = MyExperimentConfigFile(tmp_path)
        content = config_file.get_content()
        assert_with_msg(
            "experimentation" in content,
            f"Expected 'experimentation' in content, got {content}",
        )
