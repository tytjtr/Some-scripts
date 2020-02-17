#coding = utf-8

# by kysdm

# 需配合另一个sh脚本

import time
import sys
import os
import json
import shutil
import subprocess
import psutil
import re
import requests
import csv


TR_APP_VERSION = sys.argv[1][1:-1]
TR_TORRENT_DIR = sys.argv[2][1:-1]
TR_TORRENT_HASH = sys.argv[3][1:-1]
TR_TORRENT_ID = sys.argv[4][1:-1]
TR_TORRENT_NAME = sys.argv[5][1:-1]


# 记录账户上传量
def AccountLimit(size):
    if os.path.exists(f'{abs_path}/Limit.csv'):
        print('找到 Limit 数据库，初始化中...')
        with open(f'{abs_path}/Limit.csv', "r", encoding='utf-8-sig') as csv_file:
            reader = csv.reader(csv_file)
            for string in reader:
                data_csv = string
            # print(data_csv)
        csv_file.close()
    else:  # 不存在时，直接写入当前传入的账户名和文件大小
        print('Limit 数据库不存在，初始化中...')
        data_csv = ['5', '0']
    Limit = 700 * 1024 * 1024 * 1024  # 每个账户传输上限
    all_size = int(size) + int(data_csv[1])
    print(
        f'账户：{data_csv[0]} 已传输：{int(int(data_csv[1]) / 1024 / 1024 / 1024)}G')
    print(f'当前文件夹大小：{int(int(size) / 1024 / 1024 / 1024)}G')

    time.sleep(5)
    if all_size > Limit:
        change_account = int(data_csv[0]) + 1
        all_size = int(size)
        if change_account > 150:
            change_account = 5
    else:
        change_account = data_csv[0]

    print(f'当前任务使用账户：{change_account}')

    with open(f'{abs_path}/Limit.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([change_account, all_size])
        csv_file.close()
    return change_account


# 获取文件夹的大小，返回字节
def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name))
                     for name in files])
    return size


def rcloneexe(_id):
    account = AccountLimit(getdirsize(TR_TORRENT_DIR))
    # 修改rclone配置文件
    f1 = open(f'{abs_path}/rclone.conf', 'r+')
    infos = f1.readlines()
    f1.seek(0, 0)
    for line in infos:
        pattern = re.compile(r'(\/accounts\/\d+.json)')
        # print(pattern.findall(line))
        line_new = re.sub(pattern, f'/accounts/{account}.json', line)
        f1.write(line_new)
    f1.close()
    __dir = abs_path
    res1 = subprocess.call(
        f'rclone copy {TR_TORRENT_DIR} share:/盒子上传目录/{_id} -P  --config "{abs_path}/rclone.conf" --drive-acknowledge-abuse --bwlimit 45M', shell=True, cwd=__dir)

    if res1 != 0:
        print('rclone传输出现错误！')
        rcloneexe(_id)
    else:
        print('rclone传输正常完成！')


def reomvefile(path):
    __dir = abs_path
    print(f'准备删除文件夹：{path}')
    time.sleep(5)
    f = subprocess.call(f'rm -r {path}', shell=True, cwd=__dir)
    print(f'删除下载文件返回值：{f}')
    Judge = '1'
    while Judge != '0':
        try:
            os.remove(f'{abs_path}/zidonghua.lock')
            Judge = '0'
        except Exception as e:
            Judge = e
            print(e)


# 登录
def login(url, username, password):
    s = requests.session()  # 保持session
    f = s.get(url, auth=(username, password))  # GET TR管理地址
    _headers = f.request.headers  # 获取请求头
    _headers.setdefault('X-Transmission-Session-Id', '0')  # 在请求头中增加参数
    _url = f.request.url  # 获取实际TR管理地址
    data = f'''{{"method":"session-get","arguments":{{}},"tag":""}}'''  # 构造POST所需的数据
    f = s.post(rpc, data=data, headers=_headers)  # POST RPC地址
    session_id = f.headers.get('X-Transmission-Session-Id')  # 在请求头中获取 Token
    _headers['X-Transmission-Session-Id'] = session_id  # 修改请求头的参数
    return _headers


def deltorrent(_id):
    data = f'''{{"method":"torrent-remove","arguments":{{"ids":[{_id}],"delete-local-data":false}},"tag":""}}'''
    print(f'30s后删除种子：ID:{TR_TORRENT_ID}, name：{TR_TORRENT_NAME}')
    time.sleep(30)
    f = requests.post(rpc, data=data.encode('utf-8'),
                      headers=login(url, username, password))
    v = json.loads(f.text)['result']
    print(f'种子删除情况：{v}')


def huoquid(path):
    re1 = re.compile(r'^/.+/(\d+)/?', re.S)  # 分类
    _id = (re.findall(re1, path)[0])
    return _id


def yunnow():
    print('############## Start ###################')
    print(f'脚本所在绝对路径：{abs_path}')
    print(f'transmission: {TR_APP_VERSION}')
    print(f'Torrent 名称: {TR_TORRENT_NAME}')
    print(f'保存路径: {TR_TORRENT_DIR}')
    print(f'哈希值: {TR_TORRENT_HASH}')
    print("\n")

    _id = huoquid(TR_TORRENT_DIR)
    rcloneexe(_id)
    deltorrent(TR_TORRENT_ID)
    reomvefile(TR_TORRENT_DIR)

    print('############### End ####################')


def pythonnum(hashobj):
    if os.path.exists(f'{abs_path}/zidonghua.lock'):
        # print(hashobj)
        with open(f'{abs_path}/zidonghua.lock', "r", encoding='utf-8-sig') as f:
            reader = f.readlines()
            data_lock = reader[0]
        if str(data_lock) != str(hashobj):
            pythonnum = 1
        else:
            pythonnum = 0
    else:
        with open(f'{abs_path}/zidonghua.lock', "w", encoding='utf-8-sig') as f:
            f.write(hashobj)
        with open(f'{abs_path}/zidonghua.lock', "r", encoding='utf-8-sig') as f:
            reader = f.readlines()
            data_lock = reader[0]
        if str(data_lock) != str(hashobj):
            pythonnum = 1
        else:
            pythonnum = 0
    return pythonnum


if __name__ == '__main__':
    abs_path = os.path.split(os.path.realpath(__file__))[0]
    url = 'http://127.0.0.1:9091'
    rpc = f'{url}/transmission/rpc'
    username = 'admin'
    password = 'xxxxxx'

    while pythonnum(TR_TORRENT_HASH) == 1:
        print('【进程已运行】')
        time.sleep(30)

    yunnow()
