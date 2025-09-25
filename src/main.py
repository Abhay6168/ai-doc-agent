#!/usr/bin/env python3
"""
Document Summary and Quiz Generation Agent

This is the main entry point for the application that can:
1. Generate summaries from uploaded documents
2. Create quizzes based on document content
3. Handle voice input for interaction
4. Provide web interface for easy usage
"""

import os
import sys
import argparse
from typing import Optional, Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from utils import create_directories, extract_text_from_file, validate_file_type
from summarizer import DocumentSummarizer
from quiz_generator import QuizGenerator
from voice_input import VoiceInputHandler

class DocumentAgent:
    def __init__(self):
        """Initialize the Document Summary and Quiz Agent"""
        self.summarizer = DocumentSummarizer()
        self.quiz_generator = QuizGenerator()
        self.voice_handler = VoiceInputHandler()
        
        # Create necessary directories
        create_directories()
        
        print("Document Summary and Quiz Agent initialized!")
        print(f"Supported file types: {', '.join(config.SUPPORTED_EXTENSIONS)}")
    
    def process_document(self, file_path: str, generate_summary: bool = True, generate_quiz: bool = True, **kwargs) -> Dict[str, Any]:
        """
        Process a document to generate summary and/or quiz
        
        Args:
            file_path (str): Path to the document
            generate_summary (bool): Whether to generate summary
            generate_quiz (bool): Whether to generate quiz
            **kwargs: Additional parameters (num_questions, difficulty, summary_type)
            
        Returns:
            dict: Processing results
        """
        results = {
            "success": False,
            "file_path": file_path,
            "summary_data": None,
            "quiz_data": None,
            "errors": []
        }
        
        try:
            # Validate file
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not validate_file_type(os.path.basename(file_path)):
                raise ValueError(f"Unsupported file type. Supported: {config.SUPPORTED_EXTENSIONS}")
            
            print(f"\nProcessing document: {os.path.basename(file_path)}")
            
            # Extract text
            print("Extracting text from document...")
            text = extract_text_from_file(file_path)
            if not text:
                raise ValueError("Could not extract text from the document")
            
            print(f"Extracted {len(text)} characters from document")
            
            # Generate summary if requested
            if generate_summary:
                try:
                    print("Generating summary...")
                    summary_type = kwargs.get('summary_type', 'comprehensive')
                    summary_data = self.summarizer.generate_summary(text, summary_type)
                    
                    # Save summary
                    filename = os.path.splitext(os.path.basename(file_path))[0]
                    summary_path = self.summarizer.save_summary(summary_data, filename)
                    
                    results["summary_data"] = summary_data
                    results["summary_file"] = summary_path
                    print(f"✓ Summary generated and saved to: {summary_path}")
                    
                except Exception as e:
                    error_msg = f"Error generating summary: {str(e)}"
                    results["errors"].append(error_msg)
                    print(f"✗ {error_msg}")
            
            # Generate quiz if requested
            if generate_quiz:
                try:
                    print("Generating quiz...")
                    num_questions = kwargs.get('num_questions', config.DEFAULT_QUIZ_QUESTIONS)
                    difficulty = kwargs.get('difficulty', 'medium')
                    
                    quiz_data = self.quiz_generator.generate_quiz(text, num_questions, difficulty)
                    
                    # Save quiz
                    filename = os.path.splitext(os.path.basename(file_path))[0]
                    quiz_path = self.quiz_generator.save_quiz(quiz_data, filename)
                    
                    results["quiz_data"] = quiz_data
                    results["quiz_file"] = quiz_path
                    print(f"✓ Quiz with {len(quiz_data['questions'])} questions generated and saved to: {quiz_path}")
                    
                except Exception as e:
                    error_msg = f"Error generating quiz: {str(e)}"
                    results["errors"].append(error_msg)
                    print(f"✗ {error_msg}")
            
            # Mark as successful if at least one operation succeeded
            results["success"] = bool(results["summary_data"] or results["quiz_data"])
            
            if results["success"]:
                print(f"\n✓ Document processing completed successfully!")
            else:
                print(f"\n✗ Document processing failed!")
            
            return results
            
        except Exception as e:
            error_msg = f"Error processing document: {str(e)}"
            results["errors"].append(error_msg)
            print(f"✗ {error_msg}")
            return results
    
    def interactive_mode(self):
        """Run the agent in interactive mode"""
        print("\n" + "="*60)
        print("Welcome to Document Summary and Quiz Agent!")
        print("="*60)
        
        while True:
            try:
                print("\nOptions:")
                print("1. Process a document")
                print("2. Use voice input")
                print("3. Test microphone")
                print("4. Exit")
                
                choice = input("\nEnter your choice (1-4): ").strip()
                
                if choice == '1':
                    self._handle_document_processing()
                elif choice == '2':
                    self._handle_voice_input()
                elif choice == '3':
                    self._test_microphone()
                elif choice == '4':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter 1-4.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def _handle_document_processing(self):
        """Handle document processing in interactive mode"""
        try:
            # Get file path
            file_path = input("Enter the path to your document: ").strip().strip('"\'')
            
            if not os.path.exists(file_path):
                print("✗ File not found!")
                return
            
            # Get options
            print("\nWhat would you like to generate?")
            generate_summary = input("Generate summary? (y/n): ").strip().lower() in ['y', 'yes']
            generate_quiz = input("Generate quiz? (y/n): ").strip().lower() in ['y', 'yes']
            
            if not generate_summary and not generate_quiz:
                print("Nothing to generate!")
                return
            
            # Get additional parameters
            kwargs = {}
            
            if generate_summary:
                print("\nSummary type options: brief, comprehensive, detailed")
                summary_type = input("Summary type (default: comprehensive): ").strip().lower()
                if summary_type in ['brief', 'comprehensive', 'detailed']:
                    kwargs['summary_type'] = summary_type
            
            if generate_quiz:
                try:
                    num_questions = int(input(f"Number of questions (default: {config.DEFAULT_QUIZ_QUESTIONS}): ").strip() or config.DEFAULT_QUIZ_QUESTIONS)
                    kwargs['num_questions'] = max(1, min(50, num_questions))  # Limit between 1-50
                except ValueError:
                    kwargs['num_questions'] = config.DEFAULT_QUIZ_QUESTIONS
                
                print("Difficulty options: easy, medium, hard")
                difficulty = input("Difficulty (default: medium): ").strip().lower()
                if difficulty in config.QUIZ_DIFFICULTY_LEVELS:
                    kwargs['difficulty'] = difficulty
            
            # Process document
            results = self.process_document(file_path, generate_summary, generate_quiz, **kwargs)
            
            # Display results
            if results["success"]:
                print("\n" + "="*50)
                print("PROCESSING RESULTS")
                print("="*50)
                
                if results.get("summary_data"):
                    summary = results["summary_data"]
                    print(f"\n📄 SUMMARY ({summary['summary_type'].upper()}):")
                    print("-" * 40)
                    print(summary["summary"][:500] + "..." if len(summary["summary"]) > 500 else summary["summary"])
                    print(f"\nWord count: {summary['word_count']}")
                    print(f"Compression ratio: {summary['compression_ratio']}")
                    print(f"Key points: {len(summary['key_points'])}")
                
                if results.get("quiz_data"):
                    quiz = results["quiz_data"]
                    print(f"\n📝 QUIZ PREVIEW:")
                    print("-" * 40)
                    print(f"Questions: {quiz['quiz_metadata']['num_questions']}")
                    print(f"Difficulty: {quiz['quiz_metadata']['difficulty'].title()}")
                    print(f"Estimated time: {quiz['quiz_metadata']['estimated_time']}")
                    
                    # Show first question as preview
                    if quiz["questions"]:
                        q1 = quiz["questions"][0]
                        print(f"\nSample Question:")
                        print(f"Q1: {q1.get('question', 'N/A')}")
                        if q1.get('type') == 'multiple_choice' and 'options' in q1:
                            for option, text in q1['options'].items():
                                print(f"  {option}: {text}")
            
            if results["errors"]:
                print(f"\n⚠️  Errors encountered:")
                for error in results["errors"]:
                    print(f"  - {error}")
                    
        except Exception as e:
            print(f"Error in document processing: {str(e)}")
    
    def _handle_voice_input(self):
        """Handle voice input mode"""
        try:
            print("\nVoice Input Mode")
            print("-" * 30)
            
            # Test microphone first
            if not self.voice_handler.test_microphone():
                print("Microphone test failed. Please check your microphone.")
                return
            
            # Get file path through voice (optional - can still use text input)
            use_voice = input("Get parameters through voice? (y/n): ").strip().lower() in ['y', 'yes']
            
            if use_voice:
                print("\nGetting parameters through voice input...")
                params = self.voice_handler.get_voice_parameters()
                
                if params:
                    print("\nReceived parameters:")
                    for key, value in params.items():
                        print(f"  {key}: {value}")
                    
                    # Still need file path via text input for now
                    file_path = input("\nEnter document path: ").strip().strip('"\'')
                    
                    if os.path.exists(file_path):
                        # Process with voice parameters
                        results = self.process_document(
                            file_path, 
                            generate_summary=True,
                            generate_quiz=True,
                            **params
                        )
                        
                        if results["success"]:
                            print("\n✓ Document processed successfully using voice parameters!")
                    else:
                        print("File not found!")
                else:
                    print("Could not get parameters through voice input.")
            else:
                print("Voice input mode cancelled.")
                
        except Exception as e:
            print(f"Error in voice input mode: {str(e)}")
    
    def _test_microphone(self):
        """Test microphone functionality"""
        print("\nTesting microphone...")
        success = self.voice_handler.test_microphone()
        if success:
            print("✓ Microphone is working properly!")
        else:
            print("✗ Microphone test failed. Please check your setup.")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Document Summary and Quiz Generation Agent")
    parser.add_argument("--file", "-f", help="Path to document file")
    parser.add_argument("--summary", "-s", action="store_true", help="Generate summary")
    parser.add_argument("--quiz", "-q", action="store_true", help="Generate quiz")
    parser.add_argument("--questions", "-n", type=int, default=config.DEFAULT_QUIZ_QUESTIONS, help="Number of quiz questions")
    parser.add_argument("--difficulty", "-d", choices=config.QUIZ_DIFFICULTY_LEVELS, default="medium", help="Quiz difficulty")
    parser.add_argument("--summary-type", "-t", choices=["brief", "comprehensive", "detailed"], default="comprehensive", help="Summary type")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--web", "-w", action="store_true", help="Start web interface")
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = DocumentAgent()
    
    try:
        if args.web:
            # Start web interface
            print("Starting web interface...")
            from web.app import create_app
            app = create_app(agent)
            app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG)
            
        elif args.interactive or not args.file:
            # Interactive mode
            agent.interactive_mode()
            
        else:
            # Command line mode
            if not args.summary and not args.quiz:
                print("Please specify --summary and/or --quiz")
                return
            
            results = agent.process_document(
                args.file,
                generate_summary=args.summary,
                generate_quiz=args.quiz,
                num_questions=args.questions,
                difficulty=args.difficulty,
                summary_type=args.summary_type
            )
            
            if not results["success"]:
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()