from utils.testing.base_test import BaseTestCaseForFile
from utils import multiprocessing


class TestMultiprocessing(BaseTestCaseForFile):

    __abstract__ = False

    tested_file = multiprocessing

    def setUp(self):
        super().setUp()

    def test__extend_process_args_with_const_args(self):
        raise NotImplementedError("Implement this test.")

    def test__find_max_pools_for_multiprocessing(self):
        raise NotImplementedError("Implement this test.")

    def test__get_future_results_as_completed(self):
        raise NotImplementedError("Implement this test.")

    def test__get_multiprocess_results_with_tqdm(self):
        raise NotImplementedError("Implement this test.")

    def test__prepare_multiprocess_loop(self):
        raise NotImplementedError("Implement this test.")

    def test__process_function_for_imap_with_args_unpacking(self):
        raise NotImplementedError("Implement this test.")

    def test_cancel_on_timeout_with_multiprocessing(self):
        raise NotImplementedError("Implement this test.")

    def test_multiprocess_loop(self):
        raise NotImplementedError("Implement this test.")

    def test_multithread_loop(self):
        raise NotImplementedError("Implement this test.")
