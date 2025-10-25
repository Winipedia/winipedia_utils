"""module."""

from pathlib import Path

from winipedia_utils.git.gitignore.config import GitIgnoreConfigFile
from winipedia_utils.testing.assertions import assert_with_msg


class MyGitIgnoreConfigFile(GitIgnoreConfigFile):
    """GitIgnore config file for testing."""

    PATH = Path(".gitignore")

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()


class TestGitIgnoreConfigFile:
    """Test class for GitIgnoreConfigFile."""

    def test_get_path(self, tmp_path: Path) -> None:
        """Test method for get_path."""
        config_file = MyGitIgnoreConfigFile(tmp_path)
        path = config_file.get_path()
        assert_with_msg(
            path.name == ".gitignore",
            f"Expected path name to be '.gitignore', got {path.name}",
        )

    def test_load(self, tmp_path: Path) -> None:
        """Test method for load."""
        config_file = MyGitIgnoreConfigFile(tmp_path)
        loaded = config_file.load()
        assert_with_msg(
            "ignore" in loaded,
            f"Expected 'ignore' key in loaded config, got {loaded.keys()}",
        )
        assert_with_msg(
            isinstance(loaded["ignore"], list),
            f"Expected 'ignore' value to be list, got {type(loaded['ignore'])}",
        )

    def test_load_static(self, tmp_path: Path) -> None:
        """Test method for load_static."""
        MyGitIgnoreConfigFile(tmp_path)
        loaded = GitIgnoreConfigFile.load_static()
        assert_with_msg(
            "ignore" in loaded,
            f"Expected 'ignore' key in loaded config, got {loaded.keys()}",
        )
        assert_with_msg(
            isinstance(loaded["ignore"], list),
            f"Expected 'ignore' value to be list, got {type(loaded['ignore'])}",
        )

    def test_dump(self, tmp_path: Path) -> None:
        """Test method for dump."""
        config_file = MyGitIgnoreConfigFile(tmp_path)
        test_patterns = ["*.pyc", "__pycache__/", ".env"]
        config_file.dump({"ignore": test_patterns})
        assert_with_msg(
            config_file.path.exists(),
            f"Expected .gitignore file to exist at {config_file.path}",
        )
        content = config_file.path.read_text()
        assert_with_msg(
            "*.pyc" in content,
            f"Expected '*.pyc' in .gitignore content, got {content}",
        )

    def test_get_configs(self, tmp_path: Path) -> None:
        """Test method for get_configs."""
        config_file = MyGitIgnoreConfigFile(tmp_path)
        configs = config_file.get_configs()
        assert_with_msg(
            "ignore" in configs,
            f"Expected 'ignore' key in configs, got {configs.keys()}",
        )
        assert_with_msg(
            isinstance(configs["ignore"], list),
            f"Expected 'ignore' value to be list, got {type(configs['ignore'])}",
        )
        assert_with_msg(
            len(configs["ignore"]) > 0,
            f"Expected non-empty ignore list, got {configs['ignore']}",
        )
