"""Build utilities for creating and managing project builds.

This module provides functions for building and managing project artifacts,
including creating build scripts, configuring build environments, and
handling build dependencies. These utilities help with the packaging and
distribution of project code.
"""

from winipedia_utils.git.github.workflows.base.base import Workflow


def build_project() -> None:
    """Build the project."""
    # create a file with random content in BUILD_DIR
    (Workflow.ARTIFACTS_PATH / "build.txt").write_text("Hello World!")


if __name__ == "__main__":
    build_project()
