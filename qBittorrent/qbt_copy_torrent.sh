#!/bin/bash
# by kysdm
# 在'Torrent 完成时运行外部程序'中填入 /tmp/qbt_copy_torrent.sh "%N" "%L" "%G" "%F" "%R" "%D" "%C" "%Z" "%T" "%I"     # /tmp/qbt_copy_torrent.sh 为脚本所在绝对路径

Torrent_name="${1}" # %N：Torrent 名称
Category="${2}" # %L：分类
Tags="${3}" # %G: 标签 （用逗号分隔）
Content_path="${4}" # %F：内容路径（与多文件 torrent 的根目录相同）
Root_path="${5}" # %R：根目录（第一个 torrent 的子目录路径）
Save_path="${6}" # %D：保存路径
Number_of_files="${7}" # %C：文件数
Torrent_size="${8}" # %Z：Torrent 大小（字节）
Current_tracker="${9}" # %T：当前 tracker
Info_hash="${10}" # %I：哈希值

# 指定种子存放绝对路径
BT_backup='/root/.local/share/data/qBittorrent/BT_backup/'

if [[ "$Number_of_files"x == "1"x ]] && [[ "$Content_path"x == "$Root_path"x ]]; then
   if [ -n "$Current_tracker" ]; then
    # 存在tracker
    domain="$(echo $Current_tracker | awk -F'[/:]' '{print $4}')"
    hash="$(echo $Info_hash | cut -c 1-5)"
    cp -f "${BT_backup}${Info_hash}.torrent" "${Save_path}${Torrent_name}_${domain}.${hash}.torrent"
   else
    hash="$(echo $Info_hash | cut -c 1-5)"
    cp -f "${BT_backup}${Info_hash}.torrent" "${Save_path}${Torrent_name}.${hash}.torrent"
   fi
else
   if [ -n "$Current_tracker" ]; then
    # 存在tracker
    domain="$(echo $Current_tracker | awk -F'[/:]' '{print $4}')"
    hash="$(echo $Info_hash | cut -c 1-5)"
    cp -f "${BT_backup}${Info_hash}.torrent" "${Root_path}/${Torrent_name}_${domain}.${hash}.torrent"
   else
    hash="$(echo $Info_hash | cut -c 1-5)"
    cp -f "${BT_backup}${Info_hash}.torrent" "${Root_path}/${Torrent_name}.${hash}.torrent"
   fi
fi