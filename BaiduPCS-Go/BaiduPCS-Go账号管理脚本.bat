@echo off

REM 指定窗口
mode con cols=85 lines=35
title BaiduPCS-Go账号管理脚本

REM ###############################################
REM 只有这里需要手动改

REM 设置代理  //此处需要按自己电脑更改
REM set http_proxy=http://127.0.0.1:1080

REM 设置BaiduPCS-Go所在目录  //此处需要按自己电脑更改
set BaiduPCS_dir="D:\Program Files\BaiduPCS-Go-v3.5.4-windows-x64"

REM ###############################################

:menu1
cls
echo.
echo ==============================
echo.
echo  1.管理百度账号
echo  2.获取当前帐号
echo  3.获取网盘配额
echo  4.检测程序更新
echo.
echo ==============================
echo.
set user_input=0 & set /p user_input=请输入数字：
if %user_input% equ 1 set %user_input%=0 && goto menu2
if %user_input% equ 2 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go who & echo 按任意键返回菜单 && pause>nul && goto menu1
if %user_input% equ 3 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go quota & echo 按任意键返回菜单 && pause>nul && goto menu1
if %user_input% equ 4 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go update & echo 按任意键返回菜单 && pause>nul && goto menu1
echo 输入错误 3s后返回菜单 && ping /n 3 127.0.0.1>nul
goto menu1

:menu2
cls
echo.
echo ==============================
echo.
echo  1.常规登录百度帐号
echo  2.使用百度BDUSS来登录百度帐号 *未测试*
echo  3.列出帐号列表
echo  4.切换百度帐号 *未测试*
echo  5.退出百度帐号 *未测试*
echo  6.返回上级菜单
echo.
echo ==============================
echo.
set user_input=0 & set /p user_input=请输入数字：
if %user_input% equ 1 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go login & echo 按任意键返回菜单 && pause>nul && goto menu2
if %user_input% equ 2 set %user_input%=0 && set /p bduss=请输入BDUSS值： && %BaiduPCS_dir%\BaiduPCS-Go login -bduss=%bduss%  & echo 按任意键返回菜单 && pause>nul  && goto menu2
if %user_input% equ 3 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go loglist & echo 按任意键返回菜单 && pause>nul  && goto menu2
if %user_input% equ 4 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go su & echo 按任意键返回菜单 && pause>nul  && goto menu2
if %user_input% equ 5 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go logout & echo 按任意键返回菜单 && pause>nul  && goto menu2
if %user_input% equ 6 goto menu1
echo 输入错误 3s后返回菜单 && ping /n 3 127.0.0.1>nul
goto menu2