import math
import random


class RotateTransform:

    def __init__(self, min_in, max_in, random_in):
        self.random_in = random_in
        self.theta = random.uniform(min_in, max_in)
        self.random_roll = random.uniform(0, 1)

    def __repr__(self):
        return f"RotateTransform, theta = {self.theta}, r_in,r_roll = {self.random_in}, {self.random_roll}"

    def transform(self, datapoint):
        if self.random_roll <= self.random_in:
            original_x = datapoint.x
            datapoint.x = original_x * math.cos(self.theta) - datapoint.y * math.sin(self.theta)
            datapoint.y = original_x * math.sin(self.theta) + datapoint.y * math.cos(self.theta)
        return datapoint
