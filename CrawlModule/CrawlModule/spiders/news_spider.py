# coding: UTF-8
import re
from urllib.parse import urlparse
from urllib.parse import urljoin
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import Rule
from CrawlModule.newssite import news_site
from CrawlModule.items import NewsItem

from CrawlModule.newssite import site_key

'''
1. scrapy runspider news_spider.py
2. redis-cli lpush news:start_urls http://news.baidu.com/
'''


class NamiSpider(RedisSpider):
    name = 'news_redis'
    redis_key = 'news:start_urls'
    # host = "http://weibo.cn"
    start_urls = []

    for site in news_site:
        start_urls.append(site)

    # rules = [
    #     # Rule(sle(allow=("http://.*.sina.com.cn/$")), callback='parse_list'),
    #     # Rule(sle(allow=(".*doc[^/]*shtml$")), callback='parse_page'),  # , follow=True),
    #     # http: // news.k618.cn / society / 201702 / t20170227_10451138.html
    #     # http: // news.sina.com.cn / china / xlxw / 2017 - 02 - 27 / doc - ifyavvsh6960887.shtml
    #     Rule(sle(allow=(".*/\d.*html$")), callback='parse_page', follow=True),  # , follow=True),
    #     # Rule(LinkExtractor(), callback='parse_page', follow=True),
    # ]

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        # domain = kwargs.pop('domain', '')
        # self.allowed_domains = filter(None, domain.split(','))
        # super(NamiSpider, self).__init__(*args, **kwargs)
        pass

    #
    def start_requests(self):
        print('start_requests --------- ')
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        print('parse ------------- ')

        soup = BeautifulSoup(response.text, 'lxml')
        print('parse url --------- ' + response.url)
        for a in soup.find_all('a', {'href': re.compile(".*/.*\d.htm.*")}):
            # for a in soup.find_all('a', {'href': re.compile(".*[baidu|sina].*/\d.*.htm*$")}):
            # for a in soup.find_all('a', {'href': re.compile(".*/\d.*html$")}):
            # hostname = urlparse(a['href']).hostname
            try:
                new_url = urljoin(response.url, a['href'])
                hostname = urlparse(new_url).hostname
                print('---------- %s ----------- ' % hostname.split('.')[1])
                if hostname.split('.')[1] in site_key:
                    yield scrapy.Request(new_url, callback=self.parse_page)
            except Exception as e:
                continue

    def parse_page(self, response):
        print('parse url --------- ' + response.url)

        soup = BeautifulSoup(response.text, 'lxml')

        item = NewsItem()
        item['title'] = soup.title.text

        hostname = urlparse(response.url).hostname
        item['hostname'] = hostname

        if hostname.split('.')[1] not in site_key:
            return

        item['site'] = hostname

        keywords = soup.select_one('[name*="eywords"]')
        if keywords is not None:
            item['keywords'] = keywords['content'].split(',')
        else:
            item['description'] = []

        # description
        description = soup.select_one('[name*="escription"]')
        if description is not None:
            item['description'] = description['content']
        else:
            item['description'] = ""

        # author
        author = soup.select_one('[name*="uthor"]')
        if (author is None or author == ''):
            author = soup.select_one('[property*="uthor"]')
        if author is not None:
            item['author'] = author['content']
        else:
            item['author'] = ""

        # Copyright
        copyright = soup.select_one('[name*="opyright"]')
        # copyright = soup.find_one('meta', {'name': re.compile('.*opyright.*')})
        if copyright is not None:
            item['copyright'] = copyright['content']
        else:
            item['copyright'] = ""

        # time
        # publishdate published
        # time = soup.select_one('[name*="time"]')
        time = soup.find_all('meta', {'name': re.compile('.*time.*')})
        if (time is None or len(time) == 0):
            time = soup.find_all('meta', {'property': re.compile('.*time.*')})
        if time is not None and len(time) > 0:
            item['time'] = time[0]['content']
        else:
            item['time'] = ""

        # source 来源
        source = soup.find_all('meta', {'name': re.compile('.*ource.*')})
        if source is not None and len(source) > 0:
            item['source'] = source[0]['content']
        else:
            item['source'] = hostname

        # url
        item['url'] = response.url

        # 过滤css 和javasc代码
        [script.extract() for script in soup.findAll('script')]
        [style.extract() for style in soup.findAll('style')]
        soup.prettify()

        # reg1 = re.compile("<[^>]*>")
        # content = reg1.sub('', soup.prettify())

        content = ''''''
        # content 正文
        for p in soup.find_all('p'):
            # print(p.text)
            line = p.text.rstrip().replace("'", '')
            line = line.replace("\\n", '')
            line = line.replace("\\r", '')
            line = line.replace("\r\n", '')
            content += line.replace('"', '')
        item['content'] = content

        # wordCount 正文长度
        item['word_count'] = len(content)

        # class_  类别
        item['class_'] = hostname.split('.')[0]

        # filetype
        filetype = re.sub(r'(\?.*)', '', response.url.split('.')[-1])
        item['filetype'] = filetype

        # for p in soup.find_all(class_=re.compile("text")):
        #     print(p.text)

        # 返回item到pipeline
        yield item

        for a in soup.find_all('a', {'href': re.compile(".*/.*\d.htm.*")}):
            # for a in soup.find_all('a', {'href': re.compile(".*/\d.*.htm*$")}):
            try:
                new_url = urljoin(response.url, a['href'])
                if hostname.split('.')[1] in site_key:
                    yield scrapy.Request(new_url, callback=self.parse_page)
                    # yield scrapy.Request(new_url, callback=self.parse_page)
            except Exception as e:
                continue
                # yield scrapy.Request(a['href'], callback=self.parse_page)
