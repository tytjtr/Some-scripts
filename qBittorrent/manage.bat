@echo off

REM 不要试图启用<关联文件>功能 
REM 因为没用，qb会在"%LOCALAPPDATA%\qBittorrent""%APPDATA%\qBittorrent"目录生成新的配置文件,并使用

REM 日志文件生成位置在首次运行时自动指定
REM 后续如果更改qb目录，log文件并不会自动同步
REM 需要自行指定位置
REM profile\qBittorrent\data\logs\qbittorrent.log

title qbittorrent_portable

:检测QB是否已经启动
for /f "tokens=2" %%i in ('tasklist ^| findstr qbittorrent.exe') do ( set "qb_pid=%%i" )
if defined qb_pid ( echo QB已经启动 && echo PID：%qb_pid% ) else ( goto 启动QB )
echo.
ping /n 2 127.0.0.1>nul
:选择1
echo 1.尝试再次启动
echo 2.杀死QB进程
echo.
set /p user_input=请输入:
if "%user_input%"=="1"  ( echo. & goto 检测QB是否已经启动 ) else ( if "%user_input%"=="2"  ( goto 杀死QB进程 ) else ( echo. & echo 输入错误，请重新输入 & echo. & ping /n 2 127.0.0.1>nul & goto 选择1 ) )

:杀死QB进程
echo.
taskkill /pid %qb_pid% -t -f
set "qb_pid="
goto 检测QB是否已经启动

:启动QB
echo.
echo 3s后启动QB
ping /n 3 127.0.0.1>nul
start "" "%~dp0qbittorrent.exe" --portable

exit