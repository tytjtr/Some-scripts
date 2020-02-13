#coding = utf-8

# by kysdm(gxk7231@gmail.com)
#
# 传入种子ID，自动添加到 qBittorrent
#
# 批量移除了用户变量，估计运行不会报错


import time
import os
import sys
import qbittorrentapi
# pip3 install qbittorrent-api
import shutil
import argparse
import psutil
# pip3 install psutil
import urllib
from urllib import request
import csv

# **************用户变量********************

passkey = 'xxxxxxxxxxxxxxxxxx'

# **************用户变量********************


parser = argparse.ArgumentParser(description='qBittorrent batch add torrent')
parser.add_argument('-H', '--host', default='127.0.0.1:8080')
parser.add_argument('-U', '--useradmin', default='admin')
parser.add_argument('-P', '--password', default='adminadmin')
parser.add_argument('-F', '--files')
parser.add_argument('-C', '--category')
parser.add_argument('-S', '--savepath')
parser.add_argument('-L', '--speedlimit', default='0')
parser.add_argument('-I', '--torrent_id')
args = parser.parse_args()

qbt_client = qbittorrentapi.Client(
    host=args.host, username=args.useradmin, password=args.password)

try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)


def DownTorrent(var):
    url = f'https://u2.dmhy.org/download.php?id={var}&passkey={passkey}&https=1'
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('cache-control', 'no-cache'),
        ('pragma', 'no-cache'),
        ('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, f'{abs_path}/{var}.torrent')

# 这个函数可能有bug


def percentage(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小 
    @totalsize: 远程文件的大小 
    '''
    i = blocknum * blocksize
    n = totalsize
    print('\r{}{}%'.format(['/', '-', '\\'][i % 3] if n >=
                           i else '', int(i/n*100)), end='' if n >= i else '\n')


def AddTorrent(var):
    # 打印 qBittorrent 版本信息
    print(f'qBittorrent: {qbt_client.app.version}')
    print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')
    print("\n")
    try:
        Torrent_path = f'{abs_path}/{var}.torrent'
        print(Torrent_path)
        f = qbt_client.torrents_add(
            torrent_files=Torrent_path, category=var, is_root_folder=True, upload_limit=args.speedlimit)
        if f == "Ok.":
            print(f)
            with open(f'{abs_path}/u2id.csv', 'a', newline='', encoding='utf-8-sig') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([args.torrent_id])
                csv_file.close()
                print(f'ID:{args.torrent_id} 成功写入数据库！')
            os.remove(Torrent_path)
    except Exception:
        print("导入失败，请检查种子文件！")
        os.remove(Torrent_path)
    else:
        pass


def CsvTorrent():
    if os.path.exists(f'{abs_path}/u2id.csv'):  # 已存在数据库时
        print("发现数据库，正在比对中...\n")
        with open(f'{abs_path}/u2id.csv', "r", encoding='utf-8-sig') as csv_file:  # 读取数据库文件
            reader = csv.reader(csv_file)
            for string in reader:  # 将数据库的唯一识别码导入数列
                # print(string[0])
                if str(string[0]) == str(args.torrent_id):
                    print(f'ID:{args.torrent_id} 已在数据库中！')
                    exit(0)
        csv_file.close()
        print(f'ID:{args.torrent_id} 开始下载...')


if __name__ == '__main__':
    abs_path = os.path.split(os.path.realpath(__file__))[0]
    CsvTorrent()
    DownTorrent(args.torrent_id)
    AddTorrent(args.torrent_id)
