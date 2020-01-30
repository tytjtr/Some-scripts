# -*- coding: utf-8 -*-

# by kysdm
#
# **************用户变量********************
#proxy = None  # 不通过代理访问
proxy = {'https': '127.0.0.1:1800'} # 通过代理访问
cookie = ''  # 此处填入cookie 【不填好像也能访问】

# **************用户变量********************

import os
import csv
import re
import json
import time
import random
import urllib
from urllib import request


def openhtml(chaper_url, cookie, referer='https://www.pixiv.net'):
    url = chaper_url
    if proxy:
        proxy_support = request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
    else:
        opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'),
        ('cookie', cookie),
        ('Referer', referer)]
    request.install_opener(opener)
    response = request.urlopen(url)
    html = response.read().decode("utf-8")
    return html


def openjson(url):
    json_list = []
    main_url = url
    page = openhtml(main_url, cookie)
    re1 = re.compile(r'img\/(\d{4}\/\d{2}\/\d{2}\/\d{2}\/\d{2}\/\d{2})/', re.S)  # 正则表达式
    jsonobj = json.loads(page)  # 把json格式字符串转换成python对象
    for v in jsonobj['contents']:
        illust_url = v['url']
        illust_data = (re.findall(re1, illust_url))[0]  # 时间
        illust_id = v['illust_id']  # 插图ID
        user_id = v['user_id']  # 画师ID
        json_list.append([illust_id, illust_data, user_id])
    return json_list


def download(id, date, user, cookie):
    illust_id = id
    illust_date = date
    user_id = user
    # 获取当前插画的JSON信息
    page2 = openhtml(f'https://www.pixiv.net/ajax/illust/{illust_id}/pages', cookie)
    jsonobj2 = json.loads(page2)  # 转换
    re2 = re.compile(r'\/(\d+_p\d+\.\w+$)', re.S)  # 正则表达式
    for v in jsonobj2['body']:
        illust_original_url = v['urls']['original']  # 插图原画质直链
        file_name = (re.findall(re2, illust_original_url))[0]  # 提取url中的文件名
        # proxy = {'https': '127.0.0.1:1800'}
        if proxy:
            proxy_support = request.ProxyHandler(proxy)
            opener = urllib.request.build_opener(proxy_support)
        else:
            opener = urllib.request.build_opener()
        opener.addheaders = [
            ('cache-control', 'no-cache'),
            ('pragma', 'no-cache'),
            ('cookie', cookie),
            ('referer', f'https://www.pixiv.net/artworks/{illust_id}'),
            ('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')]
        urllib.request.install_opener(opener)
        if downloaded(illust_date, file_name) == 'Y':
            print(f'已下载：{file_name}')
            sleep(0.5)
            continue
        print(f'开始下载：{file_name}')
        try:
            urllib.request.urlretrieve(
                illust_original_url, f'{abs_path}\\image\\{file_name}', percentage)
        except urllib.error.URLError as e:
            print(e.reason)
            continue
        writecsv(user_id, illust_id, illust_date, file_name)
        sleep()


def downloaded(date, filename):
    mark = 'N'
    for v in csvdata:
        if filename in v and date in v:  # 比对csv中的时间和文件名信息
            mark = 'Y'
            break
    return mark


def percentage(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小 
    @totalsize: 远程文件的大小 
    '''
    i = blocknum * blocksize
    n = totalsize
    print('\r{}{}%'.format(['/', '-', '\\'][i % 3] if n >=i else '', int(i/n*100)), end='' if n >= i else '\n')


def writecsv(user, id, date, filename):     # 写入csv 防止下次重复下载
    illust_id = id
    illust_date = date
    file_name = filename
    user_id = user
    with open(f'{abs_path}\\pixiv.csv', 'a', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([user_id, illust_id, illust_date, file_name])
        csv_file.close()


def readcsv():
    csvdata = []
    if os.path.exists(f'{abs_path}\\pixiv.csv'):
        with open(f'{abs_path}\\pixiv.csv', "r", encoding='utf-8-sig') as csv_file:
            reader = csv.reader(csv_file)
            for string in reader:
                # print(string[2])
                csvdata.append([string[2], string[3]])
        csv_file.close()
        # print(title)
    return csvdata


def sleep(var=None):  # 随机延迟
    if not var:
        var = random.randint(1, 3)
    # print('暂停', var, '秒继续运行')
    time.sleep(var)


if __name__ == "__main__":
    abs_path = os.path.split(os.path.realpath(__file__))[0]  # 获取脚本所在绝对路径
    if not os.path.exists(f'{abs_path}\\image'):
        os.mkdir(f'{abs_path}\\image')  # 创建存放图片的文件夹

    j = openjson(
        'https://www.pixiv.net/ranking.php?p=1&mode=daily&content=illust&format=json')   # 【p=1 1-50】【p=2 51-100】
    csvdata = readcsv()
    for v in j:
        download(v[0], v[1], v[2], cookie)
