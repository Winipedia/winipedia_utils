from utils.logging import config
from utils.testing.base_test import BaseTestCaseForFile


class TestConfig(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = config

    def setUp(self) -> None:
        super().setUp()
