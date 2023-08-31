from src.engine.datastorage.metadata import metadata
from src.engine.datastorage.posedata import posedata

class csv_engine:
    def __init__(self, animal: str, framerate: int, csv_path: str,
                 bodyparts: list = None, coordinate_system: str = "xy",
                 csv_type: str = "DLC", verbose: bool = False):
        self.verbose = verbose

        self.pose = posedata(csv_path=csv_path,
                             csv_type=csv_type,
                             verbose=verbose)

        self.tensor, self.bodyparts = self.pose.extract_csv()

        # if bodyparts and self.bodyparts are not the same, but have the same length
        # overwrite self.bodyparts with bodyparts
        if bodyparts is not None:
            if len(bodyparts) == len(self.bodyparts):
                self.bodyparts = bodyparts
            else:
                raise ValueError("bodyparts passed in but self.bodyparts are not the same length")

        self.meta = metadata(self,
                             animal=animal,
                             csv_path=csv_path,
                             framerate=framerate,
                             bodyparts=self.bodyparts,
                             coordinate_system=coordinate_system,
                             verbose=verbose,
                             csv_type=csv_type)

    def pack_meta(self):
        return self.meta.pack()

    def return_tensor(self):
        return self.tensor

    def return_bodyparts(self):
        return self.bodyparts
