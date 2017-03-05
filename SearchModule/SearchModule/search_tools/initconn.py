# coding: UTF-8
from datetime import datetime

from elasticsearch import Elasticsearch


def get_esconn():
    es = Elasticsearch()
    return es


def demo():
    es = get_esconn()
    # es.indices.delete(index='my-index')
    es.indices.create(index='my-index', ignore=400)
    es.index(index="my-index", doc_type="test-type", id=1,
             body={"title": "饭打发打发吗范德萨发大发都没法律", "timestamp": datetime.now()})
    result = es.get(index="my-index", doc_type="test-type", id=1)['_source']
    print(result)
    print('--- result ---{}'.format(result))
    print('--- type(result)---{}'.format(type(result)))


def search():
    es = get_esconn()
    result = es.search(index='my-index', doc_type='test-type', body={"query": {
        "match": {
            "title": "哈哈"
        }
    }})
    print(result)
    print('--- result ---{}'.format(result))
    print('--- type(result)---{}'.format(type(result)))


if __name__ == '__main__':
    # print(get_esconn())
    # demo()
    search()
