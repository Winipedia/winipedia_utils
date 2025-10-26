"""Contains the publish workflow.

This workflow is used to publish the package to PyPI with poetry.
"""

from typing import Any

from winipedia_utils.git.workflows.base.base import Workflow
from winipedia_utils.git.workflows.release import ReleaseWorkflow


class PublishWorkflow(Workflow):
    """Publish workflow.

    This workflow is triggered by the release workflow.
    It publishes the package to PyPI with poetry.
    """

    def get_workflow_triggers(self) -> dict[str, Any]:
        """Get the workflow triggers."""
        return {
            "workflow_run": {
                "workflows": [ReleaseWorkflow.get_workflow_name()],
                "types": ["completed"],
            },
        }

    def get_permissions(self) -> dict[str, Any]:
        """Get the workflow permissions."""
        return {
            "contents": "read",
        }

    def get_jobs(self) -> dict[str, Any]:
        """Get the workflow jobs."""
        return self.get_standard_job(
            steps=[
                *(
                    self.get_poetry_setup_steps(
                        configure_pipy_token=True,
                    )
                ),
                self.get_publish_to_pypi_step(),
            ],
            if_condition="${{ github.event.workflow_run.conclusion == 'success' }}",
        )
