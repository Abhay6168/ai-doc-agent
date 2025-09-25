# Document Summary and Quiz Agent 🤖📚

An intelligent AI-powered agent that generates comprehensive summaries and interactive quizzes from uploaded documents. Perfect for students, researchers, educators, and anyone looking to quickly understand and test knowledge from documents.

## 🚀 Features

### 📄 Document Processing

- **Multiple Format Support**: PDF, DOCX, TXT, and Markdown files
- **Smart Text Extraction**: Advanced text processing for clean, readable content
- **Large File Support**: Handle documents up to 16MB

### 🧠 AI-Powered Summaries

- **Multiple Summary Types**:
  - **Brief**: Concise overview (under 200 words)
  - **Comprehensive**: Detailed summary (300-800 words)
  - **Detailed**: In-depth analysis (800-1200 words)
- **Key Points Extraction**: Automatic identification of main concepts
- **Statistics**: Word count, compression ratio, and more

### 📝 Interactive Quiz Generation

- **Multiple Question Types**:
  - Multiple Choice (A, B, C, D options)
  - True/False statements
  - Short Answer questions
  - Fill-in-the-blank
- **Customizable Difficulty**: Easy, Medium, Hard levels
- **Flexible Length**: 1-50 questions per quiz
- **Smart Distribution**: Balanced mix of question types

### 🎤 Voice Input Support

- **Voice Commands**: Control the application with speech
- **Parameter Input**: Set quiz parameters using voice
- **Microphone Testing**: Built-in audio testing tools

### 🌐 Web Interface

- **Modern UI**: Clean, responsive design
- **Drag & Drop**: Easy file upload
- **Real-time Progress**: Live processing updates
- **Instant Download**: JSON format results

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Microphone (optional, for voice features)

### Steps

1. **Clone the repository**:

```bash
git clone <repository-url>
cd summary-quiz-agent
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Configure API Key**:
   - Open `config.py`
   - Add your Google Gemini API key:

```python
GEMINI_API_KEY = "your-api-key-here"
```

4. **Run the application**:

```bash
# Web interface (recommended)
python src/main.py --web

# Command line interface
python src/main.py --interactive

# Direct processing
python src/main.py --file document.pdf --summary --quiz
```

## 🎯 Usage

### Web Interface

1. Start the web server: `python src/main.py --web`
2. Open browser to `http://127.0.0.1:5000`
3. Upload your document
4. Configure options (summary type, quiz questions, difficulty)
5. Click "Process Document"
6. View results and download JSON files

### Command Line

```bash
# Interactive mode
python src/main.py --interactive

# Direct processing with options
python src/main.py --file document.pdf --summary --quiz --questions 15 --difficulty hard --summary-type detailed

# Web interface
python src/main.py --web
```

### Voice Input

```bash
# Start with voice input enabled
python src/main.py --interactive
# Select option 2 for voice input
# Follow voice prompts for parameters
```

## 📁 Project Structure

```
summary-quiz-agent/
├── config.py              # Configuration and API keys
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── data/                  # Input documents (optional)
├── outputs/               # Generated results
│   ├── summaries/         # Summary JSON files
│   └── quizzes/           # Quiz JSON files
├── src/                   # Main source code
│   ├── __init__.py        # Package initialization
│   ├── main.py           # Main application entry
│   ├── summarizer.py     # Summary generation logic
│   ├── quiz_generator.py # Quiz creation logic
│   ├── voice_input.py    # Voice command handling
│   └── utils.py          # Utility functions
├── tests/                 # Test files
│   ├── test_summarizer.py
│   ├── test_quiz_generator.py
│   └── test_voice_input.py
└── web/                   # Web interface
    ├── app.py            # Flask application
    ├── templates/        # HTML templates
    │   └── index.html    # Main web interface
    └── static/           # CSS, JS, images
        ├── css/
        └── js/
```

## 🔧 Configuration Options

### Summary Types

- **brief**: Quick overview, under 200 words
- **comprehensive**: Balanced detail, 300-800 words
- **detailed**: In-depth analysis, 800-1200 words

### Quiz Difficulties

- **easy**: Basic comprehension questions
- **medium**: Standard difficulty (default)
- **hard**: Advanced analysis and critical thinking

### Supported File Types

- `.pdf` - PDF documents
- `.docx` - Microsoft Word documents
- `.txt` - Plain text files
- `.md` - Markdown files

## 📊 Output Format

### Summary JSON Structure

```json
{
  "summary": "Generated summary text...",
  "summary_type": "comprehensive",
  "original_length": 5000,
  "summary_length": 500,
  "compression_ratio": 0.1,
  "generated_at": "2024-01-01T12:00:00",
  "key_points": ["Point 1", "Point 2", "..."],
  "word_count": 100
}
```

### Quiz JSON Structure

```json
{
  "quiz_metadata": {
    "title": "Document Quiz",
    "num_questions": 10,
    "difficulty": "medium",
    "estimated_time": "15 minutes"
  },
  "questions": [
    {
      "question_number": 1,
      "question": "What is...?",
      "type": "multiple_choice",
      "options": {
        "A": "Option 1",
        "B": "Option 2",
        "C": "Option 3",
        "D": "Option 4"
      },
      "correct_answer": "A",
      "explanation": "Because...",
      "difficulty": "medium"
    }
  ]
}
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_summarizer.py

# Run with coverage
python -m pytest tests/ --cov=src
```

## 🎨 Customization

### Adding New Question Types

1. Extend `QuizGenerator._generate_questions_by_type()`
2. Implement generation logic for new type
3. Update configuration in `config.py`

### Modifying Summary Algorithms

1. Edit `DocumentSummarizer` class methods
2. Add new summary types in `config.py`
3. Update prompt engineering in summarizer methods

### Extending File Support

1. Add new extensions to `config.SUPPORTED_EXTENSIONS`
2. Implement extraction logic in `utils.py`
3. Update file validation

## 🚨 Troubleshooting

### Common Issues

**API Key Errors**:

- Verify your Gemini API key in `config.py`
- Check API quota and billing status

**File Processing Errors**:

- Ensure file is not corrupted
- Check file size (max 16MB)
- Verify file format is supported

**Microphone Issues**:

- Install PyAudio: `pip install pyaudio`
- Check microphone permissions
- Test with: `python src/main.py --interactive` → option 3

**Web Interface Not Loading**:

- Check if port 5000 is available
- Try different port: modify `config.FLASK_PORT`
- Verify all dependencies installed

## 📈 Performance Tips

1. **Large Documents**: For documents over 10MB, use "brief" summary mode
2. **Many Questions**: Limit quiz questions to 20-30 for best performance
3. **Voice Input**: Ensure quiet environment for better recognition
4. **Memory Usage**: Close other applications when processing large files

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit: `git commit -m "Add feature description"`
5. Push: `git push origin feature-name`
6. Create Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for text generation capabilities
- Flask for the web framework
- Bootstrap for UI components
- SpeechRecognition library for voice input

---

**Made with ❤️ for better learning and document analysis**
