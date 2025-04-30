import unittest

from utils.testing.base_test import BaseTestCaseForFile


def run_tests() -> None:
    # Define the path to the 'tests' folder
    tests_dir = BaseTestCaseForFile.make_test_folder_name()

    # Discover all test cases in the 'tests' folder
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(tests_dir, pattern="test_*.py")

    tests = unittest.TestSuite()
    tests.addTest(test_suite)

    runner = unittest.TextTestRunner()
    _ = runner.run(tests)


def main() -> None:
    run_tests()
