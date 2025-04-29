from utils.testing.base_test import BaseTestCaseForFile
from utils.testing import create_tests


class TestCreateTests(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = create_tests

    def setUp(self):
        super().setUp()

    def test_create_test_file(self):
        raise NotImplementedError("Implement this test.")

    def test_create_test_files(self):
        raise NotImplementedError("Implement this test.")

    def test_main(self):
        raise NotImplementedError("Implement this test.")

    def test_path_to_test_path(self):
        raise NotImplementedError("Implement this test.")

    def test_standard_test_method_content(self):
        raise NotImplementedError("Implement this test.")
