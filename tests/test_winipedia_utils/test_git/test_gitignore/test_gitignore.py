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
