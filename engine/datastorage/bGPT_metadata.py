from engine import bGPT_engine


class bGPT_metadata:

    def __init__(self, animal: str, framerate: int, engine: bGPT_engine):
        self.animal = animal
        self.body_parts_count = 0
        self.framerate = framerate
        self.engine = engine
        self.start_index = 0
        self.end_index = 0
        print(f"bGPT_metadata: metadata storage initialized")

    def __repr__(self):
        return f"bGPT_metadata:(Animal: \'{self.animal}\', Number of Body Parts: {self.body_parts_count}, Framerate:{self.framerate}fps)"

