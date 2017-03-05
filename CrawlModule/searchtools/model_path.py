# coding: UTF-8

import os

base_path = '/Users/LeonTao/Downloads/search-github/InformationSystem/ClassifyModule/model'


def get_model_path(model_name):
    return os.path.join(base_path, model_name)
