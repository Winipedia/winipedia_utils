from utils.logging import logger
from utils.testing.base_test import BaseTestCaseForFile


class TestLogger(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = logger

    def setUp(self):
        super().setUp()

    def test_get_logger(self) -> None:
        raise NotImplementedError("Implement this test.")
