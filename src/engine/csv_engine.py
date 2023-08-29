from src.engine.datastorage.metadata import metadata
from src.engine.generator import generator
from src.trainer import trainer


class csv_engine:
    def __init__(self, animal: str, framerate: int, csv_path: str,
                 bodyparts: list = None, coordinate_system: str = "xy",
                 image_transformations: list = None,
                 resample_fps: int = None, verbose: bool = False,
                 start_index: int = None, end_index: int = None):
        self.verbose = verbose
        self.resample_fps = resample_fps

        framerate = framerate
        frame_resample_by = 1
        if self.resample_fps is not None:
            frame_resample_by = framerate // self.resample_fps
            if verbose:
                print(
                    f"csv_engine: Resampling video to {self.resample_fps}fps, frames resample by {frame_resample_by}th index")
            framerate = self.resample_fps

        self.meta = metadata(self, animal, csv_path, framerate, frame_resample_by,
                             bodyparts, coordinate_system, verbose,
                             start_index, end_index)
        self.generator = generator(self.meta, verbose)

        if image_transformations is None:
            self.transformations = []
        else:
            self.transformations = image_transformations
        if verbose:
            print("csv_engine: transformation engine initialized")

    def __repr__(self):
        transformations = ', '.join([str(transform) for transform in self.transformations])
        return (f"generator:(\nMetadata:\'{self.meta}\',\n\nTransformations: [{transformations}],\n\nPose Tokens:"
                f"\'{self.pack_generator()}\', \n\nNumber of Pose Tokens: {len(self.pack_generator())})")

    def pack_generator(self, apply_transformations: bool = True):
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
        training_init = trainer(training_files_in, validate_files_in, test_files_in)