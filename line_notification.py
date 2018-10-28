import requests
from config import config
#! python3
# -*- coding: utf-8 -*-

# LINEに更新を通知する
def lineNotify(article_list):
    line_notify_token = config['line_info']['line_notify_token']
    line_notify_api = config['line_info']['line_notify_api']
    payload = {'message': article_list}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers)


