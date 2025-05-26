"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_modules.test_module
"""

import os
import sys
from importlib import import_module
from pathlib import Path
from types import ModuleType

import pytest

from winipedia_utils.modules.module import (
    create_module,
    execute_all_functions_from_module,
    get_def_line,
    get_default_init_module_content,
    get_default_module_content,
    get_isolated_obj_name,
    get_module_content_as_str,
    get_module_of_obj,
    get_name_of_obj,
    get_objs_from_obj,
    import_obj_from_importpath,
    make_obj_importpath,
    to_module_name,
    to_path,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_get_module_content_as_str(tmp_path: Path) -> None:
    """Test func for get_module_content_as_str."""
    # Create a temporary module file with known content
    module_content = '''"""Test module."""

def test_function() -> str:
    """Test function."""
    return "test"

class TestClass:
    """Test class."""
    pass
'''

    # Create module file
    module_file = tmp_path / "test_module.py"
    module_file.write_text(module_content)

    # Change to tmp_path directory and add to sys.path temporarily
    original_cwd = Path.cwd()
    original_path = sys.path[:]
    os.chdir(tmp_path)
    sys.path.insert(0, str(tmp_path))

    try:
        # Import the module using importlib
        test_module = import_module("test_module")

        # Test getting module content
        result = get_module_content_as_str(test_module)
        assert_with_msg(
            result == module_content,
            f"Expected module content to match, got {result!r}",
        )

    finally:
        # Clean up
        os.chdir(original_cwd)
        sys.path[:] = original_path
        if "test_module" in sys.modules:
            del sys.modules["test_module"]


def test_to_module_name() -> None:
    """Test func for to_module_name."""
    # Test with Path objects
    path_result = to_module_name(Path("src/package/module.py"))
    assert_with_msg(
        path_result == "src.package.module",
        f"Expected 'src.package.module', got {path_result!r}",
    )

    subpackage_result = to_module_name(Path("package/subpackage"))
    assert_with_msg(
        subpackage_result == "package.subpackage",
        f"Expected 'package.subpackage', got {subpackage_result!r}",
    )

    # Test with string paths
    str_result = to_module_name("src/package/module.py")
    assert_with_msg(
        str_result == "src.package.module",
        f"Expected 'src.package.module', got {str_result!r}",
    )

    assert_with_msg(
        to_module_name("package.module") == "package.module",
        f"Expected 'package.module', got {to_module_name('package.module')!r}",
    )

    # Test edge cases
    assert_with_msg(
        to_module_name(".") == "",
        f"Expected empty string for '.', got {to_module_name('.')!r}",
    )

    assert_with_msg(
        to_module_name("./") == "",
        f"Expected empty string for './', got {to_module_name('./')!r}",
    )

    assert_with_msg(
        to_module_name("") == "",
        f"Expected empty string for empty string, got {to_module_name('')!r}",
    )

    # Test with ModuleType
    import sys

    sys_module_name = to_module_name(sys)
    assert_with_msg(
        sys_module_name == "sys", f"Expected 'sys', got {sys_module_name!r}"
    )


def test_to_path() -> None:
    """Test func for to_path."""
    # Test module name to path conversion
    result = to_path("src.package.module", is_package=False)
    expected = Path("src/package/module.py")
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Test package path conversion
    result = to_path("src.package", is_package=True)
    expected = Path("src/package")
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Test with Path input
    result = to_path(Path("src/package/module.py"), is_package=False)
    expected = Path("src/package/module.py")
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Test with ModuleType
    import sys

    result = to_path(sys, is_package=True)
    # sys module should resolve to a .py file path
    assert_with_msg(
        result.name == "sys",
        f"Expected sys module, got {result}",
    )


def test_create_module(tmp_path: Path) -> None:
    """Test func for create_module."""
    # Change to tmp_path directory and add to sys.path
    original_cwd = Path.cwd()
    original_path = sys.path[:]
    os.chdir(tmp_path)
    sys.path.insert(0, str(tmp_path))

    try:
        # Test creating a regular module
        module_name = "test_package.test_module"
        module = create_module(module_name, is_package=False)

        assert_with_msg(
            type(module) is ModuleType, f"Expected ModuleType, got {type(module)}"
        )

        assert_with_msg(
            module.__name__ == module_name,
            f"Expected module name {module_name}, got {module.__name__}",
        )

        # Check that the file was created
        expected_path = Path("test_package/test_module.py")
        assert_with_msg(
            expected_path.exists(), f"Expected module file at {expected_path} to exist"
        )

        # Check that __init__.py was created
        init_path = Path("test_package/__init__.py")
        assert_with_msg(
            init_path.exists(), f"Expected __init__.py at {init_path} to exist"
        )

        # Test creating a package
        package_name = "test_package2"
        package = create_module(package_name, is_package=True)

        assert_with_msg(
            type(package) is ModuleType, f"Expected ModuleType, got {type(package)}"
        )

        # Check that package directory was created
        package_path = Path("test_package2")
        assert_with_msg(
            package_path.is_dir(),
            f"Expected package directory at {package_path} to exist",
        )

        # Test error case - trying to create module for current directory
        with pytest.raises(ValueError, match="has an empty name"):
            create_module(".", is_package=False)

    finally:
        os.chdir(original_cwd)
        sys.path[:] = original_path
        # Clean up imported modules
        modules_to_remove = [
            name for name in sys.modules if name.startswith("test_package")
        ]
        for module_name in modules_to_remove:
            del sys.modules[module_name]


def test_make_obj_importpath() -> None:
    """Test func for make_obj_importpath."""

    # Test with a function
    def test_func() -> None:
        pass

    result = make_obj_importpath(test_func)
    expected = f"{test_func.__module__}.{test_func.__name__}"
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Test with a class
    class TestClass:
        pass

    result = make_obj_importpath(TestClass)
    expected = f"{TestClass.__module__}.{TestClass.__name__}"
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Test with a module
    import sys

    result = make_obj_importpath(sys)
    assert_with_msg(result == "sys", f"Expected 'sys', got {result}")


def test_import_obj_from_importpath() -> None:
    """Test func for import_obj_from_importpath."""
    # Test importing a module

    result = import_obj_from_importpath("sys")

    assert_with_msg(
        result.__name__ == "sys" and hasattr(result, "path"),
        f"Expected sys module, got {result}",
    )

    # Test importing a function from a module
    result = import_obj_from_importpath("os.path.join")
    import os.path

    assert_with_msg(
        result is os.path.join, f"Expected os.path.join function, got {result}"
    )

    # Test importing a class
    result = import_obj_from_importpath("pathlib.Path")
    from pathlib import Path

    assert_with_msg(result is Path, f"Expected pathlib.Path class, got {result}")

    # Test error cases
    with pytest.raises(ImportError):
        import_obj_from_importpath("nonexistent.module")

    with pytest.raises(AttributeError):
        import_obj_from_importpath("sys.nonexistent_attr")


def test_get_isolated_obj_name() -> None:
    """Test func for get_isolated_obj_name."""
    # Test with a module
    import sys

    result = get_isolated_obj_name(sys)
    assert_with_msg(result == "sys", f"Expected 'sys', got {result}")

    # Test with a nested module
    import os.path

    result = get_isolated_obj_name(os.path)
    # On Windows, os.path is ntpath; on Unix, it's posixpath
    expected_names = ["path", "ntpath", "posixpath"]
    assert_with_msg(
        result in expected_names,
        f"Expected one of {expected_names}, got {result}",
    )

    # Test with a class
    class TestClass:
        pass

    result = get_isolated_obj_name(TestClass)
    assert_with_msg(result == "TestClass", f"Expected 'TestClass', got {result}")

    # Test with a function
    def test_function() -> None:
        pass

    result = get_isolated_obj_name(test_function)
    assert_with_msg(
        result == "test_function", f"Expected 'test_function', got {result}"
    )


def test_get_objs_from_obj(tmp_path: Path) -> None:
    """Test func for get_objs_from_obj."""
    # Create a test module with functions and classes
    module_content = '''"""Test module."""

def func1() -> str:
    """Function 1."""
    return "func1"

def func2() -> str:
    """Function 2."""
    return "func2"

class TestClass1:
    """Test class 1."""

    def method1(self) -> str:
        """Method 1."""
        return "method1"

class TestClass2:
    """Test class 2."""
    pass
'''

    # Create and import the module
    module_file = tmp_path / "test_objs_module.py"
    module_file.write_text(module_content)

    # Change to tmp_path directory and add to sys.path temporarily
    original_cwd = Path.cwd()
    original_path = sys.path[:]
    os.chdir(tmp_path)
    sys.path.insert(0, str(tmp_path))

    try:
        test_objs_module = import_module("test_objs_module")

        # Test getting objects from module
        objs = get_objs_from_obj(test_objs_module)

        # Should contain 2 functions and 2 classes
        expected_function_count = 2
        expected_class_count = 2
        expected_total_objects = expected_function_count + expected_class_count
        assert_with_msg(
            len(objs) == expected_total_objects,
            f"Expected {expected_total_objects} objects "
            f"({expected_function_count} functions + {expected_class_count} classes), "
            f"got {len(objs)}",
        )

        # Test getting objects from a class
        class_objs = get_objs_from_obj(test_objs_module.TestClass1)

        # Should contain at least the method1
        method_names = [obj.__name__ for obj in class_objs]
        assert_with_msg(
            "method1" in method_names,
            f"Expected 'method1' in class methods, got {method_names}",
        )

        # Test with non-module, non-class object
        def test_func() -> None:
            pass

        result = get_objs_from_obj(test_func)
        assert_with_msg(result == [], f"Expected empty list for function, got {result}")

    finally:
        # Clean up
        os.chdir(original_cwd)
        sys.path[:] = original_path
        if "test_objs_module" in sys.modules:
            del sys.modules["test_objs_module"]


def test_execute_all_functions_from_module(tmp_path: Path) -> None:
    """Test func for execute_all_functions_from_module."""
    # Create a test module with functions that return values
    module_content = '''"""Test module."""

def func1() -> str:
    """Function 1."""
    return "result1"

def func2() -> int:
    """Function 2."""
    return 42

def func3() -> None:
    """Function 3."""
    pass
'''

    # Create and import the module
    module_file = tmp_path / "test_exec_module.py"
    module_file.write_text(module_content)

    # Change to tmp_path directory and add to sys.path temporarily
    original_cwd = Path.cwd()
    original_path = sys.path[:]
    os.chdir(tmp_path)
    sys.path.insert(0, str(tmp_path))

    try:
        test_exec_module = import_module("test_exec_module")

        # Execute all functions
        results = execute_all_functions_from_module(test_exec_module)

        # Should have 3 results
        expected_exec_results_count = 3
        assert_with_msg(
            len(results) == expected_exec_results_count,
            f"Expected {expected_exec_results_count} results, got {len(results)}",
        )

        # Check that we got the expected return values
        assert_with_msg(
            "result1" in results, f"Expected 'result1' in results, got {results}"
        )

        test_return_value = 42
        assert_with_msg(
            test_return_value in results,
            f"Expected {test_return_value} in results, got {results}",
        )

        assert_with_msg(None in results, f"Expected None in results, got {results}")

    finally:
        # Clean up
        os.chdir(original_cwd)
        sys.path[:] = original_path
        if "test_exec_module" in sys.modules:
            del sys.modules["test_exec_module"]


def test_get_default_init_module_content() -> None:
    """Test func for get_default_init_module_content."""
    result = get_default_init_module_content()
    expected = '''"""__init__ module."""'''
    assert_with_msg(result == expected, f"Expected {expected!r}, got {result!r}")


def test_get_default_module_content() -> None:
    """Test func for get_default_module_content."""
    result = get_default_module_content()
    expected = '''"""module."""'''
    assert_with_msg(result == expected, f"Expected {expected!r}, got {result!r}")


def test_get_def_line() -> None:
    """Test func for get_def_line."""

    # Test with a function defined in this module
    def test_function() -> None:
        """Test function."""

    line_num = get_def_line(test_function)
    assert_with_msg(
        line_num > 0,
        f"Expected positive integer line number, got {line_num}",
    )

    # Test with a class method
    class TestClass:
        def test_method(self) -> None:
            """Test method."""

        @property
        def test_property(self) -> str:
            """Test property."""
            return "test"

    method_line = get_def_line(TestClass.test_method)
    assert_with_msg(
        method_line > 0,
        f"Expected positive integer line number for method, got {method_line}",
    )

    # Test with a property
    prop_line = get_def_line(TestClass.test_property)
    assert_with_msg(
        prop_line > 0,
        f"Expected positive integer line number for property, got {prop_line}",
    )


def test_get_module_of_obj() -> None:
    """Test func for get_module_of_obj."""

    # Test with a function
    def test_function() -> None:
        pass

    module = get_module_of_obj(test_function)
    assert_with_msg(
        module.__name__ == __name__,
        f"Expected module name {__name__}, got {module.__name__}",
    )

    # Test with a class method
    class TestClass:
        def test_method(self) -> None:
            pass

        @property
        def test_property(self) -> str:
            return "test"

    method_module = get_module_of_obj(TestClass.test_method)
    assert_with_msg(
        method_module.__name__ == __name__,
        f"Expected module name {__name__}, got {method_module.__name__}",
    )

    # Test with a property
    prop_module = get_module_of_obj(TestClass.test_property)
    assert_with_msg(
        prop_module.__name__ == __name__,
        f"Expected module name {__name__}, got {prop_module.__name__}",
    )

    # Test with built-in function
    import os

    os_module = get_module_of_obj(os.path.join)
    assert_with_msg(
        "posixpath" in os_module.__name__ or "ntpath" in os_module.__name__,
        f"Expected posixpath or ntpath module, got {os_module.__name__}",
    )


def test_get_name_of_obj() -> None:
    """Test func for get_name_of_obj."""

    # Test with a function
    def test_function() -> None:
        pass

    name = get_name_of_obj(test_function)
    assert_with_msg(name == "test_function", f"Expected 'test_function', got {name}")

    # Test with a class
    class TestClass:
        pass

    name = get_name_of_obj(TestClass)
    assert_with_msg(name == "TestClass", f"Expected 'TestClass', got {name}")

    # Test with a method
    class TestClass2:
        def test_method(self) -> None:
            pass

    name = get_name_of_obj(TestClass2.test_method)
    assert_with_msg(name == "test_method", f"Expected 'test_method', got {name}")
