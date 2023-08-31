import configparser
import os


class bGPT:
    # file locations
    config_path = "/bgpt_config.ini"
    OUTPUT_FOLDER = "/output"
    DATASETS_FOLDER = "/datasets"
    CONFIG = None

    # project information
    project_name = None
    project_path = None
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
        return

    def new_project(self, project_name: str, project_path: str):
        self.project_name = project_name
        self.project_path = project_path

        # if project already exists in path, throw error and terminate session
        if os.path.exists(self.project_path + '\\' + self.project_name):
            print(f"[bGPT] ERROR: Provided project name is already a directory in provided path. "
                  f"Please provide a project name that has not yet been created. Terminating session.")
            return
        else:
            self.project_path = self.project_path + '\\' + self.project_name
            os.mkdir(self.project_path)
            os.chdir(self.project_path)
            os.mkdir(self.project_path + self.OUTPUT_FOLDER)  # create output folder in path
            os.mkdir(self.project_path + self.DATASETS_FOLDER)  # create datasets folder in path
            print(f"[bGPT] new project directory created for \'{project_name}\' at \'{project_path}\'")

            self.CONFIG = configparser.ConfigParser()   # create config file in path
            self.CONFIG[self.DEFAULT_section] = {self.NAME: self.project_name,
                                                 self.PATH: self.project_path,
                                                 self.SCHEDULER: 'none',
                                                 self.GPT_MODEL: 'none'}
            self._save_config()
            return self

    def load_project(self, project_path: str):
        if not os.path.exists(project_path):  # if path does not exist, terminate session and print error
            print(f"[bGPT] ERROR: Provided path is not a valid directory. Terminating session.")
            return
        else:  # check if path exists
            os.chdir(project_path)
            self.project_path = project_path
            self._load_config(self.project_path + self.config_path)
            print(f"[bGPT] project loaded: {self.project_name}")
            return self

    def save_project(self):
        self._save_config()
        print(f"[bGPT] project saved: {self.project_name}")
        return

    def _load_config(self, config_path: str):
        if not os.path.exists(config_path):  # if path does not exist, terminate session and print error
            print(f"[bGPT] ERROR: Project path does not contain a valid configuration file. Terminating session.")
            return
        else:  # if path exists
            self.CONFIG = configparser.ConfigParser()
            self.CONFIG.read(config_path)

            self.project_name = self.CONFIG[self.DEFAULT_section][self.NAME]
            self.project_path = self.CONFIG[self.DEFAULT_section][self.PATH]
            self.project_scheduler = self.CONFIG[self.DEFAULT_section][self.SCHEDULER]
            self.active_gpt_model = self.CONFIG[self.DEFAULT_section][self.GPT_MODEL]

            print(f"[bGPT] config loaded for project: {self.project_name}")
            return

    def _save_config(self):
        with open(self.project_path + self.config_path, 'w') as configfile:
            self.CONFIG.write(configfile)
        print(f"[bGPT] config saved for project: {self.project_name}")

    def make_datasets_dictionary(self, files: list,
                                 animal: str, fps: int, use_likelihood,
                                 bodyparts=None, coordinate_system="xy"):
        print("bGPT_aid: making dictionary")

        dict = {}
        for file in files:
            dict[file] = [animal, fps, use_likelihood, bodyparts, coordinate_system]

        return dict
