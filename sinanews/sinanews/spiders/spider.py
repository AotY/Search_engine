# from urlparse import urlparse
from urllib.parse import urlparse, urljoin

import scrapy

from misc.log import info
from misc.spider import CommonSpider
from sinanews.items import sinanewsItem
from sinanews.class_config import class_config
from sinanews.class_config import count_config

try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor as sle
from bs4 import BeautifulSoup
import re


# from sinanews.items import *


# import pprint
# class MyPrettyPrinter(pprint.PrettyPrinter):
#     def format(self, object, context, maxlevels, level):
#         if isinstance(object, unicode):
#             return (object.encode('utf8'), True, False)
#         return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
#
# pp = MyPrettyPrinter()


class sinanewsSpider(CommonSpider):
    name = "sinanews"
    # allowed_domains = ["news.sina.com.cn"]
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        # "http://auto.sina.com.cn/",
        # "http://games.sina.com.cn/",
        # "http://edu.sina.com.cn/",

        "http://book.sina.com.cn/",

        # "http://news.sina.com.cn/",
        # "http://sports.sina.com.cn/",

        "http://baby.sina.com.cn/",
        # "http://mil.news.sina.com.cn/",

        # "http://ent.sina.com.cn/",
        # "http://finance.sina.com.cn/",
        # "http://collection.sina.com.cn/",
        # "http://house.sina.com.cn/",
        # "http://tech.sina.com.cn/",

        # "http://travel.sina.com.cn/",

        # "http://health.sina.com.cn/",
        # "http://fashion.sina.com.cn/",
    ]

    rules = [
        Rule(sle(allow=("http://.*.sina.com.cn/$")), callback='parse_0'),
        Rule(sle(allow=(".*doc[^/]*shtml$")), callback='parse_1'),  # , follow=True),
        # Rule(sle(allow=('society_index.shtml')), callback='parse_0', follow=True),
        # Rule(sle(allow=(".*[0-9]{8}.*htm$")), callback='parse_1', follow=True),
        # Rule(sle(allow=('/c/2015-11-19/doc-ifxkszhk0386278.shtml')), callback='parse_1', follow=True, process_request='process_request'),
    ]

    list_css_rules = {
        '#blk_yw_01 a': {
            'url': 'a::attr(href)',
            'name': 'a::text',
        }
    }

    content_css_rules = {
        'text': 'p::text',
        # 'images': 'img::attr(src)',
        # 'images-desc': '.img_descr::text',
        # need url analysis for video
        # 'video': '#J_Article_Player',
    }

    def process_request(self, r):
        info('process ' + str(r))
        return r

    def parse_0(self, response):
        # info('Parse 0 ' + response.url)
        # x = self.parse_with_rules(response, self.list_css_rules, dict)
        # pp.pprint(x)
        # print(x)
        # pdb.set_trace()
        # return self.parse_with_rules(response, self.list_css_rules, sinanewsItem)
        # if next_page:
        soup = BeautifulSoup(response.text, 'lxml')
        for a in soup.find_all('a', {'href': re.compile(".*doc[^/]*shtml$")}):
            try:
                new_url = urljoin(response.url, a['href'])
                yield scrapy.Request(new_url, callback=self.parse_1)
            except Exception as e:
                continue
                # yield scrapy.Request(response.url, callback=self.parse)
                # pass

    def parse_1(self, response):
        # 在这里解析新闻类别

        hostname = urlparse(response.url).hostname
        info("hostname ------ " + hostname)

        class_ = hostname.split('.')[0]

        if class_ in class_config.keys():
            cur_count = count_config.get(class_)
            if (cur_count < 1000):
                count_config[class_] += 1

                item = sinanewsItem()
                item['class_'] = class_

                x = self.parse_with_rules(response, self.content_css_rules, dict)

                item['content'] = x[0]
                item['url'] = response.url
                info('class_ ====== ' + item['class_'])
                yield item

                soup = BeautifulSoup(response.text, 'lxml')
                for a in soup.find_all('a', {'href': re.compile(".*doc[^/]*shtml$")}):
                    try:
                        new_url = urljoin(response.url, a['href'])
                        yield scrapy.Request(new_url, callback=self.parse_1)
                    except Exception as e:
                        continue

                        # for a in soup.find_all('a', {'href': re.compile(".*doc[^/]*shtml$")}):
                        #     try:
                        #         new_url = urljoin(response.url, a['href'])
                        #         yield scrapy.Request(new_url, callback=self.parse_1)
                        #     except Exception as e:
                        #         continue
                        # pp.pprint(x)
                        # print(x)
                        # self.parse_with_rules(response, self.css_rules, sinanewsItem)
