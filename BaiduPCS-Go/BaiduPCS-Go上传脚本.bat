@echo off&setlocal enabledelayedexpansion

REM 先用账号管理脚本设置好账号之类的，再用这个脚本
REM 直接放置在需要上传到文件夹中
REM 如需要上传 E:\123\Scans
REM 则放置在 E:\123\Scans 目录中
REM 脚本会上传 E:\123\Scans 目录中所有文件
REM 目录路径中不允许存在 空格 小括号 中括号 特殊字符 否则报错

REM ###############################################
REM 只有这里需要手动改

REM 设置代理  //此处需要按自己电脑更改
REM set http_proxy=http://127.0.0.1:1080

REM 设置BaiduPCS-Go所在目录  //此处需要按自己电脑更改
set BaiduPCS_dir=D:\Program Files\BaiduPCS-Go-v3.5.4-windows-x64

REM 调用Server酱实现上传完成微信通知  //需要curl
set ServerChan_key=

REM ###############################################

REM 指定窗口
mode con cols=85 lines=35
title BaiduPCS-Go上传脚本
REM 定义时间
set date1=%date:~0,4%-%date:~5,2%-%date:~8,2%
set date2=%time:~0,2%:%time:~3,2%:%time:~6,2%
REM 取得当前文件夹名称
for %%i in ("%cd%") do set mulu=%%~ni
REM 获取文件夹大小 
REM 某论坛大佬写的
set Dir=%~dp0
for /f "tokens=3* delims= " %%a in ('dir/a-d/s "%Dir%"^|findstr /c:"个文件"') do set size=%%~a
echo 上传目录：%Dir% && echo=
REM echo 总大小为：%size:,=% 字节
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
REM echo %d%!sun!
REM echo 总大小为：%d%!sun! 字节
REM echo 总大小为：%size% 字节
echo 上传所需空间：%d%!sun! GB (%size% 字节)
echo.
REM 显示当前使用的账号
"%BaiduPCS_dir%\BaiduPCS-Go" who
echo.
REM 显示当前账号的配额信息
"%BaiduPCS_dir%\BaiduPCS-Go" quota
echo.
REM 写自动判断不存在的 咕咕咕
echo 用心去计算下云盘空间够不够...
echo 使用的账户不对，就用账号管理脚本做切换（应该能切的吧...）
echo. & echo 按任意键启动上传
pause>nul

echo 开始上传 && ping /n 2 127.0.0.1>nul & echo.
title 大小"%d%!sun!GB" 上传目录 "%~dp0"
REM 将当前目录中的所有文件上传至 "BaiduPCS-Go上传目录"
"%BaiduPCS_dir%\BaiduPCS-Go" upload  %~dp0 /BaiduPCS-Go上传目录/上传中_%mulu%
REM 有个md5修复 可能会卡在那里 可以忽略掉修复的

REM Server酱
curl -s -q "http://sc.ftqq.com/%ServerChan_key%.send?text=%%e8%%84%%9a%%e6%%9c%%ac%%e7%%8a%%b6%%e6%%80%%81%%e9%%80%%9a%%e7%%9f%%a5&desp=BaiduPCS-Go%%e4%%b8%%8a%%e4%%bc%%a0%%e8%%84%%9a%%e6%%9c%%ac%%e5%%b7%%b2%%e7%%bb%%93%%e6%%9d%%9f%%e8%%bf%%90%%e8%%a1%%8c"

echo.
echo 上传开始时间 %date1% %date2%
set date3=%date:~0,4%-%date:~5,2%-%date:~8,2%
set date4=%time:~0,2%:%time:~3,2%:%time:~6,2%
echo 上传结束时间 %date3% %date4%
echo.
echo *************************************
echo **                                 **
echo ** 请观察日志 确定文件已经完整上传 **
echo **                                 **
echo *************************************
echo=
echo *************************************************
echo **                                             **
echo ** 按任意键移除上传中标签 否则请直接关闭窗口   **
echo **                                             **
echo *************************************************
echo=
pause>nul
echo  确定？ *按任意键继续*
pause>nul
REM 移除上传中标签
echo.
echo 开始移除上传中标签 && echo=
"%BaiduPCS_dir%\BaiduPCS-Go" mv /BaiduPCS-Go上传目录/上传中_%mulu% /BaiduPCS-Go上传目录/%mulu%
echo=
echo *************************************
echo **                                 **
echo ** 请观察日志 确定标签已经正确移除  **
echo **                                 **
echo *************************************
echo  按任意键退出脚本
pause>nul
exit