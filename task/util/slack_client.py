import os
import slack
import logging


class SlackClient:
    def __init__(self, token):
        token = token or os.environ["SLACK_API_TOKEN"]
        self.client = slack.WebClient(token=token)

    def post(self, text: str, *, channel: str = "#notify", **kwargs) -> bool:
        response = self.client.chat_postMessage(
            channel=channel,
            text=text,
            **kwargs,
        )

        return response["ok"]


class Notifier:
    def __init__(self, token=None):
        self.client = SlackClient(token=token)
        self.logger = logging.getLogger(__name__)

    def send_slack(self, text: str, is_alert, channel="#notify"):

        if not text:
            self.logger.error("text is empty")
            return
        if is_alert:
            text = f'<!channel> ERROR: {text}'

        payload = {
            'username': 'luigi-app',
            'text': text,
            'channel': channel,
        }

        self.logger.info('Posting slack: %s', str(payload))

        self.client.post(**payload)
