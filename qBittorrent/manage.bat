@echo off

REM ��Ҫ��ͼ����<�����ļ�>���� 
REM ��Ϊû�ã�qb����"%LOCALAPPDATA%\qBittorrent""%APPDATA%\qBittorrent"Ŀ¼�����µ������ļ�,��ʹ��

REM ��־�ļ�����λ�����״�����ʱ�Զ�ָ��
REM �����������qbĿ¼��log�ļ��������Զ�ͬ��
REM ��Ҫ����ָ��λ��
REM profile\qBittorrent\data\logs\qbittorrent.log

title qbittorrent_portable

:���QB�Ƿ��Ѿ�����
for /f "tokens=2" %%i in ('tasklist ^| findstr qbittorrent.exe') do ( set "qb_pid=%%i" )
if defined qb_pid ( echo QB�Ѿ����� && echo PID��%qb_pid% ) else ( goto ����QB )
echo.
ping /n 2 127.0.0.1>nul
:ѡ��1
echo 1.�����ٴ�����
echo 2.ɱ��QB����
echo.
set /p user_input=������:
if "%user_input%"=="1"  ( echo. & goto ���QB�Ƿ��Ѿ����� ) else ( if "%user_input%"=="2"  ( goto ɱ��QB���� ) else ( echo. & echo ����������������� & echo. & ping /n 2 127.0.0.1>nul & goto ѡ��1 ) )

:ɱ��QB����
echo.
taskkill /pid %qb_pid% -t -f
set "qb_pid="
goto ���QB�Ƿ��Ѿ�����

:����QB
echo.
echo 3s������QB
ping /n 3 127.0.0.1>nul
start "" "%~dp0qbittorrent.exe" --portable

exit