from utils import add___init___files
from utils.testing.base_test import BaseTestCaseForFile


class TestAddInitFiles(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = add___init___files

    def setUp(self) -> None:
        super().setUp()

    def test_add___init___files(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_main(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)
