"""Git utilities for file and directory operations.

This module provides utility functions for working with Git repositories,
including checking if paths are in .gitignore and walking directories
while respecting gitignore patterns. These utilities help with file operations
that need to respect Git's ignore rules.
"""

import fnmatch
import os
from collections.abc import Generator
from pathlib import Path

from winipedia_utils.logging.logger import get_logger

logger = get_logger(__name__)


def path_is_in_gitignore(relative_path: str | Path) -> bool:
    """Check if a path matches any pattern in the .gitignore file.

    Args:
        relative_path: The path to check, relative to the repository root

    Returns:
        True if the path matches any pattern in .gitignore, False otherwise

    Raises:
        FileNotFoundError: If the .gitignore file doesn't exist
    """
    relative_path = Path(relative_path)
    # check if the path is in the .gitignore file
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        msg = f"Gitignore file not found at {gitignore_path}"
        raise FileNotFoundError(msg)

    # Normalize the path to use forward slashes
    relative_path = relative_path.as_posix()

    with Path.open(gitignore_path) as f:
        for line in f:
            pattern = line.strip()
            if not pattern or pattern.startswith("#"):
                continue

            # Handle directory patterns (ending with /)
            if pattern.endswith("/"):
                pattern = pattern.rstrip("/")
                if relative_path.startswith(pattern):
                    return True
            # Handle regular patterns
            elif fnmatch.fnmatch(relative_path, pattern):
                return True

    return False


def walk_os_skipping_gitignore_patterns(
    folder: str | Path = ".",
) -> Generator[tuple[Path, list[str], list[str]], None, None]:
    """Walk a directory tree while skipping paths that match gitignore patterns.

    Similar to os.walk, but skips directories and files that match patterns
    in the .gitignore file.

    Args:
        folder: The root directory to start walking from

    Yields:
        Tuples of (current_path, directories, files) for each directory visited
    """
    folder = Path(folder)
    for root, dirs, files in os.walk(folder):
        rel_root = Path(root).relative_to(".")

        # skip all in patterns in .gitignore
        if path_is_in_gitignore(rel_root):
            logger.info("Skipping %s because it is in .gitignore", rel_root)
            dirs.clear()
            continue

        yield rel_root, dirs, files
