
import random

class RandomResampleFps:

    def __init__(self, fps, random_in):
        self.fps = fps
        self.random_in = random_in
        self.random_roll = random.uniform(0, 1)

    def find_closest_divisor(self):
        """
        Given an integer N and a ratio R (0 <= R <= 1),
        find a divisor of N closest to R*N.
        """
        R = random.uniform(0, 1)

        # Compute the target fps
        target_fps = R * self.fps

        # Find all divisors of N
        divisors = [i for i in range(1, self.fps + 1) if self.fps % i == 0]

        # Find the divisor closest to target_fps
        closest_divisor = min(divisors, key=lambda x: abs(x - target_fps))

        return closest_divisor

    def __repr__(self):
        return f"RandomResampleFps, fps = {self.fps}, r_in,r_roll = {self.random_in}, {self.random_roll}"

    def transform(self):
        if self.random_roll <= self.random_in:
            self.fps = self.find_closest_divisor()
        else:
            self.fps = None
        return self.fps