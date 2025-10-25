"""Contains the publish workflow.

This workflow is used to publish the package to PyPI with poetry.
"""

from pathlib import Path
from typing import Any

from winipedia_utils.git.workflows.base.base import Workflow
from winipedia_utils.git.workflows.release import ReleaseWorkflow


class PublishWorkflow(Workflow):
    """Publish workflow."""

    PATH = Path(".github/workflows/publish.yaml")

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

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
        return {
            "publish": {
                "runs-on": "ubuntu-latest",
                "if": "${{ github.event.workflow_run.conclusion == 'success' }}",
                "steps": [
                    *(
                        self.get_poetry_setup_steps(
                            configure_pipy_token=True,
                        )
                    ),
                    {
                        "name": "Build and publish to PyPI",
                        "run": "poetry publish --build",
                    },
                ],
            }
        }
