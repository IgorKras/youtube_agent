@echo off
REM YouTube Telegram Review Agent - Run Script
REM This script runs the agent with your configuration

echo ========================================
echo YouTube Telegram Review Agent
echo ========================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo.
    echo Please create a .env file with your credentials:
    echo   1. Copy .env.example to .env
    echo   2. Edit .env and add your TELEGRAM_BOT_TOKEN
    echo.
    pause
    exit /b 1
)

echo Starting agent...
echo.

REM Run the agent (python-dotenv will load .env automatically)
python -m yt_agent.cli --config config.yaml --verbose

echo.
echo ========================================
echo Agent finished!
echo Check your Telegram for the report.
echo ========================================
echo.

pause
