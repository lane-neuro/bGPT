import configparser
import os


class bGPT:
    # file locations
    config_path = "/bgpt_config.ini"
    project_path = None

    # project information
    project_name = None
    project_scheduler = None
    active_gpt_model = None

    # config section names
    DEFAULT_section = 'DEFAULT'

    # config section keys
    NAME = 'ProjectName'
    PATH = 'ProjectPath'
    SCHEDULER = 'Scheduler'
    GPT_MODEL = 'GPTModel'


    def __init__(self):
        print("[bGPT] empty constructor")

    def new_project(self, project_name: str, project_path: str):
        print(f"[bGPT] new project \'{project_name}\' at \'{project_path}\'")

    def load_project(self, project_path: str = os.getcwd()):
        if os.path.exists(project_path):  # check if path exists
            os.chdir(project_path)
        else:  # if path does not exist, terminate session and print error
            print(f"[bGPT] ERROR: Provided path is not a valid directory. Terminating session.")
            return
        print(f"[bGPT] load project at {project_path}")

    def load_config(self, config_path: str = os.getcwd() + "/bgpt_config.ini"):
        if os.path.exists(config_path):  # check if path exists
            config = configparser.ConfigParser()
            config.read(config_path)
            self.project_name = config[self.DEFAULT_section][self.NAME]
            print(f"[bGPT] config loaded for project: {self.project_name}")
        else:  # if path does not exist, terminate session and print error
            print(f"[bGPT] ERROR: Project path does not contain . Terminating session.")
            return

    def make_datasets_dictionary(self, files: list,
                                 animal: str, fps: int, use_likelihood,
                                 bodyparts=None, coordinate_system="xy"):
        print("bGPT_aid: making dictionary")

        dict = {}
        for file in files:
            dict[file] = [animal, fps, use_likelihood, bodyparts, coordinate_system]

        return dict
