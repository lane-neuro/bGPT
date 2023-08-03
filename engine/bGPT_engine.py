class bGPT_engine:
    def __init__(self, transformations=None):
        if transformations is None:
            self.transformations = []
        else:
            self.transformations = transformations
        print("bGPT_engine: transformation engine initialized")

    def transform(self, datapoint):
        for transformation in self.transformations:
            datapoint = transformation.transform(datapoint)
        return datapoint

    def add_transformation(self, transformation):
        self.transformations.append(transformation)
