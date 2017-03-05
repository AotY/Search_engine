# coding: UTF-8

class_config = {
    "育儿": 'baby',
    "书籍": 'book',
    "书": 'book',
    "收藏": 'collection',
    "教育": 'edu',
    "教学": 'edu',
    "女性": 'eladies',
    "女人": 'eladies',
    "娱乐": 'ent',
    "时尚": 'fashion',
    "金融": 'finance',
    "财经": 'finance',
    "游戏": 'games',
    # "公益": 'gongyi',
    "健康": 'health',
    "军事": 'mil',
    "新闻": 'news',
    "科技": 'tech',
    "运动": 'sports',
    "体育": 'sports',
    "旅行": 'travel',
    "旅游": 'travel',
    "汽车": 'auto',
}


def get_class(class_):
    return class_config.get(class_)


if __name__ == '__main__':
    # print(class_config.keys())
    # print(class_config.values())
    print(get_class('体育'))
