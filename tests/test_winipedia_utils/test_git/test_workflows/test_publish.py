"""module."""

import yaml
from pytest_mock import MockFixture

from winipedia_utils.git.workflows.publish import (
    _add_publish_workflow,
    _get_publish_config,
    _publish_config_is_correct,
    dump_publish_workflow,
    load_publish_workflow,
)
from winipedia_utils.modules.module import make_obj_importpath
from winipedia_utils.testing.assertions import assert_with_msg


def test_load_publish_workflow(mocker: MockFixture) -> None:
    """Test func for load_publish_workflow."""
    # mock the exist to be True
    mocker.patch("pathlib.Path.exists", return_value=True)
    # mock the read_text to return empty string
    fake_yaml_content = """
name: Test Workflow
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
"""
    mocker.patch("pathlib.Path.read_text", return_value=fake_yaml_content)

    result = load_publish_workflow()
    expected = yaml.safe_load(fake_yaml_content)
    assert_with_msg(
        result == expected,
        f"Expected {expected}, got {result}",
    )


def test_dump_publish_workflow(mocker: MockFixture) -> None:
    """Test func for dump_publish_workflow."""
    # Get the expected config
    expected_config = _get_publish_config()

    # Mock the file operations
    mock_file = mocker.mock_open()
    mocker.patch("pathlib.Path.open", mock_file)

    dump_publish_workflow(expected_config)

    # Verify the file was opened in write mode
    mock_file.assert_called_once_with("w")

    # Get what was written to the file
    written_content = "".join(call.args[0] for call in mock_file().write.call_args_list)

    # Parse the written YAML and compare
    dumped_config = yaml.safe_load(written_content)
    assert_with_msg(
        dumped_config == expected_config,
        f"Expected {expected_config}, got {dumped_config}",
    )


def test__get_publish_config() -> None:
    """Test func for _get_publish_config."""
    # Call the function
    result = _get_publish_config()

    # just assert that dict is not empty
    assert_with_msg(
        bool(result),
        f"Expected non-empty dict, got {result}",
    )


def test__publish_config_is_correct(mocker: MockFixture) -> None:
    """Test func for _publish_config_is_correct."""
    # mock the load_publish_workflow to return the correct config
    mocker.patch(
        make_obj_importpath(load_publish_workflow),
        return_value=_get_publish_config(),
    )
    result = _publish_config_is_correct()
    assert_with_msg(
        result is True,
        f"Expected True, got {result}",
    )


def test__add_publish_workflow(mocker: MockFixture) -> None:
    """Test func for _add_publish_workflow."""
    # mock _publish_config_is_correct to return True
    # mock _get_publish_config to return a dict
    # mock dump_publish_workflow to return None
    # assert dump_publish_workflow is not called
    mock_publish_config_is_correct = mocker.patch(
        make_obj_importpath(_publish_config_is_correct),
        return_value=True,
    )
    mock_dump_publish_workflow = mocker.patch(
        make_obj_importpath(dump_publish_workflow),
        return_value=None,
    )
    _add_publish_workflow()
    mock_publish_config_is_correct.assert_called_once()
    mock_dump_publish_workflow.assert_not_called()

    # mock _publish_config_is_correct to return False
    mock_publish_config_is_correct.return_value = False
    # assert _get_publish_config and dump_publish_workflow are called once
    _add_publish_workflow()
    mock_dump_publish_workflow.assert_called_once()
