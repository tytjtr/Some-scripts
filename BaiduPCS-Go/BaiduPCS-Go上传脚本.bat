@echo off&setlocal enabledelayedexpansion

REM �����˺Ź���ű����ú��˺�֮��ģ���������ű�
REM ֱ�ӷ�������Ҫ�ϴ����ļ�����
REM ����Ҫ�ϴ� E:\123\Scans
REM ������� E:\123\Scans Ŀ¼��
REM �ű����ϴ� E:\123\Scans Ŀ¼�������ļ�
REM Ŀ¼·���в�������� �ո� С���� ������ �����ַ� ���򱨴�

REM ###############################################
REM ֻ��������Ҫ�ֶ���

REM ���ô���  //�˴���Ҫ���Լ����Ը���
REM set http_proxy=http://127.0.0.1:1080

REM ����BaiduPCS-Go����Ŀ¼  //�˴���Ҫ���Լ����Ը���
set BaiduPCS_dir=D:\Program Files\BaiduPCS-Go-v3.5.4-windows-x64

REM ###############################################

REM ָ������
mode con cols=85 lines=35
title BaiduPCS-Go�ϴ��ű�
REM ����ʱ��
set date1=%date:~0,4%-%date:~5,2%-%date:~8,2%
set date2=%time:~0,2%:%time:~3,2%:%time:~6,2%
REM ȡ�õ�ǰ�ļ�������
for %%i in ("%cd%") do set mulu=%%~ni
REM ��ȡ�ļ��д�С 
REM ĳ��̳����д��
set Dir=%~dp0
for /f "tokens=3* delims= " %%a in ('dir/a-d/s "%Dir%"^|findstr /c:"���ļ�"') do set size=%%~a
echo �ϴ�Ŀ¼��%Dir% && echo=
REM echo �ܴ�СΪ��%size:,=% �ֽ�
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
REM echo �ܴ�СΪ��%d%!sun! �ֽ�
REM echo �ܴ�СΪ��%size% �ֽ�
echo �ϴ�����ռ䣺%d%!sun! GB (%size% �ֽ�)
echo.
REM ��ʾ��ǰʹ�õ��˺�
"%BaiduPCS_dir%\BaiduPCS-Go" who
echo.
REM ��ʾ��ǰ�˺ŵ������Ϣ
"%BaiduPCS_dir%\BaiduPCS-Go" quota
echo.
REM д�Զ��жϲ����ڵ� ������
echo ����ȥ���������̿ռ乻����...
echo ʹ�õ��˻����ԣ������˺Ź���ű����л���Ӧ�����еİ�...��
echo. & echo ������������ϴ�
pause>nul

echo ��ʼ�ϴ� && ping /n 2 127.0.0.1>nul & echo.
title ��С"%d%!sun!GB" �ϴ�Ŀ¼ "%~dp0"
REM ����ǰĿ¼�е������ļ��ϴ��� "BaiduPCS-Go�ϴ�Ŀ¼"
"%BaiduPCS_dir%\BaiduPCS-Go" upload  %~dp0 /BaiduPCS-Go�ϴ�Ŀ¼/�ϴ���_%mulu%
REM �и�md5�޸� ���ܻῨ������ ���Ժ��Ե��޸���
echo.
echo �ϴ�����ʱ��: %date1% %date2%
echo.
echo *************************************
echo **                                 **
echo ** ��۲���־ ȷ���ļ��Ѿ������ϴ� **
echo **                                 **
echo *************************************
echo=
echo *************************************************
echo **                                             **
echo ** ��������Ƴ��ϴ��б�ǩ ������ֱ�ӹرմ���   **
echo **                                             **
echo *************************************************
echo=
pause>nul
echo  ȷ���� *�����������*
pause>nul
REM �Ƴ��ϴ��б�ǩ
echo.
echo ��ʼ�Ƴ��ϴ��б�ǩ && echo=
"%BaiduPCS_dir%\BaiduPCS-Go" mv /BaiduPCS-Go�ϴ�Ŀ¼/�ϴ���_%mulu% /BaiduPCS-Go�ϴ�Ŀ¼/%mulu%
echo=
echo *************************************
echo **                                 **
echo ** ��۲���־ ȷ����ǩ�Ѿ���ȷ�Ƴ�  **
echo **                                 **
echo *************************************
echo  ��������˳��ű�
pause>nul
exit