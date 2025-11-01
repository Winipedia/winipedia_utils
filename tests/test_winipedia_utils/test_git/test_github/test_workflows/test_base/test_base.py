"""module."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from winipedia_utils.git.github.workflows.base.base import Workflow
from winipedia_utils.testing.assertions import assert_with_msg


@pytest.fixture
def my_test_workflow(
    config_file_factory: Callable[[type[Workflow]], type[Workflow]],
) -> type[Workflow]:
    """Create a test workflow class with tmp_path."""

    class MyTestWorkflowClass(config_file_factory(Workflow)):  # type: ignore [misc]
        """Test workflow class with tmp_path override."""

        @classmethod
        def get_workflow_triggers(cls) -> dict[str, Any]:
            """Get the workflow triggers."""
            return {"workflow_dispatch": {}}

        @classmethod
        def get_permissions(cls) -> dict[str, Any]:
            """Get the workflow permissions."""
            return {}

        @classmethod
        def get_jobs(cls) -> dict[str, Any]:
            """Get the workflow jobs."""
            return {
                "test_job": {
                    "runs-on": "ubuntu-latest",
                    "steps": [{"name": "Test Step", "run": "echo test"}],
                }
            }

    return MyTestWorkflowClass


class TestWorkflow:
    """Test class for Workflow."""

    def test_make_id_from_func(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for make_id_from_func."""

        def job_test_function() -> None:
            pass

        result = my_test_workflow.make_id_from_func(job_test_function)
        assert_with_msg(
            result == "test_function", f"Expected 'test_function', got {result}"
        )

    def test_insert_os(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for insert_os."""
        result = my_test_workflow.insert_os()
        assert_with_msg(
            result == "${{ runner.os }}",
            f"Expected '${{{{ runner.os }}}}', got {result}",
        )

    def test_get_configs(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_configs."""
        result = my_test_workflow.get_configs()
        assert_with_msg("name" in result, "Expected 'name' in configs")
        assert_with_msg("on" in result, "Expected 'on' in configs")
        assert_with_msg("jobs" in result, "Expected 'jobs' in configs")

    def test_get_parent_path(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_parent_path."""
        result = my_test_workflow.get_parent_path()
        assert_with_msg(
            result == Path(".github/workflows"),
            f"Expected '.github/workflows', got {result}",
        )

    def test_get_jobs(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_jobs."""
        result = my_test_workflow.get_jobs()
        assert_with_msg("test_job" in result, "Expected 'test_job' in jobs")

    def test_get_workflow_triggers(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_workflow_triggers."""
        result = my_test_workflow.get_workflow_triggers()
        assert_with_msg(
            "workflow_dispatch" in result, "Expected 'workflow_dispatch' in triggers"
        )

    def test_get_permissions(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_permissions."""
        result = my_test_workflow.get_permissions()
        assert_with_msg(result == {}, f"Expected empty dict, got {result}")

    def test_get_defaults(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_defaults."""
        result = my_test_workflow.get_defaults()
        assert_with_msg("run" in result, "Expected 'run' in defaults")
        assert_with_msg(result["run"]["shell"] == "bash", "Expected shell to be 'bash'")

    def test_get_workflow_name(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_workflow_name."""
        result = my_test_workflow.get_workflow_name()
        assert_with_msg(len(result) > 0, "Expected workflow name to be non-empty")

    def test_get_run_name(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_run_name."""
        result = my_test_workflow.get_run_name()
        assert_with_msg(
            result == my_test_workflow.get_workflow_name(),
            "Expected run name to match workflow name",
        )

    def test_get_job(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_job."""

        def job_test() -> None:
            pass

        result = my_test_workflow.get_job(job_test, steps=[])
        assert_with_msg(len(result) == 1, "Expected job to have one key")

    def test_make_name_from_func(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for make_name_from_func."""

        def job_test_function() -> None:
            pass

        result = my_test_workflow.make_name_from_func(job_test_function)
        assert_with_msg(len(result) > 0, "Expected name to be non-empty")

    def test_on_workflow_dispatch(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for on_workflow_dispatch."""
        result = my_test_workflow.on_workflow_dispatch()
        assert_with_msg(
            "workflow_dispatch" in result, "Expected 'workflow_dispatch' in result"
        )

    def test_on_push(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for on_push."""
        result = my_test_workflow.on_push()
        assert_with_msg("push" in result, "Expected 'push' in result")
        assert_with_msg(
            result["push"]["branches"] == ["main"],
            "Expected default branch to be 'main'",
        )

    def test_on_schedule(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for on_schedule."""
        result = my_test_workflow.on_schedule("0 0 * * *")
        assert_with_msg("schedule" in result, "Expected 'schedule' in result")

    def test_on_pull_request(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for on_pull_request."""
        result = my_test_workflow.on_pull_request()
        assert_with_msg("pull_request" in result, "Expected 'pull_request' in result")

    def test_on_workflow_run(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for on_workflow_run."""
        result = my_test_workflow.on_workflow_run()
        assert_with_msg("workflow_run" in result, "Expected 'workflow_run' in result")

    def test_permission_content(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for permission_content."""
        result = my_test_workflow.permission_content()
        assert_with_msg("contents" in result, "Expected 'contents' in result")
        assert_with_msg(
            result["contents"] == "read", "Expected default permission to be 'read'"
        )

    def test_get_step(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_step."""

        def step_test() -> None:
            pass

        result = my_test_workflow.get_step(step_test, run="echo test")
        assert_with_msg("name" in result, "Expected 'name' in step")
        assert_with_msg("id" in result, "Expected 'id' in step")

    def test_strategy_matrix_os_and_python_version(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for strategy_matrix_os_and_python_version."""
        result = my_test_workflow.strategy_matrix_os_and_python_version()
        assert_with_msg("matrix" in result, "Expected 'matrix' in strategy")

    def test_strategy_matrix_python_version(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for strategy_matrix_python_version."""
        result = my_test_workflow.strategy_matrix_python_version()
        assert_with_msg("matrix" in result, "Expected 'matrix' in strategy")

    def test_strategy_matrix_os(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for strategy_matrix_os."""
        result = my_test_workflow.strategy_matrix_os()
        assert_with_msg("matrix" in result, "Expected 'matrix' in strategy")

    def test_strategy_matrix(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for strategy_matrix."""
        result = my_test_workflow.strategy_matrix()
        assert_with_msg("matrix" in result, "Expected 'matrix' in strategy")

    def test_get_strategy(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_strategy."""
        result = my_test_workflow.get_strategy(strategy={})
        assert_with_msg("fail-fast" in result, "Expected 'fail-fast' in strategy")

    def test_matrix_os_and_python_version(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for matrix_os_and_python_version."""
        result = my_test_workflow.matrix_os_and_python_version()
        assert_with_msg("os" in result, "Expected 'os' in matrix")
        assert_with_msg(
            "python-version" in result, "Expected 'python-version' in matrix"
        )

    def test_matrix_os(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for matrix_os."""
        result = my_test_workflow.matrix_os()
        assert_with_msg("os" in result, "Expected 'os' in matrix")

    def test_matrix_python_version(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for matrix_python_version."""
        result = my_test_workflow.matrix_python_version()
        assert_with_msg(
            "python-version" in result, "Expected 'python-version' in matrix"
        )

    def test_get_matrix(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for get_matrix."""
        result = my_test_workflow.get_matrix({"test": ["value"]})
        assert_with_msg("test" in result, "Expected 'test' in matrix")

    def test_steps_core_setup(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for steps_core_setup."""
        result = my_test_workflow.steps_core_setup()
        assert_with_msg(len(result) > 0, "Expected steps to be non-empty")

    def test_steps_core_matrix_setup(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for steps_core_matrix_setup."""
        result = my_test_workflow.steps_core_matrix_setup()
        assert_with_msg(len(result) > 0, "Expected steps to be non-empty")

    def test_step_aggregate_matrix_results(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for step_aggregate_matrix_results."""
        result = my_test_workflow.step_aggregate_matrix_results()
        assert_with_msg("name" in result, "Expected 'name' in step")
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_checkout_repository(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_checkout_repository."""
        result = my_test_workflow.step_checkout_repository()
        assert_with_msg("uses" in result, "Expected 'uses' in step")

    def test_step_setup_git(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_setup_git."""
        result = my_test_workflow.step_setup_git()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_setup_python(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_setup_python."""
        result = my_test_workflow.step_setup_python()
        assert_with_msg("uses" in result, "Expected 'uses' in step")

    def test_step_setup_poetry(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_setup_poetry."""
        result = my_test_workflow.step_setup_poetry()
        assert_with_msg("uses" in result, "Expected 'uses' in step")

    def test_step_add_poetry_to_windows_path(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for step_add_poetry_to_windows_path."""
        result = my_test_workflow.step_add_poetry_to_windows_path()
        assert_with_msg("if" in result, "Expected 'if' in step")

    def test_step_add_pypi_token_to_poetry(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for step_add_pypi_token_to_poetry."""
        result = my_test_workflow.step_add_pypi_token_to_poetry()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_publish_to_pypi(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_publish_to_pypi."""
        result = my_test_workflow.step_publish_to_pypi()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_install_python_dependencies(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for step_install_python_dependencies."""
        result = my_test_workflow.step_install_python_dependencies()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_setup_keyring(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_setup_keyring."""
        result = my_test_workflow.step_setup_keyring()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_protect_repository(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_protect_repository."""
        result = my_test_workflow.step_protect_repository()
        assert_with_msg("env" in result, "Expected 'env' in step")

    def test_step_run_pre_commit_hooks(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_run_pre_commit_hooks."""
        result = my_test_workflow.step_run_pre_commit_hooks()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_commit_added_changes(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_commit_added_changes."""
        result = my_test_workflow.step_commit_added_changes()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_push_commits(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_push_commits."""
        result = my_test_workflow.step_push_commits()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_create_and_push_tag(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_create_and_push_tag."""
        result = my_test_workflow.step_create_and_push_tag()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_create_folder(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_create_folder."""
        result = my_test_workflow.step_create_folder(folder="test")
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_create_artifacts_folder(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for step_create_artifacts_folder."""
        result = my_test_workflow.step_create_artifacts_folder()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_upload_artifacts(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_upload_artifacts."""
        result = my_test_workflow.step_upload_artifacts()
        assert_with_msg("uses" in result, "Expected 'uses' in step")

    def test_step_build_artifacts(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_build_artifacts."""
        result = my_test_workflow.step_build_artifacts()
        assert_with_msg("run" in result, "Expected 'run' in step")

    def test_step_download_artifacts(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_download_artifacts."""
        result = my_test_workflow.step_download_artifacts()
        assert_with_msg("uses" in result, "Expected 'uses' in step")

    def test_step_build_changelog(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_build_changelog."""
        result = my_test_workflow.step_build_changelog()
        assert_with_msg("uses" in result, "Expected 'uses' in step")

    def test_step_create_release(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for step_create_release."""
        result = my_test_workflow.step_create_release()
        assert_with_msg("uses" in result, "Expected 'uses' in step")

    def test_insert_repo_token(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for insert_repo_token."""
        result = my_test_workflow.insert_repo_token()
        assert_with_msg(
            result == "${{ secrets.REPO_TOKEN }}",
            f"Expected '${{{{ secrets.REPO_TOKEN }}}}', got {result}",
        )

    def test_insert_version(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for insert_version."""
        result = my_test_workflow.insert_version()
        assert_with_msg(
            "poetry version" in result, "Expected 'poetry version' in result"
        )

    def test_insert_github_token(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for insert_github_token."""
        result = my_test_workflow.insert_github_token()
        assert_with_msg(
            result == "${{ secrets.GITHUB_TOKEN }}",
            f"Expected '${{{{ secrets.GITHUB_TOKEN }}}}', got {result}",
        )

    def test_insert_repository_name(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for insert_repository_name."""
        result = my_test_workflow.insert_repository_name()
        assert_with_msg(
            "github.event.repository.name" in result,
            "Expected 'github.event.repository.name' in result",
        )

    def test_insert_ref_name(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for insert_ref_name."""
        result = my_test_workflow.insert_ref_name()
        assert_with_msg(
            "github.ref_name" in result, "Expected 'github.ref_name' in result"
        )

    def test_insert_repository_ownwer(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for insert_repository_ownwer."""
        result = my_test_workflow.insert_repository_ownwer()
        assert_with_msg(
            "github.repository_owner" in result,
            "Expected 'github.repository_owner' in result",
        )

    def test_insert_matrix_os(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for insert_matrix_os."""
        result = my_test_workflow.insert_matrix_os()
        assert_with_msg("matrix.os" in result, "Expected 'matrix.os' in result")

    def test_insert_matrix_python_version(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for insert_matrix_python_version."""
        result = my_test_workflow.insert_matrix_python_version()
        assert_with_msg(
            "matrix.python-version" in result,
            "Expected 'matrix.python-version' in result",
        )

    def test_insert_artifact_name(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for insert_artifact_name."""
        result = my_test_workflow.insert_artifact_name()
        assert_with_msg(len(result) > 0, "Expected artifact name to be non-empty")

    def test_if_matrix_is_os(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for if_matrix_is_os."""
        result = my_test_workflow.if_matrix_is_os("ubuntu-latest")
        assert_with_msg("matrix.os" in result, "Expected 'matrix.os' in result")

    def test_if_matrix_is_python_version(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for if_matrix_is_python_version."""
        result = my_test_workflow.if_matrix_is_python_version("3.11")
        assert_with_msg(
            "matrix.python-version" in result,
            "Expected 'matrix.python-version' in result",
        )

    def test_if_matrix_is_os_and_python_version(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for if_matrix_is_os_and_python_version."""
        result = my_test_workflow.if_matrix_is_os_and_python_version(
            "ubuntu-latest", "3.11"
        )
        assert_with_msg("matrix.os" in result, "Expected 'matrix.os' in result")
        assert_with_msg(
            "matrix.python-version" in result,
            "Expected 'matrix.python-version' in result",
        )

    def test_if_matrix_is_latest_python_version(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for if_matrix_is_latest_python_version."""
        result = my_test_workflow.if_matrix_is_latest_python_version()
        assert_with_msg(
            "matrix.python-version" in result,
            "Expected 'matrix.python-version' in result",
        )

    def test_if_matrix_is_os_and_latest_python_version(
        self, my_test_workflow: type[Workflow]
    ) -> None:
        """Test method for if_matrix_is_os_and_latest_python_version."""
        result = my_test_workflow.if_matrix_is_os_and_latest_python_version(
            "ubuntu-latest"
        )
        assert_with_msg("matrix.os" in result, "Expected 'matrix.os' in result")

    def test_if_build_script_exists(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for if_build_script_exists."""
        result = my_test_workflow.if_build_script_exists()
        assert_with_msg("build.py" in result, "Expected 'build.py' in result")

    def test_if_file_exists(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for if_file_exists."""
        result = my_test_workflow.if_file_exists("test.txt")
        assert_with_msg("test.txt" in result, "Expected 'test.txt' in result")

    def test_if_workflow_run_is_success(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for if_workflow_run_is_success."""
        result = my_test_workflow.if_workflow_run_is_success()
        assert_with_msg("success" in result, "Expected 'success' in result")

    def test_is_correct(self, my_test_workflow: type[Workflow]) -> None:
        """Test method for is_correct."""
        # Test that an empty file is considered correct (gets EMPTY_CONFIG)
        test_workflow = my_test_workflow()
        workflow_path = test_workflow.get_path()
        workflow_path.write_text("")
        assert_with_msg(
            test_workflow.is_correct(),
            "Expected workflow to be correct when empty",
        )

        # Test that after is_correct on empty file, it has EMPTY_CONFIG
        loaded_config = test_workflow.load()
        assert_with_msg(
            loaded_config == Workflow.EMPTY_CONFIG,
            "Expected empty workflow to have EMPTY_CONFIG after is_correct check",
        )

        # Test that a workflow with proper config is correct
        proper_config = test_workflow.get_configs()
        test_workflow.dump(proper_config)
        assert_with_msg(
            test_workflow.is_correct(),
            "Expected workflow to be correct with proper config",
        )
