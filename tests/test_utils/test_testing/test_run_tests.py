from utils.testing.base_test import BaseTestCaseForFile
from utils.testing import run_tests


class TestRunTests(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = run_tests

    def setUp(self):
        super().setUp()

    def test_main(self):
        raise NotImplementedError("Implement this test.")

    def test_run_tests(self):
        raise NotImplementedError("Implement this test.")
