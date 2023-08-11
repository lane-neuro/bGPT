import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import csv
import array
from copy import deepcopy

from engine import bGPT_engine


class bGPT_datapoint:

    def __init__(self, x_in: float, y_in: float, likelihood_in: float = None):
        self.x = float(x_in)
        self.y = float(y_in)
        self.likelihood = float(likelihood_in) if likelihood_in else None

    def formatted_str(self):
        if self.likelihood is not None:
            return f"{self.x}_{self.y}_{self.likelihood}"
        else:
            return f"{self.x}_{self.y}"

    def __repr__(self):
        if self.likelihood is not None:
            return f"{self.x}_{self.y}_{self.likelihood}"
        else:
            return f"{self.x}_{self.y}"

    def transform(self, engine: bGPT_engine):
        new_datapoint = deepcopy(self)  # Create a new data point object
        return engine.transform(new_datapoint)
