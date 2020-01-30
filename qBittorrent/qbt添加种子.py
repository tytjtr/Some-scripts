#coding = utf-8

# by kysdm(gxk7231@gmail.com)
# 自动将文件夹中所有种子添加到qbt中，并删除成功添加的种子文件
# 简易用法 [将'C:\complete'目录中的种子添加到qbt中，文件保存位置为'D:\F']
# python "C:\Plugin\qbittorrent_x64_portable\qbt添加种子.py" -P "adminadmin" -F "C:\complete" -C "BT" -S "D:\F"

import time
import os
import sys
import qbittorrentapi
# pip install qbittorrent-api
import shutil
import argparse
import psutil
# pip install psutil

parser = argparse.ArgumentParser(description='Add seeds automatically')
parser.add_argument('-H', '--host', default='127.0.0.1:8080', help='qb host')
parser.add_argument('-U', '--user', default='admin', help='username')
parser.add_argument('-P', '--password', default='adminadmin', help='password')
parser.add_argument('-F', '--files', help='list of torrent files')
parser.add_argument('-C', '--category', help='torrent category')
parser.add_argument('-S', '--savepath', help='torrent save path')
parser.add_argument('-L', '--speedlimit', help='Speed limit')

args = parser.parse_args()

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(host=args.host, username=args.user, password=args.password)

# the Client will automatically acquire/maintain a logged in state in line with any request.
# therefore, this is not necessary; however, you many want to test the provided login credentials.
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

def findAllTorrent(root_dir):
    paths = []
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith((".torrent")):
                paths.append(parent + "\\" + filename + "==>" + filename)
    return paths

def judgeprocess(processname):
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == processname:
            print(pid)
            main()
            sys.exit(0)
        else:
            pass
    print("qbt未运行,3秒后退出")
    time.sleep(3)
    sys.exit(0)   

def main():
    # 打印 qBittorrent 版本信息
    print(f'qBittorrent: {qbt_client.app.version}')
    print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')
    print("\n")
    paths = findAllTorrent(args.files)
    for i in range(paths.__len__()):
        try:
            print("Torrent", (i + 1), "/", paths.__len__().__str__())
            Torrent_path = paths[i].split('==>', 1)[0]
            print(Torrent_path)
            f = qbt_client.torrents_add(torrent_files=Torrent_path, save_path=args.savepath, category=args.category, is_root_folder=True, upload_limit=args.speedlimit)
            time.sleep(1)
            if f == "Ok.":
                print(f)
                os.remove(Torrent_path)
                time.sleep(4)
        except Exception:
            print("导入失败，请检查种子文件！")
        else:
            pass


if __name__ == '__main__':
    judgeprocess("qbittorrent.exe")