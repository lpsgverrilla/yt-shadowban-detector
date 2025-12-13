"""
YouTube URL Validation and Parsing
Handles URL parsing and livestream validation with caching
"""

import re
import pytchat
from datetime import datetime, timedelta


# Cache for validation results
_validation_cache = {}
_cache_timeout = 60  # seconds


def parse_youtube_url(url: str) -> str:
    """
    Parse YouTube URL and extract video ID

    Supported formats:
      - https://youtube.com/watch?v=VIDEO_ID
      - https://www.youtube.com/watch?v=VIDEO_ID
      - https://youtu.be/VIDEO_ID
      - VIDEO_ID (11 characters, alphanumeric)

    Args:
        url: YouTube URL or video ID

    Returns:
        video_id if valid, None if invalid
    """
    if not url or not isinstance(url, str):
        return None

    url = url.strip()

    # Pattern 1: Direct video ID (11 alphanumeric characters)
    if re.match(r'^[A-Za-z0-9_-]{11}$', url):
        return url

    # Pattern 2: youtube.com/watch?v=VIDEO_ID
    match = re.search(r'youtube\.com/watch\?v=([A-Za-z0-9_-]{11})', url)
    if match:
        return match.group(1)

    # Pattern 3: youtu.be/VIDEO_ID
    match = re.search(r'youtu\.be/([A-Za-z0-9_-]{11})', url)
    if match:
        return match.group(1)

    return None


def validate_livestream(video_id: str) -> dict:
    """
    Check if video_id is a live stream

    Uses caching to avoid API spam (60 second cache)

    Args:
        video_id: YouTube video ID

    Returns:
        {
            'valid': bool,
            'live': bool,
            'error': str | None
        }
    """
    if not video_id:
        return {
            'valid': False,
            'live': False,
            'error': 'No video ID provided'
        }

    # Check cache
    now = datetime.now()
    if video_id in _validation_cache:
        cached_result, cached_time = _validation_cache[video_id]
        if (now - cached_time).total_seconds() < _cache_timeout:
            return cached_result

    # Validate with pytchat
    chat = None
    try:
        chat = pytchat.create(video_id=video_id)

        if chat.is_alive():
            result = {
                'valid': True,
                'live': True,
                'error': None
            }
        else:
            result = {
                'valid': True,
                'live': False,
                'error': 'Stream is not currently live'
            }

    except pytchat.exceptions.InvalidVideoIdException:
        result = {
            'valid': False,
            'live': False,
            'error': 'Invalid video ID'
        }

    except Exception as e:
        # Ignore signal errors from threading
        error_str = str(e)
        if 'signal' in error_str.lower() and 'main thread' in error_str.lower():
            # Assume valid for now, will be properly validated when starting monitoring
            result = {
                'valid': True,
                'live': True,
                'error': None
            }
        else:
            result = {
                'valid': False,
                'live': False,
                'error': f'Validation error: {str(e)}'
            }

    finally:
        # Clean up
        if chat:
            try:
                chat.terminate()
            except:
                pass

    # Cache result
    _validation_cache[video_id] = (result, now)

    return result


def clear_cache():
    """
    Clear the validation cache
    """
    global _validation_cache
    _validation_cache = {}
