import configparser
import os

from scheduler import scheduler


def bGPT_output(class_name: str, message_type: str, message_out: str):
    prefix = "[bGPT]"
    class_name = " (" + class_name + ") "
    message = prefix + class_name

    if message_type == "error":
        message = message + "ERROR: "
    elif message_type == "warning":
        message = message + "WARNING: "
    elif message_type == "info":
        message = message + "INFO: "
    else:
        message = message + "UNKNOWN: "

    message = message + message_out
    print(message)


class bGPT:

    def __init__(self):
        self.project_name = None

        # file locations
        self.config_path = "/bgpt_config.ini"
        self.OUTPUT_FOLDER = "/output"
        self.DATASETS_FOLDER = "/datasets"
        self.CONFIG = None

        # project information
        self.project_name = None
        self.project_path = None
        self.project_scheduler = None
        self.scheduler_size = None
        self.active_gpt_model = None

        # config section names
        self.DEFAULT_section = 'DEFAULT'

        # config section keys
        self.NAME = 'ProjectName'
        self.PATH = 'ProjectPath'
        self.SCHEDULER = 'Scheduler'
        self.SCHEDULER_SIZE = 'SchedulerSize'
        self.GPT_MODEL = 'GPTModel'
        return

    def new_project(self, project_name: str, project_path: str, scheduler_size: int = 8):
        self.project_name = project_name
        self.project_path = project_path
        self.scheduler_size = scheduler_size

        # if project already exists in path, throw error and terminate session
        if os.path.exists(self.project_path + '\\' + self.project_name):
            bGPT_output("bGPT.new_project()", "error",
                        "Provided project name is already a directory in provided path. Please provide a project name "
                        "that has not yet been created. Terminating session.")
            return
        else:
            self.project_path = self.project_path + '\\' + self.project_name
            os.mkdir(self.project_path)
            os.chdir(self.project_path)
            os.mkdir(self.project_path + self.OUTPUT_FOLDER)  # create output folder in path
            os.mkdir(self.project_path + self.DATASETS_FOLDER)  # create datasets folder in path
            bGPT_output("bGPT.new_project()", "info",
                        f"new project directory created for \'{project_name}\' at \'{project_path}\'")

            self.CONFIG = configparser.ConfigParser()  # create config file in path
            self.CONFIG[self.DEFAULT_section] = {self.NAME: self.project_name,
                                                 self.PATH: self.project_path,
                                                 self.SCHEDULER: 'none',
                                                 self.SCHEDULER_SIZE: 8,
                                                 self.GPT_MODEL: 'none'}
            self._save_config()
            return self

    def load_project(self, project_path: str):
        if not os.path.exists(project_path):  # if path does not exist, terminate session and print error
            bGPT_output("bGPT.load_project()", "error",
                        f"Provided path is not a valid directory. Terminating session.")
            return
        else:  # check if path exists
            os.chdir(project_path)
            self.project_path = project_path
            self._load_config(self.project_path + self.config_path)
            self.project_scheduler = scheduler(self.scheduler_size)

            bGPT_output("bGPT.load_project()", "info",
                        f"project loaded: {self.project_name}")
            return self

    def save_project(self):
        self._save_config()
        bGPT_output("bGPT.save_project()", "info",
                    f"project saved: {self.project_name}")
        return

    def _load_config(self, config_path: str):
        if not os.path.exists(config_path):  # if path does not exist, terminate session and print error
            bGPT_output("bGPT._load_config()", "error",
                        "Project path does not contain a valid configuration file. Terminating session.")
            return
        else:  # if path exists
            self.CONFIG = configparser.ConfigParser()
            self.CONFIG.read(config_path)

            self.project_name = self.CONFIG[self.DEFAULT_section][self.NAME]
            self.project_path = self.CONFIG[self.DEFAULT_section][self.PATH]
            self.project_scheduler = self.CONFIG[self.DEFAULT_section][self.SCHEDULER]
            self.scheduler_size = self.CONFIG[self.DEFAULT_section][self.SCHEDULER_SIZE]
            self.active_gpt_model = self.CONFIG[self.DEFAULT_section][self.GPT_MODEL]

            bGPT_output("bGPT._load_config()", "info",
                        f"config loaded for project: {self.project_name}")
            return

    def _save_config(self):
        with open(self.project_path + self.config_path, 'w') as configfile:
            self.CONFIG.write(configfile)
        bGPT_output("bGPT._save_config()", "info",
                    f"[bGPT] config saved for project: {self.project_name}")

    def make_datasets_dictionary(self, files: list,
                                 animal: str, framerate: int, csv_type: int,
                                 bodyparts=None, coordinate_system="xy"):
        ## out dated should replace ##
        dictionary = {}
        for file in files:
            dictionary[file] = [animal, framerate, bodyparts, coordinate_system]

        return dictionary
