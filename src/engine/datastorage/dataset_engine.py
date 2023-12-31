from src.engine.datastorage.metadata import metadata
from src.engine.datastorage.csv_engine import csv_engine
from src.engine.scanner import scanner

import random
import itertools

import torch


class dataset_engine:
    # definitions
    # meta = None
    # csv_scanners = None

    def __init__(self,
                 csv_paths: list = None,
                 batch_size: int = None,
                 block_size: int = None,
                 n_chars_per_bodypart: int = None,
                 animal: str = None,
                 framerate: int = None,
                 bodyparts: list = None,
                 coordinate_system: str = "xy",
                 csv_type: str = "DLC",
                 verbose: bool = False,
                 framerate_min_aug: int = 2,
                 n_bodyparts_min_aug: int = 1):

        self.csv_paths = csv_paths

        # initializes metadata
        self.meta = metadata(self,
                             animal=animal,
                             framerate=framerate,
                             bodyparts=bodyparts,
                             coordinate_system=coordinate_system,
                             verbose=verbose,
                             csv_type=csv_type,
                             csv_path=csv_paths)

        # initializes csv_engines
        self.csv_engines = {}
        for i, csv_path in enumerate(csv_paths):
            eng = csv_engine(csv_path=csv_path,
                             csv_type=self.meta.csv_type,
                             verbose=self.meta.verbose)
            self.csv_engines[i] = eng

        engine_bodyparts = self.csv_engines[0].bodyparts
        if self.meta.bodyparts is None:
            self.meta.bodyparts = engine_bodyparts
        elif not all(self.meta.bodyparts == engine_bodyparts):
            self.meta.bodyparts = engine_bodyparts

        self.packed_meta = self.meta.pack()

        n_bodyparts = len(self.meta.bodyparts)

        # initialize csv_engine scanners
        self.csv_scanners = {key: [] for key in self.csv_engines}
        for key in self.csv_scanners:
            for i in range(0, batch_size):
                scnr = scanner(nscanner=i,
                               batch_size=batch_size,
                               n_bodyparts=n_bodyparts,
                               n_bodyparts_min_aug=n_bodyparts_min_aug,
                               framerate=framerate,
                               framerate_min_aug=framerate_min_aug,
                               nrows_tensor=self.csv_engines[key].tensor.shape[0],
                               n_chars_per_bodypart=n_chars_per_bodypart,
                               block_size=block_size)
                self.csv_scanners[key].append(scnr)

        self.possible_combinations = list(itertools.product(list(self.csv_engines.keys()),
                                                            list(range(0, batch_size))))

    def train_data(self, n_examples):

        # need to add exception handling, fix tensor issue
        tensors = torch.empty((0, self.csv_engines[0].tensor.shape[1]), dtype=torch.float32)

        train_combinations = random.sample(self.possible_combinations, n_examples)
        tmp_combinations = [comb for comb in self.possible_combinations if comb not in train_combinations]

        metadatas = []

        for combination in train_combinations:
            key, nscanner = combination[0], combination[1]
            row_indices, char_index = self.csv_scanners[key][nscanner].get_indices()

            while row_indices == None:
                combination = random.sample(tmp_combinations, 1)
                ## drop combination from tmp_combinations
                row_indices, char_index = self.csv_scanners[key][nscanner].get_indices() ## WILLEM WORKING HERE
                ## NEED TO ADD None Error handling so that training loop can track when it ends an epoch

            tensor = self.csv_engines[key].num_pack(row_indices=row_indices)
            tensors = tensors.cat((tensors, tensor), dim=0)
            metadatas.append(self.packed_meta.copy())

        return metadatas, tensors
