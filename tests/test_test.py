from utils.testing.base_test import BaseTestCaseForFile
import test


class TestTest(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = test

    def setUp(self):
        super().setUp()
