"""module."""

import platform
import random
from pathlib import Path

import PyInstaller.__main__ as pyinstaller_main
import pytest
from PIL import Image
from pytest_mock import MockFixture

from winipedia_utils.dev.artifacts.builder.base.base import Builder, PyInstallerBuilder
from winipedia_utils.utils.modules.module import make_obj_importpath
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

    def test_get_app_name(self, my_test_builder: type[Builder]) -> None:
        """Test method for get_app_name."""
        result = my_test_builder.get_app_name()
        assert_with_msg(len(result) > 0, "Expected non-empty string")

    def test_get_main_path_from_src_pkg(self, my_test_builder: type[Builder]) -> None:
        """Test method for get_main_path_from_src_pkg."""
        result = my_test_builder.get_main_path_from_src_pkg()
        assert_with_msg(result == Path("main.py"), "Expected main.py")

    def test_get_root_path(self, my_test_builder: type[Builder]) -> None:
        """Test method for get_root_path."""
        result = my_test_builder.get_root_path()
        assert_with_msg(result.exists(), "Expected path to exist")

    def test_get_src_pkg_path(self, my_test_builder: type[Builder]) -> None:
        """Test method for get_src_pkg_path."""
        result = my_test_builder.get_src_pkg_path()
        assert_with_msg(result.exists(), "Expected path to exist")

    def test_get_main_path(self, my_test_builder: type[Builder]) -> None:
        """Test method for get_main_path."""
        result = my_test_builder.get_main_path()
        assert_with_msg(result.name == "main.py", "Expected main.py")


@pytest.fixture
def my_test_pyinstaller_builder(tmp_path: Path) -> type[PyInstallerBuilder]:
    """Create a test PyInstaller builder class."""

    class MyTestPyInstallerBuilder(PyInstallerBuilder):
        """Test PyInstaller builder class."""

        ARTIFACTS_PATH = Path(tmp_path / str(Builder.ARTIFACTS_PATH))

        @classmethod
        def get_add_datas(cls) -> list[tuple[Path, Path]]:
            """Get add datas."""
            return [(Path("src"), Path("dest"))]

        @classmethod
        def get_app_icon_png_path(cls) -> Path:
            """Get the app icon path."""
            path = cls.ARTIFACTS_PATH / "icon.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            r = random.randint(0, 255)  # nosec: B311  # noqa: S311
            g = random.randint(0, 255)  # nosec: B311  # noqa: S311
            b = random.randint(0, 255)  # nosec: B311  # noqa: S311

            img = Image.new("RGB", (256, 256), (r, g, b))
            img.save(path, format="PNG")
            return Path(path)

    return MyTestPyInstallerBuilder


class TestPyInstallerBuilder:
    """Test class for PyInstallerBuilder."""

    def test_get_add_datas(
        self, my_test_pyinstaller_builder: type[PyInstallerBuilder]
    ) -> None:
        """Test method for get_add_datas."""
        result = my_test_pyinstaller_builder.get_add_datas()
        assert_with_msg(len(result) == 1, "Expected one item")

    def test_get_pyinstaller_options(
        self,
        my_test_pyinstaller_builder: type[PyInstallerBuilder],
        tmp_path: Path,
    ) -> None:
        """Test method for get_pyinstaller_options."""
        options = my_test_pyinstaller_builder.get_pyinstaller_options(tmp_path)
        assert_with_msg("--name" in options, "Expected --name option")

    def test_get_app_icon_png_path(
        self, my_test_pyinstaller_builder: type[PyInstallerBuilder]
    ) -> None:
        """Test method for get_app_icon_path."""
        result = my_test_pyinstaller_builder.get_app_icon_png_path()
        assert_with_msg(result.name == "icon.png", "Expected icon.ico")

    def test_create_artifacts(
        self,
        my_test_pyinstaller_builder: type[PyInstallerBuilder],
        mocker: MockFixture,
    ) -> None:
        """Test method for create_artifacts."""
        mock_run = mocker.patch(make_obj_importpath(pyinstaller_main) + ".run")
        my_test_pyinstaller_builder.create_artifacts()
        mock_run.assert_called_once()

    def test_convert_png_to_format(
        self,
        my_test_pyinstaller_builder: type[PyInstallerBuilder],
        tmp_path: Path,
    ) -> None:
        """Test method for convert_png_to_format."""
        result = my_test_pyinstaller_builder.convert_png_to_format("ico", tmp_path)
        assert_with_msg(result.name == "icon.ico", "Expected icon.ico")

    def test_get_app_icon_path(
        self,
        my_test_pyinstaller_builder: type[PyInstallerBuilder],
        tmp_path: Path,
    ) -> None:
        """Test method for get_app_icon_path."""
        result = my_test_pyinstaller_builder.get_app_icon_path(tmp_path)
        assert_with_msg(result.stem == "icon", "Expected icon")
