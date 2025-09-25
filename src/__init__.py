"""
Document Summary and Quiz Generation Agent

A comprehensive AI-powered tool for generating summaries and quizzes from documents.
Supports PDF, DOCX, TXT, and Markdown files.
"""

__version__ = "1.0.0"
__author__ = "Document Agent Team"

from .summarizer import DocumentSummarizer
from .quiz_generator import QuizGenerator
from .voice_input import VoiceInputHandler
from . import utils

__all__ = [
    'DocumentSummarizer',
    'QuizGenerator', 
    'VoiceInputHandler',
    'utils'
]