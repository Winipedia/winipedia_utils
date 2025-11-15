"""Config utilities for test_zero.py."""

from pathlib import Path

from winipedia_utils.dev import cli
from winipedia_utils.dev.configs.base.base import ConfigFile, PythonTestsConfigFile
from winipedia_utils.dev.configs.pyproject import PyprojectConfigFile
from winipedia_utils.dev.testing.convention import TESTS_PACKAGE_NAME
from winipedia_utils.utils.modules.module import to_path


class CliTestConfigFile(PythonTestsConfigFile):
    """Config file for test_zero.py."""

    @classmethod
    def get_parent_path(cls) -> Path:
        """Get the path to the config file."""
        import_path = ConfigFile.get_module_name_replacing_start_module(
            cli, PyprojectConfigFile.get_package_name()
        )
        # is now like src_pkg.dev.cli
        # we must make it like tests.test_src_pkg.test_dev.test_cli
        parts = import_path.split(".")
        test_parts = [TESTS_PACKAGE_NAME] + ["test_" + part for part in parts]
        test_path = ".".join(test_parts)
        return to_path(
            test_path,
            is_package=True,
        )

    @classmethod
    def get_filename(cls) -> str:
        """Get the filename of the config file."""
        filename = super().get_filename()
        return "_".join(reversed(filename.split("_")))

    @classmethod
    def get_content_str(cls) -> str:
        """Get the config."""
        from_os_import_run_subprocess = (
            "from winipedia_utils.utils.os.os import run_subprocess"
        )
        from_testing_import_assert_with_msg = (
            "from winipedia_utils.utils.testing.assertions import assert_with_msg"
        )
        return f'''"""Contains an simple test for cli."""

{from_os_import_run_subprocess}
{from_testing_import_assert_with_msg}


def test_main() -> None:
    """Test for the main cli entrypoint."""
    result = run_subprocess(["poetry", "run", "winipedia-utils", "--help"])
    assert_with_msg(
        result.returncode == 0,
        "Expected returncode 0",
    )
'''
