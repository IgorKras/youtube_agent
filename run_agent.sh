#!/bin/bash
# YouTube Telegram Review Agent - Shell Script
# This script runs the agent with your configuration

# RECOMMENDED: Use .env file for credentials (see .env.example)
# Create .env file: cp .env.example .env
# Then edit .env and add your TELEGRAM_BOT_TOKEN

# Alternative: Set environment variables here (NOT RECOMMENDED for security)
# export TELEGRAM_BOT_TOKEN="your_token_here"
# export LMSTUDIO_API_BASE="http://127.0.0.1:1234/v1"
# export LMSTUDIO_MODEL="your_model_name"

# Run the agent (will automatically load .env file)
python3 -m yt_agent.cli --config config.yaml

