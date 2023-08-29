import math
import os
import random
import re
from itertools import islice

import numpy as np
import tiktoken

from src.bGPT_aid import bGPT_aid
from src.engine.csv_engine import csv_engine
from src.tranformation_lib.JitterTransform import JitterTransform
from src.tranformation_lib.PerspectiveTransform import PerspectiveTransform
from src.tranformation_lib.RandomResampleFps import RandomResampleFps
from src.tranformation_lib.RotateTransform import RotateTransform
from src.tranformation_lib.ScaleTransform import ScaleTransform
from src.tranformation_lib.TranslateTransform import TranslateTransform

print("cwd: ", os.getcwd())
datasets_dir = os.getcwd() + "/example/datasets/"
# array of dataset files in directory
test_files = os.listdir(datasets_dir)
# append datasets_dir to each file name
test_files = [datasets_dir + file for file in test_files]
print()

model_type = 'gpt2'
enc = tiktoken.get_encoding(model_type)

block_size = 1024
batch_size = 8

datasets_dictionary = bGPT_aid().make_datasets_dictionary(test_files[:2],
                                                          "mouse", 60, False)
scanners_dictionary = {key: {'scanners': {i: {'start': None, 'end': None} for i in range(0, batch_size)},
                             'length_meta': None,
                             'length_pose': None,
                             'window_width': None} for key in datasets_dictionary}


def count_characters_and_check_expected(pose_out, expected_length=None):
    # Find all substrings enclosed between < and >
    frames = re.findall(r'<(.*?)>', pose_out)

    # If expected_length is not provided, use the length of the first frame
    if expected_length is None and frames:
        expected_length = len(frames[0])

    disc = []
    for iFrame in frames:
        if len(iFrame) != expected_length:
            disc.append((len(iFrame), iFrame))

    return len(frames), disc


# initialize scanners, test functions
for key in datasets_dictionary:
    print('################### scanner functions ####################')
    print(key, ":", datasets_dictionary[key])

    scanner_dict = scanners_dictionary[key]

    bgpt_engine = csv_engine(csv_path=key,
                             animal=datasets_dictionary[key][0],
                             framerate=datasets_dictionary[key][1],
                             bodyparts=datasets_dictionary[key][3],
                             verbose=False)

    metadata = bgpt_engine.pack_meta()
    len_metadata = len(metadata)
    print('metadata:', metadata)
    enc_metadata = enc.encode_ordinary(metadata)
    len_enc_metadata = len(enc_metadata)
    print('len_enc_metadata:', len_enc_metadata)

    bodyparts = metadata.split('~')[-2]
    bodyparts = [s for s in bodyparts.split(',')]
    len_bodyparts = len(bodyparts)
    print('bodyparts:', bodyparts)
    print('len_bodyparts:', len_bodyparts)

    pose = bgpt_engine.pack_generator()
    enc_pose = enc.encode_ordinary(pose)
    len_pose = len(pose)
    len_enc_pose = len(enc_pose)

#    tokenization_compression_ratio = len_enc_pose / len_pose

    with open(key, 'r') as file:
        nrows_csv = sum(1 for _ in islice(file, 3, None))
    print('nrows_csv:', nrows_csv)

    total_frames, discrepancies = count_characters_and_check_expected(pose)
    print('total_frames:', total_frames)
    print('discrepancies:', discrepancies)
    for length, frame in discrepancies:
        print(f"Length: {length}, Frame: <{frame}>")

    characters_per_row = math.ceil(len_pose / nrows_csv)
    print('pose:', pose[:characters_per_row])
    enc_characters_per_row = len_enc_pose / nrows_csv
    print('enc_pose:', enc_pose[:math.ceil(enc_characters_per_row)])

    characters_per_bodypart = int((characters_per_row - 2) / len_bodyparts)  ## should always be 18
    if characters_per_bodypart != 18:
        print('ERROR: characters_per_bodypart != 18')

#    window_width = math.ceil(block_size / (characters_per_row * tokenization_compression_ratio))
#    print('window_width =', window_width, '; characters per row =', characters_per_row, '; characters per bodypart =',
#          characters_per_bodypart)
#    print('enc_characters_per_row =', enc_characters_per_row, '; tokenization_compression_ratio =',
#          tokenization_compression_ratio)
#    nframes_enc_block = (block_size - len_enc_metadata) / enc_characters_per_row
#    print('nframes_enc_block =', nframes_enc_block)

#    scanners_dictionary[key]['window_width'] = window_width

    scanner_dict['length_meta'] = len_metadata
    scanner_dict['length_pose'] = len_pose

    scanner_start_positions = np.arange(0, len_pose, len_pose / 8)
    scanner_start_positions = [round(i) for i in scanner_start_positions]

    for ikey in scanner_dict['scanners']:
        scanner_dict['scanners'][ikey]['start'] = scanner_start_positions[ikey]
        scanner_dict['scanners'][ikey]['end'] = scanner_start_positions[ikey] #+ window_width

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

        bgpt_engine = csv_engine(csv_path=key,
                                 animal=datasets_dictionary[key][0],
                                 framerate=fps,
                                 use_likelihood=datasets_dictionary[key][2],
                                 bodyparts=datasets_dictionary[key][3],
                                 coordinate_system=datasets_dictionary[key][4],
                                 image_transformations=random_transforms,
                                 resample_fps=r_fps,
                                 start_index=start,
                                 end_index=end,
                                 verbose=False)

        print('csv_engine:')

        metadata = bgpt_engine.pack_meta()
        print('metadata:', metadata)
        print('metadata length:', len(metadata))

        enc_metadata = enc.encode_ordinary(metadata)
        length_enc_metadata = len(enc_metadata)
        print('encoded metadata:', enc_metadata)
        print('encoded metadata length:', length_enc_metadata)

        print('ratio length metadata / length encoding data:', len(metadata) / len(enc_metadata))

        print('pose data:')
        pose = bgpt_engine.pack_generator()
        print('pose data length:', len(pose))

        print(pose[:100])
        print('...')
        print(pose[-100:])

        print('encoding pose data:')
        enc_pose = enc.encode_ordinary(pose)
        length_enc_pose = len(enc_pose)
        print('encoded pose data length:', length_enc_pose)
        print(enc_pose[:100])
        print('...')
        print(enc_pose[-100:])

        print('ratio length pose data / length encoding data:', length_enc_metadata / length_enc_pose)

        print('length enc_meta + enc_pose:', length_enc_metadata + length_enc_pose)

        enc_pose_finish_index = block_size - length_enc_metadata
        enc_pose_out = enc_pose[:enc_pose_finish_index]
        enc_pose_pred = enc_pose[enc_pose_finish_index + 1:enc_pose_finish_index + 2]
        enc_data = enc_metadata + enc_pose_out

        print('enc_data length:', len(enc_data))
        print('enc_data:', enc_data)
        print('enc_pose_pred:', enc_pose_pred)

        print('visualizing transformations...')
        bgpt_engine.visualize_transformations()

        print('###############################################')
        print()

        break
