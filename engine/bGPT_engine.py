import engine.datastorage.bGPT_metadata
from engine.bGPT_generator import bGPT_generator


class bGPT_engine:
    def __init__(self, animal: str, framerate: int, bodyparts: str, coordinate_system: str, csv_path: str, use_likelihood=True, transformations=None):
        self.use_likelihood = use_likelihood
        self.coordinate_system = coordinate_system
        self.meta = engine.datastorage.bGPT_metadata.bGPT_metadata(self, animal, framerate, bodyparts)
        self.generator = bGPT_generator(self, csv_path)

        if transformations is None:
            self.transformations = []
        else:
            self.transformations = transformations
        print("bGPT_engine: transformation engine initialized")

    def __repr__(self):
        transformations = ', '.join([str(transform) for transform in self.transformations])
        return f"bGPT_generator:(\nMetadata:\'{self.meta}\',\n\nTransformations: [{transformations}],\n\nPose Tokens:\'{self.pack_generator()}\', \n\nNumber of Pose Tokens: {len(self.pack_generator())})"

    def pack_generator(self):
        return self.generator.pose.pack()

    def visualize_transformations(self, transformations, cmap='nipy_spectral'):
        return self.generator.visualize_transformations(transformations, cmap)

    def transform(self, datapoint):
        for transformation in self.transformations:
            datapoint = transformation.transform(datapoint)
        return datapoint

    def add_transformation(self, transformation):
        self.transformations.append(transformation)
