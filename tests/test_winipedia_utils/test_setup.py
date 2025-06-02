"""Tests for winipedia_utils.setup module."""

from pytest_mock import MockFixture

from winipedia_utils.setup import _setup
from winipedia_utils.testing.assertions import assert_with_msg


def test__setup(mocker: MockFixture) -> None:
    """Test func for _setup."""
    # Mock all the functions that _setup calls
    mock_install_dev_deps = mocker.patch(
        "winipedia_utils.setup._install_dev_dependencies"
    )
    mock_add_hook = mocker.patch(
        "winipedia_utils.setup._add_package_hook_to_pre_commit_config"
    )
    mock_add_tool_configs = mocker.patch(
        "winipedia_utils.setup._add_configurations_to_pyproject_toml"
    )
    mock_run_hooks = mocker.patch("winipedia_utils.setup._run_all_hooks")
    mock_logger = mocker.patch("winipedia_utils.setup.logger")

    # Call the function
    _setup()

    # Verify all functions were called in the correct order
    assert_with_msg(
        mock_install_dev_deps.called,
        "Expected _install_dev_dependencies to be called",
    )

    assert_with_msg(
        mock_add_hook.called,
        "Expected _add_package_hook_to_pre_commit_config to be called",
    )

    assert_with_msg(
        mock_add_tool_configs.called,
        "Expected _add_tool_configurations_to_pyproject_toml to be called",
    )

    assert_with_msg(
        mock_run_hooks.called,
        "Expected _run_all_hooks to be called",
    )

    # Verify logger.info was called with completion message
    mock_logger.info.assert_called_once_with("Setup complete!")

    # Verify the functions were called in the expected order
    call_order = [
        mock_install_dev_deps,
        mock_add_hook,
        mock_add_tool_configs,
        mock_run_hooks,
    ]

    for i, mock_func in enumerate(call_order):
        assert_with_msg(
            mock_func.call_count == 1,
            f"Expected function {i + 1} to be called exactly once",
        )
