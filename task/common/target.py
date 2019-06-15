import luigi
import boto3
import botocore.exceptions

S3_BUCKET = "test-bucket"
S3_KEY_TEMPLATE = 'luigi/{date}/{task_family}'


class DefaultTarget(luigi.Target):
    def __init__(self, date, task_family):
        self.s3_bucket = S3_BUCKET
        self.s3_key = S3_KEY_TEMPLATE.format(
            date=date,
            task_family=task_family
        )
        self.s3_client = boto3.client("s3")

    def exists(self) -> bool:
        return self._s3_exits()

    def touch(self):
        self._s3_touch()

    def _s3_exits(self):
        try:
            self.s3_client.head_object(Bucket=self.s3_bucket, Key=self.s3_key)
            return True
        except botocore.exceptions.ClientError as err:
            if err.response.get('Error', {}).get('Message') == 'Not Found':
                return False
            raise

    def _s3_touch(self):
        self.s3_client.put_object(Bucket=self.s3_bucket, Key=self.s3_key, Body=b"")
