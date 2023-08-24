import random

class PerspectiveTransform:

    def __init__(self,  min_in: float, max_in: float, random_in: float):
        self.random_in = random_in
        self.perspective_coeff = random.uniform(min_in, max_in)
        self.random_roll = random.uniform(0, 1)

    def __repr__(self):
        return f"PerspectiveTransform, perspective_coeff = {self.perspective_coeff}, r_in,r_roll = {self.random_in}, {self.random_roll}"

    def transform(self, datapoint):
        if self.random_roll <= self.random_in:
            scale = 1.0 + self.perspective_coeff * datapoint.y
            datapoint.x *= scale
            datapoint.y *= scale
        return datapoint
