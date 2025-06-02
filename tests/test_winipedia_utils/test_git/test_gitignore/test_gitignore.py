"""module for the following module path (maybe truncated).

tests.test_winipedia_utils.test_git.test_gitignore
"""

from pathlib import Path

from pytest_mock import MockFixture

from winipedia_utils.git.gitignore.gitignore import (
    path_is_in_gitignore,
    walk_os_skipping_gitignore_patterns,
)
from winipedia_utils.testing.assertions import assert_with_msg


def test_path_is_in_gitignore(mocker: MockFixture) -> None:
    """Test func for path_is_in_gitignore."""
    content = """
# Comment line
*.pyc
__pycache__/
.venv/
# This is a comment
build/
dist/
*.egg-info/
.pytest_cache/
"""

    # patch Path.exists to return True for .gitignore
    mocker.patch("pathlib.Path.exists", return_value=True)
    # patch Path.open to return our mock content
    mocker.patch("pathlib.Path.read_text", return_value=content)

    # make a list of things that should be in gitignore
    in_gitignore = [
        "folder/file.pyc",
        "__pycache__/file.pdf",
        ".venv/file.py",
        "build/file.py",
        "dist/file.py",
        "folder/folder.egg-info/file.py",
        ".pytest_cache/file.py",
    ]
    # make a list of things that should not be in gitignore
    not_in_gitignore = [
        "file.py",
        "folder/file.py",
        "folder/file.txt",
        "folder/subfolder/file.py",
    ]

    for path in in_gitignore:
        assert_with_msg(
            path_is_in_gitignore(path),
            f"Expected {path} to be in gitignore",
        )
    for path in not_in_gitignore:
        assert_with_msg(
            not path_is_in_gitignore(path),
            f"Expected {path} not to be in gitignore",
        )


def test_walk_os_skipping_gitignore_patterns(mocker: MockFixture) -> None:
    """Test func for walk_os_skipping_gitignore_patterns."""
    # set up a mock os.walk that returns a few directories and files
    mocker.patch(
        "os.walk",
        return_value=[
            ("root", ["dir1", "dir2"], ["file1.smth", "file2.smth"]),
            ("root/dir1", ["dir3"], ["file3.smth", "file4.smth"]),
            ("root/dir2", [], ["file5.smth"]),
            ("root/dir1/dir3", [], ["file6.smth"]),
        ],
    )

    # set up a mock .gitignore that ignores dir2 and file4
    mocker.patch("pathlib.Path.exists", return_value=True)
    mocker.patch(
        "pathlib.Path.read_text",
        return_value="""
# ignore dir2
dir2/

# ignore file4
file4.smth
""",
    )

    # call the function and check the results
    results = list(walk_os_skipping_gitignore_patterns("root"))
    expected = [
        (Path("root"), ["dir1"], ["file1.smth", "file2.smth"]),
        (Path("root/dir1"), ["dir3"], ["file3.smth"]),
        (Path("root/dir1/dir3"), [], ["file6.smth"]),
    ]
    assert_with_msg(
        results == expected,
        f"Expected {expected}, got {results}",
    )


def test_load_gitignore(mocker: MockFixture, tmp_path: Path) -> None:
    """Test func for load_gitignore."""
    # Test when .gitignore exists
    gitignore_content = """# Comment
*.pyc
__pycache__/
dist/
build/
"""
    gitignore_path = tmp_path / ".gitignore"
    gitignore_path.write_text(gitignore_content)

    # Mock Path to return our test directory
    mocker.patch(
        "winipedia_utils.git.gitignore.gitignore.Path", return_value=gitignore_path
    )

    from winipedia_utils.git.gitignore.gitignore import load_gitignore

    result = load_gitignore()
    expected = ["# Comment", "*.pyc", "__pycache__/", "dist/", "build/"]
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")


def test_load_gitignore_creates_file_if_not_exists(
    mocker: MockFixture, tmp_path: Path
) -> None:
    """Test that load_gitignore creates .gitignore if it doesn't exist."""
    gitignore_path = tmp_path / ".gitignore"

    # Mock Path to return our test directory
    mock_path = mocker.patch("winipedia_utils.git.gitignore.gitignore.Path")
    mock_path.return_value = gitignore_path

    from winipedia_utils.git.gitignore.gitignore import load_gitignore

    result = load_gitignore()
    expected: list[str] = []  # Empty file content
    assert_with_msg(result == expected, f"Expected {expected}, got {result}")
    assert_with_msg(gitignore_path.exists(), "Expected .gitignore file to be created")


