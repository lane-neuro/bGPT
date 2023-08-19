import math
import os
import random
import numpy as np

import tiktoken

from engine.bGPT_engine import bGPT_engine
from engine.tranformation_lib.JitterTransform import JitterTransform
from engine.tranformation_lib.PerspectiveTransform import PerspectiveTransform
from engine.tranformation_lib.RotateTransform import RotateTransform
from engine.tranformation_lib.ScaleTransform import ScaleTransform
from engine.tranformation_lib.TranslateTransform import TranslateTransform

from engine.tranformation_lib.RandomResampleFps import RandomResampleFps

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

block_size = 1024
batch_size = 8

datasets_dictionary = bGPT_aid().make_datasets_dictionary(test_files[:1],
                                                          "mouse", 60, True)
scanners_dictionary = {key:{'scanners':{i:{'start':None, 'end':None} for i in range(0,batch_size)},
                            'length_meta':None,
                            'length_pose':None,
                            'window_width':None} for key in datasets_dictionary}

## initialize scanners, test functions ##
for key in datasets_dictionary:
    print('################### scanner functions ####################')
    print(key, ":", datasets_dictionary[key])

    scanner_dict = scanners_dictionary[key]

    bgpt_engine = bGPT_engine(csv_path=key,
                              animal=datasets_dictionary[key][0],
                              framerate=datasets_dictionary[key][1],
                              use_likelihood=datasets_dictionary[key][2],
                              bodyparts=datasets_dictionary[key][3],
                              verbose=False)

    metadata = bgpt_engine.pack_meta()

    pose = bgpt_engine.pack_generator()
    enc_pose = enc.encode_ordinary(pose)

    tokenization_compression_ratio = len(enc_pose)/len(pose)

    window_width = round(block_size * tokenization_compression_ratio + 0.1)

    scanners_dictionary[key]['window_width'] = window_width

    scanner_dict['length_meta'] = len(metadata)
    scanner_dict['length_pose'] = len(pose)

    scanner_start_positions = np.arange(0, len(pose), len(pose)/8)
    scanner_start_positions = [round(i) for i in scanner_start_positions]

    for ikey in scanner_dict['scanners']:
        scanner_dict['scanners'][ikey]['start'] = scanner_start_positions[ikey]
        scanner_dict['scanners'][ikey]['end'] = scanner_start_positions[ikey] + window_width

    print('scanner_dict:', scanner_dict)

    print('###############################################')
    print()

## test training functions ##
for key in datasets_dictionary:
    print('################### training functions ####################')
    print(key, ":", datasets_dictionary[key])

    scanner_dict = scanners_dictionary[key]

    for scanner in scanner_dict['scanners']:
        start = scanner_dict['scanners'][scanner]['end'] - scanner_dict['window_width']
        end = scanner_dict['scanners'][scanner]['end']

        random_transforms = [JitterTransform(0.05, 0.2, .5),
                             ScaleTransform(0.5, 1.5, .5),
                             RotateTransform(0, 2 * math.pi, .5),
                             TranslateTransform([0, 1000], [0, 1000], .5),
                             PerspectiveTransform(0.00001, 0.00005, .5)]
        r_indices = random.sample(range(len(random_transforms)), k=len(random_transforms))

        fps = datasets_dictionary[key][1]
        r_fps = RandomResampleFps(fps, 0.5).transform()
        print(f'fps: {fps}, r_fps: {r_fps}')

        bgpt_engine = bGPT_engine(csv_path=key,
                                  animal=datasets_dictionary[key][0],
                                  framerate=fps,
                                  use_likelihood=datasets_dictionary[key][2],
                                  bodyparts=datasets_dictionary[key][3],
                                  coordinate_system=datasets_dictionary[key][4],
                                  image_transformations=random_transforms,
                                  resample_fps=r_fps,
                                  start_index=start,
                                  end_index=end,
                                  verbose=True)

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

        break
