"""module."""

import yaml
from pytest_mock import MockFixture

from winipedia_utils.git.workflows.release import (
    _add_release_workflow,
    _get_release_config,
    _release_config_is_correct,
    dump_release_workflow,
    load_release_workflow,
)
from winipedia_utils.modules.module import make_obj_importpath
from winipedia_utils.testing.assertions import assert_with_info


def test_load_release_workflow(mocker: MockFixture) -> None:
    """Test func for load_release_workflow."""
    mocker.patch("pathlib.Path.exists", return_value=True)
    fake_yaml = """
name: Test Workflow
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
"""
    mocker.patch("pathlib.Path.read_text", return_value=fake_yaml)
    result = load_release_workflow()
    expected = yaml.safe_load(fake_yaml)
    assert_with_info(
        result == expected,
        expected,
        result,
        "Expected and actual values do not match.",
    )


def test_dump_release_workflow(mocker: MockFixture) -> None:
    """Test func for dump_release_workflow."""
    expected_config = _get_release_config()

    mock_file = mocker.mock_open()
    mocker.patch("pathlib.Path.open", mock_file)

    dump_release_workflow(expected_config)

    mock_file.assert_called_once_with("w")

    written_content = "".join(call.args[0] for call in mock_file().write.call_args_list)
    dumped_config = yaml.safe_load(written_content)
    assert_with_info(
        dumped_config == expected_config,
        expected_config,
        dumped_config,
        "Expected and actual values do not match.",
    )


def test__get_release_config() -> None:
    """Test func for _get_release_config."""
    # Call the function
    result = _get_release_config()

    # just assert that dict is not empty
    expected = True
    actual = bool(result)
    assert_with_info(
        actual == expected,
        expected,
        actual,
        "Expected non-empty dict, got empty dict.",
    )


def test__release_config_is_correct(mocker: MockFixture) -> None:
    """Test func for _release_config_is_correct."""
    mocker.patch(
        make_obj_importpath(load_release_workflow),
        return_value=_get_release_config(),
    )

    result = _release_config_is_correct()
    expected = True
    assert_with_info(
        result is expected,
        expected,
        result,
        "Expected True, got False.",
    )


def test__add_release_workflow(mocker: MockFixture) -> None:
    """Test func for _add_release_workflow."""
    mock_dump_release_workflow = mocker.patch(
        make_obj_importpath(dump_release_workflow),
        return_value=None,
    )
    mock_release_config_is_correct = mocker.patch(
        make_obj_importpath(_release_config_is_correct),
        return_value=True,
    )
    _add_release_workflow()
    mock_release_config_is_correct.assert_called_once()
    mock_dump_release_workflow.assert_not_called()

    mock_release_config_is_correct.return_value = False
    _add_release_workflow()
    mock_dump_release_workflow.assert_called_once()
