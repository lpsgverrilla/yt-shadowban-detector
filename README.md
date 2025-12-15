# yt-shadowban-detector

**Version:** 1.1.0

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

## Release Process

This project uses GitHub Actions for releases. Creating a new release requires two steps:

### Step 1: Prepare the Release

```bash
# Trigger the prepare-release workflow with a version number
gh workflow run prepare-release.yml -f version=X.Y.Z

# Example: Prepare version 1.0.1
gh workflow run prepare-release.yml -f version=1.0.1
```

**Version format**: Use semantic versioning (e.g., `1.0.1`) **without** the "v" prefix.

**What this workflow does**:
1. Validates the version format
2. Checks that the tag doesn't already exist
3. Updates the version in README.md (line 3)
4. Commits the change to the main branch
5. Creates and pushes an annotated git tag `v{version}`

### Step 2: Build and Release

After the prepare-release workflow completes, manually trigger the build and release workflow:

```bash
# Trigger the release workflow for the version tag
gh workflow run release.yml --ref v{version}

# Example: Build and release version 1.0.1
gh workflow run release.yml --ref v1.0.1
```

**What this workflow does**:
1. Runs all tests to ensure code quality
2. Builds the Windows executable with PyInstaller
3. Creates a release package (zip file)
4. Publishes a GitHub release with the executable

**Monitoring the workflows**:
```bash
# View recent workflow runs
gh run list --limit 5

# Watch the latest run
gh run watch
```

For detailed release documentation, see [docs/development/releasing.md](docs/development/releasing.md).

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
