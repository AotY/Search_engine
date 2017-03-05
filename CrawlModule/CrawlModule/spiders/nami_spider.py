# coding: UTF-8
from scrapy_redis.spiders import RedisSpider
import scrapy
from bs4 import BeautifulSoup

'''
1. scrapy runspider nami_spider.py
2. redis-cli lpush nami:start_urls http://1nami.com/
'''


class NamiSpider(RedisSpider):
    name = 'nami_redis'
    redis_key = 'nami:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(NamiSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        request = scrapy.Request("http://www.example.com/some_page.html",
                                 callback=self.parse_page2)
        yield {
            'name': soup.title.text,
            'url': response.url
        }

        # for title in response.css('h2.entry-title'):
        #     yield {'title': title.css('a ::text').extract_first()}
        #
        # next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        # if next_page:
        #     yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

        # return {
        #     'name': response.css('title::text').extract_first(),
        #     'url': response.url,
        # }
