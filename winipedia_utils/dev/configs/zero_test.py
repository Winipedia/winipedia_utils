"""Config utilities for test_zero.py."""

from winipedia_utils.dev.configs.base.base import PythonTestsConfigFile


class ZeroTestConfigFile(PythonTestsConfigFile):
    """Config file for test_zero.py."""

    @classmethod
    def get_filename(cls) -> str:
        """Get the filename of the config file."""
        filename = super().get_filename()
        return "_".join(reversed(filename.split("_")))

    @classmethod
    def get_content_str(cls) -> str:
        """Get the config."""
        return '''"""Contains an empty test."""


def test_zero() -> None:
    """Empty test.

    Exists so that when no tests are written yet the base fixtures are executed.
    """
'''
