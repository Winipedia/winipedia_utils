"""module."""

from winipedia_utils.git.github.workflows.health_check import HealthCheckWorkflow
from winipedia_utils.testing.assertions import assert_with_msg


class TestHealthCheckWorkflow:
    """Test class for HealthCheckWorkflow."""

    def test_get_workflow_triggers(self) -> None:
        """Test method for get_workflow_triggers."""
        triggers = HealthCheckWorkflow.get_workflow_triggers()
        assert_with_msg(
            "pull_request" in triggers,
            "Expected 'pull_request' in workflow triggers",
        )
        assert_with_msg(
            "schedule" in triggers,
            "Expected 'schedule' in workflow triggers",
        )
        assert_with_msg(
            "workflow_dispatch" in triggers,
            "Expected 'workflow_dispatch' in workflow triggers",
        )

    def test_get_permissions(self) -> None:
        """Test method for get_permissions."""
        permissions = HealthCheckWorkflow.get_permissions()
        # HealthCheckWorkflow has empty permissions (no special permissions needed)
        assert_with_msg(
            len(permissions) == 0,
            "Expected empty permissions dict for HealthCheckWorkflow",
        )

    def test_get_jobs(self) -> None:
        """Test method for get_jobs."""
        jobs = HealthCheckWorkflow.get_jobs()
        # HealthCheckWorkflow creates a standard job with poetry setup and
        # pre-commit steps
        assert_with_msg(
            len(jobs) > 0,
            "Expected at least one job",
        )
        # Check that the job has steps
        job_name = HealthCheckWorkflow.get_filename()
        assert_with_msg(
            job_name in jobs,
            f"Expected job '{job_name}' in jobs",
        )
        assert_with_msg(
            "steps" in jobs[job_name],
            "Expected 'steps' in job",
        )
