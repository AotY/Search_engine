# coding: UTF-8


# # but not deserialized
# >>> es.get(index="my-index", doc_type="test-type", id=42)['_source']
# {u'any': u'data', u'timestamp': u'2013-05-12T19:45:31.804229'}

'''
你可以使用from及size参数进行分页
使用match_all 可以查询到所有文档，是没有查询条件下的默认语句。
term主要用于精确匹配哪些值，比如数字，日期，布尔值或
terms 跟 term 有点类似，但 terms 允许指定多个匹配条件
range过滤允许我们按照指定范围查找一批数
exists 和 missing 过滤可以用于查找文档中是否包含指定字段或没有某

bool 过滤可以用来合并多个过滤条件查询结果的布尔逻辑，它包含一下操作符：
布尔查询接受多个用must, must_not, and should的查询子句. 例:

match查询是一个标准查询，不管你需要全文本查询还是精确查询基本上都要用到它。
multi_match查询允许你做match查询的基础上同时搜索多个字段
query 语句，也可以包含一条 filter 子句。 换句话说，这些语句需要首先创建一个query或filter的上下文关系。
'''
from elasticsearch import Elasticsearch

from SearchModule.search_tools import config
from SearchModule.search_tools.class_config import get_class
from SearchModule.search_tools.initconn import get_esconn


def simple_search(es, index, doc_type):
    body = {
        "query": {
            "match": {
                "content": "父亲"
            }
        }
    }
    result = es.search(index=index, doc_type=doc_type, body=body)
    print("--- result --- {}".format(type(result)))
    # print("---- hits ---- {}".format(len(result['hits']['hits'])))
    print("---- hits ---- {}".format(result['hits']['total']))
    print("---- hits ---- {}".format(result['hits']['hits'][0]))


