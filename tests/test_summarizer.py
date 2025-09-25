#!/usr/bin/env python3
"""
Test cases for DocumentSummarizer class
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from summarizer import DocumentSummarizer

class TestDocumentSummarizer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.summarizer = DocumentSummarizer()
        self.sample_text = """
        This is a sample document for testing purposes. It contains multiple sentences
        and paragraphs to test the summarization functionality. The document discusses
        various topics including technology, science, and education. This content is
        designed to be long enough to generate meaningful summaries while being simple
        enough for testing purposes.
        """
    
    def test_summarizer_initialization(self):
        """Test that summarizer initializes properly"""
        self.assertIsNotNone(self.summarizer)
        self.assertIsNotNone(self.summarizer.model)
    
    @patch('summarizer.genai.GenerativeModel')
    def test_generate_summary_brief(self, mock_model):
        """Test brief summary generation"""
        # Mock the API response
        mock_response = Mock()
        mock_response.text = "This is a brief summary of the document."
        mock_model.return_value.generate_content.return_value = mock_response
        
        # Create new summarizer with mocked model
        summarizer = DocumentSummarizer()
        summarizer.model = mock_model.return_value
        
        result = summarizer.generate_summary(self.sample_text, "brief")
        
        self.assertIsInstance(result, dict)
        self.assertIn('summary', result)
        self.assertIn('summary_type', result)
        self.assertEqual(result['summary_type'], 'brief')
        self.assertIn('word_count', result)
        self.assertIn('compression_ratio', result)
    
    def test_generate_summary_empty_text(self):
        """Test handling of empty text"""
        with self.assertRaises(ValueError):
            self.summarizer.generate_summary("")
    
    def test_generate_summary_short_text(self):
        """Test handling of very short text"""
        short_text = "Short text."
        with self.assertRaises(ValueError):
            self.summarizer.generate_summary(short_text)
    
    def test_extract_key_points(self):
        """Test key points extraction"""
        # This would need mocking in real tests
        # For now, just test that the method exists
        self.assertTrue(hasattr(self.summarizer, '_extract_key_points'))

if __name__ == '__main__':
    unittest.main()