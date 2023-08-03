class PerspectiveTransform:

    def __init__(self, perspective_coeff=0.0001):
        self.perspective_coeff = perspective_coeff

    def __repr__(self):
        return f"PerspectiveTransform, perspective_coeff = {self.perspective_coeff}"

    def transform(self, datapoint):
        scale = 1.0 + self.perspective_coeff * datapoint.y
        datapoint.x *= scale
        datapoint.y *= scale
        return datapoint
