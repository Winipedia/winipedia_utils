from utils.testing.base_test import BaseTestCaseForFile
from utils import git


class TestGit(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = git

    def setUp(self):
        super().setUp()

    def test_path_is_in_gitignore(self):
        raise NotImplementedError("Implement this test.")

    def test_walk_os_skipping_gitignore_patterns(self):
        raise NotImplementedError("Implement this test.")
