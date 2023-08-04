class ShiftTransform:
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