"""module."""

from winipedia_utils.git.github.workflows.publish import PublishWorkflow
from winipedia_utils.git.github.workflows.release import ReleaseWorkflow
from winipedia_utils.testing.assertions import assert_with_msg


class TestPublishWorkflow:
    """Test class for PublishWorkflow."""

    def test_get_workflow_triggers(self) -> None:
        """Test method for get_workflow_triggers."""
        triggers = PublishWorkflow.get_workflow_triggers()
        assert_with_msg(
            "workflow_run" in triggers,
            "Expected 'workflow_run' in workflow triggers",
        )
        assert_with_msg(
            "workflows" in triggers["workflow_run"],
            "Expected 'workflows' in workflow_run trigger",
        )
        assert_with_msg(
            ReleaseWorkflow.get_workflow_name()
            in triggers["workflow_run"]["workflows"],
            f"Expected '{ReleaseWorkflow.get_workflow_name()}' in workflows",
        )
        assert_with_msg(
            "types" in triggers["workflow_run"],
            "Expected 'types' in workflow_run trigger",
        )
        assert_with_msg(
            "completed" in triggers["workflow_run"]["types"],
            "Expected 'completed' in types",
        )

    def test_get_permissions(self) -> None:
        """Test method for get_permissions."""
        permissions = PublishWorkflow.get_permissions()
        assert_with_msg(
            "contents" in permissions,
            "Expected 'contents' in permissions",
        )
        assert_with_msg(
            permissions["contents"] == "read",
            "Expected 'contents' permission to be 'read'",
        )

    def test_get_jobs(self) -> None:
        """Test method for get_jobs."""
        jobs = PublishWorkflow.get_jobs()
        # PublishWorkflow creates a standard job with poetry setup and publish steps
        assert_with_msg(
            len(jobs) > 0,
            "Expected at least one job",
        )
        # Check that the job has steps
        job_name = PublishWorkflow.get_filename()
        assert_with_msg(
            job_name in jobs,
            f"Expected job '{job_name}' in jobs",
        )
        assert_with_msg(
            "steps" in jobs[job_name],
            "Expected 'steps' in job",
        )
        # Check that publish steps are included
        steps = jobs[job_name]["steps"]
        step_names = [step.get("name", "") for step in steps]
        assert_with_msg(
            any("publish" in name.lower() for name in step_names),
            "Expected a step with 'publish' in the name",
        )
        # Check for if condition (should only run on success)
        assert_with_msg(
            "if" in jobs[job_name],
            "Expected 'if' condition in job",
        )
