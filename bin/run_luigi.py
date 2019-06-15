from datetime import timedelta, timezone, datetime

import luigi.cmdline
from luigi_app.task_main import TaskMain
from luigi_app.util.slack_client import Notifier


def get_yesterday() -> str:
    jst = timezone(timedelta(hours=+9), 'JST')
    yesterday = datetime.now(jst) - timedelta(days=1)
    return yesterday.date().isoformat()


def parse_date(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%d')


class NotificationContext:
    def __init__(self, task_name, date):
        self.notify = Notifier()
        self.task_name = task_name
        self.date = date

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None or (isinstance(exc_val, SystemExit) and exc_val.code == 0):
            self.notify.send_slack(
                f'{self.task_name} date={self.date} success',
                False
            )
        else:
            self.notify.send_slack(
                f'{self.task_name} date={self.date} failed\n'
                f'reason: {exc_type}, {exc_val}',
                True
            )


def main():
    yesterday = get_yesterday()
    date = parse_date(yesterday).date()
    with NotificationContext("TaskMain", date):
        luigi.build([TaskMain(date=date)], local_scheduler=True)


if __name__ == '__main__':
    main()
