from utils.logging import logger
from utils.testing.base_test import BaseTestCaseForFile


class TestLogger(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = logger

    def setUp(self) -> None:
        super().setUp()

    def test_get_logger(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)
