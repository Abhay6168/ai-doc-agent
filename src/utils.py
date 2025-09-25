import os
import PyPDF2
import docx
import json
import datetime
from typing import Optional, List, Dict, Any
import config

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        config.DATA_DIR,
        config.OUTPUTS_DIR,
        config.SUMMARIES_DIR,
        config.QUIZZES_DIR,
        config.UPLOAD_FOLDER
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Extract text from various file formats
    """
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return extract_text_from_docx(file_path)
        elif file_extension in ['.txt', '.md']:
            return extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
            
    except Exception as e:
        print(f"Error extracting text from {file_path}: {str(e)}")
        return None

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")
    return text

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT/MD file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception as e:
        raise Exception(f"Error reading text file: {str(e)}")
    return text

def validate_file_type(filename: str) -> bool:
    """Check if file type is supported"""
    file_extension = os.path.splitext(filename)[1].lower()
    return file_extension in config.SUPPORTED_EXTENSIONS

def save_json_output(data: Dict[Any, Any], filename: str, output_type: str) -> str:
    """Save data as JSON file"""
    if output_type == 'summary':
        output_dir = config.SUMMARIES_DIR
    elif output_type == 'quiz':
        output_dir = config.QUIZZES_DIR
    else:
        output_dir = config.OUTPUTS_DIR
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{filename}_{timestamp}.json"
    output_path = os.path.join(output_dir, output_filename)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return output_path
    except Exception as e:
        raise Exception(f"Error saving JSON file: {str(e)}")

def clean_text(text: str) -> str:
    """Clean and preprocess text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters that might cause issues
    text = text.replace('\x00', '')  # Remove null characters
    
    return text

def chunk_text(text: str, max_length: int = 4000) -> List[str]:
    """Split text into chunks for processing"""
    if not text:
        return []
    
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for space
        if current_length + word_length > max_length and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks