from utils.testing import run_tests
from utils.testing.base_test import BaseTestCaseForFile


class TestRunTests(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = run_tests

    def setUp(self) -> None:
        super().setUp()

    def test_main(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_run_tests(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)
