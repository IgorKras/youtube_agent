from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import logging
from typing import List

logger = logging.getLogger(__name__)

class TranscriptClient:
    def __init__(self):
        self.yt_api = YouTubeTranscriptApi()

    def get_transcript(self, video_id: str, languages: List[str] = ["en"]) -> str:
        try:
            # Use instance method .list() which returns a TranscriptList object
            transcript_list = self.yt_api.list(video_id)
            
            try:
                transcript = transcript_list.find_transcript(languages)
            except NoTranscriptFound:
                # Try fallback to English or first available
                try:
                    transcript = transcript_list.find_transcript(['en'])
                except NoTranscriptFound:
                    # Just grab the first available
                    available = []
                    for t in transcript_list:
                        available.append(t)
                    if available:
                        transcript = available[0]
                    else:
                        raise NoTranscriptFound("No transcripts available")

            # fetch() returns a list of dictionaries
            transcript_data = transcript.fetch()
            return " ".join([t['text'] for t in transcript_data])

        except (TranscriptsDisabled, NoTranscriptFound) as e:
            logger.info(f"No transcript found for video {video_id}: {e}")
            return ""
        except Exception as e:
            logger.error(f"Error fetching transcript for {video_id}: {e}")
            return ""


