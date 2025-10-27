"""module."""

from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

import pytest
from pytest_mock import MockFixture

from winipedia_utils.modules.class_ import get_all_nonabstract_subclasses
from winipedia_utils.modules.module import make_obj_importpath
from winipedia_utils.testing.assertions import assert_with_msg
from winipedia_utils.text.config import (
    ConfigFile,
    DotEnvConfigFile,
    TomlConfigFile,
    YamlConfigFile,
)


@pytest.fixture
def my_test_config_file(
    config_file_factory: Callable[[type[ConfigFile]], type[ConfigFile]],
) -> type[ConfigFile]:
    """Create a test config file class with tmp_path."""

    class MyTestConfigFile(config_file_factory(ConfigFile)):  # type: ignore [misc]
        """Test config file with tmp_path override."""

        STORAGE_DICT: ClassVar[dict[str, Any]] = {
            "key0": "value0",
            "key1": "value1",
            "key2": {"key3": "value3"},
            "key4": [["value4"], {"key5": "value5", "key6": "value6"}],
        }

        @classmethod
        def get_file_extension(cls) -> str:
            """Get the file extension of the config file."""
            return "txt"

        @classmethod
        def load(cls) -> dict[str, Any] | list[Any]:
            """Load the config file."""
            return cls.STORAGE_DICT

        @classmethod
        def dump(cls, config: dict[str, Any] | list[Any]) -> None:
            """Dump the config file."""
            if not isinstance(config, dict):
                msg = f"Cannot dump {config} to txt file."
                raise TypeError(msg)
            cls.STORAGE_DICT = config

        @classmethod
        def get_parent_path(cls) -> Path:
            """Get the path to the config file."""
            return Path("parent_dir")

        @classmethod
        def get_configs(cls) -> dict[str, Any]:
            """Get the config."""
            return {
                "key1": "value1",
                "key2": {"key3": "value3"},
                "key4": [["notvalue4", "extra_value"], {"key5": "notvalue5"}],
                "key7": "value7",
            }

    return MyTestConfigFile


