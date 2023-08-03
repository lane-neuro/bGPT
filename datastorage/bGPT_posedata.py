import csv
from copy import deepcopy

from datastorage import bGPT_metadata
from datastorage.bGPT_frame import bGPT_frame
from engine import bGPT_engine


class bGPT_posedata:
    def __init__(self, meta: bGPT_metadata, csv_path: str, use_likelihood):
        self.use_likelihood = use_likelihood
        self.meta = meta
        self.csv_path = csv_path
        self.frames = []
        print(f"bGPT_posedata: pose storage initialized")

    def __repr__(self):
        return f"bGPT_posedata:(\'{self.pack()}\')"

    def pack(self):
        pose_out = ""
        if self.meta.end_index == 0:
            self.meta.end_index = len(self.frames)

        for iframe in self.frames:
            rounded_frame = self.round_frame(iframe)
            frame_str = "~"
            for coord in rounded_frame.coords:
                if self.use_likelihood:
                    frame_str += f"{coord.x}_{coord.y}_{coord.likelihood},"
                else:
                    frame_str += f"{coord.x}_{coord.y},"
            pose_out += frame_str.rstrip(',')  # Remove trailing comma if present
        return pose_out

    def round_frame(self, frame):
        # Create a deep copy so that the original data isn't modified
        rounded_frame = deepcopy(frame)
        for coord in rounded_frame.coords:
            coord.x = round(coord.x, 3)
            coord.y = round(coord.y, 3)
            if self.use_likelihood:
                coord.likelihood = round(coord.likelihood, 3)
            else:
                coord.likelihood = None  # You can set it to None or just not store it at all.
        return rounded_frame

    def extract_csv(self):
        with open(self.csv_path, mode='r') as file:
            csv_file = csv.reader(file)

            for i, row in enumerate(csv_file, -3):
                if self.meta.body_parts_count == 0:
                    self.meta.body_parts_count = (len(row) - 1) / (3 if self.use_likelihood else 2)
                if i >= 0:
                    self.frames.extend([bGPT_frame(self.use_likelihood, row[:])])
        print(
            f"bGPT_posedata: \'{self.meta.animal}\' .csv file extracted for {self.meta.body_parts_count} coordinates across {len(self.frames)} frames.")

    def transform(self, engine: bGPT_engine):
        for iframe in self.frames:
            iframe.transform(engine)
        return self
