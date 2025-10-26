"""module."""

from pathlib import Path

from winipedia_utils.git.workflows.publish import PublishWorkflow
from winipedia_utils.testing.assertions import assert_with_msg


class MyPublishWorkflow(PublishWorkflow):
    """Publish workflow for testing."""

    PATH = Path("publish.yaml")

    def __init__(self, tmp_path: Path) -> None:
        """Initialize with temporary path."""
        self.PATH = tmp_path / self.PATH
        super().__init__()


class TestPublishWorkflow:
    """Test class for PublishWorkflow."""

    def test_get_workflow_triggers(self, tmp_path: Path) -> None:
        """Test method for get_workflow_triggers."""
        workflow = MyPublishWorkflow(tmp_path)
        triggers = workflow.get_workflow_triggers()
        assert_with_msg(
            "workflow_run" in triggers,
            f"Expected 'workflow_run' key in triggers, got {triggers.keys()}",
        )
        assert_with_msg(
            "workflows" in triggers["workflow_run"],
            f"Expected 'workflows' key in workflow_run, "
            f"got {triggers['workflow_run'].keys()}",
        )
        assert_with_msg(
            "types" in triggers["workflow_run"],
            f"Expected 'types' key in workflow_run, "
            f"got {triggers['workflow_run'].keys()}",
        )

    def test_get_permissions(self, tmp_path: Path) -> None:
        """Test method for get_permissions."""
        workflow = MyPublishWorkflow(tmp_path)
        permissions = workflow.get_permissions()
        assert_with_msg(
            "contents" in permissions,
            f"Expected 'contents' key in permissions, got {permissions.keys()}",
        )
        assert_with_msg(
            permissions["contents"] == "read",
            f"Expected contents permission to be 'read', got {permissions['contents']}",
        )

    def test_get_jobs(self, tmp_path: Path) -> None:
        """Test method for get_jobs."""
        workflow = MyPublishWorkflow(tmp_path)
        jobs = workflow.get_jobs()
        assert_with_msg(
            "publish" in jobs,
            f"Expected 'publish' key in jobs, got {jobs.keys()}",
        )
        assert_with_msg(
            "runs-on" in jobs["publish"],
            f"Expected 'runs-on' key in publish job, got {jobs['publish'].keys()}",
        )
        assert_with_msg(
            "if" in jobs["publish"],
            f"Expected 'if' key in publish job, got {jobs['publish'].keys()}",
        )
        assert_with_msg(
            "steps" in jobs["publish"],
            f"Expected 'steps' key in publish job, got {jobs['publish'].keys()}",
        )
