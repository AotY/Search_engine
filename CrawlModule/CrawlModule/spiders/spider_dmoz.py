# coding: UTF-8
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup


class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    # allowed_domains = ['dmoz.org']
    allowed_domains = ['1nami.com']
    # allowed_domains = ['baidu.com']
    # start_urls = ['http://www.dmoz.org/']
    start_urls = ['http://1nami.com/']
    # start_urls = ['https://www.baidu.com/']

    rules = [
        Rule(LinkExtractor(
            restrict_css=('.top-cat', '.sub-cat', '.cat-item')
        ), callback='parse_directory', follow=True),
    ]

    def parse_directory(self, response):
        # self.headers = Headers(headers or {})
        # self.status = int(status)
        # self._set_body(body)
        # self._set_url(url)
        # self.request = request
        # self.flags = [] if flags is None else list(flags)
        print('response.headers %s' % response.headers)
        # pass
        """response.css Shortcut method implemented only by responses whose content
        is text (subclasses of TextResponse).
        """
        for div in response.css('.title-and-desc'):
            yield {
                'name': div.css('.site-title::text').extract_first(),
                'description': div.css('.site-descr::text').extract_first().strip(),
                'link': div.css('a::attr(href)').extract_first(),
            }
