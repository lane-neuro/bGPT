from engine import bGPT_engine


class bGPT_metadata:

    def __init__(self, engine: bGPT_engine, animal: str, csv_path: str, framerate: int,
                 bodyparts: list = None, coordinate_system: str = "xy", use_likelihood: bool = True):

        # stores the engine
        self.engine = engine

        # stores metadata of the animal
        self.animal = animal
        self.bodyparts = bodyparts

        # stores metadata of the video
        self.csv_path = csv_path
        self.framerate = framerate
        self.coordinate_system = coordinate_system
        self.use_likelihood = use_likelihood

        # stores current frame range
        self.start_index = 0
        self.end_index = 0

        print(f"bGPT_metadata: metadata storage initialized")

    def __repr__(self):
        return f"bGPT_metadata:(Animal: \'{self.animal}\', Framerate: {self.framerate}fps, Start index: \'{self.start_index}\')"

    def modify_bodypart_name(self, index, name):
        prior_name = self.bodyparts[index]
        self.bodyparts[index] = name
        print(f"bGPT_metadata: Bodypart [{index}](\'{prior_name}\') renamed to \'{name}\'")

    def set_start_index(self, index):
        self.start_index = index
        print(f"bGPT_metadata: Start index set to {index}")

    def set_end_index(self, index):
        self.end_index = index
        print(f"bGPT_metadata: End index set to {index}")

    def set_framerate(self, framerate):
        self.framerate = framerate
        print(f"bGPT_metadata: Framerate set to {framerate}")