class SearchTool(object):
    def __init__(self):
        self.index = config.my_index
        self.doc_type = config.my_doc_type
        # self.es = es
        self.es = get_esconn()
        # 高亮匹配的词
        self.highlight = {
            "pre_tags": ["<em class='em-label' style='color:#212121'>", "<em class='em-label' style='color:#212121>"],
            "post_tags": ["</em>", "</em>"],
            "fields": {
                "content": {}
            }
        }

    # 普通搜索
    def normal_search(self, query, page_from=0, page_size=10):
        print(' ----- normal_search --------')
        body = {
            "from": page_from, "size": page_size,
            "query": {
                "bool": {
                    "should": self.get_normal_search(query),
                    "minimum_should_match": 1,
                }
            },
            "highlight": self.highlight
        }
        result = self.es.search(index=self.index, doc_type=self.doc_type, body=body)
        # print(result)
        return result['hits']

    # 双引号 把搜索词放在双引号中，代表完全匹配搜索
    def full_match_search(self, query, page_from=0, page_size=10):
        print('--- full_match_search --- ')
        body = {
            "from": page_from, "size": page_size,
            "query": {
                "bool": {
                    "should": self.get_normal_search(query),
                    "minimum_should_match": 1,
                    "must": [
                        {"match_phrase": {"content": {"query": query.get('full_match'), "slop": 0}}}
                    ],
                }
            },
            "highlight": self.highlight
        }
        result = self.es.search(index=self.index, doc_type=self.doc_type, body=body)
        return result['hits']

    # 减号代表搜索不包含减号后面的词的页面
    def sub_search(self, query, page_from=0, page_size=10):
        body = {
            "from": page_from, "size": page_size,
            "query": {
                "bool": {
                    "should": self.get_normal_search(query),
                    "minimum_should_match": 1,
                    # "must": [{"match_phrase": {"content": {"query": query.get('must'), "slop": 0}}}],
                    "must_not": [{"match_phrase": {"content": {"query": query.get('must_not'), "slop": 0}}}]
                }
            },
            "highlight": self.highlight
        }
        result = self.es.search(index=self.index, doc_type=self.doc_type, body=body)
        return result['hits']

    # inurl: 指令用于搜索查询词出现在url 中的页面
    def inurl_search(self, query, page_from=0, page_size=10):
        body = {
            "from": page_from, "size": page_size,
            "query": {
                "bool": {
                    "should": self.get_normal_search(query),
                    "minimum_should_match": 1,
                    "must": [
                        {"match": {"url": {"query": query.get('inurl')}}}
                    ]
                }
            },
            "highlight": self.highlight
        }

        result = self.es.search(index=self.index, doc_type=self.doc_type, body=body)
        return result['hits']

    # intitle: 指令返回的是页面title 中包含关键词的页面
    def intitle_search(self, query, page_from=0, page_size=10):
        body = {
            "from": page_from, "size": page_size,
            "query": {
                "bool": {
                    "should": self.get_normal_search(query),
                    "minimum_should_match": 1,
                    "must": [
                        {"match_phrase": {"title": {"query": query.get('intitle'), "slop": 0}}}
                    ],
                }
            },
            "highlight": self.highlight
        }
        result = self.es.search(index=self.index, doc_type=self.doc_type, body=body)
        return result['hits']

    # filetype 用于搜索特定文件格式
    def filetype_search(self, query, page_from=0, page_size=10):
        body = {
            "from": page_from, "size": page_size,
            "query": {
                "bool": {
                    "should": self.get_normal_search(query),
                    "minimum_should_match": 1,
                    "filter": [
                        {"term": {"filetype": query.get('filetype')}}
                    ],
                }
            },
            "highlight": self.highlight
        }
        result = self.es.search(index=self.index, doc_type=self.doc_type, body=body)
        return result['hits']

    # site:是SEO 最熟悉的高级搜索指令
    def site_search(self, query, page_from=0, page_size=10):
        print('---- site_search ---- {}'.format(query['site']))
        body = {
            "from": page_from, "size": page_size,
            "query": {
                "bool": {
                    "should": self.get_normal_search(query),
                    "minimum_should_match": 1,
                    "filter": [{"term": {"site": query.get('site')}}]
                }
            },
            "highlight": self.highlight
        }

        print(type(body['query']))
        result = self.es.search(index=self.index, doc_type=self.doc_type, body=body)
        return result['hits']

    # class: 类别查询
    def class_search(self, query, page_from=0, page_size=10):
        print('---- class_search ---- {}'.format(query['class']))
        body = {
            "from": page_from, "size": page_size,
            "query": {
                "bool": {
                    "should": self.get_normal_search(query),
                    "minimum_should_match": 1,
                    # "filter": [{"term": {"class": query.get('class')}}]
                    "filter": [{"term": {"class": get_class(query.get('class'))}}]
                }
            },
            "highlight": self.highlight
        }

        print(type(body['query']))
        result = self.es.search(index=self.index, doc_type=self.doc_type, body=body)
        return result['hits']

    # 对外提供的搜索方法
    def search(self, query, page_from, page_size):
        query_type = query['type']
        if query_type == 'intitle':
            return self.intitle_search(query, page_from, page_size)
        elif query_type == 'inurl':
            return self.inurl_search(query, page_from, page_size)
        elif query_type == 'site':
            return self.site_search(query, page_from, page_size)
        elif query_type == 'filetype':
            return self.filetype_search(query, page_from, page_size)
        elif query_type == 'full_match':
            return self.full_match_search(query, page_from, page_size)
        elif query_type == 'sub':
            return self.sub_search(query, page_from, page_size)
        elif query_type == 'normal':
            return self.normal_search(query, page_from, page_size)
        elif query_type == 'class':
            return self.class_search(query, page_from, page_size)

    # 返回普通查询语句
    def get_normal_search(self, query):
        # match_phrase
        # normal_search = [
        #     {
        #         "match_phrase": {
        #             "title": {
        #                 "query": query.get('query'),
        #                 "slop": 5,
        #                 "boost": 3
        #             }
        #         }
        #     },
        #     {
        #         "match_phrase": {
        #             "description": {
        #                 "query": query.get('query'),
        #                 "boost": 2,
        #                 "slop": 5
        #             }
        #
        #         }
        #     },
        #     {
        #         "match_phrase": {
        #             "keywords": {
        #                 "query": query.get('query'),
        #                 "boost": 3,
        #                 "slop": 3
        #             }
        #
        #         }
        #     },
        #     {
        #         "match_phrase": {
        #             "content": {
        #                 "query": query.get('query'),
        #                 "slop": 20
        #             }
        #
        #         }
        #     },
        #     {
        #         "match": {
        #             "content": {
        #                 "query": query.get('query'),
        #                 "minimum_should_match": "75%"
        #             }
        #
        #         }
        #     }
        #
        # ]

        # match
        normal_search = [
            {
                "match": {
                    "title": {
                        "query": query.get('query'),
                        "minimum_should_match": "50%",
                        "boost": 3
                    }
                }
            },
            {
                "match": {
                    "description": {
                        "query": query.get('query'),
                        "boost": 2,
                        "minimum_should_match": "50%",
                    }

                }
            },
            {
                "match": {
                    "keywords": {
                        "query": query.get('query'),
                        "boost": 3,
                        "minimum_should_match": "50%",
                    }

                }
            },
            {
                "match": {
                    "content": {
                        "query": query.get('query'),
                        "minimum_should_match": "50%",
                    }

                }
            }
        ]
        return normal_search


if __name__ == "__main__":
    # es = Elasticsearch()
    index = "my-search"
    doc_type = "news"
    # simple_search(es, index, doc_type)
    searchtool = SearchTool()
    # query = {
    #     "query": "广州",
    #     "site": "cd.qq.com"
    # }
    # query = {
    #     "full_match": "四川",
    #     "query": "国通快递"
    # }
    # query = {
    #     "filetype": "html",
    #     "query": "国通快递"
    # }
    # query = {
    #     "intitle": "小东南亚",
    #     "query": "四川"
    # }
    # query = {
    #     "inurl": "qq.com",
    #     "query": "四川"
    # }
    query = {
        "query": "华西医院",
        "must": "小东南亚",
        "must_not": "广州"
    }
    print(searchtool.normal_search(query))
    # print(searchtool.sub_search(query))
    # print(searchtool.inurl_search(query))
    # print(searchtool.intitle_search(query))
    # print(searchtool.filetype_search(query))
    # print(searchtool.full_match_search(query))
    # print(searchtool.site_search(query))
