"""Contains base utilities for git workflows."""

from abc import abstractmethod
from pathlib import Path
from typing import Any

from winipedia_utils.text.config import YamlConfigFile
from winipedia_utils.text.string import split_on_uppercase


class Workflow(YamlConfigFile):
    """Base class for workflows."""

    @abstractmethod
    def get_workflow_triggers(self) -> dict[str, Any]:
        """Get the workflow triggers."""

    @abstractmethod
    def get_permissions(self) -> dict[str, Any]:
        """Get the workflow permissions."""

    @abstractmethod
    def get_jobs(self) -> dict[str, Any]:
        """Get the workflow jobs."""

    def get_path(self) -> Path:
        """Get the path to the config file."""
        file_name = (
            "_".join(
                split_on_uppercase(
                    self.__class__.__name__.removesuffix(Workflow.__name__)
                )
            ).lower()
            + ".yaml"
        )
        return Path(".github/workflows") / file_name

    @staticmethod
    def get_standard_job(
        name: str,
        steps: list[dict[str, Any]],
        permissions: dict[str, Any] | None = None,
        if_condition: str | None = None,
    ) -> dict[str, Any]:
        """Get a standard job."""
        job: dict[str, Any] = {
            name: {
                "runs-on": "ubuntu-latest",
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

    def get_run_name(self) -> str:
        """Get the workflow run name."""
        return f"{self.get_workflow_name()}"

    def get_configs(self) -> dict[str, Any]:
        """Get the workflow config."""
        return {
            "name": self.get_workflow_name(),
            "on": self.get_workflow_triggers(),
            "permissions": self.get_permissions(),
            "run-name": self.get_run_name(),
            "jobs": self.get_jobs(),
        }

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
        steps.append(
            {
                "name": "Extract Version from pyproject.toml",
                "id": "version",
                "run": 'version=$(poetry version -s) && echo "Project version: $version" && echo "version=v$version" >> $GITHUB_OUTPUT',  # noqa: E501
            },
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

    @staticmethod
    def get_release_steps() -> list[dict[str, Any]]:
        """Get the release steps."""
        return [
            {
                "name": "Create and Push Tag",
                "run": f"git tag {Workflow.get_version()} && git push origin {Workflow.get_version()}",  # noqa: E501
            },
            {
                "name": "Build Changelog",
                "id": "build_changelog",
                "uses": "mikepenz/release-changelog-builder-action@develop",
                "with": {"token": "${{ secrets.GITHUB_TOKEN }}"},
            },
            {
                "name": "Create GitHub Release",
                "uses": "ncipollo/release-action@main",
                "with": {
                    "tag": Workflow.get_version(),
                    "name": Workflow.get_repo_and_version(),
                    "body": "${{ steps.build_changelog.outputs.changelog }}",
                },
            },
        ]

    @staticmethod
    def get_publish_to_pypi_step() -> dict[str, Any]:
        """Get the publish step."""
        return {"name": "Build and publish to PyPI", "run": "poetry publish --build"}

    @staticmethod
    def get_pre_commit_step() -> dict[str, Any]:
        """Get the pre-commit step.

        using pre commit in case other hooks are added later
        and bc it fails if files are changed,
        setup script shouldnt change files
        """
        return {
            "name": "Run Hooks",
            "run": "poetry run pre-commit run --all-files --verbose",
        }

    @staticmethod
    def get_repository_name() -> str:
        """Get the repository name."""
        return "${{ github.event.repository.name }}"

    @staticmethod
    def get_ref_name() -> str:
        """Get the ref name."""
        return "${{ github.ref_name }}"

    @classmethod
    def get_version(cls) -> str:
        """Get the version."""
        return "${{ steps.version.outputs.version }}"

    @staticmethod
    def get_repo_and_version() -> str:
        """Get the repository name and ref name."""
        return f"{Workflow.get_repository_name()} {Workflow.get_version()}"
