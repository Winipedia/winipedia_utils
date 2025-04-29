from utils.testing.base_test import BaseTestCaseForFile
from utils import mixin


class TestMixin(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = mixin

    def setUp(self):
        super().setUp()

    def test_ABCImplementationLoggingMeta(self):
        raise NotImplementedError("Implement this test.")

    def test_ABCImplementationLoggingMixin(self):
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta(self):
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta___init__(self):
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta__check_attrs_implemented(self):
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta__check_implemented_attrs_types(self):
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta__find_all_attrs_in_parent_classes_not_implemented(self):
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta__get_implementation_type_hints(self):
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta_attrs_to_implement(self):
        raise NotImplementedError("Implement this test.")

    def test_LoggingMeta(self):
        raise NotImplementedError("Implement this test.")

    def test_LoggingMeta___new__(self):
        raise NotImplementedError("Implement this test.")

    def test_LoggingMeta__is_loggable_method(self):
        raise NotImplementedError("Implement this test.")

    def test_LoggingMeta__wrap_with_logging(self):
        raise NotImplementedError("Implement this test.")
