"""
Test that all critical modules and dependencies can be imported.
This would catch PyInstaller packaging issues like missing pytchat.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


class TestCriticalImports:
    """Test all critical third-party dependencies"""

    def test_import_pytchat(self):
        """Test pytchat and its submodules can be imported"""
        import pytchat
        assert pytchat is not None

    def test_import_pytchat_config(self):
        """Test pytchat.config submodule"""
        import pytchat.config
        assert pytchat.config is not None

    def test_import_pytchat_processors(self):
        """Test pytchat.processors submodule"""
        import pytchat.processors
        assert pytchat.processors is not None

    def test_import_pytchat_exceptions(self):
        """Test pytchat.exceptions submodule"""
        import pytchat.exceptions
        assert pytchat.exceptions is not None

    def test_import_httpx(self):
        """Test httpx (pytchat dependency)"""
        import httpx
        assert httpx is not None

    def test_import_tkinter(self):
        """Test tkinter is available"""
        import tkinter
        assert tkinter is not None

    def test_import_threading(self):
        """Test threading module"""
        import threading
        assert threading is not None

    def test_import_collections(self):
        """Test collections module"""
        import collections
        assert collections is not None

    def test_import_datetime(self):
        """Test datetime module"""
        import datetime
        assert datetime is not None


class TestProjectModules:
    """Test all project modules can be imported"""

    def test_import_strings(self):
        """Test strings module"""
        import strings
        assert strings is not None

    def test_import_url_validator(self):
        """Test url_validator module"""
        import url_validator
        assert url_validator is not None

    def test_import_chat_engine(self):
        """Test chat_engine module"""
        import chat_engine
        assert chat_engine is not None

    def test_import_ui(self):
        """Test ui module"""
        import ui
        assert ui is not None

    def test_import_main(self):
        """Test main module"""
        import main
        assert main is not None


class TestModuleFunctions:
    """Test that key functions exist in modules"""

    def test_url_validator_has_parse_function(self):
        """Test parse_youtube_url function exists"""
        from url_validator import parse_youtube_url
        assert callable(parse_youtube_url)

    def test_url_validator_has_validate_function(self):
        """Test validate_livestream function exists"""
        from url_validator import validate_livestream
        assert callable(validate_livestream)

    def test_chat_engine_has_class(self):
        """Test YouTubeChatBuffer class exists"""
        from chat_engine import YouTubeChatBuffer
        assert YouTubeChatBuffer is not None

    def test_ui_has_application_class(self):
        """Test Application class exists"""
        from ui import Application
        assert Application is not None
