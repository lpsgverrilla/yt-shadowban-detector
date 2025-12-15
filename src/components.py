"""Reusable UI components for consistent styling."""

import customtkinter as ctk
from theme import COLORS_DARK, FONTS, SPACING, DIMENSIONS


def create_primary_button(parent, text, command, **kwargs):
    """
    Create a primary action button with consistent styling.

    Args:
        parent: Parent widget
        text: Button text
        command: Click handler function
        **kwargs: Additional CTkButton parameters (state, width, etc.)

    Returns:
        CTkButton: Configured primary button
    """
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=COLORS_DARK['primary'],
        hover_color=COLORS_DARK['primary_hover'],
        text_color='white',
        font=FONTS['body'],
        corner_radius=DIMENSIONS['corner_radius'],
        height=DIMENSIONS['button_height'],
        **kwargs
    )


def create_secondary_button(parent, text, command, **kwargs):
    """
    Create a secondary action button (outlined style).

    Args:
        parent: Parent widget
        text: Button text
        command: Click handler function
        **kwargs: Additional CTkButton parameters (state, width, etc.)

    Returns:
        CTkButton: Configured secondary button
    """
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color='transparent',
        hover_color=COLORS_DARK['bg_elevated'],
        text_color=COLORS_DARK['primary'],
        border_width=2,
        border_color=COLORS_DARK['primary'],
        font=FONTS['body'],
        corner_radius=DIMENSIONS['corner_radius'],
        height=DIMENSIONS['button_height'],
        **kwargs
    )


class StatsCard:
    """
    Stats card component with large number and caption.

    Usage:
        card = StatsCard(parent_frame)
        card.pack(padx=16, pady=16, fill="x")
        card.update_stats(count=42, seconds=120)
    """

    def __init__(self, parent, **kwargs):
        """
        Initialize stats card.

        Args:
            parent: Parent widget
            **kwargs: Additional CTkFrame parameters
        """
        self.frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS_DARK['bg_surface'],
            corner_radius=DIMENSIONS['corner_radius'],
            border_width=1,
            border_color=COLORS_DARK['border'],
            **kwargs
        )

        # Large number in primary color
        self.count_label = ctk.CTkLabel(
            self.frame,
            text="0",
            font=('Segoe UI', 24, 'bold'),
            text_color=COLORS_DARK['primary']
        )
        self.count_label.pack(pady=(SPACING['md'], SPACING['xs']))

        # Caption
        self.caption_label = ctk.CTkLabel(
            self.frame,
            text="messages buffered (0 seconds)",
            font=FONTS['body_sm'],
            text_color=COLORS_DARK['text_secondary']
        )
        self.caption_label.pack(pady=(0, SPACING['md']))

    def pack(self, **kwargs):
        """Pack the stats card frame."""
        self.frame.pack(**kwargs)

    def update_stats(self, count, seconds):
        """
        Update the stats display.

        Args:
            count: Number of messages
            seconds: Time span in seconds
        """
        self.count_label.configure(text=str(count))
        self.caption_label.configure(
            text=f"messages buffered ({seconds} seconds)"
        )

    def get_count_label(self):
        """Get the count label widget for direct access if needed."""
        return self.count_label

    def get_caption_label(self):
        """Get the caption label widget for direct access if needed."""
        return self.caption_label