def test_dump_gitignore(mocker: MockFixture, tmp_path: Path) -> None:
    """Test func for dump_gitignore."""
    gitignore_path = tmp_path / ".gitignore"

    # Mock Path to return our test directory
    mocker.patch(
        "winipedia_utils.git.gitignore.gitignore.Path", return_value=gitignore_path
    )

    from winipedia_utils.git.gitignore.gitignore import dump_gitignore

    patterns = ["*.pyc", "__pycache__/", "dist/", "build/"]
    dump_gitignore(patterns)

    # Check that file was written with correct content
    assert_with_msg(gitignore_path.exists(), "Expected .gitignore file to be created")
    content = gitignore_path.read_text()
    expected_content = "*.pyc\n__pycache__/\ndist/\nbuild/"
    assert_with_msg(
        content == expected_content, f"Expected {expected_content!r}, got {content!r}"
    )


def test_dump_gitignore_overwrites_existing(
    mocker: MockFixture, tmp_path: Path
) -> None:
    """Test that dump_gitignore overwrites existing .gitignore file."""
    gitignore_path = tmp_path / ".gitignore"
    gitignore_path.write_text("old content")

    # Mock Path to return our test directory
    mocker.patch(
        "winipedia_utils.git.gitignore.gitignore.Path", return_value=gitignore_path
    )

    from winipedia_utils.git.gitignore.gitignore import dump_gitignore

    patterns = ["new", "patterns"]
    dump_gitignore(patterns)

    content = gitignore_path.read_text()
    expected_content = "new\npatterns"
    assert_with_msg(
        content == expected_content, f"Expected {expected_content!r}, got {content!r}"
    )


def test_add_patterns_to_gitignore(mocker: MockFixture) -> None:
    """Test func for add_patterns_to_gitignore."""
    # Mock load_gitignore to return existing patterns
    mock_load = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore.load_gitignore",
        return_value=["*.pyc", "__pycache__/"],
    )

    # Mock dump_gitignore to capture what gets written
    mock_dump = mocker.patch("winipedia_utils.git.gitignore.gitignore.dump_gitignore")

    from winipedia_utils.git.gitignore.gitignore import add_patterns_to_gitignore

    # Test adding new patterns
    new_patterns = ["dist/", "build/", "*.pyc"]  # *.pyc already exists
    add_patterns_to_gitignore(new_patterns)

    # Should call dump with existing + new (excluding duplicates)
    expected_patterns = ["*.pyc", "__pycache__/", "dist/", "build/"]
    mock_dump.assert_called_once_with(expected_patterns)
    mock_load.assert_called_once()


def test_add_patterns_to_gitignore_no_new_patterns(mocker: MockFixture) -> None:
    """Test add_patterns_to_gitignore when all patterns already exist."""
    # Mock load_gitignore to return existing patterns
    mock_load = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore.load_gitignore",
        return_value=["*.pyc", "__pycache__/", "dist/"],
    )

    # Mock dump_gitignore to capture what gets written
    mock_dump = mocker.patch("winipedia_utils.git.gitignore.gitignore.dump_gitignore")

    from winipedia_utils.git.gitignore.gitignore import add_patterns_to_gitignore

    # Test adding patterns that already exist
    existing_patterns = ["*.pyc", "__pycache__/"]
    add_patterns_to_gitignore(existing_patterns)

    # Should not call dump since no new patterns
    mock_dump.assert_not_called()
    mock_load.assert_called_once()


def test__get_gitignore_patterns() -> None:
    """Test func for _get_gitignore_patterns."""
    from winipedia_utils.git.gitignore.gitignore import _get_gitignore_patterns

    result = _get_gitignore_patterns()

    # Check that it returns the expected patterns
    expected_patterns = [
        "__pycache__/",
        ".idea/",
        ".mypy_cache/",
        ".pytest_cache/",
        ".ruff_cache/",
        ".vscode/",
        "dist/",
        "test.py",
        ".git/",
    ]

    assert_with_msg(
        len(result) == len(expected_patterns),
        f"Expected {len(expected_patterns)} patterns, got {len(result)}",
    )

    for pattern in expected_patterns:
        assert_with_msg(
            pattern in result, f"Expected pattern {pattern} to be in result"
        )

    # Verify the exact list matches (order matters for consistency)
    assert_with_msg(
        result == expected_patterns, f"Expected {expected_patterns}, got {result}"
    )


