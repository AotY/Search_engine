# coding: UTF-8



def news_mapping(es, index, doc_type):
    body = {
        "news": {
            "_all": {
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word",
                "term_vector": "no",
                "store": "false"
            },
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_max_word",
                    "include_in_all": "true",
                    "boost": 8
                },
                # "time": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                # "time": {"type": "string"},
                "content": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word"},
                "description": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word",
                                "boost": 8},
                "word_count": {"type": "integer"},
                "class_": {"type": "string"},
                "copyright": {"type": "string"},
                "url": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word"},
                # "url": {"type": "string"},
                "hostname": {"type": "string"},
                "site": {"type": "string"},
                "filtype": {"type": "string"},
            }
        }
    }
    es.indices.put_mapping(index=index, doc_type=doc_type, body=body)


def get_mapping(es, index, doc_type):
    es.indices.get_mapping(index=index, doc_type=doc_type)
