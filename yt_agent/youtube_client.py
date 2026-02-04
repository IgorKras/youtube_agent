import logging
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import List, Optional
from dateutil import parser
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

@dataclass
class Video:
    id: str
    title: str
    url: str
    published_at: datetime
    description: Optional[str] = None
    channel_name: Optional[str] = None

class YouTubeClient:
    def __init__(self, api_key: Optional[str] = None):
        if not api_key:
            raise ValueError("YouTube API Key is required.")
        self.api_key = api_key
        try:
            self.service = build('youtube', 'v3', developerKey=self.api_key)
        except Exception as e:
            logger.error(f"Failed to build YouTube service: {e}")
            raise

    @lru_cache(maxsize=100)
    def get_channel_id_from_handle(self, handle: str) -> Optional[str]:
        """Gets channel ID from a channel handle (e.g., @Fireship). Results are cached."""
        try:
            search_response = self.service.search().list(
                q=handle,
                type='channel',
                part='id',
                maxResults=1
            ).execute()
            if not search_response.get('items'):
                return None
            return search_response['items'][0]['id']['channelId']
        except HttpError as e:
            logger.error(f"HTTP error resolving channel handle '{handle}': {e}")
            return None
        except Exception as e:
            logger.error(f"Error resolving channel handle '{handle}': {e}")
            return None

    def get_uploads_playlist_id(self, channel_id: str) -> Optional[str]:
        """Gets the ID of the 'uploads' playlist for a given channel ID."""
        try:
            channels_response = self.service.channels().list(
                id=channel_id,
                part='contentDetails'
            ).execute()
            if not channels_response.get('items'):
                return None
            return channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except HttpError as e:
            logger.error(f"HTTP error getting uploads playlist for channel '{channel_id}': {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting uploads playlist for channel '{channel_id}': {e}")
            return None

    def get_latest_videos(self, identifier: str, max_videos: int = 1) -> List[Video]:
        """
        Gets the latest videos from a channel using its ID, handle, or full URL.
        """
        channel_id = None
        if identifier.startswith("UC") and len(identifier) == 24:
            channel_id = identifier
        elif identifier.startswith("@"):
            channel_id = self.get_channel_id_from_handle(identifier)
        elif "youtube.com/" in identifier:
            handle = identifier.split('/')[-1]
            if handle.startswith('@'):
                 channel_id = self.get_channel_id_from_handle(handle)

        if not channel_id:
            logger.error(f"Could not resolve a valid Channel ID from identifier: {identifier}")
            return []

        uploads_playlist_id = self.get_uploads_playlist_id(channel_id)
        if not uploads_playlist_id:
            logger.error(f"Could not find uploads playlist for channel ID: {channel_id}")
            return []

        try:
            playlist_items_response = self.service.playlistItems().list(
                playlistId=uploads_playlist_id,
                part='snippet',
                maxResults=max_videos
            ).execute()

            videos = []
            for item in playlist_items_response.get('items', []):
                snippet = item['snippet']
                video_id = snippet['resourceId']['videoId']
                
                videos.append(Video(
                    id=video_id,
                    title=snippet['title'],
                    url=f"https://www.youtube.com/watch?v={video_id}",
                    published_at=parser.parse(snippet['publishedAt']),
                    description=snippet.get('description'),
                    channel_name=snippet.get('channelTitle')
                ))
            
            return videos

        except HttpError as e:
            logger.error(f"HTTP error fetching videos for playlist '{uploads_playlist_id}': {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching videos for playlist '{uploads_playlist_id}': {e}")
            return []