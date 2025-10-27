"""module."""

from pathlib import Path

from winipedia_utils.git.github.workflows.base.base import Workflow
from winipedia_utils.testing.assertions import assert_with_msg


class TestWorkflow:
    """Test class for Workflow."""

    def test_get_workflow_triggers(self) -> None:
        """Test method for get_workflow_triggers."""
        # Abstract method - tested in subclasses

    def test_get_permissions(self) -> None:
        """Test method for get_permissions."""
        # Abstract method - tested in subclasses

    def test_get_jobs(self) -> None:
        """Test method for get_jobs."""
        # Abstract method - tested in subclasses

    def test_get_configs(self) -> None:
        """Test method for get_configs."""
        # Abstract method - tested in subclasses

    def test_get_parent_path(self) -> None:
        """Test method for get_parent_path."""
        parent_path = Workflow.get_parent_path()
        assert_with_msg(
            parent_path == Path(".github/workflows"),
            "Expected parent path to be '.github/workflows'",
        )

    def test_get_workflow_name(self) -> None:
        """Test method for get_workflow_name."""
        workflow_name = Workflow.get_workflow_name()
        assert_with_msg(
            len(workflow_name) > 0,
            "Expected workflow name to be non-empty",
        )

    def test_get_run_name(self) -> None:
        """Test method for get_run_name."""
        run_name = Workflow.get_run_name()
        assert_with_msg(
            len(run_name) > 0,
            "Expected run name to be non-empty",
        )
        # Run name should contain workflow name
        assert_with_msg(
            Workflow.get_workflow_name() in run_name,
            "Expected run name to contain workflow name",
        )

    def test_get_checkout_step(self) -> None:
        """Test method for get_checkout_step."""
        step = Workflow.get_checkout_step()
        assert_with_msg(
            "name" in step,
            "Expected 'name' in checkout step",
        )
        assert_with_msg(
            "uses" in step,
            "Expected 'uses' in checkout step",
        )
        assert_with_msg(
            step["name"] == "Checkout repository",
            "Expected checkout step name to be 'Checkout repository'",
        )

    def test_get_checkout_step_with_fetch_depth(self) -> None:
        """Test checkout step with fetch depth."""
        step = Workflow.get_checkout_step(fetch_depth=1)
        assert_with_msg(
            "with" in step,
            "Expected 'with' in checkout step when fetch_depth is set",
        )
        assert_with_msg(
            "fetch-depth" in step["with"],
            "Expected 'fetch-depth' in step with",
        )
        assert_with_msg(
            step["with"]["fetch-depth"] == 1,
            "Expected fetch-depth to be 1",
        )

    def test_get_poetry_setup_steps(self) -> None:
        """Test method for get_poetry_setup_steps."""
        steps = Workflow.get_poetry_setup_steps()
        assert_with_msg(
            len(steps) > 0,
            "Expected at least one poetry setup step",
        )
        # Check for checkout step
        step_names = [step.get("name", "") for step in steps]
        assert_with_msg(
            "Checkout repository" in step_names,
            "Expected 'Checkout repository' step",
        )

    def test_get_poetry_setup_steps_with_dependencies(self) -> None:
        """Test poetry setup steps with install dependencies."""
        steps = Workflow.get_poetry_setup_steps(install_dependencies=True)
        step_names = [step.get("name", "") for step in steps]
        assert_with_msg(
            "Install Dependencies" in step_names,
            "Expected 'Install Dependencies' step",
        )

    def test_get_release_steps(self) -> None:
        """Test method for get_release_steps."""
        steps = Workflow.get_release_steps()
        expected_steps = 3
        assert_with_msg(
            len(steps) == expected_steps,
            f"Expected {expected_steps} release steps",
        )
        step_names = [step.get("name", "") for step in steps]
        assert_with_msg(
            isinstance(step_names, list),
            "Expected step names to be a list",
        )
        assert_with_msg(
            "Build Changelog" in step_names,
            "Expected 'Build Changelog' step",
        )
        assert_with_msg(
            "Create GitHub Release" in step_names,
            "Expected 'Create GitHub Release' step",
        )

    def test_get_publish_to_pypi_step(self) -> None:
        """Test method for get_publish_to_pypi_step."""
        step = Workflow.get_publish_to_pypi_step()
        assert_with_msg(
            "name" in step,
            "Expected 'name' in publish step",
        )
        assert_with_msg(
            "Build and publish to PyPI" in step["name"],
            "Expected 'Build and publish to PyPI' in step name",
        )

    def test_get_pre_commit_step(self) -> None:
        """Test method for get_pre_commit_step."""
        step = Workflow.get_pre_commit_step()
        assert_with_msg(
            "name" in step,
            "Expected 'name' in pre-commit step",
        )
        assert_with_msg(
            step["name"] == "Run Hooks",
            "Expected pre-commit step name to be 'Run Hooks'",
        )
        assert_with_msg(
            "pre-commit" in step.get("run", ""),
            "Expected 'pre-commit' in run command",
        )

    def test_get_extract_version_step(self) -> None:
        """Test method for get_extract_version_step."""
        step = Workflow.get_extract_version_step()
        assert_with_msg(
            "name" in step,
            "Expected 'name' in extract version step",
        )
        assert_with_msg(
            "Extract Version" in step["name"],
            "Expected 'Extract Version' in step name",
        )
        assert_with_msg(
            "id" in step,
            "Expected 'id' in extract version step",
        )

    def test_get_setup_git_step(self) -> None:
        """Test method for get_setup_git_step."""
        step = Workflow.get_setup_git_step()
        assert_with_msg(
            "name" in step,
            "Expected 'name' in setup git step",
        )

    def test_get_commit_step(self) -> None:
        """Test method for get_commit_step."""
        step = Workflow.get_commit_step()
        assert_with_msg(
            "name" in step,
            "Expected 'name' in commit step",
        )
        assert_with_msg(
            isinstance(step["name"], str),
            "Expected 'name' to be a string",
        )
        assert_with_msg(
            "git commit" in step.get("run", ""),
            "Expected 'git commit' in run command",
        )

    def test_get_protect_repository_step(self) -> None:
        """Test method for get_protect_repository_step."""
        step = Workflow.get_protect_repository_step()
        assert_with_msg(
            "name" in step,
            "Expected 'name' in protect repository step",
        )
        assert_with_msg(
            step["name"] == "Protect Repository",
            "Expected protect repository step name to be 'Protect Repository'",
        )

    def test_get_repository_name(self) -> None:
        """Test method for get_repository_name."""
        repo_name = Workflow.get_repository_name()
        assert_with_msg(
            "${{" in repo_name,
            "Expected GitHub context variable in repository name",
        )

    def test_get_ref_name(self) -> None:
        """Test method for get_ref_name."""
        ref_name = Workflow.get_ref_name()
        assert_with_msg(
            "${{" in ref_name,
            "Expected GitHub context variable in ref name",
        )

    def test_get_version(self) -> None:
        """Test method for get_version."""
        version = Workflow.get_version()
        assert_with_msg(
            "${{" in version,
            "Expected GitHub context variable in version",
        )

    def test_get_repo_and_version(self) -> None:
        """Test method for get_repo_and_version."""
        repo_and_version = Workflow.get_repo_and_version()
        # Should contain both repository name and version
        assert_with_msg(
            Workflow.get_repository_name() in repo_and_version,
            "Expected repository name in repo_and_version",
        )
        assert_with_msg(
            Workflow.get_version() in repo_and_version,
            "Expected version in repo_and_version",
        )

    def test_get_ownwer(self) -> None:
        """Test method for get_ownwer."""
        owner = Workflow.get_ownwer()
        assert_with_msg(
            "${{" in owner,
            "Expected GitHub context variable in owner",
        )

    def test_get_github_token(self) -> None:
        """Test method for get_github_token."""
        token = Workflow.get_github_token()
        assert_with_msg(
            "${{" in token,
            "Expected GitHub context variable in token",
        )
        assert_with_msg(
            "GITHUB_TOKEN" in token,
            "Expected 'GITHUB_TOKEN' in token",
        )

    def test_get_repo_token(self) -> None:
        """Test method for get_repo_token."""
        token = Workflow.get_repo_token()
        assert_with_msg(
            "${{" in token,
            "Expected GitHub context variable in token",
        )
        assert_with_msg(
            "REPO_TOKEN" in token,
            "Expected 'REPO_TOKEN' in token",
        )

    def test_get_standard_job(self) -> None:
        """Test method for get_standard_job."""
        job = Workflow.get_standard_job()
        assert_with_msg(
            len(job) > 0,
            "Expected at least one job",
        )
        # Get the job name (first key)
        job_name = next(iter(job.keys()))
        job_config = job[job_name]
        assert_with_msg(
            "runs-on" in job_config,
            "Expected 'runs-on' in job config",
        )
        assert_with_msg(
            "steps" in job_config,
            "Expected 'steps' in job config",
        )
        assert_with_msg(
            job_config["runs-on"] == "ubuntu-latest",
            "Expected 'runs-on' to be 'ubuntu-latest'",
        )

    def test_get_standard_job_with_custom_name(self) -> None:
        """Test standard job with custom name."""
        job = Workflow.get_standard_job(name="custom_job")
        assert_with_msg(
            "custom_job" in job,
            "Expected 'custom_job' in job",
        )

    def test_get_standard_job_with_steps(self) -> None:
        """Test standard job with custom steps."""
        custom_steps = [{"name": "Test Step", "run": "echo test"}]
        job = Workflow.get_standard_job(steps=custom_steps)
        job_name = next(iter(job.keys()))
        job_config = job[job_name]
        assert_with_msg(
            len(job_config["steps"]) == 1,
            "Expected 1 step in job",
        )
        assert_with_msg(
            job_config["steps"][0]["name"] == "Test Step",
            "Expected custom step in job",
        )
