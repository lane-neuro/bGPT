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

print()

for test_file in test_files:
    print(test_file)


