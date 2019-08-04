# coding=utf-8

import bencoding
import hashlib
import os
import sys
import shutil

# "C:\Program Files\Python37\python.exe" "C:\Plugin\uTorrent_1\ut_copy_torrent.py" "-%D" "-%N" "-%T" "-%I"
torrent_folder = r'C:\\Plugin\\uTorrent_1\\'  # 种子文件存放目录

D = sys.argv[1][1:]
Dx = D.replace('\\', '\\\\')
N = sys.argv[2][1:]
T = sys.argv[3][1:]
I = sys.argv[4][1:]
# print('-------------')
# print(D)
# print(文件保存的目录)
# print(N)
# print(T)
# print(I)


def search(path, name):
    for file in os.listdir(path):
        if os.path.isfile(path + '\\' + file):
            if name in file:
                list1.append(file)
        else:
            search(path + '\\' + file, name)


def hash(filename):
    for file_fuck in filename:
        torrent_file = f'{torrent_folder}{file_fuck}'
        objTorrentFile = open(torrent_file, 'rb')
        decodedDict = bencoding.bdecode(objTorrentFile.read())
        objTorrentFile.close()
        info_hash = hashlib.sha1(bencoding.bencode(
            decodedDict[b"info"])).hexdigest()
        list2.append(f'{info_hash}==>{torrent_file}')


def copy(infohash):
    for hash in infohash:
        if I.lower() in hash:
            if T == "":
                shutil.copy(hash.split('==>', 1)[
                            1], f'{Dx}\\{N}.{I[0:6].lower()}.torrent')
            else:
                shutil.copy(hash.split('==>', 1)[
                            1], f'{Dx}\\{N}.{T.split("/")[2]}.{I[0:6].lower()}.torrent')


if __name__ == "__main__":
    list1 = []
    list2 = []
    search(os.path.abspath(torrent_folder), N)
    hash(list1)
    copy(list2)
