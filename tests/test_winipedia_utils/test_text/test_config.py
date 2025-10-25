"""module."""

from pathlib import Path
from typing import Any

from pytest_mock import MockFixture

from winipedia_utils.git.gitignore.config import GitIgnoreConfigFile
from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.testing.tests.base.utils.utils import assert_isabstrct_method
from winipedia_utils.text.config import ConfigFile, TomlConfigFile, YamlConfigFile


class MyTestConfigFile(ConfigFile):
    """Config file for testing."""

    PATH = Path("my_temp_file.txt")

    def get_config_dict(self) -> dict[str, Any]:
        """Get the config dict."""
        return {
            "key0": {"key1": [0, "value0", "value1"]},
            "key2": "notvalue2",
        }

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        self.get_path().write_text(str(self.get_config_dict()))
        self.config_dict = self.get_config_dict()
        super().__init__()

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def load(self) -> dict[str, Any]:
        """Load the config file."""
        return self.config_dict

    def dump(self, config: dict[str, Any]) -> None:
        """Dump the config file."""
        self.config_dict = config

    def get_configs(self) -> dict[str, Any]:
        """Get the config."""
        return {
            "key2": "value2",
            "key3": [1, 2, 3],
            "key4": {"key5": "value3"},
            "key6": {"key7": {"key8": [4, 5, {"key9": "value4"}]}},
        }


class TestConfigFile:
    """Test class for ConfigFile."""

    def test_init_config_files(self, mocker: MockFixture) -> None:
        """Test method for init_config_files."""
        # spy on __init__ of GitIgnoreConfigFile
        spy = mocker.spy(GitIgnoreConfigFile, GitIgnoreConfigFile.__init__.__name__)
        ConfigFile.init_config_files()
        assert_with_msg(
            spy.call_count == 1,
            f"Expected {GitIgnoreConfigFile.__init__.__name__} to be called once",
        )

    def test_get_path(self) -> None:
        """Test method for get_path."""
        assert_isabstrct_method(ConfigFile.get_path)

    def test_load(self) -> None:
        """Test method for load."""
        assert_isabstrct_method(ConfigFile.load)

    def test_dump(self) -> None:
        """Test method for dump."""
        assert_isabstrct_method(ConfigFile.dump)

    def test_get_configs(self) -> None:
        """Test method for get_configs."""
        assert_isabstrct_method(ConfigFile.get_configs)

    def test___init__(self, tmp_path: Path) -> None:
        """Test method for __init__."""
        config_file = MyTestConfigFile(tmp_path)

        # test it creates the file if it does not exist
        assert_with_msg(
            config_file.path.exists(),
            f"Expected config file to be created at {config_file.path}",
        )

    def test_add_missing_configs(self, tmp_path: Path) -> None:
        """Test method for add_missing_configs."""
        config_file = MyTestConfigFile(tmp_path)
        previous_config = config_file.get_config_dict()
        new_config = config_file.load()
        expected_config = config_file.get_configs()

        # test key0 is still in actual config
        assert_with_msg(
            "key0" in new_config,
            f"Expected key0 to be in new config, got {new_config}",
        )
        # test key0 == previous key0
        assert_with_msg(
            new_config["key0"] == previous_config["key0"],
            f"Expected key0 to be {previous_config['key0']}, got {new_config['key0']}",
        )

        # test key2 is updated from notvalue2 to value2
        assert_with_msg(
            new_config["key2"] == expected_config["key2"],
            f"Expected key2 to be {expected_config['key2']}, got {new_config['key2']}",
        )

        # assert all in expected are in new and are equal
        for k, v in expected_config.items():
            assert_with_msg(
                k in new_config, f"Expected {k} to be in new config, got {new_config}"
            )
            assert_with_msg(
                v == new_config[k],
                f"Expected {k} to be {v}, got {new_config[k]}",
            )

    def test_add_missing_dict_val(self) -> None:
        """Test method for add_missing_dict_val."""
        expected_dict = {"key0": "value0"}
        actual_dict = {"key1": "value1"}
        ConfigFile.add_missing_dict_val(expected_dict, actual_dict, "key0")
        assert_with_msg(
            actual_dict["key0"] == "value0",
            f"Expected key0 to be value0, got {actual_dict['key0']}",
        )

        expected_dict = {"key0": "value0"}
        actual_dict = {"key0": "notvalue0"}
        ConfigFile.add_missing_dict_val(expected_dict, actual_dict, "key0")
        assert_with_msg(
            actual_dict["key0"] == "value0",
            f"Expected key0 to be value0, got {actual_dict['key0']}",
        )

    def test_insert_missing_list_val(self) -> None:
        """Test method for insert_missing_list_val."""
        expected_list = ["value0", "value1", "value2"]
        actual_list = ["value0", "value1"]
        ConfigFile.insert_missing_list_val(expected_list, actual_list, 2)
        assert_with_msg(
            actual_list == expected_list,
            f"Expected {expected_list}, got {actual_list}",
        )

    def test_is_correct(self, tmp_path: Path) -> None:
        """Test method for is_correct."""
        config_file = MyTestConfigFile(tmp_path)
        assert_with_msg(
            config_file.is_correct(),
            f"Expected config file to be correct, got {config_file.path}",
        )

    def test_is_unwanted(self, tmp_path: Path) -> None:
        """Test method for is_unwanted."""
        config_file = MyTestConfigFile(tmp_path)
        assert_with_msg(
            not config_file.is_unwanted(),
            f"Expected config file to not be unwanted, got {config_file.path}",
        )
        config_file.path.write_text("")
        assert_with_msg(
            config_file.is_unwanted(),
            f"Expected config file to be unwanted, got {config_file.path}",
        )

    def test_is_correct_recursively(self) -> None:
        """Test method for is_correct_recursively."""
        dict1 = {"key0": "value0", "key1": "value1"}
        dict2 = {"key0": "value0", "key1": "value1"}
        assert_with_msg(
            ConfigFile.is_correct_recursively(dict1, dict2),
            f"Expected {dict1} to be correct, got {dict2}",
        )


