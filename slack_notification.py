import slackweb
from config import config

slack = slackweb.Slack(url=config['slack_info']['in_webhook_url'])

def slack_notify(text_="", list_=None):
    slack.notify(text=text_)
    for element in list_:
        # タイトル
        slack.notify(text=element[0])
        # url
        slack.notify(text=element[1])