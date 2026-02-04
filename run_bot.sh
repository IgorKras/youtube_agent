#!/bin/bash
# Interactive Telegram Bot Runner for YouTube Review Agent
# This script starts the agent in interactive mode, listening for commands

echo "========================================"
echo "YouTube Review Agent - Interactive Mode"
echo "========================================"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure your bot token."
    echo ""
    exit 1
fi

# Check if config.yaml exists
if [ ! -f "config.yaml" ]; then
    echo "WARNING: config.yaml not found!"
    echo "Please copy config.example.yaml to config.yaml and configure your channels."
    echo ""
    exit 1
fi

echo "Starting agent in interactive mode..."
echo "The agent will listen for commands from your Telegram chat."
echo ""
echo "Available commands:"
echo "  /review - Run YouTube review and get summaries"
echo "  /status - Check agent status"
echo "  /help   - Show help message"
echo ""
echo "Press Ctrl+C to stop the agent"
echo "========================================"
echo ""

# Run the agent in bot mode
python -m yt_agent.cli --config config.yaml --bot

echo ""
echo "Agent stopped."
