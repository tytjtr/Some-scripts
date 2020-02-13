# -*- coding: utf-8 -*-

# by kysdm

import re
from bs4 import BeautifulSoup
# pip3 install bs4
# pip3 install lxml
import requests

# **************用户变量********************

uid = 'xxxxx'
cookie = '__cfduid=xxxxx; nexusphp_u2=xxxxx; __dtsu=xxxxx'

# **************用户变量********************


def tlist():
    headers = {
        'Referer': f'https://u2.dmhy.org/userdetails.php?id={uid}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'cookie': cookie
    }
    print('开始下载列表... (如果报错，代表连接U2失败)\n')
    html = requests.get(
        f'https://u2.dmhy.org/getusertorrentlistajax.php?userid={uid}&type=leeching', headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    tobj = soup.find_all('table', attrs={'class': 'torrentname'})
    tobj2 = soup.find_all(href=re.compile(r'^details.+#seeders', re.S))
    re1 = re.compile(r'href="details.php\?id=(\d+?)&amp;hit=1"', re.S)
    re2 = re.compile(r'<img\s?alt="上传比率".+?><b>(.+?)<\/b>', re.S)
    re3 = re.compile(r'<img\s?alt="下载比率".+?><b>(.+?)<\/b>', re.S)
    re4 = re.compile(r'details.php\?id=(\d+)', re.S)
    re5 = re.compile(r'>(\d+?)</a>', re.S)

    seeders = []
    for v in tobj2:
        _id = (re.findall(re4, str(v)))[0]
        _seeders = (re.findall(re5, str(v)))[0]
        seeders.append((_id, _seeders))

    for v in tobj:
        if 'alt="2X Free"' in str(v):
            texit((re.findall(re1, str(v)))[0], '2X Free')
        elif 'alt="FREE"' in str(v):
            texit((re.findall(re1, str(v)))[0], 'FREE')
        elif 'alt="下载比率"' in str(v) and '<b>0.00X</b>' in str(v):
            texit((re.findall(re1, str(v)))[
                0], f'{(re.findall(re2, str(v)))[0]} {(re.findall(re3, str(v)))[0]}')
        else:
            Magic((re.findall(re1, str(v)))[0], seeders)


def texit(t_id, mag):
    if mag == 'FREE':
        print(f'ID：{t_id} 已存在魔法：{mag}')
    elif mag == '2X Free':
        print(f'ID：{t_id} 已存在魔法：{mag}')
    else:
        print(f'ID：{t_id} 已存在魔法：{mag}')


def Magic(torrent_id, seeders):
    for v in seeders:
        if str(v[0]) == str(torrent_id):
            if int(v[1]) == 0:
                print(f'ID：{torrent_id} 无人做种，暂不释放魔法')
            else:
                # 下面注释掉的参数，估计是用来计算所需uc的，反正有钱，不计算了
                data = {
                    'action': 'magic',
                    # 'divergence':'6.974',#全站基数
                    # 'base_everyone':'1200',
                    # 'base_self':'350',
                    # 'base_other':'500',
                    'torrent': torrent_id,  # 种子ID
                    # 'tsize':'3822707742',#种子大小
                    # 'ttl':'4163',#种子已存在时间
                    'user': 'SELF',  # 为自己放魔法
                    # 'user_other':'',
                    'start': '0',  # 魔法立即生效
                    'hours': '24',  # 魔法有效期24小时
                    'promotion': '8',  # 魔法类型为其他
                    'ur': '1.00',  # 上传比率
                    'dr': '0.00',  # 下载比率
                    'comment': ''  # 评论
                }
                headers = {
                    'Referer': f'https://u2.dmhy.org/promotion.php?action=magic&torrent={torrent_id}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                    'cookie': cookie
                }

                f = requests.post(
                    f'https://u2.dmhy.org/promotion.php?action=magic&torrent={torrent_id}', data=data, headers=headers)
                status_code = f.status_code
                if status_code == 200:
                    print(f'ID：{torrent_id} 成功施加马猴 (')
                else:
                    print(f'ID：{torrent_id} 错误，code.{status_code}')


if __name__ == "__main__":
    tlist()
