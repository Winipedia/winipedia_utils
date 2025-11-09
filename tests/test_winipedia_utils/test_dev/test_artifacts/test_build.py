"""module."""

import platform
from pathlib import Path

import pytest

from winipedia_utils.dev.artifacts.build import Build
from winipedia_utils.utils.testing.assertions import assert_with_msg


@pytest.fixture
def my_test_build(
    tmp_path: Path,
) -> type[Build]:
    """Create a test build class."""

    class MyTestBuild(Build):
        """Test build class."""

        ARTIFACTS_PATH = Path(tmp_path / str(Build.ARTIFACTS_PATH))

        @classmethod
        def get_artifacts(cls) -> list[Path]:
            """Build the project."""
            paths = [Path(cls.ARTIFACTS_PATH / "build.txt")]
            for path in paths:
                path.write_text("Hello World!")
            return paths

    return MyTestBuild


class TestBuild:
    """Test class for Build."""

    def test_get_artifacts(self, my_test_build: type[Build]) -> None:
        """Test method for get_artifacts."""
        with pytest.raises(FileNotFoundError):
            my_test_build.get_artifacts()

        my_build = my_test_build()
        artifacts = my_build.get_artifacts()
        assert_with_msg(
            len(artifacts) == 1,
            "Expected one artifact",
        )

    def test___init__(self, my_test_build: type[Build]) -> None:
        """Test method for __init__."""
        my_test_build()
        build_txt = my_test_build.ARTIFACTS_PATH / f"build-{platform.system()}.txt"
        assert_with_msg(
            build_txt.exists(),
            "Expected artifact to be built",
        )
        assert_with_msg(
            build_txt.read_text() == "Hello World!",
            "Expected correct artifact content",
        )

    def test_build(self, my_test_build: type[Build]) -> None:
        """Test method for build."""
        my_test_build.build()
        assert_with_msg(
            (my_test_build.ARTIFACTS_PATH / f"build-{platform.system()}.txt").exists(),
            "Expected artifact to be built",
        )
