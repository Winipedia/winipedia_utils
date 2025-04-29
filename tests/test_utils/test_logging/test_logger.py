from utils.testing.base_test import BaseTestCaseForFile
from utils.logging import logger


class TestLogger(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = logger

    def setUp(self):
        super().setUp()

    def test_get_logger(self):
        raise NotImplementedError("Implement this test.")
