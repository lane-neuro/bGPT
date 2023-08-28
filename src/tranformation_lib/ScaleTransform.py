import random


class ScaleTransform:

    def __init__(self, min_in: float, max_in: float, random_in: float):
        self.random_in = random_in
        self.scale = random.uniform(min_in, max_in)
        self.random_roll = random.uniform(0, 1)

    def __repr__(self):
        return f"ScaleTransform, scalar = {self.scale}, r_in,r_roll = {self.random_in}, {self.random_roll}"

    def transform(self, datapoint):
        if self.random_roll <= self.random_in:
            datapoint.x *= self.scale
            datapoint.y *= self.scale
        return datapoint
