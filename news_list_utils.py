import requests
import codecs
from parsel import Selector
from models.news_model import NewsModel
import urllib3

jxust_base = 'https://www.jxust.edu.cn'


# 获取新闻列表
def get_news_list(__url__):
    news_list = []
    req = requests.get(
        url=jxust_base + __url__,
        verify=False
    )
    content = codecs.decode(req.content, 'UTF-8')
    selector = Selector(content)
    posts_raw = selector.xpath('//div[@class="list_con"]//div[@class="left_box1"]//ul//li//a').extract()
    for post_raw in posts_raw:
        post_selector = Selector(post_raw)
        post_url = post_selector.xpath('//a/@href').extract()[0]
        post_title = post_selector.xpath('//a/text()').extract()[0].strip()
        if post_url[:7] == '../info':
            post_url = jxust_base + post_url[2:]
        news_list.append(NewsModel(post_title, post_url))
    return news_list


def get_news_list_test():
    urllib3.disable_warnings()
    news_list = get_news_list('/index/xxgg.htm')
    for news in news_list:
        print(news)


if __name__ == '__main__':
    get_news_list_test()

