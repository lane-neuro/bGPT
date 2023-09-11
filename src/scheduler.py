from batcher.token_stack import token_stack
import multiprocessing as mp


class scheduler:
    # role: timing & scheduling of dataset_engine/batcher

    def __init__(self, process_size: int = 1):
        self.process_size = process_size
        self.thread_stack = []
        self.trans_list = []
        # self.tokens = token_stack(first_token=None)
        return

    def scan_loop(self):
        # apply transformations

        # characterizer from transformations

        # tokenize characterizer output

        # add to token_stack

        return
