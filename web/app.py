#!/usr/bin/env python3
"""
Flask Web Application for Document Summary and Quiz Agent

Provides a web interface for:
1. Uploading documents
2. Generating summaries
3. Creating quizzes
4. Downloading results
"""

import os
import sys
import json
from flask import Flask, request, render_template, jsonify, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

import config
from utils import validate_file_type, create_directories
from summarizer import DocumentSummarizer
from quiz_generator import QuizGenerator

def create_app(document_agent=None):
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-change-this'  # Change this in production
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE
    
    # Create upload directory
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', config.UPLOAD_FOLDER)
    os.makedirs(upload_dir, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_dir
    
    # Initialize components
    if document_agent is None:
        summarizer = DocumentSummarizer()
        quiz_generator = QuizGenerator()
    else:
        summarizer = document_agent.summarizer
        quiz_generator = document_agent.quiz_generator
    
    create_directories()
    
    @app.route('/')
    def index():
        """Main page"""
        return render_template('index.html')
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        """Handle file upload and processing"""
        try:
            # Check if file was uploaded
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Validate file type
            if not validate_file_type(file.filename):
                return jsonify({
                    'error': f'Unsupported file type. Supported types: {", ".join(config.SUPPORTED_EXTENSIONS)}'
                }), 400
            
            # Get form parameters
            generate_summary = request.form.get('generate_summary') == 'true'
            generate_quiz = request.form.get('generate_quiz') == 'true'
            
            if not generate_summary and not generate_quiz:
                return jsonify({'error': 'Must select at least one option (summary or quiz)'}), 400
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Get processing parameters
            summary_type = request.form.get('summary_type', 'comprehensive')
            num_questions = int(request.form.get('num_questions', config.DEFAULT_QUIZ_QUESTIONS))
            difficulty = request.form.get('difficulty', 'medium')
            
            # Process the document
            results = {
                'success': False,
                'filename': filename,
                'summary_data': None,
                'quiz_data': None,
                'errors': []
            }
            
            # Extract text from file
            from utils import extract_text_from_file
            text = extract_text_from_file(file_path)
            if not text:
                return jsonify({'error': 'Could not extract text from the uploaded file'}), 400
            
            # Generate summary if requested
            if generate_summary:
                try:
                    summary_data = summarizer.generate_summary(text, summary_type)
                    results['summary_data'] = summary_data
                    # Don't save to disk for web deployment - just return data
                except Exception as e:
                    results['errors'].append(f'Summary generation failed: {str(e)}')
            
            # Generate quiz if requested
            if generate_quiz:
                try:
                    quiz_data = quiz_generator.generate_quiz(text, num_questions, difficulty)
                    results['quiz_data'] = quiz_data
                    # Don't save to disk for web deployment - just return data
                except Exception as e:
                    results['errors'].append(f'Quiz generation failed: {str(e)}')
            
            # Clean up uploaded file immediately
            try:
                os.remove(file_path)
            except:
                pass
            
            results['success'] = bool(results['summary_data'] or results['quiz_data'])
            
            return jsonify(results)
            
        except RequestEntityTooLarge:
            return jsonify({'error': 'File too large. Maximum size: 16MB'}), 413
        except Exception as e:
            return jsonify({'error': f'Server error: {str(e)}'}), 500
    
    @app.route('/download/<data_type>/<filename>')
    def download_file(data_type, filename):
        """Download generated files"""
        try:
            if data_type == 'summary':
                directory = config.SUMMARIES_DIR
            elif data_type == 'quiz':
                directory = config.QUIZZES_DIR
            else:
                return jsonify({'error': 'Invalid data type'}), 400
            
            file_path = os.path.join(directory, filename)
            
            if not os.path.exists(file_path):
                return jsonify({'error': 'File not found'}), 404
            
            return send_file(file_path, as_attachment=True)
            
        except Exception as e:
            return jsonify({'error': f'Download failed: {str(e)}'}), 500
    
    @app.route('/api/supported-types')
    def get_supported_types():
        """Get list of supported file types"""
        return jsonify({
            'supported_extensions': config.SUPPORTED_EXTENSIONS,
            'max_file_size': config.MAX_FILE_SIZE,
            'quiz_difficulties': config.QUIZ_DIFFICULTY_LEVELS,
            'summary_types': ['brief', 'comprehensive', 'detailed']
        })
    
    @app.errorhandler(413)
    def too_large(e):
        return jsonify({'error': 'File too large. Maximum size allowed is 16MB'}), 413
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

def main():
    """Run the web application"""
    # Create and run the app
    app = create_app()
    print(f"Starting Document Summary and Quiz Agent Web Interface...")
    print(f"Access the application at: http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG)

if __name__ == '__main__':
    main()