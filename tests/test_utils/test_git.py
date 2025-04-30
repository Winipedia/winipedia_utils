from utils import git
from utils.testing.base_test import BaseTestCaseForFile


class TestGit(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = git

    def setUp(self) -> None:
        super().setUp()

    def test_path_is_in_gitignore(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_walk_os_skipping_gitignore_patterns(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)
