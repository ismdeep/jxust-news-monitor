import fcntl
import json

from monitor_util.monitor_util import MonitorUtil
from news_list_utils import get_news_list
from telegram_msg_sender import TelegramMsgSender
from news_list_db import NewsListDB
import urllib3
import time

import asyncio
import sys
import os

MONITOR_INTERVAL_TIME = 10 * 60  # 10 minutes


def monitor(__url__, __tag__):
    news_list = get_news_list(__url__)
    for news in news_list:
        if not NewsListDB.has(news.url):
            TelegramMsgSender.send_text_msg(
                "#%s\n\n%s\n\n%s" % (__tag__, news.title, news.url),
                no_webpage=False
            )
            NewsListDB.add(news.url)
            NewsListDB.save()


def show_help():
    print("Usage: python3 main.py WORK_DIR")


def main():
    if len(sys.argv) <= 1:
        show_help()
        exit(-1)
    work_dir = sys.argv[1]
    os.chdir(work_dir)

    # 0. 启动时对文件加锁
    lock_file = open('monitor.lock', 'w')
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print("can't immediately write-lock the file ($!), blocking ...")
        print('Exiting....')
        return
    else:
        print('Monitor lock file LOCKED')

    # 1. Init telegram bot
    TelegramMsgSender.init_with_config('telegram_bot.json')

    # 2. Init Monitor Util
    MonitorUtil.init_with_json_config('monitor.json')

    # 3. Init NewsListDB
    NewsListDB.load()

    # 4. Start Monitor
    urllib3.disable_warnings()
    try:
        while True:
            monitor(__url__='/index/zbgg.htm', __tag__='招标公告')
            monitor(__url__='/index/xxgg.htm', __tag__='学校公告')
            monitor(__url__='/index/xycz.htm', __tag__='校园传真')
            monitor(__url__='/index/xshd.htm', __tag__='学术活动')
            asyncio.run(MonitorUtil.update_status('jxust-news-monitor', 'true'))
            time.sleep(MONITOR_INTERVAL_TIME)
    except KeyboardInterrupt:
        print('-' * 20)
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)

    # 5. 退出前保存数据
    NewsListDB.save()


if __name__ == '__main__':
    main()
