@echo off
REM YouTube Telegram Review Agent - Windows Batch Script
REM This script runs the agent with your configuration

REM RECOMMENDED: Use .env file for credentials (see .env.example)
REM Create .env file: copy .env.example .env
REM Then edit .env and add your TELEGRAM_BOT_TOKEN

REM Alternative: Set environment variables here (NOT RECOMMENDED for security)
REM set TELEGRAM_BOT_TOKEN=your_token_here
REM set LMSTUDIO_API_BASE=http://127.0.0.1:1234/v1
REM set LMSTUDIO_MODEL=your_model_name

REM Run the agent (will automatically load .env file)
REM Run the agent (will automatically load .env file)
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe -m yt_agent.cli --config config.yaml
) else (
    python -m yt_agent.cli --config config.yaml
)


REM Pause to see output (remove this line when scheduling)
pause

