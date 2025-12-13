# yt-echo-test

A simple tool to detect if you're shadowbanned in YouTube livestream chat by verifying if your messages appear publicly.

## What It Does

1. Connects to a YouTube livestream chat
2. Continuously buffers live chat messages
3. Searches for your unique message identifier
4. Shows whether your message appeared (not shadowbanned) or didn't appear (possibly shadowbanned)

## Installation

### Option 1: Run from Source

1. Install Python 3.x
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python src/main.py
   ```

### Option 2: Use Pre-built Executable

Download the appropriate executable for your platform:
- Windows: `yt-echo-test.exe`
- Linux: `yt-echo-test`

No Python installation required.

## Usage

1. **Enter Livestream URL**
   - Paste a YouTube livestream URL
   - Wait for validation (green checkmark)

2. **Enter Message Identifier**
   - Create a unique string (e.g., "test_12345")
   - Click the copy button to copy it

3. **Start Monitoring**
   - Click "Start Monitoring"
   - Wait for the buffer to start collecting messages

4. **Send Your Message**
   - Go to the livestream chat
   - Send a message containing your identifier
   - Wait a few seconds

5. **Check Result**
   - Click "Check Now"
   - See if your message was found:
     - **Green**: Message found - not shadowbanned
     - **Red**: Message not found - possibly shadowbanned

## Supported URL Formats

- `https://youtube.com/watch?v=VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `VIDEO_ID` (11 characters)

## Tips

- Use a unique identifier that's unlikely to appear in other messages
- Make sure you start monitoring BEFORE sending your message
- The buffer holds the last 200 messages
- If the stream has high traffic, check immediately after sending

## Building from Source

To create a standalone executable:

```bash
pyinstaller build.spec
```

The executable will be in the `dist/` folder.

## Technical Details

- **Buffer Size**: 200 messages (circular buffer)
- **Search**: Case-sensitive partial string matching
- **Threading**: Background worker for chat collection
- **UI Framework**: Tkinter

## Troubleshooting

**"Stream is not currently live"**
- The video must be a live stream, not a regular video or premiere

**"Connection lost"**
- Check your internet connection
- The stream may have ended
- YouTube API may be experiencing issues

**Message not found but you sent it**
- Make sure you started monitoring before sending
- The stream might have too many messages (buffer overflow)
- Try with a longer, more unique identifier

## License

MIT License