def test__gitignore_is_correct(mocker: MockFixture) -> None:
    """Test func for _gitignore_is_correct."""
    from winipedia_utils.git.gitignore.gitignore import _gitignore_is_correct

    # Test when gitignore is correct (no missing patterns)
    mock_get_missing = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore._get_missing_patterns", return_value=[]
    )

    result = _gitignore_is_correct()
    assert_with_msg(result is True, "Expected True when no missing patterns")
    mock_get_missing.assert_called_once()


def test__gitignore_is_correct_with_missing_patterns(mocker: MockFixture) -> None:
    """Test _gitignore_is_correct when there are missing patterns."""
    from winipedia_utils.git.gitignore.gitignore import _gitignore_is_correct

    # Test when gitignore has missing patterns
    mock_get_missing = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore._get_missing_patterns",
        return_value=["dist/", ".idea/"],
    )

    result = _gitignore_is_correct()
    assert_with_msg(result is False, "Expected False when there are missing patterns")
    mock_get_missing.assert_called_once()


def test__add_package_patterns_to_gitignore(mocker: MockFixture) -> None:
    """Test func for _add_package_patterns_to_gitignore."""
    from winipedia_utils.git.gitignore.gitignore import (
        _add_package_patterns_to_gitignore,
    )

    # Test case 1: When gitignore is already correct
    mock_is_correct = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore._gitignore_is_correct",
        return_value=True,
    )

    # Mock other functions to ensure they're not called
    mock_get_missing = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore._get_missing_patterns"
    )
    mock_add_patterns = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore.add_patterns_to_gitignore"
    )

    _add_package_patterns_to_gitignore()

    # Should return early without calling other functions
    mock_is_correct.assert_called_once()
    mock_get_missing.assert_not_called()
    mock_add_patterns.assert_not_called()

    # Reset mocks for test case 2
    mock_is_correct.reset_mock()
    mock_get_missing.reset_mock()
    mock_add_patterns.reset_mock()

    # Test case 2: When there are missing patterns
    mock_is_correct.return_value = False
    missing_patterns = ["dist/", ".idea/"]
    mock_get_missing.return_value = missing_patterns

    _add_package_patterns_to_gitignore()

    # Should call all functions
    mock_is_correct.assert_called_once()
    mock_get_missing.assert_called_once()
    mock_add_patterns.assert_called_once_with(missing_patterns)


def test__get_missing_patterns(mocker: MockFixture) -> None:
    """Test func for _get_missing_patterns."""
    from winipedia_utils.git.gitignore.gitignore import _get_missing_patterns

    # Mock _get_gitignore_patterns to return needed patterns
    needed_patterns = ["__pycache__/", ".idea/", "dist/", ".git/"]
    mock_get_patterns = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore._get_gitignore_patterns",
        return_value=needed_patterns,
    )

    # Mock load_gitignore to return existing patterns (some missing)
    existing_patterns = ["__pycache__/", ".idea/", "other_pattern"]
    mock_load = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore.load_gitignore",
        return_value=existing_patterns,
    )

    result = _get_missing_patterns()

    # Should return patterns that are needed but not in existing
    expected_missing = ["dist/", ".git/"]
    assert_with_msg(
        result == expected_missing, f"Expected {expected_missing}, got {result}"
    )

    mock_get_patterns.assert_called_once()
    mock_load.assert_called_once()


def test__get_missing_patterns_none_missing(mocker: MockFixture) -> None:
    """Test _get_missing_patterns when no patterns are missing."""
    from winipedia_utils.git.gitignore.gitignore import _get_missing_patterns

    # Mock _get_gitignore_patterns to return needed patterns
    needed_patterns = ["__pycache__/", ".idea/", "dist/"]
    mock_get_patterns = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore._get_gitignore_patterns",
        return_value=needed_patterns,
    )

    # Mock load_gitignore to return all needed patterns plus extra
    existing_patterns = ["__pycache__/", ".idea/", "dist/", "extra_pattern"]
    mock_load = mocker.patch(
        "winipedia_utils.git.gitignore.gitignore.load_gitignore",
        return_value=existing_patterns,
    )

    result = _get_missing_patterns()

    # Should return empty list when no patterns are missing
    expected_missing: list[str] = []
    assert_with_msg(
        result == expected_missing, f"Expected {expected_missing}, got {result}"
    )

    mock_get_patterns.assert_called_once()
    mock_load.assert_called_once()
