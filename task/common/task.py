import datetime

import luigi

from luigi_app.task.common import target


class Task(luigi.Task):
    date: datetime.date = luigi.DateParameter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.default_target = target.DefaultTarget(
            date=self.date,
            task_family=self.task_family,
        )

    @property
    def task_family(self):
        return self.get_task_family()

    def output(self):
        return [self.default_target]

    def on_success(self):
        self.default_target.touch()
