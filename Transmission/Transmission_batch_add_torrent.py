# -*- coding: utf-8 -*-

# by kysdm
# https://github.com/kysdm/Some-scripts/blob/master/Transmission/Transmission_batch_add_torrent.py
# py脚本放置在种子所在文件夹中
#
# 示例 python tr.py -H "http://192.168.1.1:9091" -U "admin" -P "admin" -S "/home/root/" -F "root.torrent"

import os
import sys
import base64
import requests
import json
import argparse
import time


parser = argparse.ArgumentParser(description='Transmission batch add torrent')
parser.add_argument('-H', '--host', default='http://127.0.0.1:9091')
parser.add_argument('-U', '--username', default='admin')
parser.add_argument('-P', '--password', default='admin')
parser.add_argument('-S', '--save_path',default='/root/transmission/download/')
parser.add_argument('-F', '--file_name')
args = parser.parse_args()


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


# 获取更多Peer
def reannounce(headers):
    data = f'''{{"method":"torrent-reannounce","arguments":{{"ids":[{_id}]}}}}'''
    f = requests.post(rpc, data=data, headers=headers)
    v = json.loads(f.text)['result']
    return v

# 开始种子
def start(headers):
    data = f'''{{"method":"torrent-start","arguments":{{"ids":[{_id}]}}}}'''
    f = requests.post(rpc, data=data, headers=headers)
    v = json.loads(f.text)['result']
    return v


def add(file, _dir, headers):
    if not os.path.exists(file):
        print(f'种子文件不存在：{file}')
        exit(0)
    f = open(file, "rb").read()
    _base64 = str(base64.b64encode(f))[2:-1]

    data = f'''{{"method":"torrent-add","arguments":{{"paused":true,"download-dir":"{_dir}","metainfo":"{_base64}"}}}}'''

    f = requests.post(rpc, data=data.encode('utf-8'), headers=headers)
    v = json.loads(f.text)

    if 'invalid or corrupt torrent file' in str(v):
        print(f'无效种子：{_file}')
        exit(0)
    elif '\'torrent-duplicate\'' in str(v):
        print(f'重复添加：{_file}')
        exit(0)
    elif '\'torrent-added\'' in str(v):
        _id = v['arguments']['torrent-added']['id']
        return _id


if __name__ == '__main__':
    abs_path = os.path.split(os.path.realpath(__file__))[0]
    url = args.host
    rpc = f'{url}/transmission/rpc'
    _file = args.file_name
    _headers = login(url, args.username, args.password)
    _id = add(f'{abs_path}/{_file}', args.save_path, _headers)
    time.sleep(15)  # 等待10秒，防止硬盘IO忙
    f1 = reannounce(_headers)
    time.sleep(10)
    f2 = start(_headers)

    if f1 == 'success' and f2 == 'success':
        print(f'{_file} 添加成功！')
    else:
        f2 = "n"
        while f2 == 'y':
            f2 = input('输入Y|y继续:')
            if 'y' == f2.lower():
                exit(1)
                break
