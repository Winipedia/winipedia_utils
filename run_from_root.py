import sys

# from utils.testing.create_tests import main as create_tests
from utils.testing.run_tests import main as run_tests

sys.dont_write_bytecode = True

if __name__ == "__main__":
    # create_tests()
    run_tests()
