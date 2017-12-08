# coding=utf-8
import sys
import urllib
import json

reload(sys)
sys.setdefaultencoding('utf-8')

keyWord='刚好遇见你'
url='http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=%s&page=1&pagesize=20&showtype=1'%(keyWord)
html = urllib.urlopen(url).read()
jsons = json.loads(html)
print(jsons['status'])