"""
Test URL validation and parsing functionality
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from url_validator import parse_youtube_url, clear_cache


class TestParseYouTubeURL:
    """Test YouTube URL parsing"""

    def test_parse_full_url(self):
        """Test parsing full YouTube URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = parse_youtube_url(url)
        assert result == "dQw4w9WgXcQ"

    def test_parse_short_url(self):
        """Test parsing short youtu.be URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        result = parse_youtube_url(url)
        assert result == "dQw4w9WgXcQ"

    def test_parse_url_without_www(self):
        """Test parsing URL without www"""
        url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
        result = parse_youtube_url(url)
        assert result == "dQw4w9WgXcQ"

    def test_parse_url_with_additional_params(self):
        """Test parsing URL with extra query parameters"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s"
        result = parse_youtube_url(url)
        assert result == "dQw4w9WgXcQ"

    def test_parse_direct_video_id(self):
        """Test parsing direct video ID (11 chars)"""
        video_id = "dQw4w9WgXcQ"
        result = parse_youtube_url(video_id)
        assert result == "dQw4w9WgXcQ"

    def test_parse_invalid_url(self):
        """Test parsing invalid URL returns None"""
        url = "https://www.google.com"
        result = parse_youtube_url(url)
        assert result is None

    def test_parse_empty_string(self):
        """Test parsing empty string returns None"""
        result = parse_youtube_url("")
        assert result is None

    def test_parse_invalid_video_id_length(self):
        """Test parsing video ID with wrong length"""
        result = parse_youtube_url("abc123")
        assert result is None

    def test_parse_url_with_whitespace(self):
        """Test parsing URL with surrounding whitespace"""
        url = "  https://www.youtube.com/watch?v=dQw4w9WgXcQ  "
        result = parse_youtube_url(url)
        assert result == "dQw4w9WgXcQ"

    def test_parse_http_url(self):
        """Test parsing HTTP (non-HTTPS) URL"""
        url = "http://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = parse_youtube_url(url)
        assert result == "dQw4w9WgXcQ"


class TestClearCache:
    """Test cache clearing functionality"""

    def test_clear_cache_runs_without_error(self):
        """Test clear_cache function executes without error"""
        try:
            clear_cache()
        except Exception as e:
            pytest.fail(f"clear_cache raised exception: {e}")
