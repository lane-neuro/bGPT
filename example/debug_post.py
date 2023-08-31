import os
from src.bGPT import bGPT

proj_path = os.getcwd() + "\\example\\test"
os.chdir(proj_path)

test_project = bGPT().load_project(proj_path)

