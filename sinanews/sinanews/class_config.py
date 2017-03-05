# coding: UTF-8

class_config = {
    'baby': "育儿",
    'book': "书籍",
    'collection': "收藏",
    'edu': "教育",
    'eladies': "女性",
    'ent': "娱乐",
    'fashion': "时尚",
    'finance': "金融",
    'games': "游戏",
    'health': "健康",
    'mil': "军事",
    'news': "新闻",
    'tech': "科技",
    'sports': "运动",
    'travel': "旅行",
    'auto': "汽车",
}

count_config = {
    'baby': 0,
    'book': 0,
    'collection': 0,
    'edu': 0,
    'eladies': 0,
    'ent': 0,
    'fashion': 0,
    'finance': 0,
    'games': 0,
    'health': 0,
    'mil': 0,
    'news': 0,
    'tech': 0,
    'sports': 0,
    'travel': 0,
    'auto': 0,
}

if __name__ == '__main__':
    print('games' in class_config.keys())
    print(class_config.keys())
    print(class_config.values())