class InfoCallout:
    """
    Informational callout box with icon and colored background.

    Usage:
        callout = InfoCallout(parent_frame, text="Important info here", icon="💡")
        callout.pack(padx=32, pady=16, fill="x")
    """

    def __init__(self, parent, text, icon="💡", color_scheme="warning", wraplength=420, **kwargs):
        """
        Initialize info callout.

        Args:
            parent: Parent widget
            text: Callout text content
            icon: Emoji or text icon to display
            color_scheme: "warning", "info", "success", or "error"
            wraplength: Text wrap length in pixels
            **kwargs: Additional CTkFrame parameters
        """
        # Select colors based on scheme
        if color_scheme == "warning":
            bg_color = COLORS_DARK['warning_bg']
            border_color = COLORS_DARK['warning']
        elif color_scheme == "info":
            bg_color = COLORS_DARK['bg_surface']
            border_color = COLORS_DARK['primary']
        elif color_scheme == "success":
            bg_color = COLORS_DARK['success_bg']
            border_color = COLORS_DARK['success']
        elif color_scheme == "error":
            bg_color = COLORS_DARK['error_bg']
            border_color = COLORS_DARK['error']
        else:
            bg_color = COLORS_DARK['bg_surface']
            border_color = COLORS_DARK['border']

        self.frame = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=DIMENSIONS['corner_radius'],
            border_width=1,
            border_color=border_color,
            **kwargs
        )

        self.content_label = ctk.CTkLabel(
            self.frame,
            text=f"{icon} {text}" if icon else text,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['caption'],
            justify="left",
            wraplength=wraplength
        )
        self.content_label.pack(padx=SPACING['md'], pady=SPACING['md'])

    def pack(self, **kwargs):
        """Pack the callout frame."""
        self.frame.pack(**kwargs)

    def configure_text(self, text, icon=None):
        """
        Update the callout text.

        Args:
            text: New text content
            icon: Optional new icon (or None to keep existing)
        """
        if icon is not None:
            self.content_label.configure(text=f"{icon} {text}")
        else:
            # Keep existing icon if any
            current_text = self.content_label.cget("text")
            if current_text and len(current_text) > 0 and current_text[0] in "💡ℹ️✅❌⚠️":
                icon_char = current_text[0]
                self.content_label.configure(text=f"{icon_char} {text}")
            else:
                self.content_label.configure(text=text)


class MessageCard:
    """
    Message display card with optional colored border.

    Usage:
        card = MessageCard(parent_frame, border_scheme="success")
        card.pack(padx=32, pady=16, fill="x")
        card.set_message(text="Hello world", timestamp="12:34:56")
    """

    def __init__(self, parent, border_scheme="neutral", **kwargs):
        """
        Initialize message card.

        Args:
            parent: Parent widget
            border_scheme: "success", "error", "warning", "info", or "neutral"
            **kwargs: Additional CTkFrame parameters
        """
        # Select border color based on scheme
        if border_scheme == "success":
            border_color = COLORS_DARK['success']
        elif border_scheme == "error":
            border_color = COLORS_DARK['error']
        elif border_scheme == "warning":
            border_color = COLORS_DARK['warning']
        elif border_scheme == "info":
            border_color = COLORS_DARK['primary']
        else:
            border_color = COLORS_DARK['border']

        self.frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS_DARK['bg_surface'],
            corner_radius=DIMENSIONS['corner_radius'],
            border_width=1,
            border_color=border_color,
            **kwargs
        )

        # Header label
        self.header_label = ctk.CTkLabel(
            self.frame,
            text="",
            text_color=COLORS_DARK['text_tertiary'],
            font=FONTS['caption']
        )
        self.header_label.pack(anchor="w", padx=SPACING['md'], pady=(SPACING['md'], SPACING['xs']))

        # Message text
        self.message_label = ctk.CTkLabel(
            self.frame,
            text="",
            font=FONTS['body'],
            text_color=COLORS_DARK['text_primary'],
            wraplength=400,
            justify="left"
        )
        self.message_label.pack(anchor="w", padx=SPACING['md'], pady=(0, SPACING['xs']))

        # Timestamp label
        self.timestamp_label = ctk.CTkLabel(
            self.frame,
            text="",
            text_color=COLORS_DARK['text_tertiary'],
            font=FONTS['caption']
        )
        self.timestamp_label.pack(anchor="e", padx=SPACING['md'], pady=(0, SPACING['md']))

    def pack(self, **kwargs):
        """Pack the message card frame."""
        self.frame.pack(**kwargs)

    def set_message(self, text, timestamp=None, header=None):
        """
        Set the message content.

        Args:
            text: Message text
            timestamp: Optional timestamp string
            header: Optional header text (e.g., "Latest Message")
        """
        if header:
            self.header_label.configure(text=header)
        else:
            self.header_label.pack_forget()

        self.message_label.configure(text=text)

        if timestamp:
            self.timestamp_label.configure(text=f"at {timestamp}")
        else:
            self.timestamp_label.pack_forget()


