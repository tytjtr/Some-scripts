@echo off&setlocal enabledelayedexpansion

REM 直接放置在需要上传到文件夹中
REM 如需要上传 E:\123\Scans
REM 则放置在 E:\123\Scans 目录中
REM 脚本会上传 E:\123\Scans 目录中所有文件
REM 目录路径中不允许存在 空格 & 否则报错

REM ##############################################
REM 需要手动改的部分

REM 设置代理  //默认不启用
REM set http_proxy=http://127.0.0.1:1080

REM 设置rclone所在目录  //必要
set rclone_dir=C:\rclone-v1.41-windows-amd64

REM 设置onedrive账户名 在rclone中定义的名称    //必要
set google_account=xxxgooglecom

REM 限速 M/S 
set Speed_limit=1.9

REM 调用Server酱实现上传完成微信通知  //需要curl
set ServerChan_key=

REM ##############################################

REM 指定窗口
mode con cols=85 lines=35
title Google Dirve文件上传脚本

::定义时间
set date1=%date:~0,4%-%date:~5,2%-%date:~8,2%
set date2=%time:~0,2%:%time:~3,2%:%time:~6,2%

::取得当前文件夹名称
for %%i in ("%cd%") do set mulu=%%~ni

::获取文件夹大小
set Dir=%~dp0
for /f "tokens=3* delims= " %%a in ('dir/a-d/s "%Dir%"^|findstr /c:"个文件"') do set size=%%~a
echo 路径：%Dir%
::echo 总大小为：%size:,=% 字节
echo=
::运算
set str1=%size:,=%
set str2=1073741824
set u=2
for %%i in (str1 str2) do if "!%%i:~,1!" == "-" set /a d+=1
if "%d%" == "1" (set d=-) else set "d="
set l=00000000&for /l %%i in (1 1 7) do set "l=!l!!l!"
set "var=4096 2048 1024 512 256 128 64 32 16 8 4 2 1"
for /l %%i in (1 1 2) do (
    set "str%%i=!str%%i:-=!"
    set /a "n=str%%i_2=0"
    for %%a in (!str%%i:.^= !) do (
        set /a n+=1
        set s=s%%a&set str%%i_!n!=0
        for %%b in (%var%) do if "!S:~%%b!" neq "" set/a str%%i_!n!+=%%b&set "S=!S:~%%b!"
        set /a len%%i+=str%%i_!n!
    )
        set str%%i=!str%%i:.=!
)
if !str1_2! gtr !str2_2! (set /a len2+=str1_2-str2_2) else set /a len1+=str2_2-str1_2
for /l %%i in (1 1 2) do (
    set str%%i=!str%%i!!l!
    for %%j in (!len%%i!) do set " str%%i=!str%%i:~,%%j!"
)
for /f "tokens=* delims=0" %%i in ("!str2!") do set s=%%i&set "str2=0%%i"
set len2=1
for %%j in (%var%) do if "!S:~%%j!" neq "" set/a len2+=%%j&set "S=!S:~%%j!"
set /a len=len2+1
if !len1! lss !len2! set len1=!len2!&set "str1=!l:~-%len2%,-%len1%!!str1!"
set /a len1+=u&set str1=0!str1!!l:~,%u%!
set str=!str1:~,%len2%!
set "i=0000000!str2!"&set /a Len_i=Len2+7
for /l %%i in (1 1 9) do (
    set "T=0"
    for /l %%j in (8 8 !Len_i!) do (
        set /a "T=1!i:~-%%j,8!*%%i+T"
        set Num%%i=!T:~-8!!Num%%i!&set /a "T=!T:~,-8!-%%i"
    )
    set Num%%i=!T!!Num%%i!
    set "Num%%i=0000000!Num%%i:~-%Len%!"
)
for /L %%a in (!len2! 1 !Len1!) do (
    set "str=!L!!str!!str1:~%%a,1!"
    set "str=!str:~-%Len%!"
    if "!str!" geq "!str2!" (
       set M=1&set i=0000000!str!
       for /l %%i in (2 1 9) do if "!i!" geq "!Num%%i!" set "M=%%i"
           set sun=!sun!!M!&set str=&set T=0
           for %%i in (!M!) do (
               for /l %%j in (8 8 !Len_i!) do (
                   set /a "T=3!i:~-%%j,8!-1!Num%%i:~-%%j,8!-!T:~,1!%%2"
                   set "str=!T:~1!!str!"
               )
           )
    ) else set sun=!sun!0
)
     set sun=!sun:~,-%u%!.!sun:~-%u%!
::echo %d%!sun!
::echo 总大小为：%d%!sun! 字节
::echo 总大小为：%size% 字节
echo 大小：%d%!sun! GB (%size% 字节)
echo=

::设置标题
title 大小"%d%!sun!GB" 上传目录 "%~dp0"

::确定
echo  确定开始上传？
pause>nul

REM rclone参数
"%rclone_dir%\rclone.exe" copy %~dp0 %google_account%:Rclone上传目录/上传中_%mulu%  --stats 6s --bwlimit %Speed_limit%M --log-level INFO

REM Server酱
curl -s -q "http://sc.ftqq.com/%ServerChan_key%.send?text=%%e8%%84%%9a%%e6%%9c%%ac%%e7%%8a%%b6%%e6%%80%%81%%e9%%80%%9a%%e7%%9f%%a5&desp=Google+Dirve%%e6%%96%%87%%e4%%bb%%b6%%e4%%b8%%8a%%e4%%bc%%a0%%e8%%84%%9a%%e6%%9c%%ac%%e5%%b7%%b2%%e7%%bb%%93%%e6%%9d%%9f%%e8%%bf%%90%%e8%%a1%%8c"

echo=
echo 上传目录 "%~dp0"
echo=
echo 上传开始时间 %date1% %date2%
set date3=%date:~0,4%-%date:~5,2%-%date:~8,2%
set date4=%time:~0,2%:%time:~3,2%:%time:~6,2%
echo 上传结束时间 %date3% %date4%
echo.
echo *************************************
echo **                                 **
echo ** 请观察日志 确定文件已经完整上传   **
echo **                                 **
echo *************************************
echo=
echo *************************************************
echo **                                             **
echo ** 按任意键移除上传中标签 否则请直接关闭窗口     **
echo **                                             **
echo *************************************************
echo.
pause>nul
echo  确定？
echo=
pause>nul
echo 开始移除上传中标签 && echo=
"%rclone_dir%\rclone.exe" move  --log-level INFO --delete-empty-src-dirs %google_account%:Rclone上传目录/上传中_%mulu% %google_account%:Rclone上传目录/%mulu%
echo=
echo *************************************
echo **                                 **
echo ** 请观察日志 确定标签已经正确移除 **
echo **                                 **
echo *************************************
echo.
echo  按任意键退出脚本
pause>nul
exit