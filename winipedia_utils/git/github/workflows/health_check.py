"""Contains the pull request workflow.

This workflow is used to run tests on pull requests.
"""

from typing import Any

from winipedia_utils.git.github.workflows.base.base import Workflow
from winipedia_utils.projects.poetry.config import PyprojectConfigFile


class HealthCheckWorkflow(Workflow):
    """Pull request workflow.

    This workflow is triggered by a pull request.
    It runs tests on the pull request.
    """

    @classmethod
    def get_workflow_triggers(cls) -> dict[str, Any]:
        """Get the workflow triggers."""
        return {
            "pull_request": {
                "types": ["opened", "synchronize", "reopened"],
            },
            "schedule": [
                {
                    # run every day at 6 am
                    "cron": "0 6 * * *",
                },
            ],
            "workflow_dispatch": {},
        }

    @classmethod
    def get_permissions(cls) -> dict[str, Any]:
        """Get the workflow permissions."""
        return {}

    @classmethod
    def get_jobs(cls) -> dict[str, Any]:
        """Get the workflow jobs."""
        matrix_job_name = f"{cls.get_filename()}_matrix"
        return {
            **cls.get_standard_job(
                name=matrix_job_name,
                runs_on="${{ matrix.os }}",
                strategy={
                    "matrix": {
                        "os": ["ubuntu-latest", "windows-latest", "macos-latest"],
                        "python-version": [
                            str(v)
                            for v in PyprojectConfigFile.get_supported_python_versions()
                        ],
                    },
                    "fail-fast": True,
                },
                steps=[
                    *(
                        cls.get_poetry_setup_steps(
                            install_dependencies=True,
                            token=True,
                            with_keyring=True,
                            strategy_matrix=True,
                        )
                    ),
                    cls.get_protect_repository_step(),
                    cls.get_pre_commit_step(),
                ],
            ),
            **cls.get_standard_job(
                needs=[matrix_job_name],
                steps=[
                    {
                        "name": "Aggregate Matrix Results",
                        "run": "echo 'Aggregating matrix results into one job.'",
                    }
                ],
            ),
        }
