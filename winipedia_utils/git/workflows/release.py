"""Contains the release workflow.

This workflow is used to create a release on GitHub.
"""

from pathlib import Path
from typing import Any

from winipedia_utils.git.workflows.base.base import Workflow


class ReleaseWorkflow(Workflow):
    """Release workflow."""

    PATH = Path(".github/workflows/release.yaml")

    def get_path(self) -> Path:
        """Get the path to the config file."""
        return self.PATH

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
        return {
            "release": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    *(
                        self.get_poetry_setup_steps(
                            install_dependencies=True,
                            fetch_depth=0,
                        )
                    ),
                    {
                        # using pre commit in case other hooks are added later
                        # and bc it fails if files are changed,
                        # setup script shouldnt change files
                        "name": "Run Hooks",
                        "run": "poetry run pre-commit run",
                    },
                    {
                        "name": "Create and Push Tag",
                        "run": f"git tag {self.get_version()} && git push origin {self.get_version()}",  # noqa: E501
                    },
                    {
                        "name": "Build Changelog",
                        "id": "build_changelog",
                        "uses": "mikepenz/release-changelog-builder-action@v5",
                        "with": {"token": "${{ secrets.GITHUB_TOKEN }}"},
                    },
                    {
                        "name": "Create GitHub Release",
                        "uses": "ncipollo/release-action@v1",
                        "with": {
                            "tag": self.get_version(),
                            "name": self.get_repo_and_version(),
                            "body": "${{ steps.build_changelog.outputs.changelog }}",
                        },
                    },
                ],
            }
        }
