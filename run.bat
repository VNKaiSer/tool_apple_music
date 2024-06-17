@echo off
REM Kiểm tra xem Python đã được cài đặt hay chưa
python --version >nul 2>&1
if %errorlevel% neq 0 (
    REM Python chưa được cài đặt, tiến hành cài đặt
    echo Python chưa được cài đặt. Bắt đầu quá trình cài đặt...
    REM Tải và cài đặt Python từ trang chủ
    start /wait https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    REM Đợi cho quá trình cài đặt hoàn tất (tối đa 30 giây)
    timeout /t 30 /nobreak >nul
    REM Kiểm tra lại sau khi cài đặt
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo 'python installed error'
    ) else (
        echo 'python installed ok'
    )
) 


@REM REM python đã cài đặt
@REM echo install dependencies from requirements.txt
@REM pip install -r requirements.txt
@REM if %errorlevel% neq 0 (
@REM     echo error install dependencies from requirements.txt
@REM ) else (
@REM     echo ok install dependencies from requirements.txt
@REM )

@REM REM 
echo Running main.py...
python main.py > log-app.txt 2>&1
if %errorlevel% neq 0 (
    echo application error
) else (
    echo run ok
)

REM
exit

