# -*- coding: utf-8 -*-

# by kysdm
# 自动查询u2上有0倍下载的种子ID

from urllib import request
import urllib
import re
import os
from bs4 import BeautifulSoup
# pip3 install bs4
# pip3 install lxml
# import subprocess

# 有空把 urllib 替换成 requests

# **************用户变量********************

cookie = '__cfduid=xxxxxxx; nexusphp_u2=xxxxxxx; __dtsu=xxxxxxx'

# **************用户变量********************


def openhtml(chaper_url, cookie):
    url = chaper_url
    # if proxy:
    #     proxy_support = request.ProxyHandler(proxy)
    #     opener = urllib.request.build_opener(proxy_support)
    # else:
    #     opener = urllib.request.build_opener()
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('dnt', '1'),
        ('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'),
        ('referer', 'https://u2.dmhy.org/index.php'),
        ('cookie', cookie)]
    request.install_opener(opener)
    response = request.urlopen(url)
    html = response.read().decode("utf-8")
    return html


def AnalysisMagic(html):
    soup = BeautifulSoup(html, 'lxml')

    # 2x 上传 1x 下载 奶子用
    # twoup_bg = soup.find_all('tr', attrs={'class': 'twoup_bg'})

    twoupfree_bg = soup.find_all(
        'tr', attrs={'class': 'twoupfree_bg'})  # 2x 上传 0x 下载
    Magic(twoupfree_bg)

    free_bg = soup.find_all('tr', attrs={'class': 'free_bg'})  # 1x 上传 0x 下载
    Magic(free_bg)

    custompromotion_bg = soup.find_all(
        'tr', attrs={'class': 'custompromotion_bg'})  # ?x 上传 ?x 下载
    Magic(custompromotion_bg)


def Magic(var):
    for v in var:
        v = str(v)
        if '<b>有效</b>' in v:
            if '全局' not in v and '>あずさ</bdo>' not in v:  # 排除全局魔法 自己创建的魔法
                re1 = re.compile(
                    r'<a.+?href="promotion\.php.+?>(\d+?)<\/a>', re.S)
                re2 = re.compile(r'<a href="details\.php\?id=(\d+?)">', re.S)
                re3 = re.compile(
                    r'<span title="&lt;time&gt;(\d{4}-\d{2}-\d{2}\s?\d{1,2}:\d{1,2}:\d{1,2})&lt;\/time&gt;">(.+?)<\/span>', re.S)
                if 'alt="Promotion"' in v:  # 自定义魔法
                    re4 = re.compile(r'<img alt="上传比率".+?><b>(.+?)</b>', re.S)
                    re5 = re.compile(r'<img alt="下载比率".+?><b>(.+?)</b>', re.S)

                    matchObj = re.match(
                        r'<img\s?alt="下载比率".+?><b>(.+?)<\/b>', v, re.S)
                    if matchObj:
                        if not '0.00X' == matchObj[0]:  # 排除下载倍率不是0的魔法   淦
                            print('非0魔法')
                            continue
                    else:
                        continue

                    # 魔法ID
                    Magic_ID = (re.findall(re1, v))[0]
                    # 种子ID
                    Torrent_ID = (re.findall(re2, v))[0]
                    # 魔法开始时间 & 时长
                    Magic_Start_Time = (re.findall(re3, v))[0][0]
                    Magic_Time = (re.findall(re3, v))[0][1]
                    Magic_UP = (re.findall(re4, v))[0]

                    # 例如自定义魔法为 2.33X 1.00X ，魔法作用于默认是 2.00X 0.50X 的种子上时，获取到的魔法是 2.33x 1.00x ，而不是正确的 2.33x 0.50X
                    # 简单来说，自定义魔法不控制下载倍率时，脚本始终认为下载倍率为1
                    try:
                        Magic_DO = (re.findall(re5, v))[0]
                    except IndexError:
                        Magic_DO = '1.00X'
                    if Magic_DO == '0.00X':
                        Torrent_ID_List.append(Torrent_ID)
                    print(
                        f'{Magic_UP}↑ {Magic_DO}↓ ==> 魔法的ID:{Magic_ID}，种子的ID：{Torrent_ID}，魔法结束时间：{Magic_Start_Time}，魔法的时长：{Magic_Time}')

                if 'alt="FREE"' in v:  # 1x 上传 0x 下载
                    Magic_ID = (re.findall(re1, v))[0]
                    Torrent_ID = (re.findall(re2, v))[0]
                    Magic_Start_Time = (re.findall(re3, v))[0][0]
                    Magic_Time = (re.findall(re3, v))[0][1]
                    Torrent_ID_List.append(Torrent_ID)
                    print(
                        f'1.00X↑ 0.00X↓ ==> 魔法的ID:{Magic_ID}，种子的ID：{Torrent_ID}，魔法结束时间：{Magic_Start_Time}，魔法的时长：{Magic_Time}')

                if 'alt="2X"' in v:    # 2x 上传 1x 下载   奶子用
                    pass

                if 'alt="2X Free"' in v:  # 2x 上传 0x 下载
                    Magic_ID = (re.findall(re1, v))[0]
                    Torrent_ID = (re.findall(re2, v))[0]
                    Magic_Start_Time = (re.findall(re3, v))[0][0]
                    Magic_Time = (re.findall(re3, v))[0][1]
                    Torrent_ID_List.append(Torrent_ID)
                    print(
                        f'0.00X↑ 0.00X↓ ==> 魔法的ID:{Magic_ID}，种子的ID：{Torrent_ID}，魔法结束时间：{Magic_Start_Time}，魔法的时长：{Magic_Time}')


if __name__ == "__main__":
    Torrent_ID_List = []  # 创建记录种子ID的LIST
    # 默认查询2页种子优惠记录
    AnalysisMagic(
        openhtml('https://u2.dmhy.org/promotion.php?action=list&page=0', cookie))
    AnalysisMagic(
        openhtml('https://u2.dmhy.org/promotion.php?action=list&page=1', cookie))

    for v in Torrent_ID_List:
        print(v)  # 打印有优惠的种子ID
        # res1 = subprocess.call(
        #     f'python3 /home/qbt_add.py -I {v}', shell=True)
