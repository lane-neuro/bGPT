import engine.datastorage.bGPT_metadata
from engine.bGPT_generator import bGPT_generator
from engine.bGPT_train import bGPT_train


class bGPT_engine:
    def __init__(self, animal: str, framerate: int, csv_path: str,
                 bodyparts: list = None, coordinate_system: str = "xy",
                 use_likelihood: bool = True, image_transformations: list = None,
                 resample_fps: int = None, verbose: bool = False):
        self.verbose = verbose
        self.resample_fps = resample_fps

        framerate = framerate
        frame_resample_by = 1
        if self.resample_fps is not None:
            frame_resample_by = framerate // self.resample_fps
            if verbose:
                print(f"bGPT_engine: Resampling video to {self.resample_fps}fps, frames resample by {frame_resample_by}th index")
            framerate = self.resample_fps

        self.meta = engine.datastorage.bGPT_metadata.bGPT_metadata(self, animal, csv_path, framerate, frame_resample_by,
                                                                   bodyparts, coordinate_system, use_likelihood, verbose)
        self.generator = bGPT_generator(self, verbose)

        if image_transformations is None:
            self.transformations = []
        else:
            self.transformations = image_transformations
        if verbose:
            print("bGPT_engine: transformation engine initialized")

    def __repr__(self):
        transformations = ', '.join([str(transform) for transform in self.transformations])
        return (f"bGPT_generator:(\nMetadata:\'{self.meta}\',\n\nTransformations: [{transformations}],\n\nPose Tokens:"
                f"\'{self.pack_generator()}\', \n\nNumber of Pose Tokens: {len(self.pack_generator())})")

    def pack_generator(self):
        return self.generator.pose.pack()

    def pack_meta(self):
        return self.meta.pack()

    def visualize_transformations(self, cmap='nipy_spectral', transformations: list = None):
        if transformations is None:
            transformations = self.transformations
        return self.generator.visualize_transformations(transformations, cmap)

    def transform(self, datapoint):
        for transformation in self.transformations:
            datapoint = transformation.transform(datapoint)
        return datapoint

    def add_transformation(self, transformation):
        self.transformations.append(transformation)

    def load_dataset(self, training_files_in, validate_files_in, test_files_in):
        training_init = bGPT_train(training_files_in, validate_files_in, test_files_in)
