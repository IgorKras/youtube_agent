import json
import os
import re
import logging
from typing import List
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


def _escape_markdown(text: str) -> str:
    """Escape basic Telegram Markdown characters."""
    return re.sub(r'([_*`\[\]])', r'\\\1', text)

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

    def _sanitize_name(self, value: str, max_length: int = 100) -> str:
        """Sanitize display names while preserving normal punctuation."""
        collapsed = re.sub(r"\s+", " ", value or "").strip()
        # Drop control characters to keep storage and output stable.
        cleaned = "".join(ch for ch in collapsed if ch.isprintable())
        return cleaned[:max_length]

    def _normalize_identifier(self, value: str, max_length: int = 300) -> str:
        """Normalize channel identifier without mutating valid URL/channel syntax."""
        normalized = (value or "").strip()
        if any(ch.isspace() for ch in normalized):
            return ""
        return normalized[:max_length]

    def add_channel(self, name: str, identifier: str) -> bool:
        """Adds a new channel if it doesn't already exist."""
        name = self._sanitize_name(name, max_length=100)
        identifier = self._normalize_identifier(identifier, max_length=300)
        
        if not name or not identifier:
            logger.warning("Invalid channel name or identifier after normalization")
            return False
        
        for ch in self.channels:
            if ch.identifier.lower() == identifier.lower():
                logger.info(f"Channel {identifier} already exists.")
                return False
        
        self.channels.append(Channel(name=name, identifier=identifier))
        self._save_channels()
        return True

    def remove_channel(self, identifier_or_name: str) -> bool:
        """Removes a channel by identifier or name (case-insensitive)."""
        search_term = (identifier_or_name or "").lower().strip()
        initial_count = len(self.channels)

        def matches(identifier: str, name: str) -> bool:
            if identifier.lower() == search_term:
                return True
            if name.lower() == search_term:
                return True
            # Support removing by handle when stored value is a full URL.
            if search_term.startswith("@") and search_term in identifier.lower():
                return True
            if not search_term.startswith("@") and f"@{search_term}" in identifier.lower():
                return True
            return False

        self.channels = [c for c in self.channels if not matches(c.identifier, c.name)]
        
        if len(self.channels) < initial_count:
            self._save_channels()
            return True
        return False

    def get_channels(self) -> List[Channel]:
        return self.channels

    def list_channels_formatted(self) -> str:
        if not self.channels:
            return "No channels configured."
        
        lines = ["📺 *Monitored Channels:*"]
        for i, ch in enumerate(self.channels, 1):
            safe_name = _escape_markdown(ch.name)
            safe_identifier = _escape_markdown(ch.identifier)
            lines.append(f"{i}. {safe_name} (`{safe_identifier}`)")
        return "\n".join(lines)
