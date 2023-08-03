import numpy as np


class JitterTransform:

    def __init__(self, jitter_strength=0.1):
        self.jitter_strength = jitter_strength

    def __repr__(self):
        return f"JitterTransform, jitter_strength = {self.jitter_strength}"

    def transform(self, datapoint):
        datapoint.x += np.random.uniform(-self.jitter_strength, self.jitter_strength)
        datapoint.y += np.random.uniform(-self.jitter_strength, self.jitter_strength)
        return datapoint
