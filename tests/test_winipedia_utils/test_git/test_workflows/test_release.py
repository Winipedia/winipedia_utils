"""module."""

from pathlib import Path

from winipedia_utils.git.workflows.release import ReleaseWorkflow
from winipedia_utils.testing.assertions import assert_with_msg


class MyReleaseWorkflow(ReleaseWorkflow):
    """Release workflow for testing."""

    PATH = Path("release.yaml")

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()


class TestReleaseWorkflow:
    """Test class for ReleaseWorkflow."""

    def test_get_workflow_triggers(self, tmp_path: Path) -> None:
        """Test method for get_workflow_triggers."""
        workflow = MyReleaseWorkflow(tmp_path)
        triggers = workflow.get_workflow_triggers()
        assert_with_msg(
            "push" in triggers,
            f"Expected 'push' key in triggers, got {triggers.keys()}",
        )
        assert_with_msg(
            "branches" in triggers["push"],
            f"Expected 'branches' key in push trigger, got {triggers['push'].keys()}",
        )

    def test_get_permissions(self, tmp_path: Path) -> None:
        """Test method for get_permissions."""
        workflow = MyReleaseWorkflow(tmp_path)
        permissions = workflow.get_permissions()
        assert_with_msg(
            "contents" in permissions,
            f"Expected 'contents' key in permissions, got {permissions.keys()}",
        )
        assert_with_msg(
            permissions["contents"] == "write",
            f"Expected contents permission to be 'write', "
            f"got {permissions['contents']}",
        )

    def test_get_jobs(self, tmp_path: Path) -> None:
        """Test method for get_jobs."""
        workflow = MyReleaseWorkflow(tmp_path)
        jobs = workflow.get_jobs()
        assert_with_msg(
            "release" in jobs,
            f"Expected 'release' key in jobs, got {jobs.keys()}",
        )
        assert_with_msg(
            "runs-on" in jobs["release"],
            f"Expected 'runs-on' key in release job, got {jobs['release'].keys()}",
        )
        assert_with_msg(
            "steps" in jobs["release"],
            f"Expected 'steps' key in release job, got {jobs['release'].keys()}",
        )
