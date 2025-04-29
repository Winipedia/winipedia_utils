import unittest
import os
import sys

from utils.testing.base_test import BaseTestCaseForFile


def run_tests():
    # Define the path to the 'tests' folder
    tests_dir = BaseTestCaseForFile.make_test_folder_name()

    # Discover all test cases in the 'tests' folder
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(tests_dir, pattern="test_*.py")

    tests = unittest.TestSuite()
    tests.addTest(test_suite)

    runner = unittest.TextTestRunner()
    runner.run(tests)


def main():
    run_tests()
