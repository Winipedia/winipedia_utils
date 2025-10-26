"""Contains the pull request workflow.

This workflow is used to run tests on pull requests.
"""

from typing import Any

from winipedia_utils.git.workflows.base.base import Workflow


class HealthCheckWorkflow(Workflow):
    """Pull request workflow.

    This workflow is triggered by a pull request.
    It runs tests on the pull request.
    """

    def get_workflow_triggers(self) -> dict[str, Any]:
        """Get the workflow triggers."""
        return {
            "pull_request": {
                "types": ["opened", "synchronize", "reopened"],
            },
            # also run once a week on main
            "schedule": [
                {
                    # run every Sunday at 2:30 am
                    "cron": "30 2 * * 0",
                },
            ],
            "workflow_dispatch": {},
        }

    def get_permissions(self) -> dict[str, Any]:
        """Get the workflow permissions."""
        return {
            "contents": "read",
        }

    def get_jobs(self) -> dict[str, Any]:
        """Get the workflow jobs."""
        return self.get_standard_job(
            "check-pull-request",
            steps=[
                *(
                    self.get_poetry_setup_steps(
                        install_dependencies=True,
                    )
                ),
                self.get_pre_commit_step(),
            ],
        )
