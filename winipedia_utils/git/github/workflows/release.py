"""Contains the release workflow.

This workflow is used to create a release on GitHub.
"""

from typing import Any

from winipedia_utils.git.github.workflows.health_check import HealthCheckWorkflow


class ReleaseWorkflow(HealthCheckWorkflow):
    """Release workflow.

    This workflow is triggered by a push to the main branch.
    It creates a tag for the release and builds a changelog.
    With tag and changelog it creates a release on GitHub
    """

    @classmethod
    def get_workflow_triggers(cls) -> dict[str, Any]:
        """Get the workflow triggers."""
        return {
            "push": {"branches": ["main"]},
            "workflow_dispatch": {},
            "schedule": [
                {
                    # run every Tuesday at 6 am
                    "cron": "0 6 * * 2",
                },
            ],
        }

    @classmethod
    def get_permissions(cls) -> dict[str, Any]:
        """Get the workflow permissions."""
        return {
            "contents": "write",
        }

    @classmethod
    def get_jobs(cls) -> dict[str, Any]:
        """Get the workflow jobs."""
        steps = super().get_jobs()
        steps[cls.get_filename()]["steps"].extend(cls.get_release_steps())
        return steps
