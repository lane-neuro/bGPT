from copy import deepcopy

from engine.datastorage.bGPT_datapoint import bGPT_datapoint
from engine import bGPT_engine


class bGPT_frame:
    def __init__(self, use_likelihood, *data_in):
        self.use_likelihood = use_likelihood
        row = []
        for jj in data_in:
            row.extend(jj)
        self.frame_num = row[0]
        self.coords = []

        step = 3
        for ii in range(1, len(row), step):
            if self.use_likelihood:
                self.coords.extend([bGPT_datapoint(row[ii], row[ii + 1], row[ii + 2])])
            else:
                self.coords.extend([bGPT_datapoint(row[ii], row[ii + 1])])

    def __repr__(self):
        frame_out = ""

        for coord in self.coords:
            frame_out = f"{frame_out},{repr(coord)}"
        return f"{frame_out}"

    def transform(self, engine: bGPT_engine):
        new_frame = deepcopy(self)  # Create a new frame object
        for coord in new_frame.coords:
            coord.transform(engine)
        return new_frame
