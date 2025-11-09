"""module."""

from pathlib import Path

import pytest

from winipedia_utils.artifacts.build import WinipediaUtilsBuild
from winipedia_utils.utils.testing.assertions import assert_with_msg


@pytest.fixture
def my_test_winipedia_utils_build(
    tmp_path: Path,
) -> type[WinipediaUtilsBuild]:
    """Create a test winipedia_utils build class."""

    class MyTestWinipediaUtilsBuild(WinipediaUtilsBuild):
        """Test winipedia_utils build class."""

        ARTIFACTS_PATH = Path(tmp_path / str(WinipediaUtilsBuild.ARTIFACTS_PATH))

        @classmethod
        def get_artifacts(cls) -> list[Path]:
            """Build the project."""
            paths = [cls.ARTIFACTS_PATH / "build.txt"]
            for path in paths:
                path.write_text("Hello World!")
            return paths

    return MyTestWinipediaUtilsBuild


class TestWinipediaUtilsBuild:
    """Test class for WinipediaUtilsBuild."""

    def test_get_artifacts(
        self, my_test_winipedia_utils_build: type[WinipediaUtilsBuild]
    ) -> None:
        """Test method for get_artifacts."""
        with pytest.raises(FileNotFoundError):
            my_test_winipedia_utils_build.get_artifacts()

        my_winipedia_utils_build = my_test_winipedia_utils_build()
        artifacts = my_winipedia_utils_build.get_artifacts()
        assert_with_msg(
            len(artifacts) == 1,
            "Expected one artifact",
        )
