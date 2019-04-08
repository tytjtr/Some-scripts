# 自动复制种子文件到下载文件存放位置
# v0.1
#
# 第一次用PS写脚本，因为没有BUG吧
#
# 【用法】
# 在qbt的完成时运行外部程序中加入下面的内容 【C:\Users\kysdm\Desktop\1.ps1】为PS脚本所在绝对路径
# PowerShell.exe -file C:\Users\kysdm\Desktop\1.ps1 -N "%N" -L "%L" -G "%G" -F "%F" -R "%R" -D "%D" -C "%C" -Z "%Z" -T "%T" -I "%I"
# 还需修改第28行的代码
#
# 接下来需要解决的问题
# 如果种子没有文件夹，复制过去的种子就肯定是与文件在同级目录的，但如果种子是带文件夹的，现阶段只能复制到上级目录，可能解决起来很简单，没时间看了-咕咕咕-
#
# 获取外部变量
param($N,$L,$G,$F,$R,$D,$C,$Z,$T,$I)
# 调试部分
# write-output "Torrent名称：$N"   | out-file -filepath   d:\debug.txt 
# write-output "分类：$L"  | out-file  -Append d:\debug.txt 
# write-output "标签（用逗号分隔）：$G"  | out-file  -Append  d:\debug.txt 
# write-output "内容路径（与多文件 torrent 的根目录相同）：$F"  | out-file  -Append d:\debug.txt 
# write-output "根目录（第一个 torrent 的子目录路径）：$R"  | out-file  -Append d:\debug.txt 
# write-output "保存路径：$D"  | out-file  -Append  d:\debug.txt 
# write-output "文件数：$C"  | out-file  -Append d:\debug.txt 
# write-output "Torrent 大小：$Z"  | out-file  -Append d:\debug.txt 
# write-output "当前 tracker：$T"  | out-file  -Append  d:\debug.txt 
# write-output "哈希值：$I"  | out-file  -Append  d:\debug.txt 

# 定义qbt存放种子文件的目录
$BT_backup = "C:\Users\kysdm\Desktop\qbittorrent_x64_portable\profile\qBittorrent\data\BT_backup"

copy-Item "$BT_backup\$I.torrent"  "$D\$N.torrent"