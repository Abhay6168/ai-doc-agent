#!/usr/bin/env python3
"""
Test cases for VoiceInputHandler class
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from voice_input import VoiceInputHandler

class TestVoiceInputHandler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        with patch('voice_input.sr.Microphone'), patch('voice_input.sr.Recognizer'):
            self.voice_handler = VoiceInputHandler()
    
    def test_voice_handler_initialization(self):
        """Test that voice handler initializes properly"""
        self.assertIsNotNone(self.voice_handler)
        self.assertIsNotNone(self.voice_handler.recognizer)
        self.assertIsNotNone(self.voice_handler.microphone)
    
    def test_extract_number(self):
        """Test number extraction from text"""
        # Test digit extraction
        self.assertEqual(self.voice_handler._extract_number("I want 5 questions"), 5)
        self.assertEqual(self.voice_handler._extract_number("Give me 15 items"), 15)
        
        # Test word extraction
        self.assertEqual(self.voice_handler._extract_number("I want five questions"), 5)
        self.assertEqual(self.voice_handler._extract_number("Give me ten items"), 10)
        
        # Test no number
        self.assertIsNone(self.voice_handler._extract_number("no numbers here"))
    
    def test_extract_difficulty(self):
        """Test difficulty extraction from text"""
        self.assertEqual(self.voice_handler._extract_difficulty("make it easy"), "easy")
        self.assertEqual(self.voice_handler._extract_difficulty("medium difficulty"), "medium")
        self.assertEqual(self.voice_handler._extract_difficulty("hard questions please"), "hard")
        self.assertEqual(self.voice_handler._extract_difficulty("difficult problems"), "hard")
        self.assertIsNone(self.voice_handler._extract_difficulty("no difficulty mentioned"))
    
    def test_extract_summary_type(self):
        """Test summary type extraction from text"""
        self.assertEqual(self.voice_handler._extract_summary_type("brief summary"), "brief")
        self.assertEqual(self.voice_handler._extract_summary_type("short overview"), "brief")
        self.assertEqual(self.voice_handler._extract_summary_type("comprehensive analysis"), "comprehensive")
        self.assertEqual(self.voice_handler._extract_summary_type("complete summary"), "comprehensive")
        self.assertEqual(self.voice_handler._extract_summary_type("detailed report"), "detailed")
        self.assertEqual(self.voice_handler._extract_summary_type("long summary"), "detailed")
        self.assertIsNone(self.voice_handler._extract_summary_type("no type mentioned"))
    
    @patch('voice_input.sr.Recognizer.listen')
    @patch('voice_input.sr.Recognizer.recognize_google')
    def test_listen_for_command_success(self, mock_recognize, mock_listen):
        """Test successful voice command recognition"""
        # Mock successful recognition
        mock_audio = Mock()
        mock_listen.return_value = mock_audio
        mock_recognize.return_value = "test command"
        
        result = self.voice_handler.listen_for_command()
        
        self.assertEqual(result, "test command")
        mock_listen.assert_called_once()
        mock_recognize.assert_called_once_with(mock_audio)
    
    @patch('voice_input.sr.Recognizer.listen')
    def test_listen_for_command_timeout(self, mock_listen):
        """Test voice command timeout"""
        # Mock timeout
        mock_listen.side_effect = Exception("WaitTimeoutError")
        
        result = self.voice_handler.listen_for_command()
        
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()