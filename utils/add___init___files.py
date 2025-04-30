import os

from utils.git import walk_os_skipping_gitignore_patterns
from utils.logging.logger import get_logger

logger = get_logger(__name__)


def add___init___files(folder: str) -> None:
    def add___init___files_for_folder(root: str, _dirs: list[str], files: list[str]) -> None:
        if "__init__.py" not in files:
            with open(os.path.join(root, "__init__.py"), "w") as f:
                logger.info(f"Adding __init__.py to {root}")
                _ = f.write("")

    _ = walk_os_skipping_gitignore_patterns(
        folder=folder,
        root_func=add___init___files_for_folder,
    )


def main() -> None:
    add___init___files(".")
