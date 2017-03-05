# coding: UTF-8

# # create an index in elasticsearch, ignore status code 400 (index already exists)
# >>> es.indices.create(index='my-index', ignore=400)
# {u'acknowledged': True}


# # datetimes will be serialized
# >>> es.index(index="my-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})
# {u'_id': u'42', u'_index': u'my-index', u'_type': u'test-type', u'_version': 1, u'ok': True}


def create_index(es, index, doc_type):
    # ignore 400 cause by IndexAlreadyExistsException when creating an index
    # es.indices.create(index=index, doc_type=doc_type, ignore=400)
    es.indices.create(index=index, ignore=400)


def delete_index(es, index):
    result = es.indices.delete(index)