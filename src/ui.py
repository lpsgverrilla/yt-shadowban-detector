"""
User Interface for yt-shadowban-detector
Redesigned step-by-step wizard interface
"""

import sys
import os
import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from datetime import datetime
from url_validator import parse_youtube_url, validate_livestream
from chat_engine import YouTubeChatBuffer
import strings as S
from theme import COLORS_DARK, FONTS, SPACING, DIMENSIONS
from components import (
    create_primary_button,
    create_secondary_button,
    StatsCard,
    InfoCallout,
    MessageCard,
    create_countdown_screen,
    create_icon_header,
    create_status_indicator
)


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Running in development mode
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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

        # Set window icon (Windows only)
        if sys.platform == "win32":
            try:
                self.root.iconbitmap(resource_path("icon.ico"))
            except Exception:
                # Icon file not found or invalid, silently ignore
                pass

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
        self.step_label.pack(anchor="e", padx=(0, SPACING['md']), pady=(SPACING['md'], SPACING['sm']))

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

        # Center container
        center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="both")

        # 📡 Satellite emoji (48pt)
        icon = ctk.CTkLabel(
            center_frame,
            text="📡",
            font=FONTS['display_icon'],
            text_color=COLORS_DARK['text_primary']
        )
        icon.pack(pady=(SPACING['2xl'], SPACING['sm']))

        # Title
        title = ctk.CTkLabel(
            center_frame,
            text="Detect YouTube Chat Shadowbans",
            font=FONTS['h1'],
            text_color=COLORS_DARK['text_primary']
        )
        title.pack(pady=(0, SPACING['md']))

        # Description text
        intro_text = S.STEP0_INTRO_TEXT.format(total_steps=S.TOTAL_STEPS)
        intro_label = ctk.CTkLabel(
            center_frame,
            text=intro_text,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body_sm'],
            wraplength=450,
            justify="center"
        )
        intro_label.pack(pady=(0, SPACING['lg']))

        # Start Detection button
        start_now_button = create_primary_button(
            center_frame,
            text="Start Detection →",
            command=lambda: self._set_state(STATE_STEP1_URL)
        )
        start_now_button.pack(pady=SPACING['sm'])

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

        # Center container
        center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="both", pady=SPACING['xl'])

        # 📡 Icon + Title
        create_icon_header(
            center_frame,
            icon="📡",
            title="Enter YouTube Livestream URL",
            pack_kwargs={'pady': (SPACING['lg'], SPACING['xl'])}
        )

        # URL entry with larger height
        url_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        url_frame.pack(fill="x", padx=SPACING['xl'], pady=(0, SPACING['sm']))

        self.url_entry = ctk.CTkEntry(
            url_frame,
            font=FONTS['body'],
            height=DIMENSIONS['input_height'],
            fg_color=COLORS_DARK['bg_elevated'],
            border_color=COLORS_DARK['border'],
            text_color=COLORS_DARK['text_primary'],
            placeholder_text="https://www.youtube.com/watch?v=..."
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

        # Status message with colored indicator dot
        _, self.status_dot, self.status_label = create_status_indicator(
            center_frame,
            initial_text=S.STEP1_HINT,
            initial_color='text_tertiary',
            pack_kwargs={'pady': (SPACING['sm'], SPACING['xl'])}
        )

        # Next step button
        self.start_button = create_primary_button(
            center_frame,
            text="Continue →",
            command=self._on_start_clicked,
            state="disabled"
        )
        self.start_button.pack(pady=SPACING['sm'])

        # Help text
        help_text = ctk.CTkLabel(
            center_frame,
            text="Paste the URL of an active YouTube livestream",
            text_color=COLORS_DARK['text_tertiary'],
            font=FONTS['caption']
        )
        help_text.pack(pady=(SPACING['xs'], 0))

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

        _, self.countdown_label, self.countdown_text = create_countdown_screen(
            self.content_frame,
            icon="📡",
            title="Preparing Detection",
            info_text="Initializing chat buffer..."
        )

        # Update countdown text to match expected string
        self.countdown_text.configure(text=S.BUFFER_DELAY_SECONDS_REMAINING)
        self.countdown_label.configure(text="8")

    def _show_search_delay_screen(self):
        """Show waiting screen before entering username"""
        self._clear_content()
        self.step_label.configure(text=S.SEARCH_DELAY_LABEL)

        _, self.countdown_label, self.countdown_text = create_countdown_screen(
            self.content_frame,
            icon="📡",
            title="Preparing Search",
            info_text="Ensuring sufficient buffer data..."
        )

        # Update countdown text to match expected string
        self.countdown_text.configure(text=S.SEARCH_DELAY_SECONDS_REMAINING)
        self.countdown_label.configure(text="8")

    def _build_step2_monitoring(self):
        """Build Step 2: Monitoring active"""
        self.step_label.configure(text=S.STEP2_LABEL)

        # Center container
        center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="both", pady=SPACING['lg'])

        # Success message
        title = ctk.CTkLabel(
            center_frame,
            text=S.STEP2_TITLE,
            font=FONTS['h1'],
            text_color=COLORS_DARK['success']
        )
        title.pack(pady=(SPACING['md'], SPACING['sm']))

        desc = ctk.CTkLabel(
            center_frame,
            text=S.STEP2_DESCRIPTION,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body']
        )
        desc.pack(pady=(0, SPACING['lg']))

        # Stats card (elevated surface)
        self.stats_card = StatsCard(center_frame)
        self.stats_card.pack(padx=SPACING['xl'], pady=SPACING['md'], fill="x")

        # Keep references for updating
        self.buffer_count_label = self.stats_card.get_count_label()
        self.buffer_caption_label = self.stats_card.get_caption_label()

        # Info callout box with lightbulb icon
        info_callout = InfoCallout(
            center_frame,
            text=S.STEP2_SELF_TEST_INFO,
            icon="💡",
            color_scheme="warning"
        )
        info_callout.pack(padx=SPACING['xl'], pady=SPACING['md'], fill="x")

        # Continue text
        continue_info = ctk.CTkLabel(
            center_frame,
            text=S.STEP2_CONTINUE_INFO,
            text_color=COLORS_DARK['text_tertiary'],
            font=FONTS['caption'],
            justify="center"
        )
        continue_info.pack(pady=(SPACING['md'], SPACING['sm']))

        # Next button
        self.next_button = create_primary_button(
            center_frame,
            text="Next Step →",
            command=self._on_next_from_monitoring
        )
        self.next_button.pack(pady=SPACING['sm'])

        # Start updating buffer stats
        self._update_buffer_stats()

    def _build_step3_send_message(self):
        """Build Step 4: Enter username to search"""
        self.step_label.configure(text=S.STEP3_LABEL)

        # Center container
        center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="both", pady=SPACING['lg'])

        # Title
        title = ctk.CTkLabel(
            center_frame,
            text=S.STEP3_TITLE,
            font=FONTS['h1'],
            text_color=COLORS_DARK['text_primary']
        )
        title.pack(pady=(SPACING['md'], SPACING['lg']))

        # Instructions
        instruction = ctk.CTkLabel(
            center_frame,
            text=S.STEP3_INSTRUCTION,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body'],
            justify="center"
        )
        instruction.pack(pady=(0, SPACING['xl']))

        # Username entry with @ prefix
        username_container = ctk.CTkFrame(center_frame, fg_color="transparent")
        username_container.pack(padx=SPACING['xl'], pady=SPACING['md'])

        username_frame = ctk.CTkFrame(
            username_container,
            fg_color=COLORS_DARK['bg_elevated'],
            corner_radius=DIMENSIONS['corner_radius'],
            border_width=1,
            border_color=COLORS_DARK['border']
        )
        username_frame.pack()

        # @ prefix label
        at_label = ctk.CTkLabel(
            username_frame,
            text="@",
            font=FONTS['h2'],
            text_color=COLORS_DARK['text_tertiary']
        )
        at_label.pack(side="left", padx=(SPACING['sm'], 0))

        self.username_entry = ctk.CTkEntry(
            username_frame,
            font=FONTS['h2'],
            width=220,
            height=DIMENSIONS['input_height'],
            fg_color="transparent",
            border_width=0,
            text_color=COLORS_DARK['text_primary'],
            placeholder_text="username"
        )
        self.username_entry.pack(side="left", padx=(0, SPACING['sm']))
        self.username_entry.bind('<KeyRelease>', self._on_username_changed)
        self.username_entry.focus()

        # Buffer still updating
        self.buffer_label_step3 = ctk.CTkLabel(
            center_frame,
            text=S.STEP3_BUFFER_LOADING,
            text_color=COLORS_DARK['text_tertiary'],
            font=FONTS['caption']
        )
        self.buffer_label_step3.pack(pady=(SPACING['lg'], SPACING['sm']))

        # Search button
        self.search_button = create_primary_button(
            center_frame,
            text="Search for Username →",
            command=self._on_search_username,
            state="disabled"
        )
        self.search_button.pack(pady=SPACING['sm'])

        # Continue updating buffer stats
        self._update_buffer_stats()

    def _build_step4_searching(self):
        """Build searching screen (brief loading while searching)"""
        self.step_label.configure(text="")

        # Center container
        center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="both")

        # 🔍 Search icon
        icon = ctk.CTkLabel(
            center_frame,
            text="🔍",
            font=FONTS['display_icon'],
            text_color=COLORS_DARK['text_primary']
        )
        icon.pack(pady=(SPACING['2xl'], SPACING['sm']))

        # Title
        title = ctk.CTkLabel(
            center_frame,
            text="Searching Chat Buffer",
            font=FONTS['h1'],
            text_color=COLORS_DARK['text_primary']
        )
        title.pack(pady=(0, SPACING['lg']))

        # Looking for username
        looking = ctk.CTkLabel(
            center_frame,
            text=S.STEP4_LOOKING_FOR.format(username=self.username),
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body']
        )
        looking.pack(pady=SPACING['sm'])

        # Status
        self.search_status = ctk.CTkLabel(
            center_frame,
            text=S.STEP4_STATUS,
            text_color=COLORS_DARK['primary'],
            font=FONTS['caption']
        )
        self.search_status.pack(pady=SPACING['md'])

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
            self.status_dot.configure(text_color=COLORS_DARK['text_tertiary'])
            self.status_label.configure(text=S.STEP1_HINT, text_color=COLORS_DARK['text_tertiary'])
            return

        # Parse URL
        self.video_id = parse_youtube_url(url)

        if not self.video_id:
            self.url_icon_label.configure(text="⚠️")
            self.start_button.configure(state="disabled")
            self.status_dot.configure(text_color=COLORS_DARK['error'])
            self.status_label.configure(text=S.STEP1_INVALID_URL, text_color=COLORS_DARK['error'])
            return

        # Show validating
        self.url_icon_label.configure(text="⏳")
        self.status_dot.configure(text_color=COLORS_DARK['warning'])
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
            self.status_dot.configure(text_color=COLORS_DARK['success'])
            self.status_label.configure(text=S.STEP1_READY, text_color=COLORS_DARK['success'])
        else:
            self.url_icon_label.configure(text="⚠️")
            self.start_button.configure(state="disabled")
            self.status_dot.configure(text_color=COLORS_DARK['error'])
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
                    # Update stats card with separate count and caption
                    if hasattr(self, 'buffer_count_label') and self.buffer_count_label.winfo_exists():
                        self.buffer_count_label.configure(text=str(msg_count))
                    if hasattr(self, 'buffer_caption_label') and self.buffer_caption_label.winfo_exists():
                        self.buffer_caption_label.configure(
                            text=f"messages buffered ({time_span} seconds)"
                        )
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

        # Center container
        result_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        result_frame.pack(expand=True, fill="both", pady=SPACING['lg'])

        if matches:
            # SUCCESS - Messages found
            match = matches[0]  # Show most recent message
            timestamp_str = match['timestamp'].strftime("%H:%M:%S")

            # ✅ Icon
            icon = ctk.CTkLabel(
                result_frame,
                text="✅",
                font=FONTS['display_icon'],
                text_color=COLORS_DARK['text_primary']
            )
            icon.pack(pady=(SPACING['lg'], SPACING['sm']))

            # Title
            title = ctk.CTkLabel(
                result_frame,
                text=S.RESULTS_SUCCESS_TITLE,
                font=FONTS['h1'],
                text_color=COLORS_DARK['success']
            )
            title.pack(pady=(0, SPACING['xs']))

            # Show count if multiple messages
            if len(matches) > 1:
                count_label = ctk.CTkLabel(
                    result_frame,
                    text=S.RESULTS_SUCCESS_COUNT.format(count=len(matches), username=self.username),
                    text_color=COLORS_DARK['text_tertiary'],
                    font=FONTS['caption']
                )
                count_label.pack(pady=SPACING['xs'])

            # Message card with green left border
            msg_card = MessageCard(result_frame, border_scheme="success")
            msg_card.pack(padx=SPACING['xl'], pady=SPACING['md'], fill="x")
            msg_card.set_message(
                text=match['message'],
                timestamp=timestamp_str,
                header=S.RESULTS_LATEST_MESSAGE
            )

        else:
            # FAILURE - No messages found (INFORMATIONAL BLUE, not error red)
            msg_count = stats['message_count']
            time_span = int(stats['time_span_seconds'])

            # ℹ️ Icon (informational, not error)
            icon = ctk.CTkLabel(
                result_frame,
                text="ℹ️",
                font=FONTS['display_icon'],
                text_color=COLORS_DARK['text_primary']
            )
            icon.pack(pady=(SPACING['lg'], SPACING['sm']))

            # Title (informational blue, not error red)
            title = ctk.CTkLabel(
                result_frame,
                text=S.RESULTS_FAIL_TITLE,
                font=FONTS['h1'],
                text_color=COLORS_DARK['primary']
            )
            title.pack(pady=(0, SPACING['md']))

            # Informational card (blue tint)
            info_card = ctk.CTkFrame(
                result_frame,
                fg_color=COLORS_DARK['bg_surface'],
                corner_radius=DIMENSIONS['corner_radius'],
                border_width=1,
                border_color=COLORS_DARK['primary']
            )
            info_card.pack(padx=SPACING['xl'], pady=SPACING['md'], fill="x")

            # Details text
            details = ctk.CTkLabel(
                info_card,
                text=f"No messages from @{self.username}\n\nChecked {msg_count} messages over {time_span} seconds",
                justify="center",
                text_color=COLORS_DARK['text_secondary'],
                font=FONTS['body']
            )
            details.pack(padx=SPACING['md'], pady=SPACING['md'])

            # Possible reasons (bulleted list)
            reasons_text = (
                "Possible reasons:\n"
                "• Messages may be shadowbanned\n"
                "• Username might be misspelled\n"
                "• User hasn't sent messages during buffer period\n"
                "• Messages were deleted by moderators"
            )
            reasons = ctk.CTkLabel(
                info_card,
                text=reasons_text,
                justify="left",
                text_color=COLORS_DARK['text_tertiary'],
                font=FONTS['caption']
            )
            reasons.pack(anchor="w", padx=SPACING['md'], pady=(0, SPACING['md']))

        # Button frame
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(pady=SPACING['md'])

        # Search Again button (searches same buffer with new username)
        search_again_btn = create_primary_button(
            button_frame,
            text=S.RESULTS_BUTTON_SEARCH_AGAIN,
            command=self._on_search_again
        )
        search_again_btn.pack(side="left", padx=SPACING['xs'])

        # Start new test button (secondary style)
        new_test_btn = create_secondary_button(
            button_frame,
            text=S.RESULTS_BUTTON_NEW_TEST,
            command=self._on_new_test
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
