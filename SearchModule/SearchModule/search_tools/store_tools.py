# coding: UTF-8


# 存储用户的查询记录
import os
import time

import jieba
import pandas as pd

dir_path = '/Users/LeonTao/Downloads/search-github/InformationSystem/SearchModule/SearchModule/data'


def get_time():
    t = time.mktime(time.localtime(time.time()))
    t_str = time.strftime("%D %H:%M:%S", time.localtime(t))
    return t_str


#
def store_query(query_):
    # now = time.time()

    search_f = open(os.path.join(dir_path, 'query.csv'), 'a')
    search_f.write(get_time() + "," + query_ + "\n")
    search_f.close()

    apriori_f = open(os.path.join(dir_path, 'apriori.csv'), 'a')
    # for token in jieba.cut_for_search(query_):
    #     if token.strip() != '':
    #         apriori_f.write(token + "," + query_ + "\n")
    if query_.strip() != '':
        query_.replace(',', '')
        apriori_f.write(query_ + "," + '1' + "\n")
        apriori_f.close()


def store_class_(class_, query_):
    # now = time.time()
    search_f = open(os.path.join(dir_path, 'class_.csv'), 'a')
    search_f.write(get_time() + "," + query_ + "," + class_ + "\n")
    search_f.close()


def get_suggestion(query_):
    suggestions = []
    df = pd.read_csv(os.path.join(dir_path, 'apriori.csv'))
    df.columns = ['name', 'value']
    gdf = df.groupby('name').sum()
    gdf.sort_values(by='value', ascending=False)
    count = 0
    for index in gdf.index:
        print(index)
        if index.find(query_.strip()) != -1:
            suggestions.append(index)
            count += 1
            if count == 5:
                break

    print(suggestions)
    return suggestions


if __name__ == '__main__':
    get_suggestion('两')
