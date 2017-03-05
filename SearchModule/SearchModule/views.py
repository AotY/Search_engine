#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
import os
import re

import django
import math

from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from SearchModule.search_tools.search import SearchTool
# Create your views here.


# import html.parser
# html_parser = html.parser.HTMLParser()
# unescaped = html_parser.unescape(my_string)
from SearchModule.search_tools.search_item import NewItem
from SearchModule.search_tools.store_tools import store_query, store_class_, get_suggestion


def hello(request):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % "Hello")
    # return render(request, 'Hello World')


# 存储用户点击新闻的列表， site ,
def class_(request):
    print(' ---- class_ ---- ')
    # if request.method == "POST":
    class_ = request.GET['class_']
    query_ = request.GET['query']
    store_class_(class_, query_)
    print(' ---- class_ ---- %s' % class_)
    return class_


# 获取查询相关词
def suggestion(request):
    print(' ---- suggestion ---- ')
    query_ = request.GET['query']
    print(' ---- query_ ---- ', query_)

    suggestions = get_suggestion(query_)

    some_data_to_dump = {
        'id': 1,
        'result_list': ','.join(suggestions),
    }
    data = json.dumps(some_data_to_dump)
    return HttpResponse(data, content_type='application/json')


def search(request):
    print('request.method: ', request.method)
    request.session.set_test_cookie()
    return render(request, 'search.html')


def search_result(request):
    # return HttpResponse("You're looking at question")
    print(' ---- search_list ----')
    # if request.method == "POST":
    query_ = request.GET['query']
    from_ = request.GET['from']
    size_ = request.GET['size']
    # print(from_)

    # 存储用户的查询记录
    store_query(query_)

    query = parse_query(query_)

    search_tools = SearchTool()
    hits = search_tools.search(query, int(from_), int(size_))

    # print(hits)
    news = []
    total = hits['total']
    print('----- total ------', total)
    print('----- total ------', len(hits['hits']))
    max_page = 0
    if total > 0:
        max_page = math.ceil(total / 10)
        for hit in hits['hits']:
            url = hit['_source']['url']
            content = hit['_source']['content']
            title = hit['_source']['title']
            class_ = hit['_source']['class']

            highlight = hit.get('highlight')

            if highlight is None:
                highlight = content[30: 120]
            else:
                highlight = highlight['content'][0]
            item = NewItem(url, content, highlight, title, class_)
            news.append(item)

    return render(request, 'search_result.html', {"result": news, "max_page": max_page})


# 分析查询条件
def parse_query(query_):
    return_query = {}
    # site
    if len(query_.split('site: ')) > 1:
        return_query['type'] = 'site'
        vals = query_.split('site: ')
        return_query['site'] = vals[-1]
        return_query['query'] = vals[0]
        pass

    elif len(query_.split('inurl: ')) > 1:  # inurl
        return_query['type'] = 'inurl'
        vals = query_.split('inurl: ')
        return_query['inurl'] = vals[-1]
        return_query['query'] = vals[0]
        pass

    elif len(query_.split('intitle: ')) > 1:
        return_query['type'] = 'intitle'
        vals = query_.split('intitle: ')
        return_query['intitle'] = vals[-1]
        return_query['query'] = vals[0]
        pass

    elif len(query_.split('filetype: ')) > 1:
        return_query['type'] = 'filetype'
        vals = query_.split('filetype: ')
        return_query['filetype'] = vals[-1]
        return_query['query'] = vals[0]
        pass

    elif len(query_.split('class: ')) > 1:
        return_query['type'] = 'class'
        vals = query_.split('class: ')
        return_query['class'] = vals[-1]
        return_query['query'] = vals[0]
        pass

    elif len(query_.split(' -')) > 1:
        return_query['type'] = 'sub'
        vals = query_.split(' -')
        return_query['must_not'] = vals[-1]
        return_query['query'] = vals[0]
        pass

    elif re.match('".*"', query_) is not None:
        return_query['type'] = 'full_match'
        vals = re.match('".*"', query_).group(0)
        # vals = query_.split(vals)
        return_query['full_match'] = vals.replace('"', '')
        return_query['query'] = ' '.join(query_.split(vals)).strip() + return_query['full_match']
        pass
    elif re.match('“.*“', query_) is not None:
        return_query['type'] = 'full_match'
        vals = re.match('“.*“', query_).group(0)
        # vals = query_.split(vals)
        return_query['full_match'] = vals.replace('“', '')
        return_query['query'] = ' '.join(query_.split(vals)).strip() + return_query['full_match']
        pass

    else:  # normal search
        return_query['type'] = 'normal'
        return_query['query'] = query_

    print('return_query -------- {}'.format(return_query))
    return return_query
