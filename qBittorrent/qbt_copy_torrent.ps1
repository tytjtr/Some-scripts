# �Զ����������ļ��������ļ����λ��
# v0.1
#
# ��һ����PSд�ű�����Ϊû��BUG��
#
# ���÷���
# ��qbt�����ʱ�����ⲿ�����м������������ ��C:\Users\kysdm\Desktop\1.ps1��ΪPS�ű����ھ���·��
# PowerShell.exe -file C:\Users\kysdm\Desktop\1.ps1 -N "%N" -L "%L" -G "%G" -F "%F" -R "%R" -D "%D" -C "%C" -Z "%Z" -T "%T" -I "%I"
# �����޸ĵ�28�еĴ���
#
# ��������Ҫ���������
# �������û���ļ��У����ƹ�ȥ�����ӾͿ϶������ļ���ͬ��Ŀ¼�ģ�����������Ǵ��ļ��еģ��ֽ׶�ֻ�ܸ��Ƶ��ϼ�Ŀ¼�����ܽ�������ܼ򵥣�ûʱ�俴��-������-
#
# ��ȡ�ⲿ����
param($N,$L,$G,$F,$R,$D,$C,$Z,$T,$I)
# ���Բ���
# write-output "Torrent���ƣ�$N"   | out-file -filepath   d:\debug.txt 
# write-output "���ࣺ$L"  | out-file  -Append d:\debug.txt 
# write-output "��ǩ���ö��ŷָ�����$G"  | out-file  -Append  d:\debug.txt 
# write-output "����·��������ļ� torrent �ĸ�Ŀ¼��ͬ����$F"  | out-file  -Append d:\debug.txt 
# write-output "��Ŀ¼����һ�� torrent ����Ŀ¼·������$R"  | out-file  -Append d:\debug.txt 
# write-output "����·����$D"  | out-file  -Append  d:\debug.txt 
# write-output "�ļ�����$C"  | out-file  -Append d:\debug.txt 
# write-output "Torrent ��С��$Z"  | out-file  -Append d:\debug.txt 
# write-output "��ǰ tracker��$T"  | out-file  -Append  d:\debug.txt 
# write-output "��ϣֵ��$I"  | out-file  -Append  d:\debug.txt 

# ����qbt��������ļ���Ŀ¼
$BT_backup = "C:\Users\kysdm\Desktop\qbittorrent_x64_portable\profile\qBittorrent\data\BT_backup"

copy-Item "$BT_backup\$I.torrent"  "$D\$N.torrent"