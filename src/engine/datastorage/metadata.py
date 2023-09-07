from engine.datastorage import csv_engine


class metadata:

    def __init__(self, engine_in: csv_engine, animal: str, csv_path: str, framerate: int,
                 bodyparts: list = None, coordinate_system: str = "xy", csv_type: str = "DLC",
                 verbose: bool = False):

        # stores the engine
        self.engine = engine_in
        self.verbose = verbose
        self.csv_type = csv_type

        # stores metadata of the animal
        self.animal = animal
        self.bodyparts = bodyparts

        # stores metadata of the video
        self.csv_path = csv_path
        self.framerate = framerate
        self.coordinate_system = coordinate_system

        if self.verbose:
            print(f"metadata: metadata storage initialized")

    def __repr__(self):
        return f"metadata:(Animal: \'{self.animal}\', Framerate: {self.framerate}fps)"

    def pack(self):
        packed = f"{self.animal}~{self.framerate}fps~{self.coordinate_system}"
        bodyparts_str = ','.join(self.bodyparts)
        packed = f"{packed}~{bodyparts_str}~"
        return packed

    def framerate(self, framerate):
        self.framerate = framerate
        if self.verbose:
            print(f"metadata: Framerate set to {framerate}")