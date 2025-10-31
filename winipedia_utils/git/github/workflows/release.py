"""Contains the release workflow.

This workflow is used to create a release on GitHub.
"""

from typing import TYPE_CHECKING, Any

from winipedia_utils.git.github.workflows.health_check import HealthCheckWorkflow

if TYPE_CHECKING:
    from winipedia_utils.git.github.workflows.base.base import Workflow


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
        permissions = super().get_permissions()
        permissions["contents"] = "write"
        return permissions

    @classmethod
    def get_jobs(cls) -> dict[str, Any]:
        """Get the workflow jobs."""
        parent_cls: type[Workflow] = cls.__bases__[0]
        jobs = parent_cls.get_jobs()
        release_job = cls.get_standard_job(
            needs=[parent_cls.get_filename()],
            steps=[
                *cls.get_release_steps(),
            ],
        )
        jobs.update(release_job)
        return jobs
