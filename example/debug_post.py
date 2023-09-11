import os
import time
from src.bGPT import bGPT
import glob
from src.engine.datastorage.dataset_engine import dataset_engine

# test dataset_engine
print(os.getcwd())

batch_size = 8
block_size = 1024
n_chars_per_bodypart = 8
animal = 'mouse'
framerate = 60
csv_paths = glob.glob('example/test/datasets/*.csv')[:1]
print(csv_paths)

# Time the instantiation of dataset_engine
start_time = time.time()
ds_engine = dataset_engine(csv_paths=csv_paths,
                           batch_size=batch_size,
                           block_size=block_size,
                           n_chars_per_bodypart=n_chars_per_bodypart,
                           animal=animal,
                           framerate=framerate)
elapsed_time = time.time() - start_time
print(f"Time taken to instantiate dataset_engine: {elapsed_time} seconds")

print(f"Possible combinations ds_engine {ds_engine.possible_combinations}")


proj_path = os.getcwd() + "\\example\\test"
os.chdir(proj_path)

test_project = bGPT.load_project(bGPT(), proj_path)
