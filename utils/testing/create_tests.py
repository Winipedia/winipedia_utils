"""
This command file exists for testing. E.g. test_command_util.py
Furthermore this command takes a path as argument and generates a general test file based on it.
"""

import os
from importlib import import_module
from typing import Any

from utils.add___init___files import add___init___files
from utils.git import walk_os_skipping_gitignore_patterns
from utils.logging.logger import get_logger
from utils.testing.base_test import BaseTestCaseForFile

logger = get_logger(__name__)


def standard_test_method_content() -> str:
    return "raise NotImplementedError('Implement this test.')"


def path_to_test_path(rel_path: str) -> str:
    # adds 'test_' to the beginning of each path part
    return os.path.join(*[f"test_{part}" for part in rel_path.split(os.sep)])


def create_test_file(rel_path: str):
    # e.g. file_path: utils/mixin_util.py
    file_name = os.path.basename(rel_path)
    module_path = rel_path.replace(os.sep, ".").replace(".py", "")
    module = import_module(module_path)
    all_functions = BaseTestCaseForFile.get_all_functions_from_module(module)
    all_cls_methods = BaseTestCaseForFile.get_all_cls_and_cls_methods_from_module(
        module
    )

    # now generate the test file content
    test_file_path = BaseTestCaseForFile.make_test_path(rel_path)

    # check if file exists
    class_name = BaseTestCaseForFile.make_test_case_cls_name(file_name)
    if os.path.exists(test_file_path):
        # read content of file
        with open(test_file_path, "r") as f:
            content = f.read()
            # if content contains BaseTestCaseForFile.make_test_case_cls_name(file_name) then skip
            if class_name in content:
                logger.warning(f"Test file {test_file_path} already exists, skipping")
                return

    os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

    module_name = module_path.split(".")[-1]
    from_module = module_path.replace(f"{module_name}", "")[:-1]
    import_module_line = f"import {module_name}"
    if from_module:
        import_module_line = f"from {from_module} {import_module_line}"

    test_code = f"""{import_module_line}
from utils.testing.base_test import BaseTestCaseForFile


class {class_name}(BaseTestCaseForFile):
    __abstract__ = False
    
    tested_file = {file_name.replace(".py", "")}

    def setUp(self):
        super().setUp()
"""
    for func in all_functions:
        test_code += f"""
    def {BaseTestCaseForFile.make_test_func_name(func)}(self) -> None:
        {standard_test_method_content()}
"""
    for cls, methods in all_cls_methods.items():
        test_code += f"""
    def {BaseTestCaseForFile.make_cls_method_test_func_name(cls, "")[:-1]}(self) -> None:
        {standard_test_method_content()}
"""
        for method in methods:
            test_code += f"""
    def {BaseTestCaseForFile.make_cls_method_test_func_name(cls, method)}(self) -> None:
        {standard_test_method_content()}
"""

    with open(test_file_path, "w") as f:
        _ = f.write(test_code)
    logger.info(f"Test file generated at {test_file_path}")


def create_test_files():
    def skip_test_folder(root: str, dirs: list[str], _: list[str]):
        if root.startswith(BaseTestCaseForFile.make_test_folder_name()):
            logger.info(f"Skipping {root} because it is a test folder")
            dirs.clear()
            return False
        return True

    def create_test_file_for_file(_: str, file: str, full_path: str, root_result: Any):
        if file.endswith(".py") and not file.startswith("__"):
            if root_result:
                # only create if root_result is True, False means that the folder is skipped
                create_test_file(full_path)

    _, __ = walk_os_skipping_gitignore_patterns(
        folder=".",
        root_func=skip_test_folder,
        file_func=create_test_file_for_file,
    )

    tests_dir = BaseTestCaseForFile.make_test_folder_name()
    add___init___files(tests_dir)


def main():
    logger.info("Creating test files for all files in project")
    create_test_files()
