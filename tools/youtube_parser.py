"""
YouTube Parser Tool - Extract transcripts from YouTube videos
"""

from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url: str) -> str:
    """
    Extract video ID from YouTube URL
    
    Args:
        url: YouTube URL
        
    Returns:
        str: Video ID
    """
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def parse_youtube(url: str) -> dict:
    """
    Get transcript from a YouTube video
    
    Args:
        url: YouTube video URL or ID
        
    Returns:
        dict: Transcript text and metadata
    """
    try:
        video_id = extract_video_id(url)
        
        if not video_id:
            return {
                "type": "youtube_content",
                "success": False,
                "error": "Invalid YouTube URL"
            }
        
        # Get transcript using the correct API
        # Try to get any available transcript
        transcript_data = None
        
        try:
            # Try getting transcript in English first
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except:
            try:
                # Try getting any available transcript
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                
                # Try to find any transcript
                for transcript in transcript_list:
                    try:
                        transcript_data = transcript.fetch()
                        break
                    except:
                        continue
            except Exception as inner_e:
                raise Exception(f"Could not retrieve transcript. Make sure the video has captions enabled. Details: {str(inner_e)}")
        
        if not transcript_data:
            raise Exception("No transcripts available for this video")
        
        # Combine all text
        full_text = " ".join([entry['text'] for entry in transcript_data])
        
        return {
            "type": "youtube_content",
            "success": True,
            "video_id": video_id,
            "transcript": full_text,
            "duration": sum([entry.get('duration', 0) for entry in transcript_data]),
            "char_count": len(full_text)
        }
    except Exception as e:
        return {
            "type": "youtube_content",
            "success": False,
            "error": str(e)
        }

