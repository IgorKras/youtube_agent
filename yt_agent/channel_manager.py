import json
import os
import re
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class Channel:
    name: str
    identifier: str

class ChannelManager:
    def __init__(self, storage_path: str = "channels.json"):
        self.storage_path = storage_path
        self.channels: List[Channel] = []
        self._load_channels()

    def _load_channels(self):
        if not os.path.exists(self.storage_path):
            self.channels = []
            return

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.channels = [Channel(**c) for c in data]
            logger.info(f"Loaded {len(self.channels)} channels from {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to load channels from {self.storage_path}: {e}")
            self.channels = []

    def _save_channels(self):
        try:
            data = [asdict(c) for c in self.channels]
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.channels)} channels to {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to save channels to {self.storage_path}: {e}")

    def _sanitize_input(self, value: str, max_length: int = 100) -> str:
        """Sanitize input to prevent injection attacks."""
        # Allow only safe characters: alphanumeric, @, -, _, spaces, and basic punctuation
        sanitized = re.sub(r'[^\w@\-\s\.]', '', value)
        return sanitized.strip()[:max_length]

    def add_channel(self, name: str, identifier: str) -> bool:
        """Adds a new channel if it doesn't already exist."""
        # Sanitize inputs
        name = self._sanitize_input(name, max_length=100)
        identifier = self._sanitize_input(identifier, max_length=50)
        
        if not name or not identifier:
            logger.warning("Invalid channel name or identifier after sanitization")
            return False
        
        for ch in self.channels:
            if ch.identifier == identifier:
                logger.info(f"Channel {identifier} already exists.")
                return False
        
        self.channels.append(Channel(name=name, identifier=identifier))
        self._save_channels()
        return True

    def remove_channel(self, identifier_or_name: str) -> bool:
        """Removes a channel by identifier or name (case-insensitive)."""
        initial_count = len(self.channels)
        self.channels = [
            c for c in self.channels 
            if c.identifier != identifier_or_name and c.name.lower() != identifier_or_name.lower()
        ]
        
        if len(self.channels) < initial_count:
            self._save_channels()
            return True
        return False

    def get_channels(self) -> List[Channel]:
        return self.channels

    def list_channels_formatted(self) -> str:
        if not self.channels:
            return "No channels configured."
        
        lines = ["📺 **Monitored Channels:**"]
        for i, ch in enumerate(self.channels, 1):
            lines.append(f"{i}. {ch.name} (`{ch.identifier}`)")
        return "\n".join(lines)
