"""
yt-shadowban-detector - YouTube Shadowban Detection Tool
Entry point for the application
"""

import customtkinter as ctk
from ui import Application
import sys


def main():
    """
    Main entry point
    """
    try:
        # Create root window
        root = ctk.CTk()

        # Create application
        app = Application(root)

        # Handle window close
        def on_closing():
            app.cleanup()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Start event loop
        root.mainloop()

    except KeyboardInterrupt:
        print("\nApplication closed by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
