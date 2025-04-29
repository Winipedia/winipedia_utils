import run_from_root
from utils.testing.base_test import BaseTestCaseForFile


class TestRunFromRoot(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = run_from_root

    def setUp(self):
        super().setUp()
