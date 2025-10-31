"""Contains base utilities for git workflows."""

from abc import abstractmethod
from pathlib import Path
from typing import Any, ClassVar

import winipedia_utils
from winipedia_utils.modules.module import make_obj_importpath
from winipedia_utils.modules.package import get_src_package
from winipedia_utils.projects.poetry.config import PyprojectConfigFile
from winipedia_utils.text.config import YamlConfigFile
from winipedia_utils.text.string import split_on_uppercase


class Workflow(YamlConfigFile):
    """Base class for workflows."""

    EMPTY_CONFIG: ClassVar[dict[str, Any]] = {
        "on": {
            "workflow_dispatch": {},
        },
        "jobs": {
            "empty": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "Empty Step",
                        "run": "echo 'Empty Step'",
                    }
                ],
            },
        },
    }

    @classmethod
    def is_correct(cls) -> bool:
        """Check if the config is correct.

        Needs some special handling since workflow files cannot be empty.
        We need a workflow that will never trigger and even if doesnt do anything.
        """
        correct = super().is_correct()
        if cls.get_path().read_text() == "":
            # dump a dispatch in there for on and an empty job for jobs
            cls.dump(cls.EMPTY_CONFIG)

        return correct or cls.load() == cls.EMPTY_CONFIG

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
            "defaults": {"run": {"shell": "bash"}},
            "jobs": cls.get_jobs(),
        }

    @classmethod
    def get_standard_job(  # noqa: PLR0913
        cls,
        name: str | None = None,
        runs_on: str = "ubuntu-latest",
        strategy: dict[str, Any] | None = None,
        permissions: dict[str, Any] | None = None,
        if_condition: str | None = None,
        steps: list[dict[str, Any]] | None = None,
        needs: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get a standard job."""
        job: dict[str, Any] = {}
        if name is None:
            name = cls.get_filename()
        job[name] = {}
        job_config = job[name]

        if permissions is not None:
            job_config["permissions"] = permissions

        if strategy is not None:
            job_config["strategy"] = strategy

        job_config["runs-on"] = runs_on

        if needs is not None:
            job_config["needs"] = needs

        if if_condition is not None:
            job_config["if"] = if_condition

        if steps is None:
            steps = []
        job_config["steps"] = steps

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
    def get_checkout_step(
        cls,
        fetch_depth: int | None = None,
        *,
        token: bool = False,
    ) -> dict[str, Any]:
        """Get the checkout step.

        Args:
        fetch_depth: The fetch depth to use. If None, no fetch depth is specified.
        token: Whether to use the repository token.

        Returns:
        The checkout step.
        """
        step: dict[str, Any] = {
            "name": "Checkout repository",
            "uses": "actions/checkout@main",
        }
        if fetch_depth is not None:
            step.setdefault("with", {})["fetch-depth"] = fetch_depth

        if token:
            step.setdefault("with", {})["token"] = cls.get_repo_token()
        return step

    @classmethod
    def get_poetry_setup_steps(  # noqa: PLR0913
        cls,
        *,
        install_dependencies: bool = False,
        fetch_depth: int | None = None,
        configure_pipy_token: bool = False,
        force_main_head: bool = False,
        token: bool = False,
        with_keyring: bool = False,
        strategy_matrix: bool = False,
    ) -> list[dict[str, Any]]:
        """Get the poetry steps.

        Args:
        install_dependencies: Whether to install dependencies.
        fetch_depth: The fetch depth to use. If None, no fetch depth is specified.
        configure_pipy_token: Whether to configure the pipy token.
        force_main_head: Whether to exit if the running branch or current commit is not
            equal to the most recent commit on main. This is useful for workflows that
            should only run on main.
        token: Whether to use the repository token.
        with_keyring: Whether to setup the keyring.
        strategy_matrix: Whether to use the strategy matrix python-version.
            This is useful for jobs that use a matrix.

        Returns:
        The poetry steps.
        """
        steps = [cls.get_checkout_step(fetch_depth, token=token)]
        if force_main_head:
            # exit with code 1 if the running branch is not main
            steps.append(
                {
                    "name": "Assert running on head of main",
                    "run": 'git fetch origin main --depth=1; main_sha=$(git rev-parse origin/main); if [ "$GITHUB_SHA" != "$main_sha" ]; then echo "Tag commit is not the latest commit on main."; exit 1; fi',  # noqa: E501
                }
            )
        steps.append(cls.get_setup_git_step())
        steps.append(
            {
                "name": "Setup Python",
                "uses": "actions/setup-python@main",
                "with": {
                    # get latest if strategy matrix python-version is not set
                    "python-version": "${{ matrix.python-version }}"
                    if strategy_matrix
                    else str(PyprojectConfigFile.get_latest_possible_python_version())
                },
            }
        )
        steps.append(
            {
                "name": "Setup Poetry",
                "uses": "snok/install-poetry@main",
            }
        )

        if configure_pipy_token:
            steps.append(
                {
                    "name": "Configure Poetry with PyPI Token",
                    "run": "poetry config pypi-token.pypi ${{ secrets.PYPI_TOKEN }}",
                }
            )

        if install_dependencies:
            steps.append({"name": "Install Dependencies", "run": "poetry install"})

        if with_keyring:
            steps.append(cls.get_setup_keyring_step())

        return steps

    @classmethod
    def get_release_steps(cls) -> list[dict[str, Any]]:
        """Get the release steps."""
        return [
            cls.get_commit_step(),
            cls.get_extract_version_step(),
            {
                "name": "Tag and Push",
                "run": f"git push && git tag {cls.get_version()} && git push origin {cls.get_version()}",  # noqa: E501
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
    def get_setup_git_step(cls) -> dict[str, Any]:
        """Get the setup git step."""
        return {
            "name": "Setup Git",
            "run": 'git config --global user.email "github-actions[bot]@users.noreply.github.com" && git config --global user.name "github-actions[bot]"',  # noqa: E501
        }

    @classmethod
    def get_commit_step(cls) -> dict[str, Any]:
        """Get the commit step."""
        return {
            "name": "Commit added changes",
            "run": "git commit --no-verify -m '[skip ci] CI/CD: Committing possible added changes (e.g.: pyproject.toml and poetry.lock)'",  # noqa: E501
        }

    @classmethod
    def get_setup_keyring_step(cls) -> dict[str, Any]:
        """Get the setup keyring step."""
        return {
            "name": "Setup CI keyring",
            "run": """poetry run pip install keyrings.alt && poetry run python -c "import keyring; from keyrings.alt.file import PlaintextKeyring; keyring.set_keyring(PlaintextKeyring()); keyring.set_password('video_vault','ci_user','ci-secret-token'); print('Keyring OK:', keyring.get_password('video_vault','ci_user'))" """,  # noqa: E501
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
