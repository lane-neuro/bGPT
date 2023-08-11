import random


class TranslateTransform:

    def __init__(self, min_max_delta_x: list, min_max_delta_y: list, random_in: float):
        self.random_in = random_in
        self.delta_x = random.uniform(min_max_delta_x[0], min_max_delta_x[1])
        self.delta_y = random.uniform(min_max_delta_y[0], min_max_delta_y[1])
        self.random_roll = random.uniform(0, 1)

    def __repr__(self):
        return f"TranslateTransform, x,y = ({self.delta_x}, {self.delta_y}), r_in,r_roll = {self.random_in}, {self.random_roll}"

    def transform(self, datapoint):
        if self.random_roll <= self.random_in:
            datapoint.x += self.delta_x
            datapoint.y += self.delta_y
        return datapoint
