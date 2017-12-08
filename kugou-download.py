# coding=utf-8
import sys
import urllib
import json
import os
import time

reload(sys)
sys.setdefaultencoding('utf-8')


# 传入数组 批量下载
def download(url):
    print(url)
    html = urllib.urlopen(url).read()
    jsons = json.loads(html)
    if jsons["status"] == 1 and len(jsons["data"]["info"]) > 0:
        for item in jsons["data"]["info"]:
            try:
                html = urllib.urlopen(
                    'http://www.kugou.com/yy/index.php?r=play/getdata&hash=%s' % (item["hash"])).read()
                jsons = json.loads(html)
            except:
                print(u'获取歌曲详情异常：' + item["filename"])
                continue
            if jsons["status"] == 1:
                try:
                    print(item["filename"] + ':' + jsons["data"]["play_url"])
                except:
                    continue
                temp = jsons["data"]["play_url"].split('/')
                rawName = temp[-1]
                temp = rawName.split('.')
                ext = temp[-1]
                try:
                    urllib.urlretrieve(jsons["data"]["play_url"],
                                       os.path.join(path, str(jsons["data"]["song_name"]) + '.' + ext))
                    # 延时100ms
                    time.sleep(0.1)
                except:
                    print(u'下载歌曲异常：'  + ':' + jsons["data"]["play_url"])
                    continue
            else:
                print(u'未获取到歌曲详情')
    else:
        print(u'未获取到数据')


keyWord = raw_input(u'请输入歌手名：'.decode('utf-8').encode('gbk'))
page = 1
pagesize = 50
path = os.path.join(sys.path[0], 'kugou')
if not os.path.exists(path):
    os.makedirs(path)

url = 'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=%s&page=%s&pagesize=%s&showtype=1' % (
    urllib.quote(keyWord.decode(sys.stdin.encoding).encode('utf8')), page, pagesize)
html = urllib.urlopen(url).read()
jsons = json.loads(html)
if jsons["status"] == 1 and len(jsons["data"]["info"]) > 0:
    total = jsons["data"]["total"]
    print(u'共：' + str(total) + u'首歌曲')
    # 计算总页数
    totalPage = (total + pagesize - 1) / pagesize
    while page <= int(totalPage):
        url = 'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=%s&page=%s&pagesize=%s&showtype=1' % (
            urllib.quote(keyWord.decode(sys.stdin.encoding).encode('utf8')), page, pagesize)
        download(url)
        page += 1
    print(u'下载完成')
else:
    print(u'未获取到数据')
