from utils import git
from utils.testing.base_test import BaseTestCaseForFile


class TestGit(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = git

    def setUp(self):
        super().setUp()

    def test_path_is_in_gitignore(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_walk_os_skipping_gitignore_patterns(self) -> None:
        raise NotImplementedError("Implement this test.")
