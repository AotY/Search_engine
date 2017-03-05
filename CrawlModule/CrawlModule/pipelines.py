# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


'''
在这里，要通过elasticsearch API将这些元数据上传到搜索引擎，建立索引
'''
#
from searchtools.initconn import get_esconn
from searchtools.put import put2es
from searchtools.config import my_index
from searchtools.config import my_doc_type
from searchtools.index import delete_index
from searchtools.index import create_index
from searchtools.mapping import news_mapping
from sklearn.externals import joblib

from searchtools.tokenizer import Tokenizer
from searchtools.model_path import get_model_path


class CrawlmodulePipeline(object):
    def __init__(self):
        print(' ----------------------- CrawlmodulePipeline init ---------------------- ')
        # self.r = redis.StrictRedis(host='localhost', port=6379)
        self.index = my_index
        self.doc_type = my_doc_type
        self.model = self.load_model(get_model_path('linearSVC'))
        self.tokenizer = Tokenizer()
        self.vectorizer = self.load_model(get_model_path('vectorizer'))
        self.es = get_esconn()  # elasticsearch 连接

        # delete
        try:
            delete_index(self.es, self.index)
        except Exception as e:
            print(e)

        # index
        create_index(self.es, self.index, self.doc_type)

        # mapping
        news_mapping(self.es, self.index, self.doc_type)

    def load_model(self, model_path):
        # model = pickle.load(open(model_path))
        model = joblib.load(model_path)
        return model

    def process_item(self, item, spider):
        print(' ----------------------- CrawlmodulePipeline process_item ---------------------- ')
        # print('content ------- ' + item['content'] )
        # print('item ------- ' + type(item))
        # put
        item['class_'] = self.get_class(item['content'])
        put2es(item, self.es, self.index, self.doc_type)
        return item

    def get_class(self, content):
        class_ = 'news'
        token_list = self.tokenizer.cut_sentence(content)
        if self.model is not None:
            predict_vectors = self.vectorizer.transform([' '.join(token_list)])
            class_ = self.model.predict(predict_vectors)[0]

        print(' ------ class_  ----- %s ' % class_)
        return class_

    def close_spider(self, spider):
        print(' ----------------------- CrawlmodulePipeline close_spider ---------------------- ')
        self.es.close()
        return

        #
        # class RedisPipeline(object):
        #
        #     def __init__(self):
        #         self.r = redis.StrictRedis(host='localhost', port=6379)
        #
        #     def process_item(self, item, spider):
        #         if not item['id']:
        #             print ('no id item!!')
        #
        #         str_recorded_item = self.r.get(item['id'])
        #         final_item = None
        #         if str_recorded_item is None:
        #             final_item = item
        #         else:
        #             ritem = eval(self.r.get(item['id']))
        #             final_item = dict(item.items() + ritem.items())
        #         self.r.set(item['id'], final_item)
        #
        #     def close_spider(self, spider):
        #         return
