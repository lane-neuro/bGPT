from copy import deepcopy

from engine.datastorage.metadata import metadata
from src.engine.datastorage.datapoint import datapoint


class frame:

    def __init__(self, meta_in, *data_in):
        row = []
        self.meta = meta_in
        for jj in data_in:
            row.extend(jj)
        self.frame_num = row[0]
        self.coords = []

        step = 3
        for ii in range(1, len(row), step):
            self.coords.extend([datapoint(self.meta, row[ii], row[ii + 1])])

    def __repr__(self):
        frame_out = ""

        for coord in self.coords:
            frame_out = f"{frame_out},{repr(coord)}"
        return f"{frame_out}"

    def transform(self):
        new_frame = deepcopy(self)  # Create a new frame object
        for coord in new_frame.coords:
            coord.transform()
        return new_frame
