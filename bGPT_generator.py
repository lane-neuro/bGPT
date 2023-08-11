from copy import deepcopy
import matplotlib.pyplot as plt

from datastorage.bGPT_metadata import bGPT_metadata
from datastorage.bGPT_posedata import bGPT_posedata
from engine.bGPT_engine import bGPT_engine
from engine.tranformation_lib.OpticalDistortTransform import OpticalDistortTransform
from engine.tranformation_lib.ShiftTransform import ShiftTransform


class bGPT_generator:

    def __init__(self, animal: str, framerate: int, csv_path: str, use_likelihood=True):
        self.use_likelihood = use_likelihood
        self.engine = bGPT_engine()
        self.meta = bGPT_metadata(animal, framerate, self.engine)
        self.pose = bGPT_posedata(self.meta, csv_path, self.use_likelihood)
        self.pose.extract_csv()

        ## special transformations for training that use full sequence information
        self.optical_distortion = OpticalDistortTransform(self.pose.frames)
        self.engine.add_transformation(self.optical_distortion)
        self.shift = ShiftTransform(self.pose.frames)
        self.engine.add_transformation(self.shift)

    def __repr__(self):
        transformations = ', '.join([str(transform) for transform in self.engine.transformations])
        return f"bGPT_generator:(\nMetadata:\'{self.meta}\',\n\nTransformations: [{transformations}],\n\nPose Tokens:\'{self.pose.pack()}\', \n\nNumber of Pose Tokens: {len(self.pose.pack())})"

    def transform(self, *args):
        transformations = list(args)
        self.engine = bGPT_engine(transformations)
        self.pose.transform(self.engine)
        return repr(self)

    def set_range(self, start_frame: int, end_frame: int):
        self.meta.start_index = start_frame
        self.meta.end_index = end_frame
        print(f"bGPT_generator: current data range set to {start_frame} : {end_frame}")

    def visualize_transformations(self, transformations, cmap='viridis'):
        plt.figure(figsize=(10, 10))

        # Create a colormap based on the number of transformations
        colormap = plt.get_cmap(cmap, len(transformations) + 2)

        # Plot the original data first
        x_original = []
        y_original = []
        for frame in self.pose.frames:
            for coord in frame.coords:
                x_original.append(coord.x)
                y_original.append(coord.y)
        plt.scatter(x_original, y_original, color=colormap(0), label='Original', s=1,
                    alpha=0.5)  # Using the first color of colormap

        current_frames = deepcopy(self.pose.frames)

        # Apply each transformation in sequence and plot
        for i, transform in enumerate(transformations):
            transformed_x = []
            transformed_y = []

            # Apply the transformation to current_frames
            for frame in current_frames:
                for coord in frame.coords:
                    transformed_coord = transform.transform(deepcopy(coord))
                    transformed_x.append(transformed_coord.x)
                    transformed_y.append(transformed_coord.y)
                    coord.x = transformed_coord.x  # Update the coordinate for the next transformation
                    coord.y = transformed_coord.y

            # Plot the transformed coordinates using the next color in the colormap
            plt.scatter(transformed_x, transformed_y, color=colormap(i + 1), label=str(transform.__repr__()), s=1,
                        alpha=0.5)

        # After applying all given transformations, apply the ShiftTransform
        shift_transform = ShiftTransform(current_frames)
        shifted_x = []
        shifted_y = []

        # Apply the shift transformation to current_frames
        for frame in current_frames:
            for coord in frame.coords:
                shifted_coord = shift_transform.transform(deepcopy(coord))
                shifted_x.append(shifted_coord.x)
                shifted_y.append(shifted_coord.y)
                coord.x = shifted_coord.x  # Update the coordinate for the next transformation
                coord.y = shifted_coord.y

        # Plot the shifted coordinates using the next color in the colormap
        plt.scatter(shifted_x, shifted_y, color=colormap(len(transformations) + 2),
                    label=str(shift_transform.__repr__()), s=1, alpha=0.5)

        plt.title("Visualization of Transformations")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.legend(loc='upper right', markerscale=5)
        plt.axis('equal')
        plt.grid(True)
        plt.show()
