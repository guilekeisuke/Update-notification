import configparser
import re

config = configparser.ConfigParser()
config.read('config.ini')

# recent_articleの記事番号を更新
def update_recent_article(article_num):
    with open('config.ini', 'r') as f:
        lines = f.readlines()
    with open('config.ini', 'w') as f:
        for line in lines:
            if re.match(r'(recent_article = )', line):
                f.write("recent_article = {}".format(article_num))
                continue
            f.write(line)