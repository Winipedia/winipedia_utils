"""module."""

import platform
from collections.abc import Callable
from pathlib import Path

import pytest

from winipedia_utils.dev.artifacts.builder.builder import WinipediaUtilsBuilder
from winipedia_utils.utils.testing.assertions import assert_with_msg


@pytest.fixture
def my_test_winipedia_utils_builder(
    builder_factory: Callable[
        [type[WinipediaUtilsBuilder]], type[WinipediaUtilsBuilder]
    ],
) -> type[WinipediaUtilsBuilder]:
    """Create a test winipedia_utils build class."""

    class MyTestWinipediaUtilsBuild(builder_factory(WinipediaUtilsBuilder)):  # type: ignore [misc]
        """Test winipedia_utils build class."""

        @classmethod
        def create_artifacts(cls, temp_artifacts_dir: Path) -> None:
            """Build the project."""
            paths = [temp_artifacts_dir / "build.txt"]
            for path in paths:
                path.write_text("Hello World!")

    return MyTestWinipediaUtilsBuild


class TestWinipediaUtilsBuilder:
    """Test class for WinipediaUtilsBuild."""

    def test_create_artifacts(
        self, my_test_winipedia_utils_builder: type[WinipediaUtilsBuilder]
    ) -> None:
        """Test method for get_artifacts."""
        my_build = my_test_winipedia_utils_builder()
        artifacts = my_build.get_artifacts()
        assert_with_msg(
            artifacts[0].name == f"build-{platform.system()}.txt",
            "Expected artifact to be built",
        )
