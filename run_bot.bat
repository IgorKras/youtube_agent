@echo off
REM Interactive Telegram Bot Runner for YouTube Review Agent
REM This script starts the agent in interactive mode, listening for commands

echo ========================================
echo YouTube Review Agent - Interactive Mode
echo ========================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your bot token.
    echo.
    pause
    exit /b 1
)

REM Check if config.yaml exists
if not exist "config.yaml" (
    echo WARNING: config.yaml not found!
    echo Please copy config.example.yaml to config.yaml and configure your channels.
    echo.
    pause
    exit /b 1
)

echo Starting agent in interactive mode...
echo The agent will listen for commands from your Telegram chat.
echo.
echo Available commands:
echo   /review - Run YouTube review and get summaries
echo   /status - Check agent status
echo   /help   - Show help message
echo.
echo Press Ctrl+C to stop the agent
echo ========================================
echo.

REM Run the agent in bot mode
REM Run the agent in bot mode
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe -m yt_agent.cli --config config.yaml --bot
) else (
    python -m yt_agent.cli --config config.yaml --bot
)


echo.
echo Agent stopped.
pause
