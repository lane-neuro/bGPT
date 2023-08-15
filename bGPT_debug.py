import math
import os
import random

from engine.bGPT_engine import bGPT_engine
from engine.tranformation_lib.JitterTransform import JitterTransform
from engine.tranformation_lib.PerspectiveTransform import PerspectiveTransform
from engine.tranformation_lib.RotateTransform import RotateTransform
from engine.tranformation_lib.ScaleTransform import ScaleTransform
from engine.tranformation_lib.TranslateTransform import TranslateTransform

print("cwd: ", os.getcwd())
datesets_dir = os.getcwd() + "\\test\\example_datasets\\"
# array of dataset files in directory
test_files = os.listdir(datesets_dir)
# append datasets_dir to each file name
test_files = [datesets_dir + file for file in test_files]

# we need to update the transformations, to take a min/max of possible values and return with random in that range.
# random, that is how likely they are to be applied at all
jitter = JitterTransform(0.05, 0.2, .5)  # 0.05 - > 0.2 ; R = 0.25
scale = ScaleTransform(0.5, 1.5, .5)  # 0.5 -> 1.5 ; R = 0.25
rotate = RotateTransform(0, 2 * math.pi, .5)  # 0 - 360 ; R = 0.25
translate = TranslateTransform([0, 1000], [0, 1000], .5)  # 0 -> 1000, 0 -> 1000 ; R = 0.25
perspective = PerspectiveTransform(0.00001, 0.00005, .5)  # 0.00001 -> 0.00005 ; R = 0.25

random_transforms = [jitter,
                     scale,
                     rotate,
                     translate,
                     perspective]
r_indices = random.sample(range(len(random_transforms)), k=len(random_transforms))
random_transforms = [random_transforms[i] for i in r_indices]

print(bgpt_engine.pack_generator()[:100])

bgpt_engine.visualize_transformations(random_transforms)
# print(random.shuffle(random_transforms))
# print(random_transforms)

###

DATASETS_DICTIONARY = {s: ['mouse', 60, False, "nose, left ear, right ear, neck, body, tail base"] for s in test_files}
print(DATASETS_DICTIONARY)
