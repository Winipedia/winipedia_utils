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
            "name" in step,
            f"Expected 'name' key in step, got {step.keys()}",
        )
        assert_with_msg(
            step["name"] == "Checkout repository",
            f"Expected name to be 'Checkout repository', got {step['name']}",
        )
        assert_with_msg(
            "uses" in step,
            f"Expected 'uses' key in step, got {step.keys()}",
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
            "${{ github.event.repository.name }}" in repo_name,
            f"Expected github variable in repo_name, got {repo_name}",
        )

    def test_get_ref_name(self, tmp_path: Path) -> None:
        """Test method for get_ref_name."""
        workflow = ConcreteWorkflow(tmp_path)
        ref_name = workflow.get_ref_name()
        assert_with_msg(
            "${{ github.ref_name }}" in ref_name,
            f"Expected github variable in ref_name, got {ref_name}",
        )

    def test_get_version(self, tmp_path: Path) -> None:
        """Test method for get_version."""
        workflow = ConcreteWorkflow(tmp_path)
        version = workflow.get_version()
        assert_with_msg(
            "${{ steps.version.outputs.version }}" in version,
            f"Expected github variable in version, got {version}",
        )

    def test_get_repo_and_version(self, tmp_path: Path) -> None:
        """Test method for get_repo_and_version."""
        workflow = ConcreteWorkflow(tmp_path)
        repo_and_version = workflow.get_repo_and_version()
        assert_with_msg(
            "${{ github.event.repository.name }}" in repo_and_version,
            f"Expected github variable in repo_and_version, got {repo_and_version}",
        )
        assert_with_msg(
            "${{ steps.version.outputs.version }}" in repo_and_version,
            f"Expected github variable in repo_and_version, got {repo_and_version}",
        )
