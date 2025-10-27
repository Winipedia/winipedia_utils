"""Contains the publish workflow.

This workflow is used to publish the package to PyPI with poetry.
"""

from typing import Any

from winipedia_utils.git.github.workflows.base.base import Workflow
from winipedia_utils.git.github.workflows.release import ReleaseWorkflow


class PublishWorkflow(Workflow):
    """Publish workflow.

    This workflow is triggered by the release workflow.
    It publishes the package to PyPI with poetry.
    """

    @classmethod
    def get_workflow_triggers(cls) -> dict[str, Any]:
        """Get the workflow triggers."""
        return {
            "workflow_run": {
                "workflows": [ReleaseWorkflow.get_workflow_name()],
                "types": ["completed"],
            },
        }

    @classmethod
    def get_permissions(cls) -> dict[str, Any]:
        """Get the workflow permissions."""
        return {
            "contents": "read",
        }

    @classmethod
    def get_jobs(cls) -> dict[str, Any]:
        """Get the workflow jobs."""
        return cls.get_standard_job(
            steps=[
                *(
                    cls.get_poetry_setup_steps(
                        configure_pipy_token=True,
                    )
                ),
                cls.get_publish_to_pypi_step(),
            ],
            if_condition="${{ github.event.workflow_run.conclusion == 'success' }}",
        )
