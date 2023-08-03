import math


class RotateTransform:

    def __init__(self, theta):
        self.theta = theta

    def __repr__(self):
        return f"RotateTransform, theta = {self.theta}"

    def transform(self, datapoint):
        original_x = datapoint.x
        datapoint.x = original_x * math.cos(self.theta) - datapoint.y * math.sin(self.theta)
        datapoint.y = original_x * math.sin(self.theta) + datapoint.y * math.cos(self.theta)
        return datapoint