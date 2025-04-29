from utils.testing import run_tests
from utils.testing.base_test import BaseTestCaseForFile


class TestRunTests(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = run_tests

    def setUp(self):
        super().setUp()

    def test_main(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_run_tests(self) -> None:
        raise NotImplementedError("Implement this test.")
