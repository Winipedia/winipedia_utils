"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_modules.test_package
"""

from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
from pytest_mock import MockFixture

from winipedia_utils.modules.package import (
    copy_package,
    find_packages,
    find_packages_as_modules,
    get_modules_and_packages_from_package,
    get_src_package,
    make_dir_with_init_file,
    make_init_module,
    make_init_modules_for_package,
    module_is_package,
    package_name_to_path,
    walk_package,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_get_src_package(mocker: MockFixture) -> None:
    """Test func for get_src_package."""
    # Mock the find_packages_as_modules function
    mock_package1 = mocker.MagicMock(spec=ModuleType)
    mock_package1.__name__ = "winipedia_utils"
    mock_package2 = mocker.MagicMock(spec=ModuleType)
    mock_package2.__name__ = "tests"

    mock_find_packages = mocker.patch(
        "winipedia_utils.modules.package.find_packages_as_modules",
        return_value=[mock_package1, mock_package2],
    )

    result = get_src_package()

    assert_with_msg(result == mock_package1, f"Expected {mock_package1}, got {result}")
    mock_find_packages.assert_called_once_with(depth=0)


def test_get_src_package_no_source_package(mocker: MockFixture) -> None:
    """Test get_src_package when only tests package exists."""
    mock_package = mocker.MagicMock(spec=ModuleType)
    mock_package.__name__ = "tests"

    mocker.patch(
        "winipedia_utils.modules.package.find_packages_as_modules",
        return_value=[mock_package],
    )

    with pytest.raises(StopIteration):
        get_src_package()


def test_make_dir_with_init_file(tmp_path: Path, mocker: MockFixture) -> None:
    """Test func for make_dir_with_init_file."""
    test_dir = tmp_path / "test_package"

    # Mock make_init_modules_for_package
    mock_make_init = mocker.patch(
        "winipedia_utils.modules.package.make_init_modules_for_package"
    )

    make_dir_with_init_file(test_dir)

    assert_with_msg(
        test_dir.exists() and test_dir.is_dir(),
        f"Expected directory {test_dir} to be created",
    )
    mock_make_init.assert_called_once_with(test_dir)


def test_make_dir_with_init_file_existing_dir(
    tmp_path: Path, mocker: MockFixture
) -> None:
    """Test make_dir_with_init_file with existing directory."""
    test_dir = tmp_path / "existing_package"
    test_dir.mkdir()

    mock_make_init = mocker.patch(
        "winipedia_utils.modules.package.make_init_modules_for_package"
    )

    make_dir_with_init_file(test_dir)

    assert_with_msg(
        test_dir.exists() and test_dir.is_dir(),
        f"Expected directory {test_dir} to still exist",
    )
    mock_make_init.assert_called_once_with(test_dir)


def test_module_is_package() -> None:
    """Test func for module_is_package."""
    # Create a mock module with __path__ attribute (package)
    mock_package = ModuleType("test_package")
    mock_package.__path__ = ["some/path"]

    # Create a mock module without __path__ attribute (regular module)
    mock_module = ModuleType("test_module")

    assert_with_msg(
        module_is_package(mock_package) is True,
        "Expected module with __path__ to be identified as package",
    )

    assert_with_msg(
        module_is_package(mock_module) is False,
        "Expected module without __path__ to not be identified as package",
    )


def test_package_name_to_path() -> None:
    """Test func for package_name_to_path."""
    # Test with string package name
    result = package_name_to_path("package.subpackage.module")
    expected = Path("package") / "subpackage" / "module"
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Test with Path object
    input_path = Path("package/subpackage")
    result = package_name_to_path(input_path)
    expected = Path("package") / "subpackage"
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Test with ModuleType
    mock_module = ModuleType("test.module")
    result = package_name_to_path(mock_module)
    expected = Path("test") / "module"
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")


def test_get_modules_and_packages_from_package(mocker: MockFixture) -> None:
    """Test func for get_modules_and_packages_from_package."""
    # Create mock package
    mock_package = ModuleType("test_package")
    mock_package.__path__ = ["test_package"]
    mock_package.__name__ = "test_package"

    # Mock pkgutil.iter_modules to return some modules and packages
    mock_iter_modules = mocker.patch("pkgutil.iter_modules")
    mock_iter_modules.return_value = [
        (None, "test_package.subpackage", True),  # is_pkg=True
        (None, "test_package.module1", False),  # is_pkg=False
        (None, "test_package.module2", False),  # is_pkg=False
    ]

    # Mock import_module
    mock_subpackage = ModuleType("test_package.subpackage")
    mock_module1 = ModuleType("test_package.module1")
    mock_module2 = ModuleType("test_package.module2")

    mock_import = mocker.patch("winipedia_utils.modules.package.import_module")
    mock_import.side_effect = [mock_subpackage, mock_module1, mock_module2] * 2

    packages, modules = get_modules_and_packages_from_package(mock_package)

    assert_with_msg(
        packages == [mock_subpackage],
        f"Expected packages [mock_subpackage], got {packages}",
    )
    assert_with_msg(
        modules == [mock_module1, mock_module2],
        f"Expected modules [mock_module1, mock_module2], got {modules}",
    )

    mock_iter_modules.assert_called_once_with(
        mock_package.__path__, prefix="test_package."
    )

    # test order is consistent so that
    assert_with_msg(
        get_modules_and_packages_from_package(mock_package) == (packages, modules),
        "Expected consistent order of packages and modules",
    )


def test_find_packages(mocker: MockFixture) -> None:
    """Test func for find_packages."""
    # Mock setuptools find_packages
    mock_find_packages = mocker.patch(
        "winipedia_utils.modules.package._find_packages",
        return_value=["package1", "package1.sub1", "package1.sub1.sub2", "package2"],
    )

    # Mock load_gitignore to return empty list (no gitignore patterns)
    mock_load_gitignore = mocker.patch(
        "winipedia_utils.modules.package.load_gitignore",
        return_value=[],
    )

    # Test without depth limit
    result = find_packages()
    expected = ["package1", "package1.sub1", "package1.sub1.sub2", "package2"]
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Test with depth limit
    result = find_packages(depth=1)
    expected = ["package1", "package1.sub1", "package2"]
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Test with depth 0
    result = find_packages(depth=0)
    expected = ["package1", "package2"]
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Verify that setuptools find_packages was called with empty exclude list
    mock_find_packages.assert_called_with(where=".", exclude=[], include=("*",))

    # Verify that load_gitignore was called
    assert_with_msg(
        mock_load_gitignore.call_count > 0,
        "Expected load_gitignore to be called for gitignore filtering",
    )


def test_find_packages_with_namespace(mocker: MockFixture) -> None:
    """Test find_packages with namespace packages."""
    mock_find_namespace = mocker.patch(
        "winipedia_utils.modules.package._find_namespace_packages",
        return_value=["ns_package1", "ns_package2"],
    )

    # Mock load_gitignore to return empty list (no gitignore patterns)
    mock_load_gitignore = mocker.patch(
        "winipedia_utils.modules.package.load_gitignore",
        return_value=[],
    )

    result = find_packages(include_namespace_packages=True)
    expected = ["ns_package1", "ns_package2"]
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    mock_find_namespace.assert_called_once_with(where=".", exclude=[], include=("*",))

    # Verify that load_gitignore was called
    assert_with_msg(
        mock_load_gitignore.call_count > 0,
        "Expected load_gitignore to be called for gitignore filtering",
    )


def test_find_packages_with_gitignore_filtering(mocker: MockFixture) -> None:
    """Test find_packages with gitignore patterns that should exclude packages."""
    # Mock setuptools find_packages to return only packages not excluded by gitignore
    mock_find_packages = mocker.patch(
        "winipedia_utils.modules.package._find_packages",
        return_value=[
            "package1",
            "package2",
        ],  # dist and build are excluded by setuptools
    )

    # Mock load_gitignore to return patterns that should exclude dist and build
    mock_load_gitignore = mocker.patch(
        "winipedia_utils.modules.package.load_gitignore",
        return_value=["dist/", "build/", "__pycache__/"],
    )

    result = find_packages()
    expected = ["package1", "package2"]
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # Verify that setuptools find_packages was called with gitignore patterns
    expected_exclude = ["dist", "build", "__pycache__"]
    mock_find_packages.assert_called_with(
        where=".", exclude=expected_exclude, include=("*",)
    )

    # Verify that load_gitignore was called
    mock_load_gitignore.assert_called_once()


def test_find_packages_as_modules(mocker: MockFixture) -> None:
    """Test func for find_packages_as_modules."""
    # Mock find_packages
    mock_find_packages = mocker.patch(
        "winipedia_utils.modules.package.find_packages",
        return_value=["package1", "package2"],
    )

    # Mock import_module
    mock_package1 = ModuleType("package1")
    mock_package2 = ModuleType("package2")
    mock_import = mocker.patch("winipedia_utils.modules.package.import_module")
    mock_import.side_effect = [mock_package1, mock_package2]

    result = find_packages_as_modules(depth=1, include_namespace_packages=True)
    expected = [mock_package1, mock_package2]
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")

    # The function should call find_packages with exclude=None (default parameter)
    mock_find_packages.assert_called_once_with(
        depth=1,
        include_namespace_packages=True,
        where=".",
        exclude=None,
        include=("*",),
    )


def test_walk_package(mocker: MockFixture) -> None:
    """Test func for walk_package."""
    # Create mock package hierarchy
    root_package = ModuleType("root")
    sub_package1 = ModuleType("root.sub1")
    sub_package2 = ModuleType("root.sub2")
    module1 = ModuleType("root.module1")
    module2 = ModuleType("root.sub1.module2")
    module3 = ModuleType("root.sub2.module3")

    # Mock get_modules_and_packages_from_package
    mock_get_modules = mocker.patch(
        "winipedia_utils.modules.package.get_modules_and_packages_from_package"
    )

    # Define side effects for different packages
    def side_effect(package: ModuleType) -> tuple[list[ModuleType], list[ModuleType]]:
        if package == root_package:
            return [sub_package1, sub_package2], [module1]
        if package == sub_package1:
            return [], [module2]
        if package == sub_package2:
            return [], [module3]
        return [], []

    mock_get_modules.side_effect = side_effect

    result = list(walk_package(root_package))
    expected = [
        (root_package, [module1]),
        (sub_package1, [module2]),
        (sub_package2, [module3]),
    ]

    assert_with_msg(
        len(result) == len(expected),
        f"Expected {len(expected)} results, got {len(result)}",
    )

    for i, (pkg, modules) in enumerate(result):
        expected_pkg, expected_modules = expected[i]
        assert_with_msg(
            pkg == expected_pkg,
            f"Expected package {expected_pkg}, got {pkg} at index {i}",
        )
        assert_with_msg(
            modules == expected_modules,
            f"Expected modules {expected_modules}, got {modules} at index {i}",
        )


def test_make_init_modules_for_package(tmp_path: Path, mocker: MockFixture) -> None:
    """Test func for make_init_modules_for_package."""
    # Create test directory structure
    test_package = tmp_path / "test_package"
    sub_dir1 = test_package / "subdir1"
    sub_dir2 = test_package / "subdir2"
    sub_dir1.mkdir(parents=True)
    sub_dir2.mkdir(parents=True)

    # Create an existing __init__.py in one directory
    (sub_dir1 / "__init__.py").write_text("# existing")

    # Mock to_path
    mock_to_path = mocker.patch("winipedia_utils.modules.module.to_path")
    mock_to_path.return_value = test_package

    # Mock walk_os_skipping_gitignore_patterns
    mock_walk = mocker.patch(
        "winipedia_utils.modules.package.walk_os_skipping_gitignore_patterns"
    )
    mock_walk.return_value = [
        (sub_dir1, [], ["__init__.py"]),  # Has __init__.py
        (sub_dir2, [], []),  # No __init__.py
    ]

    # Mock make_init_module
    mock_make_init = mocker.patch("winipedia_utils.modules.package.make_init_module")

    make_init_modules_for_package("test.package")

    # Should only call make_init_module for sub_dir2 (no existing __init__.py)
    mock_make_init.assert_called_once_with(sub_dir2)


def test_make_init_module(tmp_path: Path, mocker: MockFixture) -> None:
    """Test func for make_init_module."""
    test_dir = tmp_path / "test_package"

    # Mock to_path to return the test directory
    mock_to_path = mocker.patch("winipedia_utils.modules.module.to_path")
    mock_to_path.return_value = test_dir

    # Mock get_default_init_module_content
    mock_content = mocker.patch(
        "winipedia_utils.modules.module.get_default_init_module_content"
    )
    mock_content.return_value = '"""__init__ module."""'

    make_init_module(test_dir)

    init_file = test_dir / "__init__.py"
    assert_with_msg(
        init_file.exists(), f"Expected __init__.py file to be created at {init_file}"
    )
    assert_with_msg(
        init_file.read_text() == '"""__init__ module."""',
        "Expected correct content in __init__.py",
    )


def test_make_init_module_with_init_path(tmp_path: Path, mocker: MockFixture) -> None:
    """Test make_init_module when path already points to __init__.py."""
    test_dir = tmp_path / "test_package"
    init_path = test_dir / "__init__.py"

    # Mock to_path to return the init file path directly
    mock_to_path = mocker.patch("winipedia_utils.modules.module.to_path")
    mock_to_path.return_value = init_path

    # Mock get_default_init_module_content
    mock_content = mocker.patch(
        "winipedia_utils.modules.module.get_default_init_module_content"
    )
    mock_content.return_value = '"""__init__ module."""'

    make_init_module(init_path)

    assert_with_msg(
        init_path.exists(), f"Expected __init__.py file to be created at {init_path}"
    )
    assert_with_msg(
        init_path.read_text() == '"""__init__ module."""',
        "Expected correct content in __init__.py",
    )


def test_copy_package(mocker: MockFixture) -> None:
    """Test func for copy_package."""
    # Create source package structure
    src_package = ModuleType("src_package")
    sub_package = ModuleType("src_package.sub")
    module1 = ModuleType("src_package.module1")
    module2 = ModuleType("src_package.sub.module2")

    # Mock dependencies
    mock_to_path = mocker.patch("winipedia_utils.modules.module.to_path")
    mock_get_isolated_name = mocker.patch(
        "winipedia_utils.modules.module.get_isolated_obj_name"
    )
    mock_create_module = mocker.patch("winipedia_utils.modules.module.create_module")
    mock_get_content = mocker.patch(
        "winipedia_utils.modules.module.get_module_content_as_str"
    )

    # Set up mock returns
    src_path = Path("src_package")
    dst_path = Path("dst")

    def mock_to_path_side_effect(obj: Any, *, is_package: bool) -> Path:
        if is_package:
            return {
                src_package: src_path,
                "dst": dst_path,
                sub_package: src_path / "sub",
            }.get(obj, Path("mock_path"))
        msg = "Not a package"
        raise ValueError(msg)

    mock_to_path.side_effect = mock_to_path_side_effect

    def mock_get_isolated_name_side_effect(obj: Any) -> str:
        return {
            src_package: "src_package",
            module1: "module1.py",
            module2: "module2.py",
        }.get(obj, "mock_name")

    mock_get_isolated_name.side_effect = mock_get_isolated_name_side_effect

    def mock_get_content_side_effect(obj: Any) -> str:
        return {
            module1: "# module1 content",
            module2: "# module2 content",
        }.get(obj, "# mock content")

    mock_get_content.side_effect = mock_get_content_side_effect

    # Mock walk_package
    mock_walk = mocker.patch("winipedia_utils.modules.package.walk_package")
    mock_walk.return_value = [
        (src_package, [module1]),
        (sub_package, [module2]),
    ]

    # Mock Path.write_text to avoid file system operations
    mock_write_text = mocker.patch("pathlib.Path.write_text")

    # Test with file content
    copy_package(src_package, "dst", with_file_content=True)

    # Verify create_module calls
    expected_call_count = 4
    assert_with_msg(
        mock_create_module.call_count >= expected_call_count,
        f"Expected at least {expected_call_count} calls to create_module, "
        f"got {mock_create_module.call_count}",
    )

    # Verify write_text was called for modules with content
    expected_write_calls = 2
    assert_with_msg(
        mock_write_text.call_count >= expected_write_calls,
        f"Expected at least {expected_write_calls} calls to write_text, "
        f"got {mock_write_text.call_count}",
    )


def test_copy_package_without_content(mocker: MockFixture) -> None:
    """Test copy_package without file content."""
    src_package = ModuleType("src_package")
    module1 = ModuleType("src_package.module1")

    # Mock dependencies
    mock_to_path = mocker.patch("winipedia_utils.modules.module.to_path")
    mock_get_isolated_name = mocker.patch(
        "winipedia_utils.modules.module.get_isolated_obj_name"
    )
    mocker.patch("winipedia_utils.modules.module.create_module")
    mock_get_content = mocker.patch(
        "winipedia_utils.modules.module.get_module_content_as_str"
    )

    # Set up mock returns
    src_path = Path("src_package")
    dst_path = Path("dst")

    def mock_to_path_side_effect2(obj: Any, *, is_package: bool) -> Path:
        if is_package:
            return {
                src_package: src_path,
                "dst": dst_path,
            }.get(obj, Path("mock_path"))
        msg = "Not a package"
        raise ValueError(msg)

    mock_to_path.side_effect = mock_to_path_side_effect2

    def mock_get_isolated_name_side_effect2(obj: Any) -> str:
        return {
            src_package: "src_package",
            module1: "module1.py",
        }.get(obj, "mock_name")

    mock_get_isolated_name.side_effect = mock_get_isolated_name_side_effect2

    # Mock walk_package
    mock_walk = mocker.patch("winipedia_utils.modules.package.walk_package")
    mock_walk.return_value = [(src_package, [module1])]

    # Test without file content
    copy_package(src_package, "dst", with_file_content=False)

    # Should not call get_module_content_as_str
    mock_get_content.assert_not_called()
