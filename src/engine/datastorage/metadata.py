import src.engine.csv_engine
import engine


class metadata:

    def __init__(self, engine_in: src.csv_engine, animal: str, csv_path: str, framerate: int, frame_resample_by: int,
                 bodyparts: list = None, coordinate_system: str = "xy", use_likelihood: bool = True,
                 verbose: bool = False, start_index: int = None, end_index: int = None):

        # stores the engine
        self.engine = engine_in
        self.verbose = verbose

        # stores metadata of the animal
        self.animal = animal
        self.bodyparts = bodyparts

        # stores metadata of the video
        self.csv_path = csv_path
        self.framerate = framerate
        self.frame_resample_by = frame_resample_by
        self.coordinate_system = coordinate_system
        self.use_likelihood = use_likelihood

        # stores current frame range
        self.start_index = start_index
        self.end_index = end_index

        if self.verbose:
            print(f"metadata: metadata storage initialized")

    def __repr__(self):
        return f"metadata:(Animal: \'{self.animal}\', Framerate: {self.framerate}fps, Start index: \'{self.start_index}\')"

    def pack(self):
        packed = f"{self.animal}~{self.framerate}~{self.coordinate_system}"
        bodyparts_str = ','.join(self.bodyparts)
        packed = f"{packed}~{bodyparts_str}~"
        return packed

    def modify_bodypart_name(self, index, name):
        prior_name = self.bodyparts[index]
        self.bodyparts[index] = name
        if self.verbose:
            print(f"metadata: Bodypart [{index}](\'{prior_name}\') renamed to \'{name}\'")

    def set_start_index(self, index):
        self.start_index = index
        if self.verbose:
            print(f"metadata: Start index set to {index}")

    def set_end_index(self, index):
        self.end_index = index
        if self.verbose:
            print(f"metadata: End index set to {index}")

    def set_framerate(self, framerate):
        self.framerate = framerate
        if self.verbose:
            print(f"metadata: Framerate set to {framerate}")