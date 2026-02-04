import requests
import logging
import os
import time
from typing import Union, List, Dict, Any

logger = logging.getLogger(__name__)

class TelegramClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        # Use session for connection pooling
        self.session = requests.Session()

    def send_message(self, chat_id: Union[str, int], text: str) -> Dict[str, Any]:
        # Telegram message length limit is 4096 characters.
        # We'll split at 4000 to be safe.
        max_length = 4000
        
        if len(text) <= max_length:
            return self._send_chunk(chat_id, text)

        else:
            parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
            result = None
            for i, part in enumerate(parts):
                header = f"[Part {i+1}/{len(parts)}]\n" if len(parts) > 1 else ""
                result = self._send_chunk(chat_id, header + part)
                time.sleep(1) # Rate limiting niceness
            return result

    def _send_chunk(self, chat_id: Union[str, int], text: str) -> Dict[str, Any]:
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown" # Or MarkdownV2, but Markdown is simpler for basic formatting
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return {}
    
    def delete_message(self, chat_id: Union[str, int], message_id: int) -> bool:
        """Delete a specific message.
        
        Args:
            chat_id: Chat ID
            message_id: Message ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        url = f"{self.base_url}/deleteMessage"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("ok", False)
        except requests.exceptions.RequestException as e:
            logger.debug(f"Failed to delete message {message_id}: {e}")
            return False

