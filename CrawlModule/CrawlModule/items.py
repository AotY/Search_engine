# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlmoduleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsItem(scrapy.Item):
    #title
    title = scrapy.Field()

    #keywords
    keywords = scrapy.Field()

    #description
    description = scrapy.Field()

    # author
    author = scrapy.Field()

    # copyright
    copyright = scrapy.Field()

    #time
    time = scrapy.Field()

    # source 来源
    source = scrapy.Field()

    #url
    url = scrapy.Field()

    # site
    site = scrapy.Field()

    #hostname
    hostname = scrapy.Field()

    # content 正文
    content = scrapy.Field()

    #wordCount
    word_count = scrapy.Field()

    #class_
    class_ = scrapy.Field()

    #file_type
    filetype = scrapy.Field()
