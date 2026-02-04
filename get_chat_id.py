"""
Helper script to get your Telegram chat ID.

Usage:
1. Set your TELEGRAM_BOT_TOKEN environment variable
2. Send a message to your bot in Telegram
3. Run this script: python get_chat_id.py
"""

import os
import sys
import requests

def get_chat_id():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        print("\nOn Windows (PowerShell):")
        print('  $env:TELEGRAM_BOT_TOKEN="your_token_here"')
        print("\nOn Linux/macOS:")
        print('  export TELEGRAM_BOT_TOKEN="your_token_here"')
        sys.exit(1)
    
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('ok'):
            print(f"Error: {data.get('description', 'Unknown error')}")
            sys.exit(1)
        
        results = data.get('result', [])
        
        if not results:
            print("No messages found.")
            print("\nPlease:")
            print("1. Send a message to your bot in Telegram")
            print("2. Run this script again")
            sys.exit(0)
        
        # Get unique chat IDs
        chat_ids = set()
        for update in results:
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                chat_type = update['message']['chat']['type']
                chat_title = update['message']['chat'].get('title', 
                             update['message']['chat'].get('first_name', 'Unknown'))
                chat_ids.add((chat_id, chat_type, chat_title))
        
        print("Found the following chats:\n")
        for chat_id, chat_type, chat_title in sorted(chat_ids):
            print(f"  Chat ID: {chat_id}")
            print(f"  Type: {chat_type}")
            print(f"  Name: {chat_title}")
            print()
        
        print("Use one of these chat IDs in your config.yaml")
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Telegram API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    get_chat_id()
