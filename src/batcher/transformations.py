import matplotlib.pyplot as plt


class transformations:

    def __init__(self):
        self.trans_list = None

    def transform(self, *args):
        self.trans_list = list(args)
        # self.engine = csv_engine(transformations)
        self.pose.transform()
        self.pose.frames = _ShiftTransform(self.pose.frames)
        return repr(self)

    def visualize_transformations(self, trans_in: list, cmap='nipy_spectral'):
        trans_in.append('')

        plt.figure(figsize=(10, 10))

        # Create a colormap based on the number of transformations
        colormap = plt.get_cmap(cmap, len(trans_in) + 1)

        # Plot the original data first
        x_original = []
        y_original = []
        for frame in self.pose.frames:
            for coord in frame.coords:
                x_original.append(coord.x)
                y_original.append(coord.y)
        plt.scatter(x_original, y_original, color=colormap(0), label='Original', s=1,
                    alpha=0.5)  # Using the first color of colormap

        current_frames = self.pose.frames

        # Apply each transformation in transformations then plots
        for i, transformation in enumerate(trans_in):
            if self.verbose:
                print(i, transformation)

            transformed_x = []
            transformed_y = []

            # Apply the transformation to current_frames
            for frame in current_frames:
                for coord in frame.coords:
                    transformed_coord = transformation.transform(coord)
                    transformed_x.append(transformed_coord.x)
                    transformed_y.append(transformed_coord.y)
                    coord.x = transformed_coord.x  # Update the coordinate for the next transformation
                    coord.y = transformed_coord.y

            if i == len(trans_in) - 2:
                trans_in[-1] = _ShiftTransform(current_frames)

            # Plot the transformed coordinates using the next color in the colormap
            plt.scatter(transformed_x, transformed_y, color=colormap(i + 1),
                        label=str(transformation.__repr__()), s=1,
                        alpha=0.75)

        plt.title("Visualization of Transformations")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.legend(loc='upper right', markerscale=5)
        plt.axis('equal')
        plt.grid(True)
        plt.show()


class _ShiftTransform:
    def __init__(self, pose_frames):
        x_vals = [coord.x for frame in pose_frames for coord in frame.coords]
        y_vals = [coord.y for frame in pose_frames for coord in frame.coords]

        self.shift_x = abs(min(x_vals)) if min(x_vals) < 0 else 0
        self.shift_y = abs(min(y_vals)) if min(y_vals) < 0 else 0

    def __repr__(self):
        return f"ShiftTransform, shift_x = {self.shift_x}, shift_y = {self.shift_y}"

    def transform(self, datapoint):
        datapoint.x += self.shift_x
        datapoint.y += self.shift_y
        return datapoint
