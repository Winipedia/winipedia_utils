"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_git.test_pre_commit.test_config
"""

from pathlib import Path

from pytest_mock import MockFixture

from winipedia_utils.git.pre_commit import config
from winipedia_utils.git.pre_commit.config import PreCommitConfigFile
from winipedia_utils.modules.module import make_obj_importpath
from winipedia_utils.os.os import run_subprocess
from winipedia_utils.testing.assertions import assert_with_msg


class MyPreCommitConfigFile(PreCommitConfigFile):
    """Pre-commit config file for testing."""

    PATH = Path(".pre-commit-config.yaml")

    def __init__(self, tmp_path: Path, mocker: MockFixture) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        # Mock the install method to avoid running subprocess
        mocker.patch.object(PreCommitConfigFile, "install")
        super().__init__()


class TestPreCommitConfigFile:
    """Test class for PreCommitConfigFile."""

    def test___init__(self, tmp_path: Path, mocker: MockFixture) -> None:
        """Test method for __init__."""
        config_file = MyPreCommitConfigFile(tmp_path, mocker)
        assert_with_msg(
            config_file.path.exists(),
            f"Expected config file to exist at {config_file.path}",
        )

    def test_get_path(self, tmp_path: Path, mocker: MockFixture) -> None:
        """Test method for get_path."""
        config_file = MyPreCommitConfigFile(tmp_path, mocker)
        path = config_file.get_path()
        assert_with_msg(
            path.name == ".pre-commit-config.yaml",
            f"Expected path name to be '.pre-commit-config.yaml', got {path.name}",
        )

    def test_get_configs(self, tmp_path: Path, mocker: MockFixture) -> None:
        """Test method for get_configs."""
        config_file = MyPreCommitConfigFile(tmp_path, mocker)
        configs = config_file.get_configs()
        assert_with_msg(
            "repos" in configs,
            f"Expected 'repos' key in configs, got {configs.keys()}",
        )
        assert_with_msg(
            len(configs["repos"]) > 0,
            f"Expected non-empty repos list, got {configs['repos']}",
        )
        assert_with_msg(
            "hooks" in configs["repos"][0],
            f"Expected 'hooks' key in repo, got {configs['repos'][0].keys()}",
        )

    def test_install(self, mocker: MockFixture) -> None:
        """Test method for install."""
        # Mock run_subprocess to avoid actually running the command
        # Patch where it's imported in the config module
        mock_run = mocker.patch(
            f"{make_obj_importpath(config)}.{run_subprocess.__name__}"
        )
        PreCommitConfigFile.install()
        assert_with_msg(
            mock_run.called,
            "Expected run_subprocess to be called",
        )
