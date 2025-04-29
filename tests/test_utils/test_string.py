from utils.testing.base_test import BaseTestCaseForFile
from utils import string


class TestString(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = string

    def setUp(self):
        super().setUp()

    def test_ask_for_input_with_timeout(self):
        raise NotImplementedError("Implement this test.")

    def test_find_best_fit_for_text(self):
        raise NotImplementedError("Implement this test.")

    def test_find_xml_namespaces(self):
        raise NotImplementedError("Implement this test.")

    def test_get_new_unique_character_for_str(self):
        raise NotImplementedError("Implement this test.")

    def test_get_reusable_hash(self):
        raise NotImplementedError("Implement this test.")

    def test_get_variable_name(self):
        raise NotImplementedError("Implement this test.")

    def test_remove_query_params_from_url(self):
        raise NotImplementedError("Implement this test.")

    def test_to_lower_stripped_str(self):
        raise NotImplementedError("Implement this test.")

    def test_to_str_io(self):
        raise NotImplementedError("Implement this test.")

    def test_to_stripped_str(self):
        raise NotImplementedError("Implement this test.")

    def test_value_to_truncated_string(self):
        raise NotImplementedError("Implement this test.")
