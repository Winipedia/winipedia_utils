from utils.testing.base_test import BaseTestCaseForFile
from utils.logging import config


class TestConfig(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = config

    def setUp(self):
        super().setUp()
