import torch
import pandas as pd
import warnings

from bGPT import bGPT_output


class posedata:
    def __init__(self, csv_path: str, csv_type: str, verbose: bool = False):
        self.csv_path: str = csv_path
        self.csv_type = csv_type
        self.verbose = verbose

        self.tensor, self.bodyparts = self.extract_csv()

        if self.verbose:
            bGPT_output("posedata", "info", f"storage initialized")
            bGPT_output("posedata", "info", f"Bodyparts: {self.bodyparts}")
            bGPT_output("posedata", "info", f"Tensor shape: {self.tensor.shape}")

    def extract_dlc_csv(self):
        def open_dlc_csv(csv_path):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                df = pd.read_csv(csv_path)

                # set the second row as the columns and drop columns and first row
                df.columns = df.iloc[0]
                df = df.drop(df.index[0:2])

                # drop the first column
                df = df.drop(df.columns[0], axis=1)

                # drop every third column, which is the likelihood, avoid dropping same name columns by using indexing
                # get indexes to keep
                drop_columns_index = range(2, len(df.columns), 3)
                keep_columns_index = [i for i in range(len(df.columns)) if i not in drop_columns_index]

                # drop by index
                df = df.iloc[:, keep_columns_index]

                return df

        def convert_dlc_csv_to_tensor(df):
            df_tensor = torch.tensor(df.values.astype('float32'), dtype=torch.float32)

            return df_tensor

        csv_path = self.csv_path
        df = open_dlc_csv(csv_path)
        tensor = convert_dlc_csv_to_tensor(df)
        bodyparts = [col for col in df.columns[::2]]
        return tensor, bodyparts

    def extract_csv(self):
        if self.csv_type == "DLC":
            tensor, bodyparts = self.extract_dlc_csv()
        return tensor, bodyparts
