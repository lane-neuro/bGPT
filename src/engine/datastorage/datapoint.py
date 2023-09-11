from copy import deepcopy
from engine.datastorage.metadata import metadata


class datapoint:

    def __init__(self, meta_in: metadata, x_in: float, y_in: float):
        self.metadata = meta_in
        self.x = float(x_in)
        self.y = float(y_in)

    def formatted_str(self):
        return f"{self.x}_{self.y}"

    def __repr__(self):
        return f"{self.x}_{self.y}"

    def transform(self):
        new_datapoint = deepcopy(self)  # Create a new data point object
        return self.metadata.engine.transform(new_datapoint)
