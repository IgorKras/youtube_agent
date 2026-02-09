import os
import yaml
from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class RunConfig:
    timezone: str = "UTC"
    max_videos_per_channel: int = 1

@dataclass
class ChannelConfig:
    name: str
    identifier: str

@dataclass
class TelegramConfig:
    chat_id: Union[str, int]

@dataclass
class LLMConfig:
    api_base: str = "http://127.0.0.1:1234"
    model: str = "local-model"
    temperature: float = 0.2
    max_sentences_per_video: int = 5
    language: str = "en"
    include_links: bool = True
    group_by_channel: bool = True
    title: str = "YouTube Daily Review"

@dataclass
class YouTubeConfig:
    api_key: Optional[str] = None

@dataclass
class Config:
    run: RunConfig
    telegram: TelegramConfig
    llm: LLMConfig
    youtube: YouTubeConfig

def load_config(path: str) -> Config:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("Config root must be a YAML mapping/object.")

    # Run Config
    run_data = data.get('run', {})
    run_config = RunConfig(
        timezone=run_data.get('timezone', 'UTC'),
        max_videos_per_channel=run_data.get('max_videos_per_channel', 1)
    )


    # Telegram
    telegram_data = data.get('telegram', {})
    chat_id = telegram_data.get('chat_id')
    if not chat_id:
        raise ValueError("telegram.chat_id is required in config")
    telegram_config = TelegramConfig(chat_id=chat_id)

    # LLM
    llm_data = data.get('llm', {})
    
    # Environment variable overrides for LLM
    api_base = os.environ.get('LMSTUDIO_API_BASE', llm_data.get('api_base', "http://127.0.0.1:1234"))
    model = os.environ.get('LMSTUDIO_MODEL', llm_data.get('model', "local-model"))

    llm_config = LLMConfig(
        api_base=api_base,
        model=model,
        temperature=llm_data.get('temperature', 0.2),
        max_sentences_per_video=llm_data.get('max_sentences_per_video', 5),
        language=llm_data.get('language', 'en'),
        include_links=llm_data.get('include_links', True),
        group_by_channel=llm_data.get('group_by_channel', True),
        title=llm_data.get('title', "YouTube Daily Review")
    )

    # YouTube
    youtube_config = YouTubeConfig(
        api_key=os.environ.get('YOUTUBE_API_KEY')
    )

    return Config(
        run=run_config,
        telegram=telegram_config,
        llm=llm_config,
        youtube=youtube_config
    )
