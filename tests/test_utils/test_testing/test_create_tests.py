from utils.testing import create_tests
from utils.testing.base_test import BaseTestCaseForFile


class TestCreateTests(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = create_tests

    def setUp(self):
        super().setUp()

    def test_create_test_file(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_create_test_files(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_main(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_path_to_test_path(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_standard_test_method_content(self) -> None:
        raise NotImplementedError("Implement this test.")
