from utils import multiprocessing
from utils.testing.base_test import BaseTestCaseForFile


class TestMultiprocessing(BaseTestCaseForFile):
    __abstract__ = False

    tested_file = multiprocessing

    def setUp(self) -> None:
        super().setUp()

    def test__extend_process_args_with_const_args(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test__find_max_pools_for_multiprocessing(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test__get_future_results_as_completed(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test__get_multiprocess_results_with_tqdm(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test__prepare_multiprocess_loop(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test__process_function_for_imap_with_args_unpacking(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_cancel_on_timeout_with_multiprocessing(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_multiprocess_loop(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)

    def test_multithread_loop(self) -> None:
        msg = "Implement this test."
        raise NotImplementedError(msg)
