"""module."""

from pathlib import Path
from typing import Any

from winipedia_utils.git.workflows.base.base import Workflow
from winipedia_utils.testing.assertions import assert_with_msg


class ConcreteWorkflow(Workflow):
    """Concrete implementation of Workflow for testing."""

    PATH = Path("test_workflow.yaml")

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with optional temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

    def get_workflow_triggers(self) -> dict[str, Any]:
        """Get the workflow triggers."""
        return {"push": {"branches": ["main"]}}

    def get_permissions(self) -> dict[str, Any]:
        """Get the workflow permissions."""
        return {"contents": "read"}

    def get_jobs(self) -> dict[str, Any]:
        """Get the workflow jobs."""
        return {"test": {"runs-on": "ubuntu-latest", "steps": []}}


class TestWorkflow:
    """Test class for Workflow."""

    def test_get_path(self, tmp_path: Path) -> None:
        """Test method for get_path."""
        workflow = ConcreteWorkflow(tmp_path)
        path = workflow.get_path()
        assert_with_msg(
            len(str(path)) > 0,
            f"Expected non-empty path, got {path}",
        )

    def test_get_standard_job(self) -> None:
        """Test method for get_standard_job."""
        steps: list[dict[str, Any]] = [{"name": "Test Step", "run": "echo test"}]
        job = Workflow.get_standard_job(name="test_job", steps=steps)
        assert_with_msg(
            len(job) > 0,
            f"Expected non-empty job dict, got {job}",
        )
        job_name = next(iter(job.keys()))
        assert_with_msg(
            "runs-on" in job[job_name],
            f"Expected 'runs-on' key in job, got {job[job_name].keys()}",
        )
        assert_with_msg(
            "steps" in job[job_name],
            f"Expected 'steps' key in job, got {job[job_name].keys()}",
        )

    def test_get_standard_job_name(self) -> None:
        """Test method for get_standard_job_name."""
        job_name = ConcreteWorkflow.get_standard_job_name()
        assert_with_msg(
            len(job_name) > 0,
            f"Expected non-empty job name, got {job_name}",
        )

    def test_get_release_steps(self) -> None:
        """Test method for get_release_steps."""
        steps = Workflow.get_release_steps()
        assert_with_msg(
            len(steps) > 0,
            f"Expected non-empty steps list, got {steps}",
        )

    def test_get_publish_to_pypi_step(self) -> None:
        """Test method for get_publish_to_pypi_step."""
        step = Workflow.get_publish_to_pypi_step()
        assert_with_msg(
            len(step) > 0,
            f"Expected non-empty step dict, got {step}",
        )
        assert_with_msg(
            "name" in step or "run" in step,
            f"Expected 'name' or 'run' key in step, got {step.keys()}",
        )

    def test_get_pre_commit_step(self) -> None:
        """Test method for get_pre_commit_step."""
        step = Workflow.get_pre_commit_step()
        assert_with_msg(
            len(step) > 0,
            f"Expected non-empty step dict, got {step}",
        )
        assert_with_msg(
            "name" in step or "run" in step,
            f"Expected 'name' or 'run' key in step, got {step.keys()}",
        )

    def test_get_workflow_triggers(self, tmp_path: Path) -> None:
        """Test method for get_workflow_triggers."""
        # This is abstract, tested via concrete implementation
        workflow = ConcreteWorkflow(tmp_path)
        triggers = workflow.get_workflow_triggers()
        assert_with_msg(
            len(triggers) > 0,
            f"Expected non-empty triggers, got {triggers}",
        )

    def test_get_permissions(self, tmp_path: Path) -> None:
        """Test method for get_permissions."""
        # This is abstract, tested via concrete implementation
        workflow = ConcreteWorkflow(tmp_path)
        permissions = workflow.get_permissions()
        assert_with_msg(
            len(permissions) > 0,
            f"Expected non-empty permissions, got {permissions}",
        )

    def test_get_jobs(self, tmp_path: Path) -> None:
        """Test method for get_jobs."""
        # This is abstract, tested via concrete implementation
        workflow = ConcreteWorkflow(tmp_path)
        jobs = workflow.get_jobs()
        assert_with_msg(
            len(jobs) > 0,
            f"Expected non-empty jobs, got {jobs}",
        )

    def test_get_workflow_name(self) -> None:
        """Test method for get_workflow_name."""
        workflow_name = ConcreteWorkflow.get_workflow_name()
        assert_with_msg(
            workflow_name == "Concrete Workflow",
            f"Expected 'Concrete Workflow', got {workflow_name}",
        )

    def test_get_run_name(self, tmp_path: Path) -> None:
        """Test method for get_run_name."""
        workflow = ConcreteWorkflow(tmp_path)
        run_name = workflow.get_run_name()
        assert_with_msg(
            "Concrete Workflow" in run_name,
            f"Expected 'Concrete Workflow' in run_name, got {run_name}",
        )

    def test_get_configs(self, tmp_path: Path) -> None:
        """Test method for get_configs."""
        workflow = ConcreteWorkflow(tmp_path)
        configs = workflow.get_configs()
        assert_with_msg(
            "name" in configs,
            f"Expected 'name' key in configs, got {configs.keys()}",
        )
        assert_with_msg(
            "on" in configs,
            f"Expected 'on' key in configs, got {configs.keys()}",
        )
        assert_with_msg(
            "permissions" in configs,
            f"Expected 'permissions' key in configs, got {configs.keys()}",
        )
        assert_with_msg(
            "run-name" in configs,
            f"Expected 'run-name' key in configs, got {configs.keys()}",
        )
        assert_with_msg(
            "jobs" in configs,
            f"Expected 'jobs' key in configs, got {configs.keys()}",
        )

    def test_get_checkout_step(self) -> None:
        """Test method for get_checkout_step."""
        step = ConcreteWorkflow.get_checkout_step()
        assert_with_msg(
            len(step) > 0,
            f"Expected non-empty step dict, got {step}",
        )
        assert_with_msg(
            "name" in step or "uses" in step,
            f"Expected 'name' or 'uses' key in step, got {step.keys()}",
        )

    def test_get_poetry_setup_steps(self) -> None:
        """Test method for get_poetry_setup_steps."""
        steps = ConcreteWorkflow.get_poetry_setup_steps()
        assert_with_msg(
            len(steps) > 0,
            f"Expected non-empty steps list, got {steps}",
        )

    def test_get_repository_name(self, tmp_path: Path) -> None:
        """Test method for get_repository_name."""
        workflow = ConcreteWorkflow(tmp_path)
        repo_name = workflow.get_repository_name()
        assert_with_msg(
            len(repo_name) > 0,
            f"Expected non-empty repo_name, got {repo_name}",
        )

    def test_get_ref_name(self, tmp_path: Path) -> None:
        """Test method for get_ref_name."""
        workflow = ConcreteWorkflow(tmp_path)
        ref_name = workflow.get_ref_name()
        assert_with_msg(
            len(ref_name) > 0,
            f"Expected non-empty ref_name, got {ref_name}",
        )

    def test_get_version(self, tmp_path: Path) -> None:
        """Test method for get_version."""
        workflow = ConcreteWorkflow(tmp_path)
        version = workflow.get_version()
        assert_with_msg(
            len(version) > 0,
            f"Expected non-empty version, got {version}",
        )

    def test_get_repo_and_version(self, tmp_path: Path) -> None:
        """Test method for get_repo_and_version."""
        workflow = ConcreteWorkflow(tmp_path)
        repo_and_version = workflow.get_repo_and_version()
        assert_with_msg(
            len(repo_and_version) > 0,
            f"Expected non-empty repo_and_version, got {repo_and_version}",
        )
