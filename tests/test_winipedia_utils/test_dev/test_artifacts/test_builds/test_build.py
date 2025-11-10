"""module."""

from pathlib import Path

import pytest

from winipedia_utils.dev.artifacts.builds.build import WinipediaUtilsBuilder
from winipedia_utils.utils.testing.assertions import assert_with_msg


@pytest.fixture
def my_test_winipedia_utils_builder(
    tmp_path: Path,
) -> type[WinipediaUtilsBuilder]:
    """Create a test winipedia_utils build class."""

    class MyTestWinipediaUtilsBuild(WinipediaUtilsBuilder):
        """Test winipedia_utils build class."""

        ARTIFACTS_PATH = Path(tmp_path / str(WinipediaUtilsBuilder.ARTIFACTS_PATH))

        @classmethod
        def get_artifacts(cls) -> list[Path]:
            """Build the project."""
            paths = [cls.ARTIFACTS_PATH / "build.txt"]
            for path in paths:
                path.write_text("Hello World!")
            return paths

    return MyTestWinipediaUtilsBuild


class TestWinipediaUtilsBuilder:
    """Test class for WinipediaUtilsBuild."""

    def test_create_artifacts(
        self, my_test_winipedia_utils_builder: type[WinipediaUtilsBuilder]
    ) -> None:
        """Test method for get_artifacts."""
        with pytest.raises(FileNotFoundError):
            my_test_winipedia_utils_builder.get_artifacts()

        my_winipedia_utils_build = my_test_winipedia_utils_builder()
        artifacts = my_winipedia_utils_build.get_artifacts()
        assert_with_msg(
            len(artifacts) == 1,
            f"Expected {1} artifact, got {len(artifacts)}",
        )
