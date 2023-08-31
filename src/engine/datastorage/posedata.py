import torch
import pandas as pd

class posedata:
    def __init__(self, meta, verbose):
        self.meta = meta
        self.verbose = verbose
        self.csv_path = self.meta.csv_path

        if self.meta.is_dlc:
            tensor, bodyparts = self.extract_dlc_csv()
            self.tensor = tensor
            self.bodyparts = bodyparts

        meta_bodyparts = self.meta.bodyparts
        if meta_bodyparts is not None:
            ## check if length of bodyparts is the same as meta bodyparts
            if len(meta_bodyparts) != len(self.bodyparts):
                raise ValueError(f"posedata: Bodyparts in metadata ({len(meta_bodyparts)}) does not match bodyparts in DLC csv ({len(bodyparts)})")
            else:
                ## overwrite self.body_parts with meta bodyparts
                self.bodyparts = meta_bodyparts

        if self.verbose:
            print(f"posedata: posedata storage initialized")
            print(f"posedata: Bodyparts: {self.bodyparts}")
            print(f"posedata: Tensor shape: {self.tensor.shape}")

    def extract_dlc_csv(self):
        def open_dlc_csv(csv_path):
            df = pd.read_csv(csv_path)

            ## set the second row as the columns and drop columns and first row
            df.columns = df.iloc[0]
            df = df.drop(df.index[0:2])

            ## drop the first column
            df = df.drop(df.columns[0], axis=1)

            ## drop every third column, which is the likelihood, avoid dropping same name columns by using indexing
            ## get indexes to keep
            drop_columns_index = range(2, len(df.columns), 3)
            keep_columns_index = [i for i in range(len(df.columns)) if i not in drop_columns_index]

            ## drop by index
            df = df.iloc[:, keep_columns_index]

            return df

        def convert_dlc_csv_to_tensor(df):
            df_tensor = torch.tensor(df.values.astype('float32'), dtype=torch.float32)
            return df_tensor
        csv_path = self.csv_path
        df = open_dlc_csv(csv_path)
        tensor = convert_dlc_csv_to_tensor(df)
        bodyparts = df.columns[::2]
        return tensor, bodyparts
