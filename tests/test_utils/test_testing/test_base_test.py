from utils.testing.base_test import BaseTestCaseForFile
from utils.testing import base_test


class TestBaseTest(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = base_test

    def setUp(self):
        super().setUp()

    def test_BaseTestCaseForFile(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile___getattribute__(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile__get_untested_summary_error_msg(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_get_all_cls_and_cls_methods_from_module(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_get_all_functions_from_module(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_cls_method_test_func_name(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_cls_test_func_name(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_test_case_cls_name(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_test_folder_name(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_test_func_name(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_make_test_path(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_setUp(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_test_all_class_methods_tested(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_test_all_functions_in_file_tested(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_test_correct_test_cls_name(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_test_correct_test_file_path(self):
        raise NotImplementedError("Implement this test.")

    def test_BaseTestCaseForFile_test_tested_file_is_correct_type(self):
        raise NotImplementedError("Implement this test.")
