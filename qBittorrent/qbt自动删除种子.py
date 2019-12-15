#coding = utf-8

# by kysdm(gxk7231@gmail.com)
# 自动删除指定分类超过指定做种时间的种子
# 简易用法 [删除种子分类为'BT'且做种时间已超过5分钟的种子不<删除已下载的文件>]
# python "C:\Plugin\qbittorrent_x64_portable\qbt自动删除种子.py" -P "adminadmin" -C "BT" -T "5"

import time
import sys
import os,datetime
import qbittorrentapi
# pip install qbittorrent-api
import shutil
import argparse
import psutil
# pip install psutil

parser = argparse.ArgumentParser(description='Automatically delete BT seeds')
parser.add_argument('-H', '--host', default='127.0.0.1:8080', help='qb host')
parser.add_argument('-U', '--user', default='admin', help='username')
parser.add_argument('-P', '--password', default='adminadmin', help='password')
parser.add_argument('-T', '--time', default='5', help='How long does it take to delete a seed')
parser.add_argument('-C', '--category', help='Category of torrent')
args = parser.parse_args()

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(host=args.host, username=args.user, password=args.password)

# the Client will automatically acquire/maintain a logged in state in line with any request.
# therefore, this is not necessary; however, you many want to test the provided login credentials.
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

def main():
    # 打印 qBittorrent 版本信息
    print(f'qBittorrent: {qbt_client.app.version}')
    print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')
    print("\n")
    for torrent in qbt_client.torrents_info(category=args.category):
        nowtime = datetime.datetime.now() # 当前系统时间 [时间元组]
        complete_time = torrent.completion_on # 种子完成时间 [时间戳]
        # api v2.2 种子未完成 complete_time=4294967295 [2106-02-07 14:28:15]
        # api v2.3 种子未完成 complete_time=-28800 [错误]
        if complete_time < 0: # 兼容 api v2.3
            complete_time = 4294967295
        complete_time_humanity = datetime.datetime.fromtimestamp(complete_time)# 种子完成时间 [时间元组]
        # print(f'种子哈希值：{torrent.hash}')
        # print(f'种子名：{torrent.name}')
        # print(f'种子当前状态：{torrent.state}')
        # print(f'种子下载完成时间：{complete_time_humanity}')
        TimeDifference = int(str(((nowtime - complete_time_humanity).total_seconds())).split('.', 1)[0])  # 与当前系统时间相差时间 单位S
        # print(f'与当前时间相差：{TimeDifference} 秒')

        if (TimeDifference) > (int(args.time)*60):
#            print(f'超过{args.time}分钟：{torrent.name}')
#            print("\n")
            print(f'删除种子：{torrent.name}')
            qbt_client.torrents_delete(delete_files=torrent.name, hashes=torrent.hash)
            time.sleep(1)
            print("\n")
        else:
             pass
#            print(f'未超过{args.time}分钟：{torrent.name}')
#            time.sleep(3)
#            print("\n")

def judgeprocess(processname):
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == processname:
            print(f'PID：{pid}\n')
            main()
            sys.exit(0)
        else:
            pass
    print("qbt未运行,3秒后退出")
    time.sleep(3)
    sys.exit(0)      
if __name__ == '__main__':
    judgeprocess("qbittorrent.exe")