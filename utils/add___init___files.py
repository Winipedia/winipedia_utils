import os

from utils.git import walk_os_skipping_gitignore_patterns
from utils.logging.logger import get_logger

logger = get_logger(__name__)


def add___init___files(folder: str):

    def add___init___files_for_folder(root: str, dirs: list[str], files: list[str]):

        if "__init__.py" not in files:
            with open(os.path.join(root, "__init__.py"), "w") as f:
                logger.info(f"Adding __init__.py to {root}")
                f.write("")

    walk_os_skipping_gitignore_patterns(
        folder=folder,
        root_func=add___init___files_for_folder,
    )


def main():
    add___init___files(".")
