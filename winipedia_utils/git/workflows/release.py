"""Contains the release workflow.

This workflow is used to create a release on GitHub.
"""

from pathlib import Path
from typing import Any

import yaml

from winipedia_utils.git.workflows.base.base import _get_poetry_setup_steps

RELEASE_WORKFLOW_PATH = Path(".github/workflows/release.yaml")


def load_release_workflow() -> dict[str, Any]:
    """Load the release workflow."""
    path = RELEASE_WORKFLOW_PATH
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    return yaml.safe_load(path.read_text()) or {}


def dump_release_workflow(config: dict[str, Any]) -> None:
    """Dump the release workflow."""
    path = RELEASE_WORKFLOW_PATH
    with path.open("w") as f:
        yaml.safe_dump(config, f, sort_keys=False)


def _get_release_config() -> dict[str, Any]:
    """Dict that represents the release workflow yaml."""
    return {
        "name": "Create Release",
        "on": {"push": {"tags": ["v*"]}},
        "jobs": {
            "release": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    *(
                        _get_poetry_setup_steps(
                            install_dependencies=True,
                            fetch_depth=0,
                        )
                    ),
                    {
                        "name": "Run Pre-commit Hooks",
                        "run": "poetry run pre-commit run --all-files",
                    },
                    {
                        "name": "Build Changelog",
                        "id": "build_changelog",
                        "uses": "mikepenz/release-changelog-builder-action@v5",
                        "with": {"token": "${{ secrets.GITHUB_TOKEN }}"},
                    },
                    {
                        "name": "Create Release",
                        "uses": "ncipollo/release-action@v1",
                        "with": {
                            "tag": "${{ github.ref_name }}",
                            "name": "${{ github.event.repository.name }}-${{ github.ref_name }}",  # noqa: E501
                            "body": "${{ steps.build_changelog.outputs.changelog }}",
                        },
                    },
                ],
            }
        },
    }


def _release_config_is_correct() -> bool:
    """Check if the release workflow is correct."""
    config = load_release_workflow()
    return bool(config == _get_release_config())


def _add_release_workflow() -> None:
    """Add the release workflow."""
    if _release_config_is_correct():
        return
    config = _get_release_config()
    dump_release_workflow(config)
