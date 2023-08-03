class OpticalDistortTransform:

    def __init__(self, pose_frames, K1=5e-10):
        x_vals = [coord.x for frame in pose_frames for coord in frame.coords]
        y_vals = [coord.y for frame in pose_frames for coord in frame.coords]

        self.x_center = (max(x_vals) + min(x_vals)) / 2
        self.y_center = (max(y_vals) + min(y_vals)) / 2

        # Calculate k1 based on your requirements.
        # Here, I've simply normalized it based on the image space,
        # but you might want to adjust this based on the desired distortion level.
        self.k1 = K1 * (max(x_vals) - min(x_vals))

    def __repr__(self):
        return f"OpticalDistortTransform, k1 = {self.k1}"

    def transform(self, datapoint):
        x = datapoint.x - self.x_center
        y = datapoint.y - self.y_center
        r2 = x ** 2 + y ** 2
        x_distorted = x * (1 + self.k1 * r2) + self.x_center
        y_distorted = y * (1 + self.k1 * r2) + self.y_center
        datapoint.x = x_distorted
        datapoint.y = y_distorted
        return datapoint
