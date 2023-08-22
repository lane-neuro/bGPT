import csv
from copy import deepcopy
from itertools import islice

from engine.datastorage import bGPT_metadata
from engine.datastorage.bGPT_frame import bGPT_frame
from engine import bGPT_engine


class bGPT_posedata:
    def __init__(self, meta: bGPT_metadata, verbose):
        self.meta = meta
        self.verbose = verbose
        self.frames = []
        self.frame_resample_by = self.meta.frame_resample_by
        self.start_index = self.meta.start_index
        self.end_index = self.meta.end_index
        if self.end_index is not None:
            self.end_index = int(self.end_index * self.frame_resample_by)
        if self.verbose:
            print(f"bGPT_posedata: pose storage initialized")
            print(f"bGPT_posedata: frame resample by {self.frame_resample_by}")
            print(f"bGPT_posedata: start index {self.start_index}, end index {self.end_index}")

    def __repr__(self):
        return f"bGPT_posedata:(\'{self.pack()}\')"

    def pack(self):
        pose_out = ""
        if self.meta.end_index == 0:
            self.meta.end_index = len(self.frames)

        for iframe in self.frames:
            rounded_frame = self.round_frame(iframe)
            frame_str = "<"
            for coord in rounded_frame.coords:
                x_str = "{:08.3f}".format(coord.x)
                y_str = "{:08.3f}".format(coord.y)
                if self.meta.use_likelihood:
                    likelihood_str = "{:07.3f}".format(coord.likelihood)
                    frame_str += f"{x_str} {y_str} {likelihood_str}_"
                else:
                    frame_str += f"{x_str} {y_str}_"
            frame_str += ">"
            pose_out += frame_str.rstrip(',')  # Remove trailing comma if present
        return pose_out

    def round_frame(self, frame):
        # Create a deep copy so that the original data isn't modified
        rounded_frame = deepcopy(frame)
        for coord in rounded_frame.coords:
            coord.x = round(coord.x, 3)
            coord.y = round(coord.y, 3)
            if self.meta.use_likelihood:
                coord.likelihood = round(coord.likelihood, 3)
            else:
                coord.likelihood = None  # You can set it to None or just not store it at all.
        return rounded_frame

    def extract_csv(self):
        with open(self.meta.csv_path, mode='r') as file:
            csv_file = csv.reader(file)

            for i, row in enumerate(csv_file):
                if i == 1:
                    all_bodyparts = row[1:]
                    csv_file.__next__()
                    break

            if self.meta.bodyparts is not None:
                subset_indices = []
                for i, bodypart in enumerate(all_bodyparts):
                    if bodypart in self.meta.bodyparts:
                        subset_indices.append(i)
                subset_indices = [i+1 for i in subset_indices]
            else:
                subset_indices = [i+1 for i in range(0, len(all_bodyparts))]
                self.meta.bodyparts = all_bodyparts[::3]
            subset_indices.insert(0, 0)

            if self.verbose:
                print('Subset indices:', subset_indices)
                print('self.meta.bodyparts', self.meta.bodyparts)

            for row in islice(csv_file, self.start_index, self.end_index, self.frame_resample_by):
                self.frames.extend([bGPT_frame(self.meta.use_likelihood, row[:])])

        if self.verbose:
            print(f"bGPT_posedata: \'{self.meta.animal}\' .csv file extracted for {self.meta.bodyparts} coordinates across {len(self.frames)} frames.")

    def transform(self, engine: bGPT_engine):
        for iframe in self.frames:
            iframe.transform(engine)
        return self
