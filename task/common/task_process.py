import os
import pandas as pd

from luigi_app.task.common.task import Task
from luigi_app.task.common.task_get_from_s3 import TaskGetFromS3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_DATA_DIR = os.path.join(BASE_DIR, "../../data")


class TaskProcess(Task):

    def run(self):
        input_path = os.path.join(LOCAL_DATA_DIR, "raw.csv")
        output_path = os.path.join(LOCAL_DATA_DIR, "processed.csv")
        df = pd.read_csv(input_path, header=None, sep=",")
        df[3] = df[1] + df[2]
        df = df.drop([1, 2], axis=1)
        df.to_csv(output_path, index=False, header=False)

    def requires(self):
        return TaskGetFromS3(self.date)
