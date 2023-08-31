class bGPT:

    def __init__(self):
        print("[bGPT] initializing")

    def make_datasets_dictionary(self, files: list,
                                 animal: str, fps: int, use_likelihood,
                                 bodyparts=None, coordinate_system="xy"):
        print("bGPT_aid: making dictionary")

        dict = {}
        for file in files:
            dict[file] = [animal, fps, use_likelihood, bodyparts, coordinate_system]

        return dict
