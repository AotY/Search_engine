#!/usr/bin/env python
# -*-coding:utf-8-*-
# QingTao
from __future__ import division
import codecs
import os

import jieba
import jieba.posseg as pseg
import re

from pybloom import BloomFilter
import pickle

SYSTEM_SEPARATOR = r'/'

encoding = 'UTF-8'

dir_path = '/Users/LeonTao/Downloads/search-github/InformationSystem/ClassificationData'
stop_words_path = '/Users/LeonTao/Downloads/search-github/InformationSystem/ClassifyModule/Resource/all_stopwords.txt'


class Tokenizer(object):
    def __init__(self, dir_path=dir_path, stop_word_path=stop_words_path, user_dict_path=None):

        self.user_dict_path = user_dict_path

        self.stop_word_path = stop_word_path
        self.bloomFilter = BloomFilter(capacity=3000, error_rate=0.0001)

        # 结巴分词进行初始化 (加载词典等等）
        self.init_jieba()

        # 加载停顿词库
        self.load_stop_word()

        if dir_path is not None and os.path.isdir(dir_path):
            self.dir_path = dir_path
            dir_name = dir_path.split(SYSTEM_SEPARATOR)[-1]
            self.token_dir = dir_path.replace(dir_name, 'token_' + dir_name)
            if not os.path.exists(self.token_dir):
                os.mkdir(self.token_dir)

    # 结巴分词进行初始化
    def init_jieba(self):
        # 加载用户词典
        if self.user_dict_path is not None:
            jieba.load_userdict(self.user_dict_path)
            # jieba.add_word(r'(\d+)-(\d+)-(\d+)')

    def start(self):
        # self.load_stop_word() #加载停顿词库
        self.load_dir(self.dir_path, self.token_dir)
        return self.token_dir

    # 加载停顿词
    def load_stop_word(self):
        with codecs.open(self.stop_word_path, 'rb', encoding='utf-8') as f:
            for line in f:
                self.bloomFilter.add(line.rstrip())

    def load_dir(self, dir_path, new_dir_path):
        file_list = os.listdir(dir_path)
        for file_name in file_list:
            if os.path.isdir(os.path.join(dir_path, file_name)):
                new_dir_path = os.path.join(self.token_dir, file_name)
                if not os.path.exists(new_dir_path):
                    os.mkdir(new_dir_path)
                self.load_dir(os.path.join(dir_path, file_name), new_dir_path)  # 递归遍历
            else:
                file_path = os.path.join(dir_path, file_name)
                new_path = os.path.join(new_dir_path, file_name)
                self.token_file(file_path, new_path)

    def token_file(self, file_path, new_path):
        # 分词 ， 除去stop_words , 根据词性选择
        sentense = ""
        with codecs.open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            for line in f:
                # if not line.startswith(u''):
                line = ''.join(line.split())
                sentense += line

        no_stop_list = self.cut_sentence(sentense)
        tokener_f = codecs.open(new_path, 'w', encoding=encoding)
        tokener_f.write(" ".join(no_stop_list))

    # 进行分词
    def cut_sentence(self, sentense):
        # # 精确模式 HMM 参数用来控制是否使用 HMM 模型  于未登录词，采用了基于汉字成词能力的 HMM 模型，使用了 Viterbi 算法
        seg_list = jieba.cut(sentense, cut_all=False, HMM=True)
        no_stop_list = self.remove_stop(seg_list)
        return no_stop_list

    # 获取词性
    def posseg_cut(self, document):
        pos_data = jieba.posseg.cut(document)
        pos_list = []
        for w in pos_data:
            pos_list.append((w.word, w.flag))  # make every word and tag as a tuple and add them to a list
        return pos_list

    # 去除停顿词
    def remove_stop(self, seg_list):
        return [word for word in seg_list if word not in self.bloomFilter]


if __name__ == "__main__":
    dir_path = '/Users/LeonTao/Downloads/search-github/InformationSystem/ClassificationData'
    stop_words_path = '/Users/LeonTao/Downloads/search-github/InformationSystem/ClassifyModule/Resource/all_stopwords.txt'
    tokener = Tokenizer(dir_path, stop_words_path, None)

    tokener.start()
