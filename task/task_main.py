from luigi_app.task.common.task import Task
from luigi_app.task.common.task_upload_to_s3 import TaskUploadToS3


class TaskMain(Task):

    def requires(self):
        return TaskUploadToS3(self.date)
