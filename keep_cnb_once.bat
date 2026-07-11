@echo off
REM CNB 自动续期 - 一次性运行脚本
echo [%date% %time%] CNB keep-alive triggered >> "%~dp0keep_cnb_log.txt"
cd /d "%~dp0"
python keep_cnb_alive.py --once >> "%~dp0keep_cnb_log.txt" 2>&1