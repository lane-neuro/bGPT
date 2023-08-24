import numpy as np
import random


class JitterTransform:

    def __init__(self, min_in: float, max_in: float, random_in: float):
        self.random_in = random_in
        self.jitter_strength = random.uniform(min_in, max_in)
        self.random_roll = random.uniform(0, 1)

    def __repr__(self):
        return f"JitterTransform, jitter_strength = {self.jitter_strength}, r_in,r_roll = {self.random_in}, {self.random_roll}"

    def transform(self, datapoint):
        if self.random_roll <= self.random_in:
            datapoint.x += np.random.uniform(-self.jitter_strength, self.jitter_strength)
            datapoint.y += np.random.uniform(-self.jitter_strength, self.jitter_strength)
        return datapoint
