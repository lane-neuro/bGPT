class ScaleTransform:

    def __init__(self, scale):
        self.scale = scale
        print(" -> ScaleTransform: initialized with scale = ", self.scale)

    def __repr__(self):
        return f"ScaleTransform, scalar = {self.scale}"

    def transform(self, datapoint):
        datapoint.x *= self.scale
        datapoint.y *= self.scale
        return datapoint
