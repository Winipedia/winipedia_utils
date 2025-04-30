from utils import string
from utils.testing.base_test import BaseTestCaseForFile


class TestString(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = string

    def setUp(self) -> None:
        super().setUp()

    def test_ask_for_input_with_timeout(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_find_best_fit_for_text(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_find_xml_namespaces(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_get_new_unique_character_for_str(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_get_reusable_hash(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_get_variable_name(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_remove_query_params_from_url(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_to_lower_stripped_str(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_to_str_io(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_to_stripped_str(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_value_to_truncated_string(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)
