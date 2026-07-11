@echo off
echo ============================================
echo   CNB 自动续期设置
echo ============================================
echo.
echo 此脚本会创建 Windows 计划任务，每12小时自动续期
echo 确保你以管理员身份运行此脚本
echo.

cd /d "%~dp0"

set TASK_NAME=CNB_KeepAlive
set SCRIPT_PATH=%~dp0keep_cnb_once.bat

echo 正在创建计划任务: %TASK_NAME%
echo 脚本路径: %SCRIPT_PATH%
echo.

schtasks /create /tn "%TASK_NAME%" /tr "\"%SCRIPT_PATH%\"" /sc hourly /mo 12 /f

if %errorlevel% equ 0 (
    echo.
    echo [成功] 计划任务已创建！
    echo.
    echo 任务详情:
    schtasks /query /tn "%TASK_NAME%" /fo list /v
) else (
    echo.
    echo [失败] 创建计划任务失败，请以管理员身份运行此脚本
)

echo.
pause