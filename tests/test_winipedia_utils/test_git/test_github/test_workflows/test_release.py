"""module."""

from winipedia_utils.git.github.workflows.release import ReleaseWorkflow
from winipedia_utils.testing.assertions import assert_with_msg


class TestReleaseWorkflow:
    """Test class for ReleaseWorkflow."""

    def test_get_workflow_triggers(self) -> None:
        """Test method for get_workflow_triggers."""
        triggers = ReleaseWorkflow.get_workflow_triggers()
        assert_with_msg(
            "push" in triggers,
            "Expected 'push' in workflow triggers",
        )
        assert_with_msg(
            "branches" in triggers["push"],
            "Expected 'branches' in push trigger",
        )
        assert_with_msg(
            "main" in triggers["push"]["branches"],
            "Expected 'main' in branches",
        )

    def test_get_permissions(self) -> None:
        """Test method for get_permissions."""
        permissions = ReleaseWorkflow.get_permissions()
        assert_with_msg(
            "contents" in permissions,
            "Expected 'contents' in permissions",
        )
        assert_with_msg(
            permissions["contents"] == "write",
            "Expected 'contents' permission to be 'write'",
        )

    def test_get_jobs(self) -> None:
        """Test method for get_jobs."""
        jobs = ReleaseWorkflow.get_jobs()
        # ReleaseWorkflow extends HealthCheckWorkflow jobs with release steps
        assert_with_msg(
            len(jobs) > 0,
            "Expected at least one job",
        )
        # Check that the job has steps
        job_name = ReleaseWorkflow.get_filename()
        assert_with_msg(
            job_name in jobs,
            f"Expected job '{job_name}' in jobs",
        )
        assert_with_msg(
            "steps" in jobs[job_name],
            "Expected 'steps' in job",
        )
        # Check that release steps are included
        steps = jobs[job_name]["steps"]
        step_names = [step.get("name", "") for step in steps]
        assert_with_msg(
            any("Tag" in name for name in step_names),
            "Expected a step with 'Tag' in the name",
        )
