"""
YouTube Chat Buffer and Search Engine
Handles continuous buffering of chat messages and searching for identifiers
"""

import pytchat
from collections import deque
from threading import Thread, Lock, Event
from datetime import datetime
import time


class YouTubeChatBuffer:
    """
    Buffers YouTube livestream chat messages and provides search functionality
    """

    def __init__(self, video_id: str):
        """
        Initialize the chat buffer

        Args:
            video_id: YouTube video ID (11 character string)
        """
        self.video_id = video_id
        self.chat = None
        self.buffer = deque(maxlen=200)
        self.buffer_lock = Lock()
        self.worker_thread = None
        self.stop_flag = Event()
        self.stream_ended_flag = Event()
        self.error_message = None
        self.first_message_time = None

    def start_buffering(self, chat_object=None) -> bool:
        """
        Start buffering messages in background thread

        Args:
            chat_object: Optional pre-created pytchat object (to avoid signal issues)

        Returns:
            True if successfully started, False otherwise
        """
        try:
            # Use provided chat object or create new one
            if chat_object:
                self.chat = chat_object
            else:
                # Initialize pytchat connection
                self.chat = pytchat.create(video_id=self.video_id)

            # Validate stream is live
            if not self.chat.is_alive():
                self.error_message = "Stream is not live"
                return False

            # Start worker thread
            self.stop_flag.clear()
            self.stream_ended_flag.clear()
            self.worker_thread = Thread(target=self._buffer_loop, daemon=True)
            self.worker_thread.start()

            return True

        except pytchat.exceptions.InvalidVideoIdException:
            self.error_message = "Invalid video ID"
            return False
        except Exception as e:
            self.error_message = f"Failed to connect: {str(e)}"
            return False

    def _buffer_loop(self):
        """
        Main worker loop - runs in background thread
        Continuously fetches and buffers chat messages
        """
        reconnect_attempts = 0
        max_reconnect_attempts = 3
        backoff_time = 1.0

        while not self.stop_flag.is_set():
            try:
                if self.chat and self.chat.is_alive():
                    # Fetch new messages
                    for message in self.chat.get().sync_items():
                        # Create message dict
                        # Strip @ from username if present
                        author_name = message.author.name
                        if author_name.startswith('@'):
                            author_name = author_name[1:]

                        msg_dict = {
                            'author': author_name,
                            'message': message.message,
                            'timestamp': datetime.now()
                        }

                        # Add to buffer with lock
                        with self.buffer_lock:
                            self.buffer.append(msg_dict)
                            if self.first_message_time is None:
                                self.first_message_time = datetime.now()

                    # Reset reconnect counter on success
                    reconnect_attempts = 0
                    backoff_time = 1.0

                else:
                    # Stream has ended
                    self.stream_ended_flag.set()
                    break

                # Sleep between fetches
                time.sleep(0.5)

            except Exception as e:
                # Handle connection errors with exponential backoff
                reconnect_attempts += 1

                if reconnect_attempts <= max_reconnect_attempts:
                    self.error_message = f"Connection error, retrying... ({reconnect_attempts}/{max_reconnect_attempts})"
                    time.sleep(backoff_time)
                    backoff_time *= 2  # Exponential backoff

                    # Cannot reconnect from background thread due to pytchat signal issues
                    # Just log the error and continue trying with existing connection
                else:
                    # Max retries exceeded
                    self.error_message = f"Connection lost after {max_reconnect_attempts} attempts"
                    break

    def search_buffer(self, identifier: str) -> list:
        """
        Search buffer for messages containing the identifier

        Args:
            identifier: String to search for (case-sensitive, partial match)

        Returns:
            List of matching message dicts with author and timestamp
        """
        matches = []

        with self.buffer_lock:
            for msg in self.buffer:
                # Case-sensitive partial string matching
                if identifier in msg['message']:
                    matches.append({
                        'author': msg['author'],
                        'message': msg['message'],
                        'timestamp': msg['timestamp']
                    })

        return matches

    def search_by_username(self, username: str) -> list:
        """
        Search buffer for messages from a specific username

        Args:
            username: Username to search for (case-insensitive)

        Returns:
            List of matching message dicts with message and timestamp
        """
        matches = []
        username_lower = username.lower()

        with self.buffer_lock:
            for msg in self.buffer:
                # Case-insensitive username matching
                if msg['author'].lower() == username_lower:
                    matches.append({
                        'author': msg['author'],
                        'message': msg['message'],
                        'timestamp': msg['timestamp']
                    })

        return matches

    def get_buffer_stats(self) -> dict:
        """
        Get statistics about the current buffer

        Returns:
            Dict with message_count and time_span_seconds
        """
        with self.buffer_lock:
            message_count = len(self.buffer)

            if self.first_message_time is not None:
                time_span = (datetime.now() - self.first_message_time).total_seconds()
            else:
                time_span = 0.0

        return {
            'message_count': message_count,
            'time_span_seconds': time_span
        }

    def stop_buffering(self):
        """
        Stop the buffering thread and clean up resources
        """
        # Set stop flag
        self.stop_flag.set()

        # Wait for thread to finish
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5.0)

        # Terminate pytchat connection
        if self.chat:
            try:
                self.chat.terminate()
            except:
                pass

    def is_stream_ended(self) -> bool:
        """
        Check if the stream has ended

        Returns:
            True if stream ended, False otherwise
        """
        return self.stream_ended_flag.is_set()

    def get_error_message(self) -> str:
        """
        Get the last error message

        Returns:
            Error message string or None
        """
        return self.error_message
