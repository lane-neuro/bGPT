import math
import os


class trainer:

    def __init__(self, train_files_in, validate_files_in, test_files_in):
        self.train_files = train_files_in
        self.validate_files = validate_files_in
        self.test_files = test_files_in
        print(f"trainer: training data initialized")

    def __repr__(self):
        return f"trainer:(\n'train files:{self.train}\n',\n'validate files{self.validate}\n',\n'test files{self.test}\n')"
