import sys
import math
import os

from bGPT_generator import bGPT_generator
from engine.tranformation_lib.JitterTransform import JitterTransform
from engine.tranformation_lib.OpticalDistortTransform import OpticalDistortTransform
from engine.tranformation_lib.PerspectiveTransform import PerspectiveTransform
from engine.tranformation_lib.RotateTransform import RotateTransform
from engine.tranformation_lib.ScaleTransform import ScaleTransform
from engine.tranformation_lib.TranslateTransform import TranslateTransform

print("cwd: ", os.getcwd())
datesets_dir = os.getcwd() + "/test/datasets/"
test_file = ("8-30-2021-2-08 PM-Mohammad-ETHSensor-CB3-3_reencodedDLC_resnet50_odor-arenaOct3shuffle1_200000_filtered"
             ".csv")

generator = bGPT_generator(animal="mouse",
                           framerate=60,
                           csv_path=datesets_dir + test_file,
                           use_likelihood=False)
jitter = JitterTransform()
scale = ScaleTransform(1.5)
rotate = RotateTransform(math.radians(180))
translate = TranslateTransform(100, 100)
optical_distortion = OpticalDistortTransform(generator.pose.frames, 5e-10)
perspective = PerspectiveTransform()

print(generator.pose.pack()[:100])

generator.visualize_transformations([jitter, scale, rotate, translate, optical_distortion, perspective])
