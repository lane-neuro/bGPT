import math
import os
import random

import tiktoken

from engine.bGPT_engine import bGPT_engine
from engine.tranformation_lib.JitterTransform import JitterTransform
from engine.tranformation_lib.PerspectiveTransform import PerspectiveTransform
from engine.tranformation_lib.RotateTransform import RotateTransform
from engine.tranformation_lib.ScaleTransform import ScaleTransform
from engine.tranformation_lib.TranslateTransform import TranslateTransform

from bGPT_aid import bGPT_aid

print("cwd: ", os.getcwd())
datesets_dir = os.getcwd() + "\\test\\example_datasets\\"
# array of dataset files in directory
test_files = os.listdir(datesets_dir)
# append datasets_dir to each file name
test_files = [datesets_dir + file for file in test_files]
print()

model_type = 'gpt2'
enc = tiktoken.get_encoding(model_type)

datasets_dictionary = bGPT_aid().make_datasets_dictionary(test_files,
                                                        "mouse", 60, True)
for key in datasets_dictionary:
    print('###############################################')
    print(key, ":", datasets_dictionary[key])

    random_transforms = [JitterTransform(0.05, 0.2, .5),
                         ScaleTransform(0.5, 1.5, .5),
                         RotateTransform(0, 2 * math.pi, .5),
                         TranslateTransform([0, 1000], [0, 1000], .5),
                         PerspectiveTransform(0.00001, 0.00005, .5)]
    r_indices = random.sample(range(len(random_transforms)), k=len(random_transforms))

    bgpt_engine = bGPT_engine(csv_path = key,
                              animal = datasets_dictionary[key][0],
                              framerate = datasets_dictionary[key][1],
                              use_likelihood = datasets_dictionary[key][2],
                              bodyparts = datasets_dictionary[key][3],
                              coordinate_system = datasets_dictionary[key][4],
                              transformations = random_transforms,
                              verbose = False)

    print('bGPT_engine:')

    metadata = bgpt_engine.pack_meta()
    print('metadata:', metadata)
    print('metadata length:', len(metadata))

    enc_metadata = enc.encode_ordinary(metadata)
    print('encoded metadata:', enc_metadata)
    print('encoded metadata length:', len(enc_metadata))

    print('ratio length metadata / length encoding data:', len(metadata) / len(enc_metadata))

    print('pose data:')
    pose = bgpt_engine.pack_generator()
    print('pose data length:', len(pose))

    print(pose[:100])
    print('...')
    print(pose[-100:])

    print('encoding pose data:')
    enc_pose = enc.encode_ordinary(pose)
    print('encoded pose data length:', len(enc_pose))
    print(enc_pose[:100])
    print('...')
    print(enc_pose[-100:])

    print('ratio length pose data / length encoding data:', len(pose) / len(enc_pose))

    print('visualizing transformations...')
    bgpt_engine.visualize_transformations()

    print('###############################################')
    print()

