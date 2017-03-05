# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

import redis

from scrapy import signals

import json
import codecs
from collections import OrderedDict
import os
import datetime



class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class RedisPipeline(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379)

    def process_item(self, item, spider):
        if not item['id']:
            print('no id item!!')

        str_recorded_item = self.r.get(item['id'])
        final_item = None
        if str_recorded_item is None:
            final_item = item
        else:
            ritem = eval(self.r.get(item['id']))
            final_item = dict(item.items() + ritem.items())
        self.r.set(item['id'], final_item)

    def close_spider(self, spider):
        return


class FilePipeline(object):
    def __init__(self):
        self.init_path = '/Users/LeonTao/Downloads/search-github/InformationSystem/ClassificationData/'

    def process_item(self, item, spider):
        dir_path = self.init_path + item['class_']
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        # 使用URL的md5码来当文件名

        file_name = hashlib.md5(item['url'].encode('utf-8')).hexdigest()
        # file_name = str(datetime.datetime.now().microsecond)
        file_path = os.path.join(dir_path, file_name)

        content_list = item['content']['text']
        if (len(content_list) > 0):
            f = codecs.open(file_path, 'w', encoding='utf-8')
            f.write(' '.join(content_list))
            f.close()
        return item

    def close_spider(self, spider):
        pass
