"""Contains base utilities for git workflows."""

from abc import abstractmethod
from pathlib import Path
from typing import Any

import winipedia_utils
from winipedia_utils.modules.module import make_obj_importpath
from winipedia_utils.modules.package import get_src_package
from winipedia_utils.text.config import YamlConfigFile
from winipedia_utils.text.string import split_on_uppercase


class Workflow(YamlConfigFile):
    """Base class for workflows."""

    @classmethod
    @abstractmethod
    def get_workflow_triggers(cls) -> dict[str, Any]:
        """Get the workflow triggers."""

    @classmethod
    @abstractmethod
    def get_permissions(cls) -> dict[str, Any]:
        """Get the workflow permissions."""

    @classmethod
    @abstractmethod
    def get_jobs(cls) -> dict[str, Any]:
        """Get the workflow jobs."""

    @classmethod
    def get_parent_path(cls) -> Path:
        """Get the path to the config file."""
        return Path(".github/workflows")

    @classmethod
    def get_configs(cls) -> dict[str, Any]:
        """Get the workflow config."""
        return {
            "name": cls.get_workflow_name(),
            "on": cls.get_workflow_triggers(),
            "permissions": cls.get_permissions(),
            "run-name": cls.get_run_name(),
            "jobs": cls.get_jobs(),
        }

    @classmethod
    def get_standard_job(
        cls,
        name: str | None = None,
        runs_on: str = "ubuntu-latest",
        permissions: dict[str, Any] | None = None,
        if_condition: str | None = None,
        steps: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Get a standard job."""
        if name is None:
            name = cls.get_filename()

        if steps is None:
            steps = []

        job: dict[str, Any] = {
            name: {
                "runs-on": runs_on,
                "steps": steps,
            }
        }
        if permissions is not None:
            job[name]["permissions"] = permissions

        if if_condition is not None:
            job[name]["if"] = if_condition
        return job

    @classmethod
    def get_workflow_name(cls) -> str:
        """Get the workflow name."""
        return " ".join(split_on_uppercase(cls.__name__))

    @classmethod
    def get_run_name(cls) -> str:
        """Get the workflow run name."""
        return f"{cls.get_workflow_name()}"

    @classmethod
    def get_checkout_step(cls, fetch_depth: int | None = None) -> dict[str, Any]:
        """Get the checkout step.

        Args:
        fetch_depth: The fetch depth to use. If None, no fetch depth is specified.

        Returns:
        The checkout step.
        """
        step: dict[str, Any] = {
            "name": "Checkout repository",
            "uses": "actions/checkout@main",
        }
        if fetch_depth is not None:
            step["with"] = {"fetch-depth": fetch_depth}
        return step

    @classmethod
    def get_poetry_setup_steps(
        cls,
        *,
        install_dependencies: bool = False,
        fetch_depth: int | None = None,
        configure_pipy_token: bool = False,
        force_main_head: bool = False,
    ) -> list[dict[str, Any]]:
        """Get the poetry steps.

        Args:
        install_dependencies: Whether to install dependencies.
        fetch_depth: The fetch depth to use. If None, no fetch depth is specified.
        configure_pipy_token: Whether to configure the pipy token.
        force_main_head: Whether to exit if the running branch or current commit is not
            equal to the most recent commit on main. This is useful for workflows that
            should only run on main.

        Returns:
        The poetry steps.
        """
        steps = [cls.get_checkout_step(fetch_depth)]
        if force_main_head:
            # exit with code 1 if the running branch is not main
            steps.append(
                {
                    "name": "Assert running on head of main",
                    "run": 'git fetch origin main --depth=1; main_sha=$(git rev-parse origin/main); if [ "$GITHUB_SHA" != "$main_sha" ]; then echo "Tag commit is not the latest commit on main."; exit 1; fi',  # noqa: E501
                }
            )
        steps.append(
            {
                "name": "Setup Python",
                "uses": "actions/setup-python@main",
                "with": {"python-version": "3.x"},
            }
        )
        steps.append(
            {
                "name": "Install Poetry",
                "run": "curl -sSL https://install.python-poetry.org | python3 -",
            }
        )
        if configure_pipy_token:
            steps.append(
                {
                    "name": "Configure Poetry",
                    "run": "poetry config pypi-token.pypi ${{ secrets.PYPI_TOKEN }}",
                }
            )
        if install_dependencies:
            steps.append({"name": "Install Dependencies", "run": "poetry install"})
        return steps

    @classmethod
    def get_release_steps(cls) -> list[dict[str, Any]]:
        """Get the release steps."""
        return [
            {
                "name": "Create and Push Tag",
                "run": f"git tag {cls.get_version()} && git push origin {cls.get_version()}",  # noqa: E501
            },
            {
                "name": "Build Changelog",
                "id": "build_changelog",
                "uses": "mikepenz/release-changelog-builder-action@develop",
                "with": {"token": cls.get_github_token()},
            },
            {
                "name": "Create GitHub Release",
                "uses": "ncipollo/release-action@main",
                "with": {
                    "tag": cls.get_version(),
                    "name": cls.get_repo_and_version(),
                    "body": "${{ steps.build_changelog.outputs.changelog }}",
                },
            },
        ]

    @classmethod
    def get_extract_version_step(cls) -> dict[str, Any]:
        """Get the extract version step."""
        return {
            "name": "Extract Version from pyproject.toml",
            "id": "version",
            "run": 'version=$(poetry version -s) && echo "Project version: $version" && echo "version=v$version" >> $GITHUB_OUTPUT',  # noqa: E501
        }

    @classmethod
    def get_publish_to_pypi_step(cls) -> dict[str, Any]:
        """Get the publish step."""
        return {"name": "Build and publish to PyPI", "run": "poetry publish --build"}

    @classmethod
    def get_pre_commit_step(cls) -> dict[str, Any]:
        """Get the pre-commit step.

        using pre commit in case other hooks are added later
        and bc it fails if files are changed,
        setup script shouldnt change files
        """
        step: dict[str, Any] = {
            "name": "Run Hooks",
            "run": "poetry run pre-commit run --all-files --verbose",
        }
        if get_src_package() == winipedia_utils:
            step["env"] = {"REPO_TOKEN": cls.get_repo_token()}
        return step

    @classmethod
    def get_commit_step(cls) -> dict[str, Any]:
        """Get the commit step."""
        return {
            "name": "Commit Changes",
            "run": "poetry run git commit --no-verify -m 'CI/CD: Committing possible changes to pyproject.toml and poetry.lock' && poetry run git push",  # noqa: E501
        }

    @classmethod
    def get_protect_repository_step(cls) -> dict[str, Any]:
        """Get the protect repository step."""
        from winipedia_utils.git.github.repo import (  # noqa: PLC0415
            protect,  # avoid circular import
        )

        return {
            "name": "Protect Repository",
            "run": f"poetry run python -m {make_obj_importpath(protect)}",
            "env": {
                "REPO_TOKEN": cls.get_repo_token(),
            },
        }

    @classmethod
    def get_repository_name(cls) -> str:
        """Get the repository name."""
        return "${{ github.event.repository.name }}"

    @classmethod
    def get_ref_name(cls) -> str:
        """Get the ref name."""
        return "${{ github.ref_name }}"

    @classmethod
    def get_version(cls) -> str:
        """Get the version."""
        return "${{ steps.version.outputs.version }}"

    @classmethod
    def get_repo_and_version(cls) -> str:
        """Get the repository name and ref name."""
        return f"{cls.get_repository_name()} {cls.get_version()}"

    @classmethod
    def get_ownwer(cls) -> str:
        """Get the repository owner."""
        return "${{ github.repository_owner }}"

    @classmethod
    def get_github_token(cls) -> str:
        """Get the GitHub token."""
        return "${{ secrets.GITHUB_TOKEN }}"

    @classmethod
    def get_repo_token(cls) -> str:
        """Get the repository token."""
        return "${{ secrets.REPO_TOKEN }}"
