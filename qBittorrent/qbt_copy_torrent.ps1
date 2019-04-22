# 自动复制种子文件到下载文件存放位置
# v0.3
#
# 【用法】
# 在qbt的完成时运行外部程序中加入下面的内容 【C:\Plugin\qbittorrent_x64_portable\qbt_copy_torrent.ps1】为PS脚本所在绝对路径
# PowerShell.exe -file "C:\Plugin\qbittorrent_x64_portable\qbt_copy_torrent.ps1" -N "%N" -L "%L" -G "%G" -F "%F" -R "%R" -D "%D" -C "%C" -Z "%Z" -T "%T" -I "%I"
# 还需修改第12,13行的代码
#
param($N,$L,$G,$F,$R,$D,$C,$Z,$T,$I) # 获取外部变量

$debug_switch = "1" # 0不输出log，1输出log
$BT_backup = "C:\Plugin\qbittorrent_x64_portable\profile\qBittorrent\data\BT_backup" # 定义qbt存放种子文件的目录
$log_folder = "C:\Plugin\qbittorrent_x64_portable\log" # 定义脚本debug日志文件存放位置

If( $debug_switch -eq 1 )
  { 
   switch( Test-Path $log_folder )   {      "False"  { New-Item $log_folder -type directory }    } # 判断Log文件夹是否存在
   $time = Get-Date -Format 'yyyyMMddHHmmss'  #获取当前时间
   $outlog = -join ("$log_folder","\","$time","_","$I",".log")
   write-output "Torrent名称：$N"   | out-file -filepath  $outlog
   write-output "分类：$L"  | out-file  -Append $outlog
   write-output "标签（用逗号分隔）：$G"  | out-file  -Append  $outlog
   write-output "内容路径（与多文件 torrent 的根目录相同）：$F"  | out-file  -Append $outlog 
   write-output "根目录（第一个 torrent 的子目录路径）：$R"  | out-file  -Append $outlog
   write-output "保存路径：$D"  | out-file  -Append  $outlog
   write-output "文件数：$C"  | out-file  -Append $outlog 
   write-output "Torrent 大小：$Z"  | out-file  -Append $outlog 
   write-output "当前 tracker：$T"  | out-file  -Append  $outlog 
   write-output "哈希值：$I"  | out-file  -Append  $outlog 
  }

$shortI=$I.Substring(0,7)
  
If( ($C -eq 1) -and ("$F" -eq "$R") )
  {
   $outname = -join ("$D","\","$N","_","$time",".torrent")  
  }
Else
  {
   $outname = -join ("$R","\","$N","_","$time",".torrent")  
  }
 
copy-Item "$BT_backup\$I.torrent"  "$outname" 