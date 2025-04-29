import inspect
from types import ModuleType
import os

from unittest import TestCase

from utils.mixin import ABCImplementationLoggingMixin


class BaseTestCaseForFile(TestCase, ABCImplementationLoggingMixin):
    """
    The goal of this Test Class is to enforce testing of all functions in a file
    The Subclasses will be named after the schema: class Test{FileName}(BaseTestCaseForFile)
    so multiprocess_util.py will have a test class named TestMultiprocessUtil(BaseTestCaseForFile)
    Every function in that file must be tested in that class otherwise the base tests will raise an error
    Every functions tested will be with naming convention test_{function_name}
    So func_name1 becomes test_func_name1 and _func_name2 becomes test__func_name2

    Every class in the file must have all its methods tested in the test class
    So you need test_ClassName for every class in the file and test_ClassName_method_name for every method in the class
    e.g. test_ClassName_method_name1, test_ClassName__protected_method_name2, test_ClassName___magic_method_name3__

    This base class enforces testing when writing new functions in an already tested file

    When wanting several different specific tests for a function,
    then implement them inside the test func as sub funcs and call them from the test func

    This set up allows for a clear and simple structure for the future where the tests folder mirrors
    the apps folder and each file has a test file with the same name and each folder has a test folder
    """

    __abstract__ = True

    tested_file: ModuleType = NotImplemented

    def setUp(self):
        super().setUp()

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)
        abstract = object.__getattribute__(self, "__abstract__")
        if abstract and item.startswith("test_") and callable(attr):

            def skip_abstract_class_test(*_, **__):
                """
                The base tests defined in base test classes are not meant to be executed.
                They are meant to be inherited by other test classes and executed there during testing.
                """

            return skip_abstract_class_test
        return attr

    def test_tested_file_is_correct_type(self):
        self.assertTrue(isinstance(self.tested_file, ModuleType))
        self.assertTrue(inspect.ismodule(self.tested_file))

    def test_correct_test_cls_name(self):
        module_name = self.tested_file.__name__.split(".")[-1]
        if module_name == "__main__":
            raise ValueError("The module name cannot be __main__")
        supposed_class_name = self.make_test_case_cls_name(module_name)
        actual_class_name = self.__class__.__name__
        self.assertEqual(supposed_class_name, actual_class_name)

    @staticmethod
    def make_test_case_cls_name(file_name: str) -> str:
        file_name = os.path.basename(file_name).replace(".py", "")
        # get the supposed class name, e.g. TestMultiprocessUtil from multiprocess_util.py
        supposed_class_name = f"Test_{file_name}"
        # wherever the file name has _a the name of the class should be A or _b should be B
        supposed_class_name = supposed_class_name.split("_")
        supposed_class_name = "".join([s.capitalize() for s in supposed_class_name])
        return supposed_class_name

    def test_correct_test_file_path(self):
        file_path = self.tested_file.__name__.replace(".", os.sep)
        supposed_test_file_path = self.make_test_path(file_path)

        test_file_path = self.__class__.__module__.replace(".", os.sep)
        test_file_path = os.path.join(self.make_test_folder_name(), test_file_path)

        self.assertEqual(supposed_test_file_path, test_file_path)

    @staticmethod
    def make_test_folder_name() -> str:
        return "tests"

    @staticmethod
    def make_test_path(file_path: str) -> str:
        # puts test_ in front of each path part
        test_path = os.path.join(*[f"test_{part}" for part in file_path.split(os.sep)])
        # now put it in the folder that contains tests
        test_folder_name = BaseTestCaseForFile.make_test_folder_name()
        test_path = os.path.join(test_folder_name, test_path)
        return test_path

    def test_all_functions_in_file_tested(self):
        """Ensure all user-defined functions in the file are tested."""
        # Get all user-defined functions in the file
        functions = self.get_all_functions_from_module(file=self.tested_file)

        # Get all test functions in the class
        test_functions = [f for f in dir(self) if callable(getattr(self, f))]

        # Get all functions that are not tested
        functions_not_tested = [
            self.make_test_func_name(f)
            for f in functions
            if self.make_test_func_name(f) not in test_functions
        ]

        self.assertFalse(
            functions_not_tested,
            self._get_untested_summary_error_msg(
                untested_functions=functions_not_tested
            ),
        )

    @staticmethod
    def get_all_functions_from_module(file: ModuleType) -> list:
        return [
            f
            for f, obj in inspect.getmembers(file, inspect.isfunction)
            if obj.__module__ == file.__name__  # Ensure it's from the target module
        ]

    @staticmethod
    def make_test_func_name(func_name: str) -> str:
        return f"test_{func_name}"

    def test_all_class_methods_tested(self):
        """Ensure all methods of user-defined classes in the file are tested."""
        # Get all user-defined classes in the file
        cls_methods = self.get_all_cls_and_cls_methods_from_module(
            file=self.tested_file
        )

        # Get all test functions in the class
        test_functions = [f for f in dir(self) if callable(getattr(self, f))]

        # Check methods for each class
        untested_methods = {}
        for cls, methods in cls_methods.items():
            # Check if each method is tested
            untested = [
                self.make_cls_method_test_func_name(cls, method)
                for method in methods
                if self.make_cls_method_test_func_name(cls, method)
                not in test_functions
            ]
            test_cls_func_name = self.make_cls_test_func_name(cls)
            if test_cls_func_name not in test_functions:
                untested.insert(0, test_cls_func_name)
            if untested:
                untested_methods[cls.__name__] = untested

        self.assertFalse(
            untested_methods,
            self._get_untested_summary_error_msg(untested_cls_methods=untested_methods),
        )

    @staticmethod
    def get_all_cls_and_cls_methods_from_module(file: ModuleType) -> dict:
        classes = [
            obj
            for name, obj in inspect.getmembers(file, inspect.isclass)
            if obj.__module__ == file.__name__  # Ensure it's from the target module
        ]
        cls_methods = {}
        for cls in classes:
            # Get all methods of the class
            methods = [
                name
                for name, method in inspect.getmembers(cls)
                if (
                    (
                        inspect.isfunction(method) or inspect.ismethod(method)
                    )  # Include instance, static, and class methods
                    and method.__module__
                    == file.__name__  # Ensure it's from the target module
                    and name in cls.__dict__
                )
            ]
            cls_methods[cls] = methods
        return cls_methods

    @staticmethod
    def make_cls_method_test_func_name(cls: type, method_name: str) -> str:
        return f"{BaseTestCaseForFile.make_cls_test_func_name(cls)}_{method_name}"

    @staticmethod
    def make_cls_test_func_name(cls: type) -> str:
        return f"test_{cls.__name__}"

    def _get_untested_summary_error_msg(
        self,
        untested_cls_methods: dict = None,
        untested_functions: list = None,
    ) -> str:
        if untested_cls_methods is None and untested_functions is None:
            raise ValueError(
                "Either untested_cls_methods or untested_functions must be provided."
            )

        if untested_cls_methods is None:
            untested_cls_methods = {}
        if untested_functions is None:
            untested_functions = []

        msg = f"""
        {self.__class__.__module__} is testing {self.tested_file.__name__}
        This error is raised because not all functions and methods in the file are tested.
        For more information, see the docstring of BaseTestCaseForFile in {BaseTestCaseForFile.__module__}.
        The following tests have to be implemented in {self.__class__.__module__}:
        """
        for cls, methods in untested_cls_methods.items():
            msg += f"""
            Class: {cls}
            """
            for method in methods:
                msg += f"""
                - {method}
                """

        for func in untested_functions:
            msg += f"""
            - {func}
            """

        return msg
