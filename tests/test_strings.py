"""
Test that all string constants are properly defined
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import strings as S


class TestAppStrings:
    """Test app-level strings"""

    def test_app_title_exists(self):
        """Test APP_TITLE is defined"""
        assert hasattr(S, 'APP_TITLE')
        assert isinstance(S.APP_TITLE, str)
        assert len(S.APP_TITLE) > 0

    def test_total_steps_exists(self):
        """Test TOTAL_STEPS is defined"""
        assert hasattr(S, 'TOTAL_STEPS')
        assert isinstance(S.TOTAL_STEPS, int)
        assert S.TOTAL_STEPS > 0


class TestStep0Strings:
    """Test Step 0 (intro) strings"""

    def test_step0_label(self):
        assert hasattr(S, 'STEP0_LABEL')
        assert isinstance(S.STEP0_LABEL, str)

    def test_step0_intro_text(self):
        assert hasattr(S, 'STEP0_INTRO_TEXT')
        assert isinstance(S.STEP0_INTRO_TEXT, str)
        assert '{total_steps}' in S.STEP0_INTRO_TEXT

    def test_step0_button(self):
        assert hasattr(S, 'STEP0_BUTTON')
        assert isinstance(S.STEP0_BUTTON, str)


class TestStep1Strings:
    """Test Step 1 (URL entry) strings"""

    def test_step1_label(self):
        assert hasattr(S, 'STEP1_LABEL')

    def test_step1_title(self):
        assert hasattr(S, 'STEP1_TITLE')

    def test_step1_hint(self):
        assert hasattr(S, 'STEP1_HINT')

    def test_step1_button(self):
        assert hasattr(S, 'STEP1_BUTTON')

    def test_step1_validating(self):
        assert hasattr(S, 'STEP1_VALIDATING')

    def test_step1_ready(self):
        assert hasattr(S, 'STEP1_READY')

    def test_step1_invalid_url(self):
        assert hasattr(S, 'STEP1_INVALID_URL')


class TestConnectingStrings:
    """Test connecting screen strings"""

    def test_connecting_title(self):
        assert hasattr(S, 'CONNECTING_TITLE')

    def test_connecting_status(self):
        assert hasattr(S, 'CONNECTING_STATUS')


class TestBufferDelayStrings:
    """Test buffer delay screen strings"""

    def test_buffer_delay_title(self):
        assert hasattr(S, 'BUFFER_DELAY_TITLE')

    def test_buffer_delay_info(self):
        assert hasattr(S, 'BUFFER_DELAY_INFO')

    def test_buffer_delay_seconds_remaining(self):
        assert hasattr(S, 'BUFFER_DELAY_SECONDS_REMAINING')


class TestSearchDelayStrings:
    """Test search delay screen strings"""

    def test_search_delay_label(self):
        assert hasattr(S, 'SEARCH_DELAY_LABEL')

    def test_search_delay_title(self):
        assert hasattr(S, 'SEARCH_DELAY_TITLE')

    def test_search_delay_info(self):
        assert hasattr(S, 'SEARCH_DELAY_INFO')

    def test_search_delay_seconds_remaining(self):
        assert hasattr(S, 'SEARCH_DELAY_SECONDS_REMAINING')


class TestStep2Strings:
    """Test Step 2 (monitoring) strings"""

    def test_step2_label(self):
        assert hasattr(S, 'STEP2_LABEL')

    def test_step2_title(self):
        assert hasattr(S, 'STEP2_TITLE')

    def test_step2_description(self):
        assert hasattr(S, 'STEP2_DESCRIPTION')

    def test_step2_buffer_stats(self):
        assert hasattr(S, 'STEP2_BUFFER_STATS')
        assert '{count}' in S.STEP2_BUFFER_STATS
        assert '{seconds}' in S.STEP2_BUFFER_STATS

    def test_step2_buffer_initial(self):
        assert hasattr(S, 'STEP2_BUFFER_INITIAL')

    def test_step2_info(self):
        assert hasattr(S, 'STEP2_INFO')

    def test_step2_self_test_info(self):
        assert hasattr(S, 'STEP2_SELF_TEST_INFO')

    def test_step2_continue_info(self):
        assert hasattr(S, 'STEP2_CONTINUE_INFO')

    def test_step2_button(self):
        assert hasattr(S, 'STEP2_BUTTON')


class TestStep3Strings:
    """Test Step 3 (username entry) strings"""

    def test_step3_label(self):
        assert hasattr(S, 'STEP3_LABEL')

    def test_step3_title(self):
        assert hasattr(S, 'STEP3_TITLE')

    def test_step3_instruction(self):
        assert hasattr(S, 'STEP3_INSTRUCTION')

    def test_step3_username_label(self):
        assert hasattr(S, 'STEP3_USERNAME_LABEL')

    def test_step3_buffer_loading(self):
        assert hasattr(S, 'STEP3_BUFFER_LOADING')

    def test_step3_button(self):
        assert hasattr(S, 'STEP3_BUTTON')


class TestStep4Strings:
    """Test Step 4 (searching) strings"""

    def test_step4_title(self):
        assert hasattr(S, 'STEP4_TITLE')

    def test_step4_looking_for(self):
        assert hasattr(S, 'STEP4_LOOKING_FOR')
        assert '{username}' in S.STEP4_LOOKING_FOR

    def test_step4_status(self):
        assert hasattr(S, 'STEP4_STATUS')


class TestResultsStrings:
    """Test results screen strings"""

    def test_results_label(self):
        assert hasattr(S, 'RESULTS_LABEL')

    def test_results_success_title(self):
        assert hasattr(S, 'RESULTS_SUCCESS_TITLE')

    def test_results_success_count(self):
        assert hasattr(S, 'RESULTS_SUCCESS_COUNT')
        assert '{count}' in S.RESULTS_SUCCESS_COUNT
        assert '{username}' in S.RESULTS_SUCCESS_COUNT

    def test_results_latest_message(self):
        assert hasattr(S, 'RESULTS_LATEST_MESSAGE')

    def test_results_timestamp(self):
        assert hasattr(S, 'RESULTS_TIMESTAMP')
        assert '{time}' in S.RESULTS_TIMESTAMP

    def test_results_fail_title(self):
        assert hasattr(S, 'RESULTS_FAIL_TITLE')

    def test_results_fail_details(self):
        assert hasattr(S, 'RESULTS_FAIL_DETAILS')
        assert '{username}' in S.RESULTS_FAIL_DETAILS
        assert '{count}' in S.RESULTS_FAIL_DETAILS
        assert '{seconds}' in S.RESULTS_FAIL_DETAILS

    def test_results_button_search_again(self):
        assert hasattr(S, 'RESULTS_BUTTON_SEARCH_AGAIN')

    def test_results_button_new_test(self):
        assert hasattr(S, 'RESULTS_BUTTON_NEW_TEST')


class TestMessageBoxStrings:
    """Test message box strings"""

    def test_msgbox_error(self):
        assert hasattr(S, 'MSGBOX_ERROR')

    def test_msgbox_error_invalid_url(self):
        assert hasattr(S, 'MSGBOX_ERROR_INVALID_URL')

    def test_msgbox_connection_failed(self):
        assert hasattr(S, 'MSGBOX_CONNECTION_FAILED')

    def test_msgbox_connection_failed_msg(self):
        assert hasattr(S, 'MSGBOX_CONNECTION_FAILED_MSG')
        assert '{error}' in S.MSGBOX_CONNECTION_FAILED_MSG

    def test_msgbox_stream_ended(self):
        assert hasattr(S, 'MSGBOX_STREAM_ENDED')

    def test_msgbox_stream_ended_msg(self):
        assert hasattr(S, 'MSGBOX_STREAM_ENDED_MSG')

    def test_msgbox_no_username(self):
        assert hasattr(S, 'MSGBOX_NO_USERNAME')

    def test_msgbox_no_username_msg(self):
        assert hasattr(S, 'MSGBOX_NO_USERNAME_MSG')


class TestStringFormatting:
    """Test that format strings work correctly"""

    def test_step0_intro_text_formatting(self):
        """Test intro text can be formatted with total_steps"""
        result = S.STEP0_INTRO_TEXT.format(total_steps=S.TOTAL_STEPS)
        assert str(S.TOTAL_STEPS) in result

    def test_step2_buffer_stats_formatting(self):
        """Test buffer stats can be formatted"""
        result = S.STEP2_BUFFER_STATS.format(count=10, seconds=30)
        assert '10' in result
        assert '30' in result

    def test_step4_looking_for_formatting(self):
        """Test looking for can be formatted with username"""
        result = S.STEP4_LOOKING_FOR.format(username="testuser")
        assert 'testuser' in result

    def test_results_success_count_formatting(self):
        """Test success count can be formatted"""
        result = S.RESULTS_SUCCESS_COUNT.format(count=5, username="testuser")
        assert '5' in result
        assert 'testuser' in result
