#!/usr/bin/env python3
"""
Test cases for QuizGenerator class
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quiz_generator import QuizGenerator

class TestQuizGenerator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.quiz_generator = QuizGenerator()
        self.sample_text = """
        This is a sample document for testing quiz generation. It contains information
        about various subjects including mathematics, science, and history. The document
        provides facts and details that can be used to create meaningful quiz questions
        for educational purposes.
        """
    
    def test_quiz_generator_initialization(self):
        """Test that quiz generator initializes properly"""
        self.assertIsNotNone(self.quiz_generator)
        self.assertIsNotNone(self.quiz_generator.model)
    
    @patch('quiz_generator.genai.GenerativeModel')
    def test_generate_quiz_basic(self, mock_model):
        """Test basic quiz generation"""
        # Mock the API response
        mock_response = Mock()
        mock_response.text = '''[
            {
                "question": "What is the main topic?",
                "type": "multiple_choice",
                "options": {"A": "Math", "B": "Science", "C": "History", "D": "All"},
                "correct_answer": "D",
                "explanation": "The document covers all topics",
                "difficulty": "medium"
            }
        ]'''
        mock_model.return_value.generate_content.return_value = mock_response
        
        # Create new quiz generator with mocked model
        quiz_gen = QuizGenerator()
        quiz_gen.model = mock_model.return_value
        
        result = quiz_gen.generate_quiz(self.sample_text, 5, "medium")
        
        self.assertIsInstance(result, dict)
        self.assertIn('quiz_metadata', result)
        self.assertIn('questions', result)
        self.assertIn('instructions', result)
        self.assertIn('scoring', result)
    
    def test_generate_quiz_empty_text(self):
        """Test handling of empty text"""
        with self.assertRaises(ValueError):
            self.quiz_generator.generate_quiz("")
    
    def test_generate_quiz_short_text(self):
        """Test handling of very short text"""
        short_text = "Short."
        with self.assertRaises(ValueError):
            self.quiz_generator.generate_quiz(short_text)
    
    def test_calculate_question_distribution(self):
        """Test question distribution calculation"""
        question_types = ["multiple_choice", "true_false", "short_answer"]
        distribution = self.quiz_generator._calculate_question_distribution(10, question_types)
        
        self.assertIsInstance(distribution, dict)
        self.assertEqual(sum(distribution.values()), 10)
        
        for q_type in question_types:
            self.assertIn(q_type, distribution)
            self.assertGreaterEqual(distribution[q_type], 0)
    
    def test_estimate_completion_time(self):
        """Test completion time estimation"""
        time_easy = self.quiz_generator._estimate_completion_time(10, "easy")
        time_medium = self.quiz_generator._estimate_completion_time(10, "medium")
        time_hard = self.quiz_generator._estimate_completion_time(10, "hard")
        
        self.assertIsInstance(time_easy, str)
        self.assertIsInstance(time_medium, str)
        self.assertIsInstance(time_hard, str)
        self.assertIn("minutes", time_easy)

if __name__ == '__main__':
    unittest.main()