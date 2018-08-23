@echo off

REM 指定窗口大小
mode con cols=85 lines=35

REM 定义时间
set date123=%date:~0,4%-%date:~5,2%-%date:~8,2%

REM 设置代理
REM set http_proxy=http://127.0.0.1:1080

REM 设置BaiduPCS-Go所在目录
set BaiduPCS_dir="D:\Program Files (x86)\BaiduPCS-Go-v3.5.4-windows-x64"

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