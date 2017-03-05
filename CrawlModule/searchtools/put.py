# coding: UTF-8

from datetime import datetime
from elasticsearch import Elasticsearch


def put2es(item, es, index, doc_type):
    # 将item存入elasticsearch中

    body = {
        "title": item['title'],
        "description": item['description'],
        "hostname": item['hostname'],
        "site": item['site'],
        "keywords": item['keywords'],
        "url": item['url'],
        "word_count": item['word_count'],
        "class": item['class_'],
        "source": item['source'],
        "time": item['time'],
        "copyright": item['copyright'],
        "author": item['author'],
        "filetype": item['filetype'],
        "content": item['content']}

    es.index(index=index, doc_type=doc_type, body=body)
    pass

    '''
     {"error":{"root_cause":
     [{"type":"mapper_parsing_exception","reason":"failed to parse [time]"}],
     "type":"mapper_parsing_exception","reason":"failed to parse [time]",
     "caused_by":{"type":"illegal_argument_exception","reason":"Invalid format: \"\""}},
     "status":400}


    '''
    #
    # doc = {
    #     'author': 'kimchy3',
    #     'text': 'Elasticsearch: cool. bonsai cool.',
    #     'timestamp': datetime.now(),
    # }
    # res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
    # print(res['created'])
    #
    # res = es.index(index="test-index", doc_type='tweet', id=3, body=doc)
    # print(res['created'])
    #
    # res = es.get(index="test-index", doc_type='tweet', id=1)
    # print(res['_source'])
    #
    # es.indices.refresh(index="test-index")
    #
    # res = es.search(index="test-index", body={"query": {"match_all": {}}})
    # print("Got %d Hits:" % res['hits']['total'])
    # for hit in res['hits']['hits']:
    #     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
