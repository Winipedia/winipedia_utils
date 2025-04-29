from utils.testing.base_test import BaseTestCaseForFile
import run_from_root


class TestRunFromRoot(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = run_from_root

    def setUp(self):
        super().setUp()
