"""
UI Strings for yt-echo-test
All text labels and messages organized by screen
"""

# =============================================================================
# APP
# =============================================================================
APP_TITLE = "yt-echo-test"

# Total number of steps (for display in intro)
TOTAL_STEPS = 4

# =============================================================================
# STEP 0 - INTRO
# =============================================================================
STEP0_LABEL = "Step 0"
STEP0_INTRO_TEXT = (
    "Sometimes a user will send a message on the chat of a YouTube livestream, "
    "and on his browser he will see the message normally, but others watching "
    "the public stream won't see it.\n\n"
    "This program allows you to confirm that messages sent by a particular user "
    "in a YouTube livestream has indeed been made public for all.\n\n"
    "The program will guide you through the {total_steps} needed steps."
)
STEP0_BUTTON = "Start now"

# =============================================================================
# STEP 1 - URL ENTRY
# =============================================================================
STEP1_LABEL = "Step 1"
STEP1_TITLE = "Paste YouTube Livestream URL"
STEP1_HINT = "Paste a live stream URL above"
STEP1_BUTTON = "Next step"
STEP1_VALIDATING = "Validating..."
STEP1_READY = "Ready to start"
STEP1_INVALID_URL = "Invalid YouTube URL"

# =============================================================================
# CONNECTING SCREEN
# =============================================================================
CONNECTING_TITLE = "🔗 Connecting to livestream..."
CONNECTING_STATUS = "Please wait..."

# =============================================================================
# BUFFER DELAY SCREEN
# =============================================================================
BUFFER_DELAY_TITLE = "⏳ Preparing..."
BUFFER_DELAY_INFO = "Please wait..."
BUFFER_DELAY_SECONDS_REMAINING = "seconds remaining"

# =============================================================================
# SEARCH DELAY SCREEN
# =============================================================================
SEARCH_DELAY_LABEL = "Step 3"
SEARCH_DELAY_TITLE = "⏳ Searching..."
SEARCH_DELAY_INFO = "Please wait..."
SEARCH_DELAY_SECONDS_REMAINING = "seconds remaining"

# =============================================================================
# STEP 2 - MONITORING
# =============================================================================
STEP2_LABEL = "Step 2"
STEP2_TITLE = "✅ Monitoring Live Chat"
STEP2_DESCRIPTION = "Buffering messages from the stream..."
STEP2_BUFFER_STATS = "Buffer: {count} messages ({seconds} sec)"
STEP2_BUFFER_INITIAL = "Buffer: 0 messages (0 sec)"
STEP2_INFO = "The app is collecting chat messages."
STEP2_SELF_TEST_INFO = (
    "If you want to detect your own messages, this is the time to send one.\n"
    "Make sure it is indeed sent, and also not deleted by bots or moderators after sent."
)
STEP2_CONTINUE_INFO = "Click 'Next Step' when ready to continue."
STEP2_BUTTON = "Next Step"

# =============================================================================
# STEP 3 - USERNAME ENTRY (shown as Step 4 in UI)
# =============================================================================
STEP3_LABEL = "Step 4"
STEP3_TITLE = "👤 Enter Username to Search"
STEP3_INSTRUCTION = (
    "Enter the username of the person whose messages\n"
    "you want to find in the chat buffer:"
)
STEP3_USERNAME_LABEL = "Username:"
STEP3_BUFFER_LOADING = "Buffer: ... messages"
STEP3_BUTTON = "Search for Username"

# =============================================================================
# STEP 4 - SEARCHING
# =============================================================================
STEP4_TITLE = "🔍 Searching Chat Buffer"
STEP4_LOOKING_FOR = "Looking for username: {username}"
STEP4_STATUS = "Checking messages..."

# =============================================================================
# STEP 5 - RESULTS
# =============================================================================
RESULTS_LABEL = "Results"

# Success
RESULTS_SUCCESS_TITLE = "Messages Found!"
RESULTS_SUCCESS_COUNT = "Found {count} messages from @{username}"
RESULTS_LATEST_MESSAGE = "Latest message:"
RESULTS_TIMESTAMP = "Timestamp: {time}"

# Failure
RESULTS_FAIL_TITLE = "No Messages Found"
RESULTS_FAIL_DETAILS = (
    "No messages from @{username}\n\n"
    "Checked {count} messages over {seconds} seconds"
)

# Buttons
RESULTS_BUTTON_SEARCH_AGAIN = "Search Again"
RESULTS_BUTTON_NEW_TEST = "Start New Test"

# =============================================================================
# MESSAGE BOXES
# =============================================================================
MSGBOX_ERROR = "Error"
MSGBOX_ERROR_INVALID_URL = "Invalid YouTube URL"
MSGBOX_CONNECTION_FAILED = "Connection Failed"
MSGBOX_CONNECTION_FAILED_MSG = "Failed to connect: {error}"
MSGBOX_STREAM_ENDED = "Stream Ended"
MSGBOX_STREAM_ENDED_MSG = "The livestream has ended."
MSGBOX_NO_USERNAME = "No Username"
MSGBOX_NO_USERNAME_MSG = "Please enter a username to search for"
