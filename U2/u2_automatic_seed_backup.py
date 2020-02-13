# -*- coding: utf-8 -*-

# by kysdm(gxk7231@gmail.com)
# 将脚本改成能看的过去的样子，估计能运行的吧
# 有些变量还是定死的，如果不能满足下面的要求，那就需要自己改脚本了

# 要求
# 假设脚本所在文件夹为x
# accounts 文件夹放置在x中
# accounts json 文件 1.json 2.json 3.json ... 199.json 200.json
# rclone.conf 文件放置在x中
#   [share]
#   type = drive
#   scope = drive
#   service_account_file = f'{x}/accounts/24.json'
#   team_drive = xxxxxxxxxxx
# qBittorrent 下载目录为 Downloads，并在x中
# python3.6+


# 用法
# 在 qBittorrent 'Torrent 完成时运行外部程序' 填入以下信息
# python3 /home/u2_automatic_seed_backup.py  -H "127.0.0.1:8080" -U "xxx" -P "xxx"  -TN "%N" -C "%L" -CP "%F" -RP "%R" -SP "%D" -N "%C" -I "%I"

import time
import sys
import os
import datetime
import qbittorrentapi
# pip3 install qbittorrent-api
import shutil
import argparse
import psutil
# pip3 install psutil
import re
import subprocess
import csv


abs_path = os.path.split(os.path.realpath(__file__))[0]

# **************用户变量********************

BT_backup = r'/root/.local/share/data/qBittorrent/BT_backup'  # 指定种子存放绝对路径
BT_FILCE = f'{abs_path}/Downloads/ZHONGZI'  # 从 BT_backup 复制的种子文件存放位置
RAR = r'/home/rar/rar'  # RAR二进制文件绝对路径 【需要可执行权限】
rclone = r'/home/rclone/rclone'  # rclone二进制文件绝对路径 【需要可执行权限】
RAR_Password = 'xxxxx'  # RAR压缩包的密码

# **************用户变量********************

parser = argparse.ArgumentParser(description='Automatically delete BT seeds')
parser.add_argument('-H', '--host', default='127.0.0.1:8080')
parser.add_argument('-U', '--username', default='admin')
parser.add_argument('-P', '--password', default='adminadmin')
parser.add_argument('-TN', '--Torrent_name')            # %N：Torrent 名称
parser.add_argument('-C', '--Category')                 # %L：分类
# parser.add_argument('-T', '--Tags')                     # %G: 标签 （用逗号分隔）
parser.add_argument('-CP', '--Content_path')
parser.add_argument('-RP', '--Root_path')
parser.add_argument('-SP', '--Save_path')               # %D：保存路径
parser.add_argument('-N', '--Number_of_files')          # %C：文件数
# parser.add_argument('-TS', '--Torrent_size')            # %Z：Torrent 大小（字节）
# parser.add_argument('-CT', '--Current_tracker')         # %T：当前 tracker
parser.add_argument('-I', '--Info_hash')                # %I：哈希值
args = parser.parse_args()

qbt_client = qbittorrentapi.Client(
    host=args.host, username=args.username, password=args.password)


try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)


def copytorrent():
    print('复制种子开始运行')
    hashobj = args.Info_hash[0:5]
    shutil.copy(f'{BT_backup}/{args.Info_hash}.torrent',
                f'{BT_FILCE}/{args.Category}-{args.Torrent_name}.{hashobj}.torrent')


def movefile():
    if (args.Number_of_files == '1') and (args.Content_path == args.Root_path):
        shutil.move(f'{args.Save_path}{args.Torrent_name}',
                    f'{mubiaowenjianjia}')
    else:
        shutil.move(f'{args.Root_path}', f'{mubiaowenjianjia}')


def deltorrent():
    print(f'删除种子:{args.Torrent_name}')
    qbt_client.torrents_delete(
        delete_files=args.Torrent_name, hashes=args.Info_hash)
    time.sleep(1)
    print("\n")


# 记录账户上传量
def AccountLimit(size):
    if os.path.exists(f'{abs_path}/Limit.csv'):  # 已存在数据库时
        print('找到 Limit 数据库，初始化中...')
        with open(f'{abs_path}/Limit.csv', "r", encoding='utf-8-sig') as csv_file:  # 读取数据库文件
            reader = csv.reader(csv_file)
            for string in reader:  # 将数据库的唯一识别码导入数列
                data_csv = string
        csv_file.close()
    else:  # 不存在时，直接写入当前传入的账户名和文件大小
        print('Limit 数据库不存在，初始化中...')
        data_csv = ['1', '0']  # 谷歌团队盘用户json的"最小"的文件名

    Limit = 700 * 1024 * 1024 * 1024  # 每个账户传输上限
    all_size = int(size) + int(data_csv[1])
    print(
        f'账户：{data_csv[0]} 已传输：{int(int(data_csv[1]) / 1024 / 1024 / 1024)}G')
    print(f'当前文件夹大小：{int(int(size) / 1024 / 1024 / 1024)}G')

    time.sleep(5)
    if all_size > Limit:
        change_account = int(data_csv[0]) + 1
        all_size = int(size)
        if change_account > 200:  # 谷歌团队盘用户json的"最大"的文件名
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


# 列出文件夹中的文件，不包含文件夹
def readfile(path):
    files = os.listdir(path)
    file_list = []
    for file in files:  # 遍历文件夹
        file_path = f'{path}/{file}'
        if not os.path.isdir(file_path):
            file_list.append(file_path)
    return file_list


