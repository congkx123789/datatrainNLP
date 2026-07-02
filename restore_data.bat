@echo off
echo =======================================================
echo   Automated Data Restoration for datatrainNLP
echo =======================================================
echo.
python scripts\restore_data.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Data restoration failed!
    pause
    exit /b %errorlevel%
)
echo.
echo [SUCCESS] All data has been successfully restored!
pause
