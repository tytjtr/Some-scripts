@echo off

REM ָ������
mode con cols=85 lines=35
title BaiduPCS-Go�˺Ź���ű�

REM ###############################################
REM ֻ��������Ҫ�ֶ���

REM ���ô���  //�˴���Ҫ���Լ����Ը���
REM set http_proxy=http://127.0.0.1:1080

REM ����BaiduPCS-Go����Ŀ¼  //�˴���Ҫ���Լ����Ը���
set BaiduPCS_dir="D:\Program Files\BaiduPCS-Go-v3.5.4-windows-x64"

REM ###############################################

:menu1
cls
echo.
echo ==============================
echo.
echo  1.����ٶ��˺�
echo  2.��ȡ��ǰ�ʺ�
echo  3.��ȡ�������
echo  4.���������
echo.
echo ==============================
echo.
set user_input=0 & set /p user_input=���������֣�
if %user_input% equ 1 set %user_input%=0 && goto menu2
if %user_input% equ 2 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go who & echo ����������ز˵� && pause>nul && goto menu1
if %user_input% equ 3 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go quota & echo ����������ز˵� && pause>nul && goto menu1
if %user_input% equ 4 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go update & echo ����������ز˵� && pause>nul && goto menu1
echo ������� 3s�󷵻ز˵� && ping /n 3 127.0.0.1>nul
goto menu1

:menu2
cls
echo.
echo ==============================
echo.
echo  1.�����¼�ٶ��ʺ�
echo  2.ʹ�ðٶ�BDUSS����¼�ٶ��ʺ� *δ����*
echo  3.�г��ʺ��б�
echo  4.�л��ٶ��ʺ� *δ����*
echo  5.�˳��ٶ��ʺ� *δ����*
echo  6.�����ϼ��˵�
echo.
echo ==============================
echo.
set user_input=0 & set /p user_input=���������֣�
if %user_input% equ 1 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go login & echo ����������ز˵� && pause>nul && goto menu2
if %user_input% equ 2 set %user_input%=0 && set /p bduss=������BDUSSֵ�� && %BaiduPCS_dir%\BaiduPCS-Go login -bduss=%bduss%  & echo ����������ز˵� && pause>nul  && goto menu2
if %user_input% equ 3 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go loglist & echo ����������ز˵� && pause>nul  && goto menu2
if %user_input% equ 4 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go su & echo ����������ز˵� && pause>nul  && goto menu2
if %user_input% equ 5 set %user_input%=0 && %BaiduPCS_dir%\BaiduPCS-Go logout & echo ����������ز˵� && pause>nul  && goto menu2
if %user_input% equ 6 goto menu1
echo ������� 3s�󷵻ز˵� && ping /n 3 127.0.0.1>nul
goto menu2