"""
User Interface for yt-echo-test
Redesigned step-by-step wizard interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from datetime import datetime
import random
import string
from url_validator import parse_youtube_url, validate_livestream
from chat_engine import YouTubeChatBuffer
import strings as S


# UI States (Step-by-step flow)
STATE_STEP0_INTRO = 0
STATE_STEP1_URL = 1
STATE_CONNECTING = 2
STATE_STEP2_MONITORING = 3
STATE_STEP3_SEND_MESSAGE = 4
STATE_STEP4_SEARCHING = 5
STATE_STEP5_RESULTS = 6




class Application:
    """
    Main application window with step-by-step wizard interface
    """

    def __init__(self, root):
        self.root = root
        self.root.title(S.APP_TITLE)
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        # Try to keep window on top
        try:
            self.root.attributes('-topmost', True)
        except:
            pass

        # State management
        self.current_state = STATE_STEP1_URL
        self.chat_buffer = None
        self.validation_after_id = None
        self.stats_after_id = None
        self.username = None
        self.video_id = None
        self.last_search_results = None
        self.last_search_stats = None

        # Timing safeguards
        self.buffer_delay = 8  # Seconds to wait after buffering starts
        self.search_delay = 8  # Seconds to wait before entering username
        self.delay_timer_id = None

        # Build UI
        self._build_ui()

        # Set initial state
        self._set_state(STATE_STEP0_INTRO)

    def _build_ui(self):
        """
        Build all UI components
        """
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Step indicator
        self.step_label = ttk.Label(main_frame, text="Step 1", font=("TkDefaultFont", 9), foreground="gray")
        self.step_label.pack(anchor=tk.E, pady=(0, 10))

        # Content frame (this changes based on state)
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # We'll build different content for each step dynamically

    def _clear_content(self):
        """Clear all widgets from content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _build_step0_intro(self):
        """Build Step 0: Introduction screen"""
        self.step_label.config(text=S.STEP0_LABEL)

        # Centered explanatory text
        intro_text = S.STEP0_INTRO_TEXT.format(total_steps=S.TOTAL_STEPS)

        intro_label = ttk.Label(self.content_frame, text=intro_text,
                                foreground="gray", font=("TkDefaultFont", 10),
                                wraplength=400, justify=tk.CENTER)
        intro_label.pack(expand=True, pady=(60, 40))

        # Start now button
        start_now_button = ttk.Button(self.content_frame, text=S.STEP0_BUTTON,
                                      command=lambda: self._set_state(STATE_STEP1_URL))
        start_now_button.pack(pady=20)

    def _set_state(self, state):
        """
        Set UI state and rebuild interface for that step

        Args:
            state: One of the STATE_* constants
        """
        self.current_state = state
        self._clear_content()

        if state == STATE_STEP0_INTRO:
            self._build_step0_intro()
        elif state == STATE_STEP1_URL:
            self._build_step1_url()
        elif state == STATE_CONNECTING:
            self._build_connecting()
        elif state == STATE_STEP2_MONITORING:
            self._build_step2_monitoring()
        elif state == STATE_STEP3_SEND_MESSAGE:
            self._build_step3_send_message()
        elif state == STATE_STEP4_SEARCHING:
            self._build_step4_searching()
        elif state == STATE_STEP5_RESULTS:
            self._build_step5_results()

    def _build_step1_url(self):
        """Build Step 1: Enter URL"""
        self.step_label.config(text=S.STEP1_LABEL)

        # Title
        title = ttk.Label(self.content_frame, text=S.STEP1_TITLE,
                         font=("TkDefaultFont", 12, "bold"))
        title.pack(pady=(20, 30))

        # URL entry
        url_frame = ttk.Frame(self.content_frame)
        url_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        self.url_entry = ttk.Entry(url_frame, font=("TkDefaultFont", 10))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.url_entry.bind('<KeyRelease>', self._on_url_changed)

        self.url_icon_label = ttk.Label(url_frame, text="", width=3, font=("TkDefaultFont", 12))
        self.url_icon_label.pack(side=tk.LEFT, padx=(5, 0))

        # Status message
        self.status_label = ttk.Label(self.content_frame, text=S.STEP1_HINT,
                                     foreground="gray", font=("TkDefaultFont", 9))
        self.status_label.pack(pady=(0, 30))

        # Next step button
        self.start_button = ttk.Button(self.content_frame, text=S.STEP1_BUTTON,
                                       command=self._on_start_clicked, state=tk.DISABLED)
        self.start_button.pack(pady=20)

    def _build_connecting(self):
        """Build connecting screen"""
        self.step_label.config(text="")

        # Connecting message
        msg = ttk.Label(self.content_frame, text=S.CONNECTING_TITLE,
                       font=("TkDefaultFont", 12))
        msg.pack(pady=100)

        status = ttk.Label(self.content_frame, text=S.CONNECTING_STATUS, foreground="gray")
        status.pack()

    def _show_buffer_delay_screen(self):
        """Show waiting screen while buffering initializes"""
        self._clear_content()
        self.step_label.config(text="")

        # Title
        title = ttk.Label(self.content_frame, text=S.BUFFER_DELAY_TITLE,
                         font=("TkDefaultFont", 12, "bold"))
        title.pack(pady=(60, 20))

        # Info
        info = ttk.Label(self.content_frame,
                        text=S.BUFFER_DELAY_INFO,
                        foreground="gray", justify=tk.CENTER)
        info.pack(pady=10)

        # Countdown display
        self.countdown_label = ttk.Label(self.content_frame, text="8",
                                        font=("TkDefaultFont", 36, "bold"),
                                        foreground="blue")
        self.countdown_label.pack(pady=40)

        self.countdown_text = ttk.Label(self.content_frame, text=S.BUFFER_DELAY_SECONDS_REMAINING,
                                       foreground="gray")
        self.countdown_text.pack()

    def _show_search_delay_screen(self):
        """Show waiting screen before entering username"""
        self._clear_content()
        self.step_label.config(text=S.SEARCH_DELAY_LABEL)

        # Title
        title = ttk.Label(self.content_frame, text=S.SEARCH_DELAY_TITLE,
                         font=("TkDefaultFont", 12, "bold"))
        title.pack(pady=(60, 20))

        # Info
        info = ttk.Label(self.content_frame,
                        text=S.SEARCH_DELAY_INFO,
                        foreground="gray", justify=tk.CENTER)
        info.pack(pady=10)

        # Countdown display
        self.countdown_label = ttk.Label(self.content_frame, text="8",
                                        font=("TkDefaultFont", 36, "bold"),
                                        foreground="blue")
        self.countdown_label.pack(pady=40)

        self.countdown_text = ttk.Label(self.content_frame, text=S.SEARCH_DELAY_SECONDS_REMAINING,
                                       foreground="gray")
        self.countdown_text.pack()

    def _build_step2_monitoring(self):
        """Build Step 2: Monitoring active"""
        self.step_label.config(text=S.STEP2_LABEL)

        # Success message
        title = ttk.Label(self.content_frame, text=S.STEP2_TITLE,
                         font=("TkDefaultFont", 12, "bold"), foreground="green")
        title.pack(pady=(20, 10))

        desc = ttk.Label(self.content_frame, text=S.STEP2_DESCRIPTION,
                        foreground="gray")
        desc.pack(pady=(0, 30))

        # Buffer stats (large display)
        self.buffer_stats_frame = ttk.Frame(self.content_frame)
        self.buffer_stats_frame.pack(pady=20)

        self.buffer_label = ttk.Label(self.buffer_stats_frame,
                                      text=S.STEP2_BUFFER_INITIAL,
                                      font=("TkDefaultFont", 14))
        self.buffer_label.pack()

        # Info text
        info = ttk.Label(self.content_frame,
                        text=S.STEP2_INFO,
                        foreground="gray", justify=tk.CENTER, font=("TkDefaultFont", 9))
        info.pack(pady=(30, 5))

        # Self-test info
        self_test_info = ttk.Label(self.content_frame,
                        text=S.STEP2_SELF_TEST_INFO,
                        foreground="gray", justify=tk.CENTER, font=("TkDefaultFont", 9))
        self_test_info.pack(pady=(5, 5))

        # Continue text
        continue_info = ttk.Label(self.content_frame,
                        text=S.STEP2_CONTINUE_INFO,
                        foreground="gray", justify=tk.CENTER, font=("TkDefaultFont", 9))
        continue_info.pack(pady=(5, 20))

        # Next button
        self.next_button = ttk.Button(self.content_frame, text=S.STEP2_BUTTON,
                                     command=self._on_next_from_monitoring)
        self.next_button.pack(pady=20)

        # Start updating buffer stats
        self._update_buffer_stats()

    def _build_step3_send_message(self):
        """Build Step 4: Enter username to search"""
        self.step_label.config(text=S.STEP3_LABEL)

        # Title
        title = ttk.Label(self.content_frame, text=S.STEP3_TITLE,
                         font=("TkDefaultFont", 12, "bold"))
        title.pack(pady=(20, 20))

        # Instructions
        instruction = ttk.Label(self.content_frame,
                               text=S.STEP3_INSTRUCTION,
                               foreground="gray", justify=tk.CENTER)
        instruction.pack(pady=(0, 20))

        # Username entry
        username_frame = ttk.Frame(self.content_frame)
        username_frame.pack(padx=40, pady=20)

        username_label = ttk.Label(username_frame, text=S.STEP3_USERNAME_LABEL, font=("TkDefaultFont", 10))
        username_label.pack(side=tk.LEFT, padx=(0, 10))

        self.username_entry = ttk.Entry(username_frame, font=("TkDefaultFont", 12), width=25)
        self.username_entry.pack(side=tk.LEFT)
        self.username_entry.bind('<KeyRelease>', self._on_username_changed)
        self.username_entry.focus()

        # Buffer still updating
        self.buffer_label_step3 = ttk.Label(self.content_frame,
                                           text=S.STEP3_BUFFER_LOADING,
                                           foreground="gray", font=("TkDefaultFont", 9))
        self.buffer_label_step3.pack(pady=(30, 10))

        # Search button
        self.search_button = ttk.Button(self.content_frame, text=S.STEP3_BUTTON,
                                       command=self._on_search_username, state=tk.DISABLED)
        self.search_button.pack(pady=20)

        # Continue updating buffer stats
        self._update_buffer_stats()

    def _build_step4_searching(self):
        """Build searching screen (brief loading while searching)"""
        self.step_label.config(text="")

        # Searching animation
        title = ttk.Label(self.content_frame, text=S.STEP4_TITLE,
                         font=("TkDefaultFont", 12, "bold"))
        title.pack(pady=(40, 20))

        looking = ttk.Label(self.content_frame, text=S.STEP4_LOOKING_FOR.format(username=self.username),
                           foreground="gray")
        looking.pack(pady=10)

        self.search_status = ttk.Label(self.content_frame, text=S.STEP4_STATUS,
                                      foreground="blue")
        self.search_status.pack(pady=20)

    def _build_step5_results(self):
        """Build Step 5: Results - will be populated by _display_results"""
        self.step_label.config(text=S.RESULTS_LABEL)
        # Results content will be added by _display_results method

    # Event Handlers

    def _on_url_changed(self, event=None):
        """Handle URL entry changes with debouncing"""
        # Cancel previous validation if exists
        if self.validation_after_id:
            self.root.after_cancel(self.validation_after_id)

        # Schedule validation after 500ms
        self.validation_after_id = self.root.after(500, self._validate_url)

    def _validate_url(self):
        """Validate the entered URL"""
        url = self.url_entry.get().strip()

        if not url:
            self.url_icon_label.config(text="")
            self.start_button.config(state=tk.DISABLED)
            self.status_label.config(text=S.STEP1_HINT, foreground="gray")
            return

        # Parse URL
        self.video_id = parse_youtube_url(url)

        if not self.video_id:
            self.url_icon_label.config(text="⚠️")
            self.start_button.config(state=tk.DISABLED)
            self.status_label.config(text=S.STEP1_INVALID_URL, foreground="red")
            return

        # Show validating
        self.url_icon_label.config(text="⏳")
        self.status_label.config(text=S.STEP1_VALIDATING, foreground="blue")

        # Schedule validation to run after UI updates
        self.root.after(50, self._do_validation, self.video_id)

    def _do_validation(self, video_id):
        """Perform validation (runs after UI updates)"""
        result = validate_livestream(video_id)
        self._handle_validation_result(result)

    def _handle_validation_result(self, result):
        """Handle validation result"""
        if result['valid'] and result['live']:
            self.url_icon_label.config(text="✓")
            self.start_button.config(state=tk.NORMAL)
            self.status_label.config(text=S.STEP1_READY, foreground="green")
        else:
            self.url_icon_label.config(text="⚠️")
            self.start_button.config(state=tk.DISABLED)
            self.status_label.config(text=result['error'], foreground="red")

    def _on_start_clicked(self):
        """Start monitoring - transition to connecting state"""
        if not self.video_id:
            messagebox.showerror(S.MSGBOX_ERROR, S.MSGBOX_ERROR_INVALID_URL)
            return

        # Go to connecting screen
        self._set_state(STATE_CONNECTING)

        # Schedule connection
        self.root.after(100, self._do_connection, self.video_id)

    def _do_connection(self, video_id):
        """Perform the actual connection"""
        try:
            import pytchat
            chat = pytchat.create(video_id=video_id)

            # Start buffering
            self.chat_buffer = YouTubeChatBuffer(video_id)
            success = self.chat_buffer.start_buffering(chat_object=chat)

            if success:
                # Show waiting screen with countdown
                self._show_buffer_delay_screen()
                # Wait before showing monitoring screen
                self._start_countdown(self.buffer_delay, self._on_buffer_delay_complete)
            else:
                error_msg = self.chat_buffer.get_error_message() if self.chat_buffer else "Unknown error"
                messagebox.showerror(S.MSGBOX_CONNECTION_FAILED, error_msg)
                self._set_state(STATE_STEP1_URL)

        except Exception as e:
            messagebox.showerror(S.MSGBOX_CONNECTION_FAILED, S.MSGBOX_CONNECTION_FAILED_MSG.format(error=str(e)))
            self._set_state(STATE_STEP1_URL)

    def _update_buffer_stats(self):
        """Update buffer statistics display"""
        # Only update if in monitoring or send message states
        if self.current_state not in [STATE_STEP2_MONITORING, STATE_STEP3_SEND_MESSAGE]:
            return

        if self.chat_buffer:
            stats = self.chat_buffer.get_buffer_stats()
            msg_count = stats['message_count']
            time_span = int(stats['time_span_seconds'])

            stats_text = S.STEP2_BUFFER_STATS.format(count=msg_count, seconds=time_span)

            # Update appropriate label based on current state
            try:
                if self.current_state == STATE_STEP2_MONITORING:
                    if hasattr(self, 'buffer_label') and self.buffer_label.winfo_exists():
                        self.buffer_label.config(text=stats_text)
                elif self.current_state == STATE_STEP3_SEND_MESSAGE:
                    if hasattr(self, 'buffer_label_step3') and self.buffer_label_step3.winfo_exists():
                        self.buffer_label_step3.config(text=stats_text)
            except tk.TclError:
                # Widget was destroyed, stop updating
                return

            # Check for errors
            if self.chat_buffer.is_stream_ended():
                messagebox.showwarning(S.MSGBOX_STREAM_ENDED, S.MSGBOX_STREAM_ENDED_MSG)
            elif self.chat_buffer.get_error_message():
                error = self.chat_buffer.get_error_message()
                messagebox.showerror(S.MSGBOX_ERROR, error)

        # Schedule next update in 2 seconds
        self.stats_after_id = self.root.after(2000, self._update_buffer_stats)

    def _start_countdown(self, seconds, callback):
        """Start a countdown timer"""
        self.countdown_seconds = seconds
        self.countdown_callback = callback
        self._update_countdown()

    def _update_countdown(self):
        """Update countdown display"""
        if hasattr(self, 'countdown_label') and self.countdown_label.winfo_exists():
            self.countdown_label.config(text=str(self.countdown_seconds))

            if self.countdown_seconds > 0:
                self.countdown_seconds -= 1
                self.delay_timer_id = self.root.after(1000, self._update_countdown)
            else:
                # Countdown finished, execute callback
                if self.countdown_callback:
                    self.countdown_callback()

    def _on_buffer_delay_complete(self):
        """Called after buffer delay completes"""
        self._set_state(STATE_STEP2_MONITORING)

    def _on_next_from_monitoring(self):
        """User clicked Next Step from monitoring screen"""
        # Cancel stats timer before changing screens
        if self.stats_after_id:
            self.root.after_cancel(self.stats_after_id)
            self.stats_after_id = None

        # Show search delay screen first, then go to username entry
        self._show_search_delay_screen()
        self._start_countdown(self.search_delay, self._on_search_delay_complete)

    def _on_search_delay_complete(self):
        """Called after search delay completes - show username entry"""
        self._set_state(STATE_STEP3_SEND_MESSAGE)

    def _on_username_changed(self, event=None):
        """Handle username entry changes"""
        username = self.username_entry.get().strip()
        if username:
            self.search_button.config(state=tk.NORMAL)
        else:
            self.search_button.config(state=tk.DISABLED)

    def _on_search_username(self):
        """User clicked search button - perform search immediately"""
        self.username = self.username_entry.get().strip()

        if not self.username:
            messagebox.showwarning(S.MSGBOX_NO_USERNAME, S.MSGBOX_NO_USERNAME_MSG)
            return

        # Perform search immediately (delay already happened before username entry)
        self._perform_search()

    def _perform_search(self):
        """Actually perform the search after delay"""
        # Go to searching state
        self._set_state(STATE_STEP4_SEARCHING)

        # Search in background thread
        def search_worker():
            matches = self.chat_buffer.search_by_username(self.username)
            stats = self.chat_buffer.get_buffer_stats()
            self.root.after(0, self._display_results, matches, stats)

        Thread(target=search_worker, daemon=True).start()

    def _display_results(self, matches, stats):
        """Display search results"""
        # Store results for potential re-search
        self.last_search_results = matches
        self.last_search_stats = stats

        self._set_state(STATE_STEP5_RESULTS)

        if matches:
            # Messages found
            match = matches[0]  # Show most recent message
            timestamp_str = match['timestamp'].strftime("%H:%M:%S")

            result_frame = ttk.Frame(self.content_frame)
            result_frame.pack(expand=True, fill=tk.BOTH, pady=30)

            icon = ttk.Label(result_frame, text="✅", font=("TkDefaultFont", 48))
            icon.pack(pady=(20, 10))

            title = ttk.Label(result_frame, text=S.RESULTS_SUCCESS_TITLE,
                            font=("TkDefaultFont", 16, "bold"), foreground="green")
            title.pack(pady=5)

            # Show count if multiple messages
            if len(matches) > 1:
                count_label = ttk.Label(result_frame,
                                       text=S.RESULTS_SUCCESS_COUNT.format(count=len(matches), username=self.username),
                                       foreground="gray", font=("TkDefaultFont", 9))
                count_label.pack(pady=5)

            # Show latest message
            msg_frame = ttk.Frame(result_frame, relief=tk.SOLID, borderwidth=1)
            msg_frame.pack(padx=40, pady=15, fill=tk.X)

            msg_label = ttk.Label(msg_frame, text=S.RESULTS_LATEST_MESSAGE,
                                 foreground="gray", font=("TkDefaultFont", 9))
            msg_label.pack(anchor=tk.W, padx=10, pady=(10, 5))

            message_text = ttk.Label(msg_frame, text=match['message'],
                                    font=("TkDefaultFont", 11), wraplength=350)
            message_text.pack(padx=10, pady=(0, 5))

            timestamp_label = ttk.Label(msg_frame, text=S.RESULTS_TIMESTAMP.format(time=timestamp_str),
                                       foreground="gray", font=("TkDefaultFont", 9))
            timestamp_label.pack(anchor=tk.E, padx=10, pady=(0, 10))

        else:
            # No messages found
            msg_count = stats['message_count']
            time_span = int(stats['time_span_seconds'])

            result_frame = ttk.Frame(self.content_frame)
            result_frame.pack(expand=True, fill=tk.BOTH, pady=40)

            icon = ttk.Label(result_frame, text="❌", font=("TkDefaultFont", 48))
            icon.pack(pady=(20, 10))

            title = ttk.Label(result_frame, text=S.RESULTS_FAIL_TITLE,
                            font=("TkDefaultFont", 16, "bold"), foreground="red")
            title.pack(pady=10)

            details = ttk.Label(result_frame,
                              text=S.RESULTS_FAIL_DETAILS.format(username=self.username, count=msg_count, seconds=time_span),
                              justify=tk.CENTER, foreground="gray", font=("TkDefaultFont", 10))
            details.pack(pady=10)

        # Button frame
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(pady=10)

        # Search Again button (searches same buffer with new username)
        search_again_btn = ttk.Button(button_frame, text=S.RESULTS_BUTTON_SEARCH_AGAIN,
                                      command=self._on_search_again)
        search_again_btn.pack(side=tk.LEFT, padx=5)

        # Start new test button
        new_test_btn = ttk.Button(button_frame, text=S.RESULTS_BUTTON_NEW_TEST,
                                  command=self._on_new_test)
        new_test_btn.pack(side=tk.LEFT, padx=5)

    def _on_search_again(self):
        """Search again with a different username (keeps buffer)"""
        # Go directly to username entry (skip delay since buffer is already collected)
        self._set_state(STATE_STEP3_SEND_MESSAGE)

    def _on_new_test(self):
        """Reset and start a new test"""
        # Cancel any pending callbacks
        if self.validation_after_id:
            self.root.after_cancel(self.validation_after_id)
        if self.stats_after_id:
            self.root.after_cancel(self.stats_after_id)
        if self.delay_timer_id:
            self.root.after_cancel(self.delay_timer_id)

        # Stop buffering in background
        if self.chat_buffer:
            buffer_to_stop = self.chat_buffer
            self.chat_buffer = None

            def stop_worker():
                buffer_to_stop.stop_buffering()

            Thread(target=stop_worker, daemon=True).start()

        # Reset state
        self.username = None
        self.video_id = None
        self.last_search_results = None
        self.last_search_stats = None

        # Go back to step 1
        self._set_state(STATE_STEP1_URL)

    def cleanup(self):
        """Cleanup resources before closing"""
        if self.chat_buffer:
            self.chat_buffer.stop_buffering()
