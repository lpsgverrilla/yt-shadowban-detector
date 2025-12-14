"""
Test chat engine functionality
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from collections import deque

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from chat_engine import YouTubeChatBuffer


class TestYouTubeChatBufferInit:
    """Test YouTubeChatBuffer initialization"""

    def test_init_creates_buffer(self):
        """Test buffer is created on initialization"""
        buffer = YouTubeChatBuffer("test_video_id")
        assert buffer.buffer is not None
        assert isinstance(buffer.buffer, deque)

    def test_init_sets_video_id(self):
        """Test video_id is set correctly"""
        video_id = "dQw4w9WgXcQ"
        buffer = YouTubeChatBuffer(video_id)
        assert buffer.video_id == video_id

    def test_buffer_is_unlimited(self):
        """Test buffer has no max length (unlimited)"""
        buffer = YouTubeChatBuffer("test_video_id")
        # deque with no maxlen should have maxlen = None
        assert buffer.buffer.maxlen is None

    def test_init_flags_are_clear(self):
        """Test stop and stream_ended flags are cleared on init"""
        buffer = YouTubeChatBuffer("test_video_id")
        assert not buffer.stop_flag.is_set()
        assert not buffer.stream_ended_flag.is_set()

    def test_init_no_error_message(self):
        """Test error_message is None on init"""
        buffer = YouTubeChatBuffer("test_video_id")
        assert buffer.error_message is None


class TestBufferStats:
    """Test buffer statistics functionality"""

    def test_get_buffer_stats_empty(self):
        """Test stats on empty buffer"""
        buffer = YouTubeChatBuffer("test_video_id")
        stats = buffer.get_buffer_stats()
        assert stats['message_count'] == 0
        assert stats['time_span_seconds'] == 0.0

    def test_get_buffer_stats_returns_dict(self):
        """Test stats returns correct structure"""
        buffer = YouTubeChatBuffer("test_video_id")
        stats = buffer.get_buffer_stats()
        assert isinstance(stats, dict)
        assert 'message_count' in stats
        assert 'time_span_seconds' in stats


class TestSearchBuffer:
    """Test buffer search functionality"""

    def test_search_empty_buffer(self):
        """Test searching empty buffer returns empty list"""
        buffer = YouTubeChatBuffer("test_video_id")
        results = buffer.search_buffer("test")
        assert results == []

    def test_search_buffer_with_messages(self):
        """Test searching buffer with manually added messages"""
        buffer = YouTubeChatBuffer("test_video_id")

        # Manually add messages to buffer
        buffer.buffer.append({
            'author': 'user1',
            'message': 'Hello world',
            'timestamp': datetime.now()
        })
        buffer.buffer.append({
            'author': 'user2',
            'message': 'Test message',
            'timestamp': datetime.now()
        })

        results = buffer.search_buffer("Test")
        assert len(results) == 1
        assert results[0]['message'] == 'Test message'

    def test_search_buffer_case_sensitive(self):
        """Test search is case-sensitive"""
        buffer = YouTubeChatBuffer("test_video_id")

        buffer.buffer.append({
            'author': 'user1',
            'message': 'Hello World',
            'timestamp': datetime.now()
        })

        # Should not find lowercase 'world'
        results = buffer.search_buffer("world")
        assert len(results) == 0

        # Should find capitalized 'World'
        results = buffer.search_buffer("World")
        assert len(results) == 1


class TestSearchByUsername:
    """Test username search functionality"""

    def test_search_by_username_empty(self):
        """Test searching by username in empty buffer"""
        buffer = YouTubeChatBuffer("test_video_id")
        results = buffer.search_by_username("testuser")
        assert results == []

    def test_search_by_username_found(self):
        """Test finding messages by username"""
        buffer = YouTubeChatBuffer("test_video_id")

        buffer.buffer.append({
            'author': 'testuser',
            'message': 'Message 1',
            'timestamp': datetime.now()
        })
        buffer.buffer.append({
            'author': 'otheruser',
            'message': 'Message 2',
            'timestamp': datetime.now()
        })
        buffer.buffer.append({
            'author': 'testuser',
            'message': 'Message 3',
            'timestamp': datetime.now()
        })

        results = buffer.search_by_username("testuser")
        assert len(results) == 2
        assert results[0]['author'] == 'testuser'
        assert results[1]['author'] == 'testuser'

    def test_search_by_username_case_insensitive(self):
        """Test username search is case-insensitive"""
        buffer = YouTubeChatBuffer("test_video_id")

        buffer.buffer.append({
            'author': 'TestUser',
            'message': 'Hello',
            'timestamp': datetime.now()
        })

        # Should find with lowercase
        results = buffer.search_by_username("testuser")
        assert len(results) == 1

        # Should find with uppercase
        results = buffer.search_by_username("TESTUSER")
        assert len(results) == 1


class TestErrorHandling:
    """Test error handling and status methods"""

    def test_is_stream_ended_initially_false(self):
        """Test stream_ended flag is initially False"""
        buffer = YouTubeChatBuffer("test_video_id")
        assert buffer.is_stream_ended() is False

    def test_get_error_message_initially_none(self):
        """Test error message is initially None"""
        buffer = YouTubeChatBuffer("test_video_id")
        assert buffer.get_error_message() is None

    def test_stop_buffering_without_start(self):
        """Test stop_buffering can be called without starting"""
        buffer = YouTubeChatBuffer("test_video_id")
        try:
            buffer.stop_buffering()
        except Exception as e:
            pytest.fail(f"stop_buffering raised exception: {e}")
