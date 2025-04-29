from utils.testing.create_tests import main as create_tests
from utils.testing.run_tests import main as run_tests
from utils.add___init___files import main as add___init___files

import sys

sys.dont_write_bytecode = True

if __name__ == "__main__":
    # run_tests()
    create_tests()
    # add___init___files()
