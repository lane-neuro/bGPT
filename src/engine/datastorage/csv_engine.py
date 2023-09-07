from src.engine.datastorage.posedata import posedata


class csv_engine:
    meta = None

    def __init__(self, csv_path, csv_type, verbose):
        self.pose = posedata(csv_path=csv_path,
                             csv_type=csv_type,
                             verbose=verbose)

        self.tensor, self.bodyparts = self.pose.extract_csv()

    def num_pack(self, row_indices):
        return self.tensor[row_indices[0]:row_indices[1]]

    def pack_meta(self):
        return self.meta.pack()

    def return_tensor(self):
        return self.tensor

    def return_bodyparts(self):
        return self.bodyparts
