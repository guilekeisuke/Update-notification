#! python3
# -*- coding: utf-8 -*-

# 1LDKのwebサイトが更新されると通知するシステム

import line_notification
from bs4 import BeautifulSoup
import urllib.request as url_req
from config import config, update_recent_article
from slack_notification import slack_notify

first_view = url_req.urlopen(config['web_info']['url']).read()
soup = BeautifulSoup(first_view, "lxml")


def extract_pick_up(soup=soup):
    """
    htmlを詠み込み、最新記事を抜粋
    """
    episodes = soup.find_all("ul", class_="test-readable_product-list series-episode-list ")
    return episodes[0:4]

def extract_url(column):
    """
    エピソードのurlを取得
    """
    episode_html = BeautifulSoup(str(column), "lxml")
    url = episode_html.find("a").get("href")
    return url


def extract_title(column):
    """
    エピソードのタイトルを取得する
    """
    episode_html = BeautifulSoup(str(column), "lxml")
    title = episode_html.find("h4").string
    return title

def extract_update_article(columns):
    """
    更新された記事を抽出
    更新前の最新の記事のindexはconfig.iniで管理
    """
    # 最新の記事番号を取得
    recent_article = config['web_info']['recent_article']
    # 更新された記事のurlを取得
    article_list = []
    update_start = False
    # 逆順に取得していき、最新話の次からの話のurlを取得
    for column in reversed(columns):
        url = extract_url(column)
        # 記事番号取得
        article_num = url.replace('https://tonarinoyj.jp/episode/', "")

        # タイトル取得
        title = extract_title(column)
        # 取得すべきurl
        if update_start:
            article_list.append([title, url])
            recent_article = article_num
            continue
        # 前回取得した最新話かどうか判定
        if recent_article == article_num:
            update_start = True

    # config更新
    update_recent_article(recent_article)
    if article_list == []:
        return [["最新話はアップされていません", "https://tonarinoyj.jp/episode/13932016480028985383"]]
    return article_list


if __name__ == "__main__":
    episodes = extract_pick_up()
    url = extract_url(episodes[0])
    article_list = extract_update_article(episodes)
    slack_notify(text_="---ワンパンマン最新話---", list_=article_list)


