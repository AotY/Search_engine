# coding: UTF-8
from bs4 import BeautifulSoup
import requests
import re

# url = 'http://news.163.com/17/0226/11/CE6QLQEF000189FH.html'
url = 'http://news.sina.com.cn/china/xlxw/2017-02-26/doc-ifyavvsh6855133.shtml'
res = requests.get(url)

# print(res.text)

res.encoding = res.apparent_encoding

soup = BeautifulSoup(res.text, 'lxml')

# soup.prefix()

# for meta in soup.find_all('meta'):
#     print(meta)
# print(type(meta))

# title
# print(soup.find(name=re.compile('title')).text)


print('status: ', res.status_code)
# keywords ，以数组保存
# keywords = soup.select_one('[name*="eywords"]')['content']
# print(soup.select_one('[name*="eywords"]')['content'])
# keywords.split(',')

# print(soup.find(name=re.compile("[kK]eywords")))
# print(soup.find(name=['keywords', 'Keywords']))



#description
# soup.select_one('[name$="escription"]')['content']
# description = soup.select_one('[name*="escription"]')['content']
# print(description)


#author
# print(soup.find_all('meta', {'name': re.compile('.*author.*')}))
#

#Copyright
# soup.find_all('meta', {'name': re.compile('.*opyright.*')})




#content 正文
# for p in soup.find_all('p'):
#     print(p.text)


#site：
# from urllib.parse import urlparse
# urlparse(res.url).hostname #netloc