class TestConfigFile:
    """Test class for ConfigFile."""

    def test_get_parent_path(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for get_parent_path."""
        expected = Path("parent_dir")
        actual = my_test_config_file.get_parent_path()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_load(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for load."""
        # assert is dict
        assert_with_msg(
            isinstance(my_test_config_file.load(), dict),
            "Expected dict",
        )

    def test_dump(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for dump."""
        # assert dumps correctly
        storage_dict = my_test_config_file.load()
        dunmp_dict = {"key": "value"}
        assert_with_msg(
            storage_dict != dunmp_dict,
            "Expected different dicts",
        )

        my_test_config_file.dump(dunmp_dict)
        assert_with_msg(
            my_test_config_file.load() == dunmp_dict,
            "Expected dump to work",
        )
        # assert raises TypeError if not dict
        with pytest.raises(TypeError):
            my_test_config_file.dump([])

    def test_get_file_extension(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for get_file_extension."""
        assert_with_msg(
            my_test_config_file.get_file_extension() == "txt",
            "Expected txt",
        )

    def test_get_configs(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for get_configs."""
        assert_with_msg(
            isinstance(my_test_config_file.get_configs(), dict),
            "Expected dict",
        )

    def test___init__(
        self, my_test_config_file: type[ConfigFile], mocker: MockFixture
    ) -> None:
        """Test method for __init__."""
        # create file first to not trigger dunmp in init
        my_test_config_file.get_path().parent.mkdir(parents=True, exist_ok=True)
        # write non-empty file to trigger add_missing_configs,
        # empty file triggers is_unwanted
        my_test_config_file.get_path().write_text("test")
        my_test_config_file()
        after = my_test_config_file.load()

        # assert config is correct
        assert_with_msg(
            after
            == {
                "key0": "value0",
                "key1": "value1",
                "key2": {"key3": "value3"},
                "key4": [
                    ["notvalue4", "extra_value", "value4"],
                    {"key5": "notvalue5", "key6": "value6"},
                ],
                "key7": "value7",
            },
            "Expected config to be correct",
        )

        # remove file to trigger init dump
        my_test_config_file.get_path().unlink()
        my_test_config_file()
        # assert path exists
        assert_with_msg(
            my_test_config_file.get_path().exists(),
            "Expected path to exist",
        )
        # assert config is == get_configs, not any of previous config
        assert_with_msg(
            my_test_config_file.load() == my_test_config_file.get_configs(),
            "Expected config to be correct",
        )

        # mock is_correct to return False
        mocker.patch.object(
            my_test_config_file,
            my_test_config_file.is_correct.__name__,
            return_value=False,
        )
        with pytest.raises(ValueError, match="not correct"):
            my_test_config_file()

    def test_get_path(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for get_path."""
        # will be my.txt not my_test.txt bc the fixture factory
        # creates a runtime subclass TestConfigFile so filename will removesuffix
        # see implementation of config_file_factory fixture and get_filename
        expected = Path("parent_dir/my.txt")
        actual = my_test_config_file.get_path()
        # assert actual ends with expected
        assert_with_msg(
            actual.as_posix().endswith(expected.as_posix()),
            f"Expected {expected}, got {actual}",
        )

    def test_get_filename(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for get_filename."""
        expected = "my"
        actual = my_test_config_file.get_filename()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_add_missing_configs(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for add_missing_configs."""
        # same test as in init test
        expected: dict[str, Any] = {
            "key0": "value0",
            "key1": "value1",
            "key2": {"key3": "value3"},
            "key4": [
                ["notvalue4", "extra_value", "value4"],
                {"key5": "notvalue5", "key6": "value6"},
            ],
            "key7": "value7",
        }
        actual = my_test_config_file.add_missing_configs()
        assert_with_msg(actual == expected, "Expected config to be correct")

    def test_add_missing_dict_val(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for add_missing_dict_val."""
        expected: dict[str, Any] = {"key": "value"}
        actual: dict[str, Any] = {}
        my_test_config_file.add_missing_dict_val(expected, actual, "key")
        assert_with_msg(
            actual["key"] == expected["key"], "Expected config to be correct"
        )

    def test_insert_missing_list_val(
        self, my_test_config_file: type[ConfigFile]
    ) -> None:
        """Test method for insert_missing_list_val."""
        expected: list[Any] = ["value"]
        actual: list[Any] = []
        my_test_config_file.insert_missing_list_val(expected, actual, 0)
        assert_with_msg(actual[0] == expected[0], "Expected config to be correct")

    def test_is_correct(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for is_correct."""
        assert_with_msg(
            not my_test_config_file.is_correct(),
            "Expected config to be correct",
        )
        assert_with_msg(
            my_test_config_file().is_correct(),
            "Expected config to be correct",
        )

    def test_is_unwanted(self, my_test_config_file: type[ConfigFile]) -> None:
        """Test method for is_unwanted."""
        my_test_config_file().get_path().write_text("")
        assert_with_msg(
            my_test_config_file.is_unwanted(),
            "Expected config to be unwanted",
        )

    def test_is_correct_recursively(
        self, my_test_config_file: type[ConfigFile]
    ) -> None:
        """Test method for is_correct_recursively."""
        expected: dict[str, Any] = {
            "key0": "value0",
            "key1": "value1",
            "key2": {"key3": "value3"},
            "key4": [
                ["notvalue4", "extra_value"],
                {"key5": "notvalue5", "key6": "value6"},
            ],
            "key7": "value7",
        }
        actual: dict[str, Any] = {
            "key0": "value0",
            "key1": "value1",
            "key2": {"key3": "value3"},
            "key4": [
                ["notvalue4", "extra_value", "extra_value2"],
                {"key5": "notvalue5", "key6": "value6"},
            ],
            "key7": "value7",
            "key8": "value8",
        }
        assert_with_msg(
            my_test_config_file.is_correct_recursively(expected, actual),
            "Expected config to be correct",
        )
        # change one in actual to not be correct
        actual["key2"]["key3"] = "notvalue3"
        assert_with_msg(
            not my_test_config_file.is_correct_recursively(expected, actual),
            "Expected config to be correct",
        )

    def test_init_config_files(
        self, my_test_config_file: type[ConfigFile], mocker: MockFixture
    ) -> None:
        """Test method for init_config_files."""
        # mock get_all_nonabstract_subclasses to return my_test_config_file
        mocker.patch(
            make_obj_importpath(get_all_nonabstract_subclasses),
            return_value={my_test_config_file},
        )
        my_test_config_file.init_config_files()
        assert_with_msg(
            my_test_config_file.load() == my_test_config_file.get_configs(),
            "Expected config to be correct",
        )
        # other files were also created

        tmp_path = Path(
            my_test_config_file.get_path()
            .as_posix()
            .split(my_test_config_file.get_parent_path().as_posix())[0]
        )
        num_created = len(list(tmp_path.rglob("*.*")))
        assert_with_msg(num_created == 1, "Expected other files to be created")

    def test_get_python_setup_script(
        self, my_test_config_file: type[ConfigFile]
    ) -> None:
        """Test method for get_python_setup_script."""
        expected = "python -m winipedia_utils.setup"
        actual = my_test_config_file.get_python_setup_script()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")


@pytest.fixture
def my_test_yaml_config_file(
    config_file_factory: Callable[[type[YamlConfigFile]], type[YamlConfigFile]],
) -> type[YamlConfigFile]:
    """Create a test yaml config file class with tmp_path."""

    class MyTestYamlConfigFile(config_file_factory(YamlConfigFile)):  # type: ignore [misc]
        """Test yaml config file with tmp_path override."""

        @classmethod
        def get_parent_path(cls) -> Path:
            """Get the path to the config file."""
            return Path()

        @classmethod
        def get_configs(cls) -> dict[str, Any]:
            """Get the config."""
            return {"key": "value"}

    return MyTestYamlConfigFile


class TestYamlConfigFile:
    """Test class for YamlConfigFile."""

    def test_load(self, my_test_yaml_config_file: type[YamlConfigFile]) -> None:
        """Test method for load."""
        my_test_yaml_config_file()
        expected = {"key": "value"}
        actual = my_test_yaml_config_file.load()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_dump(self, my_test_yaml_config_file: type[YamlConfigFile]) -> None:
        """Test method for dump."""
        my_test_yaml_config_file.dump({"key": "value"})
        assert_with_msg(
            my_test_yaml_config_file.load() == {"key": "value"},
            "Expected dump to work",
        )

    def test_get_file_extension(
        self, my_test_yaml_config_file: type[YamlConfigFile]
    ) -> None:
        """Test method for get_file_extension."""
        assert_with_msg(
            my_test_yaml_config_file.get_file_extension() == "yaml",
            "Expected yaml",
        )


@pytest.fixture
def my_test_toml_config_file(
    config_file_factory: Callable[[type[TomlConfigFile]], type[TomlConfigFile]],
) -> type[TomlConfigFile]:
    """Create a test toml config file class with tmp_path."""

    class MyTestTomlConfigFile(config_file_factory(TomlConfigFile)):  # type: ignore [misc]
        """Test toml config file with tmp_path override."""

        @classmethod
        def get_parent_path(cls) -> Path:
            """Get the path to the config file."""
            return Path()

        @classmethod
        def get_configs(cls) -> dict[str, Any]:
            """Get the config."""
            return {"key": "value"}

    return MyTestTomlConfigFile


class TestTomlConfigFile:
    """Test class for TomlConfigFile."""

    def test_load(self, my_test_toml_config_file: type[TomlConfigFile]) -> None:
        """Test method for load."""
        my_test_toml_config_file()
        expected = {"key": "value"}
        actual = my_test_toml_config_file.load()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_dump(self, my_test_toml_config_file: type[TomlConfigFile]) -> None:
        """Test method for dump."""
        my_test_toml_config_file.dump({"key": "value"})
        assert_with_msg(
            my_test_toml_config_file.load() == {"key": "value"},
            "Expected dump to work",
        )

    def test_get_file_extension(
        self, my_test_toml_config_file: type[TomlConfigFile]
    ) -> None:
        """Test method for get_file_extension."""
        assert_with_msg(
            my_test_toml_config_file.get_file_extension() == "toml",
            "Expected toml",
        )


@pytest.fixture
def my_test_dotenv_config_file(
    config_file_factory: Callable[[type[DotEnvConfigFile]], type[DotEnvConfigFile]],
) -> type[DotEnvConfigFile]:
    """Create a test dotenv config file class with tmp_path."""

    class MyTestDotEnvConfigFile(config_file_factory(DotEnvConfigFile)):  # type: ignore [misc]
        """Test dotenv config file with tmp_path override."""

    return MyTestDotEnvConfigFile


class TestDotEnvConfigFile:
    """Test class for DotEnvConfigFile."""

    def test_load(self, my_test_dotenv_config_file: type[DotEnvConfigFile]) -> None:
        """Test method for load."""
        # Create the .env file with some content
        my_test_dotenv_config_file.get_path().parent.mkdir(parents=True, exist_ok=True)
        my_test_dotenv_config_file.get_path().write_text(
            "KEY1=value1\nKEY2=value2\nKEY3="
        )

        # Load and verify
        loaded = my_test_dotenv_config_file.load()
        assert_with_msg(loaded["KEY1"] == "value1", "Expected KEY1=value1")
        assert_with_msg(loaded["KEY2"] == "value2", "Expected KEY2=value2")
        assert_with_msg(loaded["KEY3"] == "", "Expected KEY3 to be empty string")

    def test_dump(self, my_test_dotenv_config_file: type[DotEnvConfigFile]) -> None:
        """Test method for dump."""
        # dump should raise ValueError if config is not empty (truthy)
        with pytest.raises(ValueError, match=r"Cannot dump .* to \.env file"):
            my_test_dotenv_config_file.dump({"key": "value"})

        # dump with empty dict should NOT raise ValueError (empty dict is falsy)
        # This is the expected behavior based on the implementation
        my_test_dotenv_config_file.dump({})

    def test_get_file_extension(
        self, my_test_dotenv_config_file: type[DotEnvConfigFile]
    ) -> None:
        """Test method for get_file_extension."""
        assert_with_msg(
            my_test_dotenv_config_file.get_file_extension() == "env",
            "Expected env",
        )

    def test_get_filename(
        self, my_test_dotenv_config_file: type[DotEnvConfigFile]
    ) -> None:
        """Test method for get_filename."""
        # Should return empty string so path becomes .env not env.env
        expected = ""
        actual = my_test_dotenv_config_file.get_filename()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_get_parent_path(
        self, my_test_dotenv_config_file: type[DotEnvConfigFile]
    ) -> None:
        """Test method for get_parent_path."""
        # Should return Path() (root)
        expected = Path()
        actual = my_test_dotenv_config_file.get_parent_path()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_get_configs(
        self, my_test_dotenv_config_file: type[DotEnvConfigFile]
    ) -> None:
        """Test method for get_configs."""
        # Should return empty dict
        expected: dict[str, Any] = {}
        actual = my_test_dotenv_config_file.get_configs()
        assert_with_msg(actual == expected, f"Expected {expected}, got {actual}")

    def test_is_correct(
        self, my_test_dotenv_config_file: type[DotEnvConfigFile]
    ) -> None:
        """Test method for is_correct."""
        # Create the file
        my_test_dotenv_config_file.get_path().parent.mkdir(parents=True, exist_ok=True)
        my_test_dotenv_config_file.get_path().touch()

        # Should be correct if file exists (even if empty)
        assert_with_msg(
            my_test_dotenv_config_file.is_correct(),
            "Expected .env file to be correct when it exists",
        )

        # Remove the file
        my_test_dotenv_config_file.get_path().unlink()

        # Should still be correct because get_configs returns empty dict
        # and is_correct_recursively({}, {}) returns True (empty subset of empty)
        # The implementation: super().is_correct() or cls.get_path().exists()
        # Since get_configs() is {} and load() would be {}, they match
        assert_with_msg(
            my_test_dotenv_config_file.is_correct(),
            "Expected .env file to be correct even when doesn't exist (empty)",
        )
