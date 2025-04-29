from utils import mixin
from utils.testing.base_test import BaseTestCaseForFile


class TestMixin(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = mixin

    def setUp(self):
        super().setUp()

    def test_ABCImplementationLoggingMeta(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_ABCImplementationLoggingMixin(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta___init__(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta__check_attrs_implemented(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta__check_implemented_attrs_types(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta__find_all_attrs_in_parent_classes_not_implemented(
        self,
    ) -> None:
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta__get_implementation_type_hints(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_ImplementationMeta_attrs_to_implement(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_LoggingMeta(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_LoggingMeta___new__(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_LoggingMeta__is_loggable_method(self) -> None:
        raise NotImplementedError("Implement this test.")

    def test_LoggingMeta__wrap_with_logging(self) -> None:
        raise NotImplementedError("Implement this test.")
