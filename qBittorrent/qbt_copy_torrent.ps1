# �Զ����������ļ��������ļ����λ��
# v0.3
#
# ���÷���
# ��qbt�����ʱ�����ⲿ�����м������������ ��C:\Plugin\qbittorrent_x64_portable\qbt_copy_torrent.ps1��ΪPS�ű����ھ���·��
# PowerShell.exe -file "C:\Plugin\qbittorrent_x64_portable\qbt_copy_torrent.ps1" -N "%N" -L "%L" -G "%G" -F "%F" -R "%R" -D "%D" -C "%C" -Z "%Z" -T "%T" -I "%I"
# �����޸ĵ�12,13�еĴ���
#
param($N,$L,$G,$F,$R,$D,$C,$Z,$T,$I) # ��ȡ�ⲿ����

$debug_switch = "1" # 0�����log��1���log
$BT_backup = "C:\Plugin\qbittorrent_x64_portable\profile\qBittorrent\data\BT_backup" # ����qbt��������ļ���Ŀ¼
$log_folder = "C:\Plugin\qbittorrent_x64_portable\log" # ����ű�debug��־�ļ����λ��

If( $debug_switch -eq 1 )
  { 
   switch( Test-Path $log_folder )   {      "False"  { New-Item $log_folder -type directory }    } # �ж�Log�ļ����Ƿ����
   $time = Get-Date -Format 'yyyyMMddHHmmss'  #��ȡ��ǰʱ��
   $outlog = -join ("$log_folder","\","$time","_","$I",".log")
   write-output "Torrent���ƣ�$N"   | out-file -filepath  $outlog
   write-output "���ࣺ$L"  | out-file  -Append $outlog
   write-output "��ǩ���ö��ŷָ�����$G"  | out-file  -Append  $outlog
   write-output "����·��������ļ� torrent �ĸ�Ŀ¼��ͬ����$F"  | out-file  -Append $outlog 
   write-output "��Ŀ¼����һ�� torrent ����Ŀ¼·������$R"  | out-file  -Append $outlog
   write-output "����·����$D"  | out-file  -Append  $outlog
   write-output "�ļ�����$C"  | out-file  -Append $outlog 
   write-output "Torrent ��С��$Z"  | out-file  -Append $outlog 
   write-output "��ǰ tracker��$T"  | out-file  -Append  $outlog 
   write-output "��ϣֵ��$I"  | out-file  -Append  $outlog 
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