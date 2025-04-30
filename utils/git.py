import fnmatch
import os
from collections.abc import Callable
from typing import Any

from utils.logging.logger import get_logger

logger = get_logger(__name__)


def path_is_in_gitignore(relative_path: str) -> bool:
    # check if the path is in the .gitignore file
    gitignore_path = ".gitignore"
    if not os.path.exists(gitignore_path):
        msg = f"Gitignore file not found at {gitignore_path}"
        raise Exception(msg)

    # Normalize the path to use forward slashes
    relative_path = relative_path.replace(os.sep, "/")

    with open(gitignore_path) as f:
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
    folder: str = ".",
    root_func: Callable[[str, list[str], list[str]], Any] | None = None,
    file_func: Callable[[str, str, str, Any], Any] | None = None,
) -> tuple[list[Any], list[Any]]:
    """Walks through the folder and calls the function for each directory and file."""
    root_results: list[Any] = []
    file_results: list[Any] = []
    for root, dirs, files in os.walk(folder):
        root = os.path.relpath(root, ".")

        # skip all in patterns in .gitignore
        if path_is_in_gitignore(root):
            logger.info(f"Skipping {root} because it is in .gitignore")
            dirs.clear()
            continue

        if root_func:
            root_result = root_func(root, dirs, files)
            root_results.append(root_result)

        if file_func:
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, folder)
                if path_is_in_gitignore(relative_path):
                    continue
                file_result = file_func(root, file, relative_path, root_result)
                file_results.append(file_result)

    return root_results, file_results
