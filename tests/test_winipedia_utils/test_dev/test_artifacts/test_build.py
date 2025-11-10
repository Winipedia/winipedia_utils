"""module."""

import platform
from pathlib import Path

import pytest
from pytest_mock import MockFixture

from winipedia_utils.dev.artifacts.build import Builder
from winipedia_utils.utils.testing.assertions import assert_with_msg


@pytest.fixture
def my_test_builder(
    tmp_path: Path,
) -> type[Builder]:
    """Create a test build class."""

    class MyTestBuilder(Builder):
        """Test build class."""

        ARTIFACTS_PATH = Path(tmp_path / str(Builder.ARTIFACTS_PATH))

        @classmethod
        def create_artifacts(cls) -> None:
            """Build the project."""
            paths = [Path(cls.ARTIFACTS_PATH / "build.txt")]
            for path in paths:
                path.write_text("Hello World!")

    return MyTestBuilder


class TestBuilder:
    """Test class for Build."""

    def test_create_artifacts(
        self, my_test_builder: type[Builder], mocker: MockFixture
    ) -> None:
        """Test method for get_artifacts."""
        with pytest.raises(FileNotFoundError):
            my_test_builder.create_artifacts()

        # spy on create_artifacts
        spy = mocker.spy(my_test_builder, my_test_builder.create_artifacts.__name__)

        my_build = my_test_builder()

        spy.assert_called_once()

        artifacts = my_build.get_artifacts()
        assert_with_msg(
            len(artifacts) == 1,
            f"Expected {1} artifact, got {len(artifacts)}",
        )

    def test___init__(self, my_test_builder: type[Builder]) -> None:
        """Test method for __init__."""
        my_test_builder()
        build_txt = my_test_builder.ARTIFACTS_PATH / f"build-{platform.system()}.txt"
        assert_with_msg(
            build_txt.exists(),
            "Expected artifact to be built",
        )
        assert_with_msg(
            build_txt.read_text() == "Hello World!",
            "Expected correct artifact content",
        )

    def test_build(self, my_test_builder: type[Builder]) -> None:
        """Test method for build."""
        my_test_builder.build()
        assert_with_msg(
            (
                my_test_builder.ARTIFACTS_PATH / f"build-{platform.system()}.txt"
            ).exists(),
            "Expected artifact to be built",
        )

    def test_get_artifacts(self, my_test_builder: type[Builder]) -> None:
        """Test method for get_artifacts."""
        my_test_builder.build()
        artifacts = my_test_builder.get_artifacts()
        assert_with_msg(
            len(artifacts) == 1,
            "Expected one artifact",
        )

    def test_get_non_abstract_subclasses(self) -> None:
        """Test method for get_non_abstract_builders."""
        builders = Builder.get_non_abstract_subclasses()
        assert_with_msg(
            len(builders) == 1,
            "Expected one builder",
        )

    def test_init_all_non_abstract_subclasses(
        self, my_test_builder: type[Builder], mocker: MockFixture
    ) -> None:
        """Test method for init_all_non_abstract."""
        # mock get_non_abstract_subclasses to return my_test_builder
        mocker.patch.object(
            Builder,
            Builder.get_non_abstract_subclasses.__name__,
            return_value={my_test_builder},
        )
        Builder.init_all_non_abstract_subclasses()
        artifacts = my_test_builder.get_artifacts()
        assert_with_msg(
            len(artifacts) == 1,
            "Expected one artifact",
        )
