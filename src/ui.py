"""
User Interface for yt-shadowban-detector
Redesigned step-by-step wizard interface
"""

import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from datetime import datetime
from url_validator import parse_youtube_url, validate_livestream
from chat_engine import YouTubeChatBuffer
import strings as S
from theme import COLORS_DARK, FONTS, SPACING, DIMENSIONS


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
        self.root.title("yt-shadowban-detector")  # Text-only window title
        self.root.geometry(f"{DIMENSIONS['window_width']}x{DIMENSIONS['window_height']}")
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
        main_frame = ctk.CTkFrame(self.root, fg_color=COLORS_DARK['bg_app'])
        main_frame.pack(fill="both", expand=True, padx=SPACING['lg'], pady=SPACING['lg'])

        # Step indicator
        self.step_label = ctk.CTkLabel(
            main_frame,
            text="Step 1",
            font=FONTS['caption'],
            text_color=COLORS_DARK['text_tertiary']
        )
        self.step_label.pack(anchor="e", pady=(0, SPACING['sm']))

        # Content frame (this changes based on state)
        self.content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        # We'll build different content for each step dynamically

    def _clear_content(self):
        """Clear all widgets from content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _build_step0_intro(self):
        """Build Step 0: Introduction screen"""
        self.step_label.configure(text=S.STEP0_LABEL)

        # Centered explanatory text
        intro_text = S.STEP0_INTRO_TEXT.format(total_steps=S.TOTAL_STEPS)

        intro_label = ctk.CTkLabel(
            self.content_frame,
            text=intro_text,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body_sm'],
            wraplength=450,
            justify="center"
        )
        intro_label.pack(expand=True, pady=(SPACING['2xl'], SPACING['xl']))

        # Start now button
        start_now_button = ctk.CTkButton(
            self.content_frame,
            text=S.STEP0_BUTTON,
            command=lambda: self._set_state(STATE_STEP1_URL),
            fg_color=COLORS_DARK['primary'],
            hover_color=COLORS_DARK['primary_hover'],
            text_color='white',
            font=FONTS['body'],
            corner_radius=DIMENSIONS['corner_radius'],
            height=DIMENSIONS['button_height']
        )
        start_now_button.pack(pady=SPACING['lg'])

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
        self.step_label.configure(text=S.STEP1_LABEL)

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP1_TITLE,
            font=FONTS['h1'],
            text_color=COLORS_DARK['text_primary']
        )
        title.pack(pady=(SPACING['lg'], SPACING['xl']))

        # URL entry
        url_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        url_frame.pack(fill="x", padx=SPACING['lg'], pady=(0, SPACING['sm']))

        self.url_entry = ctk.CTkEntry(
            url_frame,
            font=FONTS['body'],
            height=DIMENSIONS['input_height'],
            fg_color=COLORS_DARK['bg_elevated'],
            border_color=COLORS_DARK['border'],
            text_color=COLORS_DARK['text_primary']
        )
        self.url_entry.pack(side="left", fill="x", expand=True)
        self.url_entry.bind('<KeyRelease>', self._on_url_changed)

        self.url_icon_label = ctk.CTkLabel(
            url_frame,
            text="",
            width=30,
            font=FONTS['h2']
        )
        self.url_icon_label.pack(side="left", padx=(SPACING['sm'], 0))

        # Status message
        self.status_label = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP1_HINT,
            text_color=COLORS_DARK['text_tertiary'],
            font=FONTS['caption']
        )
        self.status_label.pack(pady=(0, SPACING['xl']))

        # Next step button
        self.start_button = ctk.CTkButton(
            self.content_frame,
            text=S.STEP1_BUTTON,
            command=self._on_start_clicked,
            state="disabled",
            fg_color=COLORS_DARK['primary'],
            hover_color=COLORS_DARK['primary_hover'],
            text_color='white',
            font=FONTS['body'],
            corner_radius=DIMENSIONS['corner_radius'],
            height=DIMENSIONS['button_height']
        )
        self.start_button.pack(pady=SPACING['lg'])

    def _build_connecting(self):
        """Build connecting screen"""
        self.step_label.configure(text="")

        # Connecting message
        msg = ctk.CTkLabel(
            self.content_frame,
            text=S.CONNECTING_TITLE,
            font=FONTS['h1'],
            text_color=COLORS_DARK['text_primary']
        )
        msg.pack(pady=100)

        status = ctk.CTkLabel(
            self.content_frame,
            text=S.CONNECTING_STATUS,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body']
        )
        status.pack()

    def _show_buffer_delay_screen(self):
        """Show waiting screen while buffering initializes"""
        self._clear_content()
        self.step_label.configure(text="")

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text=S.BUFFER_DELAY_TITLE,
            font=FONTS['h1'],
            text_color=COLORS_DARK['text_primary']
        )
        title.pack(pady=(SPACING['2xl'], SPACING['lg']))

        # Info
        info = ctk.CTkLabel(
            self.content_frame,
            text=S.BUFFER_DELAY_INFO,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body'],
            justify="center"
        )
        info.pack(pady=SPACING['sm'])

        # Countdown display
        self.countdown_label = ctk.CTkLabel(
            self.content_frame,
            text="8",
            font=FONTS['display'],
            text_color=COLORS_DARK['primary']
        )
        self.countdown_label.pack(pady=SPACING['xl'])

        self.countdown_text = ctk.CTkLabel(
            self.content_frame,
            text=S.BUFFER_DELAY_SECONDS_REMAINING,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body']
        )
        self.countdown_text.pack()

    def _show_search_delay_screen(self):
        """Show waiting screen before entering username"""
        self._clear_content()
        self.step_label.configure(text=S.SEARCH_DELAY_LABEL)

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text=S.SEARCH_DELAY_TITLE,
            font=FONTS['h1'],
            text_color=COLORS_DARK['text_primary']
        )
        title.pack(pady=(SPACING['2xl'], SPACING['lg']))

        # Info
        info = ctk.CTkLabel(
            self.content_frame,
            text=S.SEARCH_DELAY_INFO,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body'],
            justify="center"
        )
        info.pack(pady=SPACING['sm'])

        # Countdown display
        self.countdown_label = ctk.CTkLabel(
            self.content_frame,
            text="8",
            font=FONTS['display'],
            text_color=COLORS_DARK['primary']
        )
        self.countdown_label.pack(pady=SPACING['xl'])

        self.countdown_text = ctk.CTkLabel(
            self.content_frame,
            text=S.SEARCH_DELAY_SECONDS_REMAINING,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body']
        )
        self.countdown_text.pack()

    def _build_step2_monitoring(self):
        """Build Step 2: Monitoring active"""
        self.step_label.configure(text=S.STEP2_LABEL)

        # Success message
        title = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP2_TITLE,
            font=FONTS['h1'],
            text_color=COLORS_DARK['success']
        )
        title.pack(pady=(SPACING['lg'], SPACING['sm']))

        desc = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP2_DESCRIPTION,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body']
        )
        desc.pack(pady=(0, SPACING['xl']))

        # Buffer stats (large display)
        self.buffer_stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.buffer_stats_frame.pack(pady=SPACING['lg'])

        self.buffer_label = ctk.CTkLabel(
            self.buffer_stats_frame,
            text=S.STEP2_BUFFER_INITIAL,
            font=FONTS['h2'],
            text_color=COLORS_DARK['text_primary']
        )
        self.buffer_label.pack()

        # Info text
        info = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP2_INFO,
            text_color=COLORS_DARK['text_tertiary'],
            font=FONTS['caption'],
            justify="center"
        )
        info.pack(pady=(SPACING['xl'], SPACING['xs']))

        # Self-test info
        self_test_info = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP2_SELF_TEST_INFO,
            text_color=COLORS_DARK['text_tertiary'],
            font=FONTS['caption'],
            justify="center"
        )
        self_test_info.pack(pady=(SPACING['xs'], SPACING['xs']))

        # Continue text
        continue_info = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP2_CONTINUE_INFO,
            text_color=COLORS_DARK['text_tertiary'],
            font=FONTS['caption'],
            justify="center"
        )
        continue_info.pack(pady=(SPACING['xs'], SPACING['lg']))

        # Next button
        self.next_button = ctk.CTkButton(
            self.content_frame,
            text=S.STEP2_BUTTON,
            command=self._on_next_from_monitoring,
            fg_color=COLORS_DARK['primary'],
            hover_color=COLORS_DARK['primary_hover'],
            text_color='white',
            font=FONTS['body'],
            corner_radius=DIMENSIONS['corner_radius'],
            height=DIMENSIONS['button_height']
        )
        self.next_button.pack(pady=SPACING['lg'])

        # Start updating buffer stats
        self._update_buffer_stats()

    def _build_step3_send_message(self):
        """Build Step 4: Enter username to search"""
        self.step_label.configure(text=S.STEP3_LABEL)

        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP3_TITLE,
            font=FONTS['h1'],
            text_color=COLORS_DARK['text_primary']
        )
        title.pack(pady=(SPACING['lg'], SPACING['lg']))

        # Instructions
        instruction = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP3_INSTRUCTION,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body'],
            justify="center"
        )
        instruction.pack(pady=(0, SPACING['lg']))

        # Username entry
        username_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        username_frame.pack(padx=SPACING['xl'], pady=SPACING['lg'])

        username_label = ctk.CTkLabel(
            username_frame,
            text=S.STEP3_USERNAME_LABEL,
            font=FONTS['body'],
            text_color=COLORS_DARK['text_primary']
        )
        username_label.pack(side="left", padx=(0, SPACING['sm']))

        self.username_entry = ctk.CTkEntry(
            username_frame,
            font=FONTS['h2'],
            width=250,
            height=DIMENSIONS['input_height'],
            fg_color=COLORS_DARK['bg_elevated'],
            border_color=COLORS_DARK['border'],
            text_color=COLORS_DARK['text_primary']
        )
        self.username_entry.pack(side="left")
        self.username_entry.bind('<KeyRelease>', self._on_username_changed)
        self.username_entry.focus()

        # Buffer still updating
        self.buffer_label_step3 = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP3_BUFFER_LOADING,
            text_color=COLORS_DARK['text_tertiary'],
            font=FONTS['caption']
        )
        self.buffer_label_step3.pack(pady=(SPACING['xl'], SPACING['sm']))

        # Search button
        self.search_button = ctk.CTkButton(
            self.content_frame,
            text=S.STEP3_BUTTON,
            command=self._on_search_username,
            state="disabled",
            fg_color=COLORS_DARK['primary'],
            hover_color=COLORS_DARK['primary_hover'],
            text_color='white',
            font=FONTS['body'],
            corner_radius=DIMENSIONS['corner_radius'],
            height=DIMENSIONS['button_height']
        )
        self.search_button.pack(pady=SPACING['lg'])

        # Continue updating buffer stats
        self._update_buffer_stats()

    def _build_step4_searching(self):
        """Build searching screen (brief loading while searching)"""
        self.step_label.configure(text="")

        # Searching animation
        title = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP4_TITLE,
            font=FONTS['h1'],
            text_color=COLORS_DARK['text_primary']
        )
        title.pack(pady=(SPACING['xl'], SPACING['lg']))

        looking = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP4_LOOKING_FOR.format(username=self.username),
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body']
        )
        looking.pack(pady=SPACING['sm'])

        self.search_status = ctk.CTkLabel(
            self.content_frame,
            text=S.STEP4_STATUS,
            text_color=COLORS_DARK['primary'],
            font=FONTS['body']
        )
        self.search_status.pack(pady=SPACING['lg'])

    def _build_step5_results(self):
        """Build Step 5: Results - will be populated by _display_results"""
        self.step_label.configure(text=S.RESULTS_LABEL)
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
            self.url_icon_label.configure(text="")
            self.start_button.configure(state="disabled")
            self.status_label.configure(text=S.STEP1_HINT, text_color=COLORS_DARK['text_tertiary'])
            return

        # Parse URL
        self.video_id = parse_youtube_url(url)

        if not self.video_id:
            self.url_icon_label.configure(text="⚠️")
            self.start_button.configure(state="disabled")
            self.status_label.configure(text=S.STEP1_INVALID_URL, text_color=COLORS_DARK['error'])
            return

        # Show validating
        self.url_icon_label.configure(text="⏳")
        self.status_label.configure(text=S.STEP1_VALIDATING, text_color=COLORS_DARK['primary'])

        # Schedule validation to run after UI updates
        self.root.after(50, self._do_validation, self.video_id)

    def _do_validation(self, video_id):
        """Perform validation (runs after UI updates)"""
        result = validate_livestream(video_id)
        self._handle_validation_result(result)

    def _handle_validation_result(self, result):
        """Handle validation result"""
        if result['valid'] and result['live']:
            self.url_icon_label.configure(text="✓")
            self.start_button.configure(state="normal")
            self.status_label.configure(text=S.STEP1_READY, text_color=COLORS_DARK['success'])
        else:
            self.url_icon_label.configure(text="⚠️")
            self.start_button.configure(state="disabled")
            self.status_label.configure(text=result['error'], text_color=COLORS_DARK['error'])

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
                        self.buffer_label.configure(text=stats_text)
                elif self.current_state == STATE_STEP3_SEND_MESSAGE:
                    if hasattr(self, 'buffer_label_step3') and self.buffer_label_step3.winfo_exists():
                        self.buffer_label_step3.configure(text=stats_text)
            except Exception:
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
            self.countdown_label.configure(text=str(self.countdown_seconds))

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
            self.search_button.configure(state="normal")
        else:
            self.search_button.configure(state="disabled")

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

            result_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            result_frame.pack(expand=True, fill="both", pady=SPACING['xl'])

            icon = ctk.CTkLabel(
                result_frame,
                text="✅",
                font=FONTS['display_icon'],
                text_color=COLORS_DARK['text_primary']
            )
            icon.pack(pady=(SPACING['lg'], SPACING['sm']))

            title = ctk.CTkLabel(
                result_frame,
                text=S.RESULTS_SUCCESS_TITLE,
                font=FONTS['h1'],
                text_color=COLORS_DARK['success']
            )
            title.pack(pady=SPACING['xs'])

            # Show count if multiple messages
            if len(matches) > 1:
                count_label = ctk.CTkLabel(
                    result_frame,
                    text=S.RESULTS_SUCCESS_COUNT.format(count=len(matches), username=self.username),
                    text_color=COLORS_DARK['text_tertiary'],
                    font=FONTS['caption']
                )
                count_label.pack(pady=SPACING['xs'])

            # Show latest message
            msg_frame = ctk.CTkFrame(
                result_frame,
                fg_color=COLORS_DARK['bg_surface'],
                border_color=COLORS_DARK['border'],
                border_width=1,
                corner_radius=DIMENSIONS['corner_radius']
            )
            msg_frame.pack(padx=SPACING['xl'], pady=SPACING['md'], fill="x")

            msg_label = ctk.CTkLabel(
                msg_frame,
                text=S.RESULTS_LATEST_MESSAGE,
                text_color=COLORS_DARK['text_tertiary'],
                font=FONTS['caption']
            )
            msg_label.pack(anchor="w", padx=SPACING['sm'], pady=(SPACING['sm'], SPACING['xs']))

            message_text = ctk.CTkLabel(
                msg_frame,
                text=match['message'],
                font=FONTS['body'],
                text_color=COLORS_DARK['text_primary'],
                wraplength=400
            )
            message_text.pack(padx=SPACING['sm'], pady=(0, SPACING['xs']))

            timestamp_label = ctk.CTkLabel(
                msg_frame,
                text=S.RESULTS_TIMESTAMP.format(time=timestamp_str),
                text_color=COLORS_DARK['text_tertiary'],
                font=FONTS['caption']
            )
            timestamp_label.pack(anchor="e", padx=SPACING['sm'], pady=(0, SPACING['sm']))

        else:
            # No messages found
            msg_count = stats['message_count']
            time_span = int(stats['time_span_seconds'])

            result_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            result_frame.pack(expand=True, fill="both", pady=SPACING['xl'])

            icon = ctk.CTkLabel(
                result_frame,
                text="❌",
                font=FONTS['display_icon'],
                text_color=COLORS_DARK['text_primary']
            )
            icon.pack(pady=(SPACING['lg'], SPACING['sm']))

            title = ctk.CTkLabel(
                result_frame,
                text=S.RESULTS_FAIL_TITLE,
                font=FONTS['h1'],
                text_color=COLORS_DARK['error']
            )
            title.pack(pady=SPACING['sm'])

            details = ctk.CTkLabel(
                result_frame,
                text=S.RESULTS_FAIL_DETAILS.format(username=self.username, count=msg_count, seconds=time_span),
                justify="center",
                text_color=COLORS_DARK['text_secondary'],
                font=FONTS['body'],
                wraplength=450
            )
            details.pack(pady=SPACING['sm'])

        # Button frame
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(pady=SPACING['sm'])

        # Search Again button (searches same buffer with new username)
        search_again_btn = ctk.CTkButton(
            button_frame,
            text=S.RESULTS_BUTTON_SEARCH_AGAIN,
            command=self._on_search_again,
            fg_color=COLORS_DARK['primary'],
            hover_color=COLORS_DARK['primary_hover'],
            text_color='white',
            font=FONTS['body'],
            corner_radius=DIMENSIONS['corner_radius'],
            height=DIMENSIONS['button_height']
        )
        search_again_btn.pack(side="left", padx=SPACING['xs'])

        # Start new test button
        new_test_btn = ctk.CTkButton(
            button_frame,
            text=S.RESULTS_BUTTON_NEW_TEST,
            command=self._on_new_test,
            fg_color="transparent",
            hover_color=COLORS_DARK['bg_elevated'],
            text_color=COLORS_DARK['primary'],
            border_width=2,
            border_color=COLORS_DARK['primary'],
            font=FONTS['body'],
            corner_radius=DIMENSIONS['corner_radius'],
            height=DIMENSIONS['button_height']
        )
        new_test_btn.pack(side="left", padx=SPACING['xs'])

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
