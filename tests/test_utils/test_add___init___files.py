from utils.testing.base_test import BaseTestCaseForFile
from utils import add___init___files


class TestAddInitFiles(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = add___init___files

    def setUp(self):
        super().setUp()

    def test_add___init___files(self):
        raise NotImplementedError("Implement this test.")

    def test_main(self):
        raise NotImplementedError("Implement this test.")
