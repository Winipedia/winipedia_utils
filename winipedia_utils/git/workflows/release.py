"""Contains the release workflow.

This workflow is used to create a release on GitHub.
"""

from typing import Any

from winipedia_utils.git.workflows.health_check import HealthCheckWorkflow


class ReleaseWorkflow(HealthCheckWorkflow):
    """Release workflow.

    This workflow is triggered by a push to the main branch.
    It creates a tag for the release and builds a changelog.
    With tag and changelog it creates a release on GitHub
    """

    def get_workflow_triggers(self) -> dict[str, Any]:
        """Get the workflow triggers."""
        return {"push": {"branches": ["main"]}}

    def get_permissions(self) -> dict[str, Any]:
        """Get the workflow permissions."""
        return {
            "contents": "write",
        }

    def get_jobs(self) -> dict[str, Any]:
        """Get the workflow jobs."""
        steps = super().get_jobs()
        steps[self.get_standard_job_name()]["steps"].extend(self.get_release_steps())
        return steps
