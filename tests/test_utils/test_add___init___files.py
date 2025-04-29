from utils import add___init___files
from utils.testing.base_test import BaseTestCaseForFile


class TestAddInitFiles(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = add___init___files

    def setUp(self):
        super().setUp()

    def test_add___init___files(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_main(self) -> None:
        raise NotImplementedError("Implement this test.")
