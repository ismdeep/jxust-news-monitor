import fcntl

from news_list_utils import get_news_list
from telegram_msg_sender import TelegramMsgSender
from news_list_db import NewsListDB
import urllib3
import time

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


def main():
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
    # 2. Init NewsListDB
    NewsListDB.load()
    # 3. Start Monitor
    urllib3.disable_warnings()
    try:
        while True:
            monitor(__url__='/index/zbgg.htm', __tag__='招标公告')
            monitor(__url__='/index/xxgg.htm', __tag__='学校公告')
            monitor(__url__='/index/xycz.htm', __tag__='校园传真')
            monitor(__url__='/index/xshd.htm', __tag__='学术活动')
            time.sleep(MONITOR_INTERVAL_TIME)
    except KeyboardInterrupt:
        print('-' * 20)
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
    # 4. 退出前保存数据
    NewsListDB.save()


if __name__ == '__main__':
    main()