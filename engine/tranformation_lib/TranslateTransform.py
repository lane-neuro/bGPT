class TranslateTransform:

    def __init__(self, delta_x, delta_y):
        self.delta_x = delta_x
        self.delta_y = delta_y

    def __repr__(self):
        return f"TranslateTransform, x,y = ({self.delta_x}, {self.delta_y})"

    def transform(self, datapoint):
        datapoint.x += self.delta_x
        datapoint.y += self.delta_y
        return datapoint
