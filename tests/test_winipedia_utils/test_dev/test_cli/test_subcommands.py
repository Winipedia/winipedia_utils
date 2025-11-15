"""module."""

from pytest_mock import MockFixture

from winipedia_utils.dev.cli import subcommands
from winipedia_utils.utils.modules.module import make_obj_importpath


def test_create_root(mocker: MockFixture) -> None:
    """Test func for create_root."""
    mock_create_root = mocker.patch(
        make_obj_importpath(subcommands) + ".create_root_cmd"
    )

    subcommands.create_root()
    mock_create_root.assert_called_once()


def test_create_tests(mocker: MockFixture) -> None:
    """Test func for create_tests."""
    mock_create_tests = mocker.patch(
        make_obj_importpath(subcommands) + ".create_tests_cmd"
    )

    subcommands.create_tests()
    mock_create_tests.assert_called_once()


def test_setup(mocker: MockFixture) -> None:
    """Test func for setup."""
    mock_setup = mocker.patch(make_obj_importpath(subcommands) + ".setup_cmd")

    subcommands.setup()
    mock_setup.assert_called_once()
