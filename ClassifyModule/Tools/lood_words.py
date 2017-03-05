#!/usr/bin/env python
# -*- coding: utf-8 -*-
# QingTao
import codecs
import os

dir_path = '/Users/LeonTao/Downloads/search-github/InformationSystem/token_ClassificationData'


def load_words(dir_path=dir_path):
    train_data = []
    train_label = []
    count = 0
    # for class_ in class_config.keys():
    for class_ in os.listdir(dir_path):
        class_path = os.path.join(dir_path, class_)
        for f_name in os.listdir(class_path):
            file_path = os.path.join(class_path, f_name)
            count += 1
            print('--- file_path --- %s' % file_path)
            f = codecs.open(file_path, 'r', encoding='UTF-8')
            train_data.append(f.readline())
            # train_data.append(f.readline().rstrip().split())
            train_label.append(class_)

            f.close()

            # with codecs.open(file_path, 'r', encoding='UTF-8') as f:
            #     for line in f:
            #         words = line
            #         if len(words) > 3:
            #             all_words.append(words)

    print(count)
    return train_data, train_label


# test_data = []
# test_labels = []

# for curr_class in file_names:
#     flag = 1
#
#     file_path = os.path.join(data_dir, curr_class)
#     with open(file_path, 'r') as f:
#         for line in f:
#             if flag % 10 == 9:
#                 test_data.append(line)
#                 test_labels.append(curr_class.split('.')[0])
#             # else:
#             train_data.append(line)
#             train_labels.append(curr_class.split('.')[0])
#
#             flag += 1


if __name__ == '__main__':
    # dir_path = '/Users/LeonTao/Downloads/search-github/InformationSystem/token_ClassificationData'
    load_words()
