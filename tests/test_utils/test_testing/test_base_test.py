from utils.testing import base_test
from utils.testing.base_test import BaseTestCaseForFile


class TestBaseTest(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = base_test

    def setUp(self):
        super().setUp()

    def test_BaseTestCaseForFile(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile___getattribute__(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile__get_untested_summary_error_msg(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_get_all_cls_and_cls_methods_from_module(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_get_all_functions_from_module(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_cls_method_test_func_name(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_cls_test_func_name(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_test_case_cls_name(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_test_folder_name(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_test_func_name(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_test_path(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_setUp(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_test_all_class_methods_tested(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_test_all_functions_in_file_tested(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_test_correct_test_cls_name(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_test_correct_test_file_path(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_test_tested_file_is_correct_type(self) -> None:
        raise NotImplementedError("Implement this test.")
