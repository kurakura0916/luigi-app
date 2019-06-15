import os
import boto3

from luigi_app.task.common.task import Task

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_DATA_DIR = os.path.join(BASE_DIR, "../../data/")

S3_BUCKET = "test-luigi"
S3_KEY_TEMPLATE = '{date}/test.csv'


class TaskGetFromS3(Task):

    def run(self):
        os.makedirs(LOCAL_DATA_DIR, exist_ok=True)
        s3_resource = boto3.resource("s3")
        bucket = s3_resource.Bucket(S3_BUCKET)

        s3_key = S3_KEY_TEMPLATE.format(date=self.date)
        input_path = os.path.join(LOCAL_DATA_DIR, os.path.basename("raw.csv"))
        bucket.download_file(s3_key, input_path)
