import os
import boto3

from luigi_app.task.common.task import Task
from luigi_app.task.common.task_process import TaskProcess


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_DATA_DIR = os.path.join(BASE_DIR, "../../data/")
LOCAL_INPUT_PATH = os.path.join(LOCAL_DATA_DIR, "processed.csv")

S3_BUCKET = "test-luigi"
S3_KEY_TEMPLATE = '{date}/processed.csv'


class TaskUploadToS3(Task):

    def run(self):
        s3_resource = boto3.resource("s3")
        bucket = s3_resource.Bucket(S3_BUCKET)

        s3_key = S3_KEY_TEMPLATE.format(date=self.date)
        with open(LOCAL_INPUT_PATH, mode="rb") as file:
            bucket.put_object(Key=s3_key, Body=file)

    def requires(self):
        return TaskProcess(self.date)