def create_countdown_screen(parent, icon="📡", title="Please Wait", info_text="", countdown_label_var=None):
    """
    Create a countdown screen with icon, title, info, and countdown number.

    Args:
        parent: Parent frame
        icon: Emoji icon to display
        title: Screen title
        info_text: Informational text
        countdown_label_var: Variable to store countdown label reference

    Returns:
        tuple: (center_frame, countdown_label, countdown_text_label)
    """
    # Center container
    center_frame = ctk.CTkFrame(parent, fg_color="transparent")
    center_frame.pack(expand=True, fill="both")

    # Icon
    icon_label = ctk.CTkLabel(
        center_frame,
        text=icon,
        font=FONTS['display_icon'],
        text_color=COLORS_DARK['text_primary']
    )
    icon_label.pack(pady=(SPACING['2xl'], SPACING['sm']))

    # Title
    title_label = ctk.CTkLabel(
        center_frame,
        text=title,
        font=FONTS['h1'],
        text_color=COLORS_DARK['text_primary']
    )
    title_label.pack(pady=(0, SPACING['lg']))

    # Info text
    if info_text:
        info_label = ctk.CTkLabel(
            center_frame,
            text=info_text,
            text_color=COLORS_DARK['text_secondary'],
            font=FONTS['body'],
            justify="center"
        )
        info_label.pack(pady=SPACING['sm'])

    # Countdown display (large number in primary color)
    countdown_label = ctk.CTkLabel(
        center_frame,
        text="0",
        font=FONTS['display'],
        text_color=COLORS_DARK['primary']
    )
    countdown_label.pack(pady=SPACING['lg'])

    # Countdown text
    countdown_text_label = ctk.CTkLabel(
        center_frame,
        text="seconds remaining",
        text_color=COLORS_DARK['text_secondary'],
        font=FONTS['caption']
    )
    countdown_text_label.pack()

    return center_frame, countdown_label, countdown_text_label


def create_icon_header(parent, icon, title, pack_kwargs=None):
    """
    Create an icon + title header.

    Args:
        parent: Parent widget
        icon: Emoji or text icon
        title: Header title text
        pack_kwargs: Optional kwargs for pack() method

    Returns:
        CTkFrame: Header frame containing icon and title
    """
    if pack_kwargs is None:
        pack_kwargs = {}

    header_frame = ctk.CTkFrame(parent, fg_color="transparent")
    header_frame.pack(**pack_kwargs)

    icon_label = ctk.CTkLabel(
        header_frame,
        text=f"{icon} ",
        font=FONTS['h1'],
        text_color=COLORS_DARK['text_primary']
    )
    icon_label.pack(side="left")

    title_label = ctk.CTkLabel(
        header_frame,
        text=title,
        font=FONTS['h1'],
        text_color=COLORS_DARK['text_primary']
    )
    title_label.pack(side="left")

    return header_frame


def create_status_indicator(parent, initial_text="", initial_color="text_tertiary", pack_kwargs=None):
    """
    Create a status indicator with colored dot and text.

    Args:
        parent: Parent widget
        initial_text: Initial status text
        initial_color: Initial color key from COLORS_DARK
        pack_kwargs: Optional kwargs for pack() method

    Returns:
        tuple: (frame, dot_label, text_label) for updating status
    """
    if pack_kwargs is None:
        pack_kwargs = {}

    status_frame = ctk.CTkFrame(parent, fg_color="transparent")
    status_frame.pack(**pack_kwargs)

    dot_label = ctk.CTkLabel(
        status_frame,
        text="●",
        font=FONTS['body'],
        text_color=COLORS_DARK.get(initial_color, COLORS_DARK['text_tertiary'])
    )
    dot_label.pack(side="left", padx=(0, SPACING['xs']))

    text_label = ctk.CTkLabel(
        status_frame,
        text=initial_text,
        text_color=COLORS_DARK.get(initial_color, COLORS_DARK['text_tertiary']),
        font=FONTS['caption']
    )
    text_label.pack(side="left")

    return status_frame, dot_label, text_label
