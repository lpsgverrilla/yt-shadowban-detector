# yt-shadowban-detector

**Version:** 1.0.0

A Windows desktop application that detects whether messages sent by a specific user in a YouTube livestream chat are visible to all viewers or have been shadowbanned.

## Objective

Verify if YouTube livestream chat messages are publicly visible. Sometimes users see their own messages successfully sent, but other viewers cannot see them due to shadowbanning by moderators or automated systems. This tool acts as an independent third-party observer to confirm message visibility.

## How It Works

The application connects to YouTube's public livestream chat API (via [pytchat](https://github.com/taizan-hokuto/pytchat)) and continuously buffers all incoming chat messages in real-time. Users can then search for messages from a specific username to verify they appear in the public chat feed.

**Data Retrieval:**
- Uses pytchat library to access YouTube's innertube API (same API used by youtube.com)
- Polls the public chat feed every ~0.5 seconds
- Stores messages locally in memory during the session
- No data is sent to external servers (runs entirely locally)

## Tech Stack

- **Python 3.12** - Primary language
- **Tkinter** - GUI framework
- **pytchat 0.5.5** - YouTube live chat API library
- **Threading** - Asynchronous message buffering
- **PyInstaller** - Executable bundling
- **pytest** - Testing framework (105 tests, 100% passing)

## Documentation

Complete technical documentation is available in the `docs/` folder:

```
docs/
├── getting-started/    Setup, installation, and quick start guides
├── architecture/       System design, threading model, and data structures
├── api-reference/      High-level module documentation
├── development/        Testing, building, and release workflows
├── guides/             User flows, troubleshooting, and error handling
└── reference/          Dependencies, limitations, and future enhancements
```

**For developers and LLM agents**: See [CLAUDE.md](CLAUDE.md) for a navigation guide to the documentation structure, or start with [docs/README.md](docs/README.md) for a complete index.

## Installation

Download the latest release from the [Releases page](https://github.com/lpsgverrilla/yt-shadowban-detector/releases) and run `yt-shadowban-detector.exe`.

## Building from Source

```bash
# Clone repository
git clone https://github.com/lpsgverrilla/yt-shadowban-detector.git
cd yt-shadowban-detector

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
python -m PyInstaller build.spec

# Executable will be in dist/yt-shadowban-detector.exe
```

## Usage

1. Launch the application
2. Paste a YouTube livestream URL
3. Wait for chat messages to buffer
4. Enter the username to search for
5. View results (messages found or not found)

## Disclaimer

**This project is not affiliated with, endorsed by, or associated with YouTube or Google LLC.**

Use at your own risk. This tool accesses publicly available chat data through unofficial APIs that may change or be restricted at any time.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Repository

[https://github.com/lpsgverrilla/yt-shadowban-detector](https://github.com/lpsgverrilla/yt-shadowban-detector)
