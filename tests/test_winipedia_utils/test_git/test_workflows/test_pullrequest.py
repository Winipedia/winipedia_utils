"""module."""

from pathlib import Path

from winipedia_utils.git.workflows.pullrequest import PullRequestWorkflow
from winipedia_utils.testing.assertions import assert_with_msg


class MyPullRequestWorkflow(PullRequestWorkflow):
    """Pull request workflow for testing."""

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.path = tmp_path / "pullrequest.yaml"
        super().__init__()

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.path


class TestPullRequestWorkflow:
    """Test class for PullRequestWorkflow."""

    def test_get_workflow_triggers(self, tmp_path: Path) -> None:
        """Test method for get_workflow_triggers."""
        workflow = MyPullRequestWorkflow(tmp_path)
        triggers = workflow.get_workflow_triggers()
        assert_with_msg(
            "pull_request" in triggers,
            f"Expected 'pull_request' key in triggers, got {triggers.keys()}",
        )
        pr_trigger = triggers["pull_request"]
        assert_with_msg(
            "types" in pr_trigger,
            f"Expected 'types' key in pull_request, got {pr_trigger.keys()}",
        )

    def test_get_permissions(self, tmp_path: Path) -> None:
        """Test method for get_permissions."""
        workflow = MyPullRequestWorkflow(tmp_path)
        permissions = workflow.get_permissions()
        assert_with_msg(
            "contents" in permissions,
            f"Expected 'contents' key in permissions, got {permissions.keys()}",
        )
        assert_with_msg(
            permissions["contents"] == "read",
            f"Expected 'read' permission, got {permissions['contents']}",
        )

    def test_get_jobs(self, tmp_path: Path) -> None:
        """Test method for get_jobs."""
        workflow = MyPullRequestWorkflow(tmp_path)
        jobs = workflow.get_jobs()
        assert_with_msg(
            "check pull request" in jobs,
            f"Expected 'check pull request' job, got {jobs.keys()}",
        )
        assert_with_msg(
            "steps" in jobs["check pull request"],
            f"Expected 'steps' key in job, got {jobs['check pull request'].keys()}",
        )
        assert_with_msg(
            len(jobs["check pull request"]["steps"]) > 0,
            f"Expected non-empty steps, got {jobs['check pull request']['steps']}",
        )
