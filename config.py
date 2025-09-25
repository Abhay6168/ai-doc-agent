import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = ""  # Replace with your valid Gemini API key
MODEL_NAME = "gemini-1.5-flash"

# File paths
DATA_DIR = "data"
OUTPUTS_DIR = "outputs"
SUMMARIES_DIR = os.path.join(OUTPUTS_DIR, "summaries")
QUIZZES_DIR = os.path.join(OUTPUTS_DIR, "quizzes")

# Supported file types
SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.txt', '.md']

# Quiz configuration
DEFAULT_QUIZ_QUESTIONS = 10
QUIZ_DIFFICULTY_LEVELS = ['easy', 'medium', 'hard']

# Summary configuration
MAX_SUMMARY_LENGTH = 1000
MIN_SUMMARY_LENGTH = 200

# Flask configuration
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Upload configuration
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = "uploads"
