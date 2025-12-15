"""Theme constants for the dark-themed UI."""

import customtkinter as ctk

# Set global appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Dark theme color palette
COLORS_DARK = {
    # Primary accent - satellite/radar blue
    'primary': '#60A5FA',           # Light blue - main actions
    'primary_hover': '#3B82F6',     # Darker blue on hover
    'primary_subtle': '#1E40AF',    # Subtle accents

    # Status colors
    'success': '#34D399',           # Bright green - messages found
    'success_bg': '#064E3B',        # Dark green background
    'error': '#F87171',             # Bright red - informative, not alarming
    'error_bg': '#7F1D1D',          # Dark red background
    'warning': '#FBBF24',           # Bright amber - validation warnings
    'warning_bg': '#78350F',        # Dark amber background

    # Backgrounds (layered depth)
    'bg_app': '#0F172A',            # Darkest - main window (slate-950)
    'bg_surface': '#1E293B',        # Medium - cards (slate-800)
    'bg_elevated': '#334155',       # Lightest - inputs (slate-700)

    # Borders
    'border': '#475569',            # Medium contrast (slate-600)
    'border_focus': '#60A5FA',      # Primary color for focused inputs

    # Text hierarchy
    'text_primary': '#F1F5F9',      # Main text (slate-100)
    'text_secondary': '#CBD5E1',    # Body text (slate-300)
    'text_tertiary': '#94A3B8',     # Hints, captions (slate-400)
    'text_disabled': '#64748B',     # Disabled state (slate-500)
}

# Font definitions
FONTS = {
    'display_icon': ('Segoe UI', 48, 'normal'),  # 📡✅❌
    'display': ('Segoe UI', 36, 'bold'),         # Countdown
    'h1': ('Segoe UI', 18, 'bold'),              # Step titles
    'h2': ('Segoe UI', 14, 'bold'),              # Section headers
    'body': ('Segoe UI', 13, 'normal'),          # Body text
    'body_sm': ('Segoe UI', 12, 'normal'),       # Small body
    'caption': ('Segoe UI', 10, 'normal'),       # Captions
}

# Spacing constants
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
    '2xl': 48,
}

# Dimension constants
DIMENSIONS = {
    'window_width': 540,
    'window_height': 600,
    'button_height': 44,
    'input_height': 40,
    'corner_radius': 8,
}