def rcloneexe():
    Local_directory = mubiaowenjianjia
    account = AccountLimit(getdirsize(Local_directory))

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
        f'{rclone} copy {Local_directory} share:/盒子上传目录/{args.Category} --stats 30s --log-level INFO  --config "{abs_path}/rclone.conf" --drive-acknowledge-abuse --bwlimit 45M', shell=True, cwd=__dir)
    res2 = subprocess.call(
        f'{rclone} copy {BT_FILCE} share:/盒子上传目录/种子文件/ --stats 30s --log-level INFO  --config "{abs_path}/rclone.conf" --drive-acknowledge-abuse --bwlimit 45M', shell=True, cwd=__dir)
    if res1 != 0 or res2 != 0:
        print('rclone传输出现错误！')
        rcloneexe()
    else:
        print('rclone传输正常完成！')


def reomvefile():
    __dir = abs_path
    print(f'准备删除文件夹：{mubiaowenjianjia}')
    time.sleep(5)
    f = subprocess.call(f'rm -r {mubiaowenjianjia}', shell=True, cwd=__dir)
    print(f'删除下载文件返回值：{f}')
    f2 = subprocess.call(
        f'rm {BT_FILCE}/{args.Category}*.torrent', shell=True, cwd=__dir)
    print(f'删除种子文件返回值：{f2}')
    Judge = '1'
    while Judge != '0':
        try:
            os.remove(f'{abs_path}/zidonghua.lock')
            Judge = '0'
        except Exception as e:
            Judge = e
            print(e)


def yunnow():
    print('############## Start ###################')
    print(f'脚本所在绝对路径：{abs_path}')
    print(f'qBittorrent: {qbt_client.app.version}')
    print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')
    print("\n")
    print(f'Torrent 名称: {args.Torrent_name}')
    print(f'分类: {args.Category}')
    # print(f'内容路径（与多文件 torrent 的根目录相同）: {args.Content_path}')
    # print(f'根目录（第一个 torrent 的子目录路径）: {args.Root_path}')
    print(f'保存路径: {args.Save_path}')
    print(f'文件数: {args.Number_of_files}')
    print(f'哈希值: {args.Info_hash}')
    print("\n")
    global mubiaowenjianjia
    mubiaowenjianjia = f'{abs_path}/Downloads/{args.Category}'
    if not os.path.exists(f'{mubiaowenjianjia}'):  # 创建存放文件的文件夹
        os.mkdir(f'{mubiaowenjianjia}')
    if not os.path.exists(f'{BT_FILCE}'):  # 创建存放文件的文件夹
        os.mkdir(f'{BT_FILCE}')
    copytorrent()
    if "no" in args.Category: #种子分类中包含no字符串时脚本直接退出
        print('此种子需要做种，程序退出')

        Judge = '1'
        while Judge != '0':
            try:
                os.remove(f'{abs_path}/zidonghua.lock')
                Judge = '0'
            except Exception as e:
                Judge = e
                print(e)
        exit(0)

    # 一堆猛如虎的操作
    time.sleep(10)
    deltorrent()
    time.sleep(5)
    movefile()
    time.sleep(5)
    CreateRAR()
    time.sleep(5)
    rcloneexe()
    time.sleep(5)
    reomvefile()
    print('############### End ####################')


def pythonnum(hashobj):
    if os.path.exists(f'{abs_path}/zidonghua.lock'):
        with open(f'{abs_path}/zidonghua.lock', "r", encoding='utf-8-sig') as f:  # 读取数据库文件
            reader = f.readlines()
            data_lock = reader[0]
        if str(data_lock) != str(hashobj):
            pythonnum = 1
        else:
            pythonnum = 0
    else:
        with open(f'{abs_path}/zidonghua.lock', "w", encoding='utf-8-sig') as f:
            f.write(hashobj)
        with open(f'{abs_path}/zidonghua.lock', "r", encoding='utf-8-sig') as f:  # 读取数据库文件
            reader = f.readlines()
            data_lock = reader[0]
        if str(data_lock) != str(hashobj):
            pythonnum = 1
        else:
            pythonnum = 0
    return pythonnum


def CreateRAR():
    RAR_File_Name = f'{args.Category}-{args.Torrent_name}.rar'
    Folder = f'{args.Torrent_name}'
    __dir = f'{abs_path}/Downloads/{args.Category}'
    print(
        f'创建RAR文件...\nRAR文件名：{RAR_File_Name}\n被压缩文件夹：{Folder}\n运行启动路径：{__dir}')
    time.sleep(3)
    try:
        res3 = subprocess.call(
            f'{RAR} a -hp"{RAR_Password}" -v4294967296B -m0 -ma5 -rr5p -md32M "{RAR_File_Name}" "{Folder}"', shell=True, cwd=__dir)
        if res3 != 0:
            print('RAR文件创建错误！\n')
        else:
            print('RAR文件创建成功！\n')

            if not os.path.exists(f'{__dir}/{args.Torrent_name} - RAR'):  # 创建存放文件的文件夹
                os.mkdir(f'{__dir}/{args.Torrent_name} - RAR')
            for v in readfile(__dir):
                if v.lower().endswith(".rar"):
                    shutil.move(f'{v}', f'{__dir}/{args.Torrent_name} - RAR')
    except Exception as e:
        print(f'发生错误：{e}')


if __name__ == '__main__':
    while pythonnum(args.Info_hash) == 1:
        print('【进程已运行】')
        time.sleep(30)
    yunnow()