class MyYamlConfigFile(YamlConfigFile):
    """Yaml config file for testing."""

    PATH = Path("my_temp_file.yaml")

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def get_configs(self) -> dict[str, Any]:
        """Get the config."""
        return {"key0": "value0"}

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()


class TestYamlConfigFile:
    """Test class for YamlConfigFile."""

    def test_get_python_setup_script(self) -> None:
        """Test method for get_poetry_run_setup_script."""
        expected = "python -m winipedia_utils.setup"
        actual = YamlConfigFile.get_python_setup_script()
        assert_with_msg(
            expected == actual,
            f"Expected {expected} to be poetry run setup script, got {actual}",
        )

    def test_load(self, tmp_path: Path) -> None:
        """Test method for load."""
        config_file = MyYamlConfigFile(tmp_path)
        expected, actual = config_file.get_configs(), config_file.load()
        assert_with_msg(
            expected == actual,
            f"Expected {expected} to be loaded, got {actual}",
        )

    def test_dump(self, tmp_path: Path) -> None:
        """Test method for dump."""
        config_file = MyYamlConfigFile(tmp_path)
        config_file.path.write_text("")
        config_file.dump(config_file.get_configs())
        expected, actual = config_file.get_configs(), config_file.load()
        assert_with_msg(
            expected == actual,
            f"Expected {expected} to be dumped, got {actual}",
        )


class MyTomlConfigFile(TomlConfigFile):
    """Toml config file for testing."""

    PATH = Path("my_temp_file.toml")

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def get_configs(self) -> dict[str, Any]:
        """Get the config."""
        return {"key0": "value0"}

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()


class TestTomlConfigFile:
    """Test class for TomlConfigFile."""

    def test_load(self, tmp_path: Path) -> None:
        """Test method for load."""
        config_file = MyTomlConfigFile(tmp_path)
        expected, actual = config_file.get_configs(), config_file.load()
        assert_with_msg(
            expected == actual,
            f"Expected {expected} to be loaded, got {actual}",
        )

    def test_dump(self, tmp_path: Path) -> None:
        """Test method for dump."""
        config_file = MyTomlConfigFile(tmp_path)
        config_file.path.write_text("")
        config_file.dump(config_file.get_configs())
        expected, actual = config_file.get_configs(), config_file.load()
        assert_with_msg(
            expected == actual,
            f"Expected {expected} to be dumped, got {actual}",
        )
