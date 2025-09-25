import google.generativeai as genai
import json
import datetime
from typing import List, Dict, Any, Optional
import config
from utils import clean_text, save_json_output

class QuizGenerator:
    def __init__(self):
        """Initialize the quiz generator with Gemini API"""
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
        
    def generate_quiz(self, 
                     text: str, 
                     num_questions: int = 10, 
                     difficulty: str = "medium",
                     question_types: List[str] = None) -> Dict[str, Any]:
        """
        Generate a quiz from the given text
        
        Args:
            text (str): Source text for quiz generation
            num_questions (int): Number of questions to generate
            difficulty (str): Difficulty level - 'easy', 'medium', 'hard'
            question_types (list): Types of questions to include
            
        Returns:
            dict: Quiz data with questions and metadata
        """
        try:
            if not text or len(text.strip()) < 100:
                raise ValueError("Text is too short to generate meaningful quiz questions")
            
            # Set default question types if not provided
            if question_types is None:
                question_types = ["multiple_choice", "true_false", "short_answer"]
            
            # Clean the text
            cleaned_text = clean_text(text)
            
            # Generate questions
            questions = self._generate_questions(cleaned_text, num_questions, difficulty, question_types)
            
            # Prepare quiz data
            quiz_data = {
                "quiz_metadata": {
                    "title": "Document Quiz",
                    "description": f"Quiz generated from document content",
                    "num_questions": len(questions),
                    "difficulty": difficulty,
                    "question_types": question_types,
                    "generated_at": datetime.datetime.now().isoformat(),
                    "source_text_length": len(text),
                    "estimated_time": self._estimate_completion_time(len(questions), difficulty)
                },
                "questions": questions,
                "instructions": self._generate_instructions(difficulty),
                "scoring": self._generate_scoring_guide(len(questions))
            }
            
            return quiz_data
            
        except Exception as e:
            raise Exception(f"Error generating quiz: {str(e)}")
    
    def _generate_questions(self, text: str, num_questions: int, difficulty: str, question_types: List[str]) -> List[Dict[str, Any]]:
        """Generate quiz questions based on the text"""
        questions = []
        
        # Calculate distribution of question types
        distribution = self._calculate_question_distribution(num_questions, question_types)
        
        for question_type, count in distribution.items():
            if count > 0:
                type_questions = self._generate_questions_by_type(text, question_type, count, difficulty)
                questions.extend(type_questions)
        
        # Shuffle questions randomly
        import random
        random.shuffle(questions)
        
        # Number the questions
        for i, question in enumerate(questions, 1):
            question["question_number"] = i
        
        return questions
    
    def _generate_questions_by_type(self, text: str, question_type: str, count: int, difficulty: str) -> List[Dict[str, Any]]:
        """Generate questions of a specific type"""
        if question_type == "multiple_choice":
            return self._generate_multiple_choice(text, count, difficulty)
        elif question_type == "true_false":
            return self._generate_true_false(text, count, difficulty)
        elif question_type == "short_answer":
            return self._generate_short_answer(text, count, difficulty)
        elif question_type == "fill_in_blank":
            return self._generate_fill_in_blank(text, count, difficulty)
        else:
            return []
    
    def _generate_multiple_choice(self, text: str, count: int, difficulty: str) -> List[Dict[str, Any]]:
        """Generate multiple choice questions"""
        prompt = f"""
        Based on the following text, create {count} multiple choice questions with {difficulty} difficulty.
        
        For each question, provide:
        1. A clear question
        2. Four answer options (A, B, C, D)
        3. The correct answer letter
        4. A brief explanation for the correct answer
        
        Format as JSON array with this structure:
        [
          {{
            "question": "Question text here?",
            "options": {{
              "A": "Option A text",
              "B": "Option B text", 
              "C": "Option C text",
              "D": "Option D text"
            }},
            "correct_answer": "A",
            "explanation": "Explanation of why this is correct",
            "type": "multiple_choice",
            "difficulty": "{difficulty}"
          }}
        ]
        
        Text:
        {text}
        """
        
        try:
            response = self._call_gemini_api(prompt)
            cleaned_response = self._clean_json_response(response)
            questions = json.loads(cleaned_response)
            return questions if isinstance(questions, list) else []
        except Exception as e:
            # Fallback if JSON parsing fails
            return self._generate_fallback_multiple_choice(text, count, difficulty)
    
    def _generate_true_false(self, text: str, count: int, difficulty: str) -> List[Dict[str, Any]]:
        """Generate true/false questions"""
        prompt = f"""
        Based on the following text, create {count} true/false questions with {difficulty} difficulty.
        
        Format as JSON array with this structure:
        [
          {{
            "question": "Statement to evaluate as true or false",
            "correct_answer": true,
            "explanation": "Explanation of why this is true/false",
            "type": "true_false",
            "difficulty": "{difficulty}"
          }}
        ]
        
        Text:
        {text}
        """
        
        try:
            response = self._call_gemini_api(prompt)
            cleaned_response = self._clean_json_response(response)
            questions = json.loads(cleaned_response)
            return questions if isinstance(questions, list) else []
        except:
            return self._generate_fallback_true_false(text, count, difficulty)
    
    def _generate_short_answer(self, text: str, count: int, difficulty: str) -> List[Dict[str, Any]]:
        """Generate short answer questions"""
        prompt = f"""
        Based on the following text, create {count} short answer questions with {difficulty} difficulty.
        These should require 1-3 sentence responses.
        
        Format as JSON array with this structure:
        [
          {{
            "question": "Question requiring a short answer?",
            "sample_answer": "Example of a good answer",
            "key_points": ["key point 1", "key point 2"],
            "type": "short_answer",
            "difficulty": "{difficulty}"
          }}
        ]
        
        Text:
        {text}
        """
        
        try:
            response = self._call_gemini_api(prompt)
            cleaned_response = self._clean_json_response(response)
            questions = json.loads(cleaned_response)
            return questions if isinstance(questions, list) else []
        except:
            return self._generate_fallback_short_answer(text, count, difficulty)
    
    def _generate_fill_in_blank(self, text: str, count: int, difficulty: str) -> List[Dict[str, Any]]:
        """Generate fill-in-the-blank questions"""
        prompt = f"""
        Based on the following text, create {count} fill-in-the-blank questions with {difficulty} difficulty.
        
        Format as JSON array with this structure:
        [
          {{
            "question": "Sentence with _____ representing the blank to fill",
            "correct_answer": "word or phrase that fills the blank",
            "context": "Additional context if needed",
            "type": "fill_in_blank",
            "difficulty": "{difficulty}"
          }}
        ]
        
        Text:
        {text}
        """
        
        try:
            response = self._call_gemini_api(prompt)
            cleaned_response = self._clean_json_response(response)
            questions = json.loads(cleaned_response)
            return questions if isinstance(questions, list) else []
        except:
            return []
    
    def _clean_json_response(self, response: str) -> str:
        """Clean API response by removing markdown code block formatting"""
        cleaned_response = response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]  # Remove ```json
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]  # Remove ```
        return cleaned_response.strip()
    
    def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API with error handling"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")
    
    def _calculate_question_distribution(self, total_questions: int, question_types: List[str]) -> Dict[str, int]:
        """Calculate how many questions of each type to generate"""
        distribution = {}
        questions_per_type = total_questions // len(question_types)
        remaining = total_questions % len(question_types)
        
        for i, q_type in enumerate(question_types):
            distribution[q_type] = questions_per_type
            if i < remaining:
                distribution[q_type] += 1
        
        return distribution
    
    def _estimate_completion_time(self, num_questions: int, difficulty: str) -> str:
        """Estimate time to complete the quiz"""
        base_time_per_question = {
            "easy": 1,      # 1 minute per question
            "medium": 1.5,  # 1.5 minutes per question
            "hard": 2       # 2 minutes per question
        }
        
        total_minutes = int(num_questions * base_time_per_question.get(difficulty, 1.5))
        return f"{total_minutes} minutes"
    
    def _generate_instructions(self, difficulty: str) -> str:
        """Generate quiz instructions"""
        base_instructions = "Please read each question carefully and select the best answer."
        
        if difficulty == "easy":
            return f"{base_instructions} This is an easy-level quiz focusing on basic comprehension."
        elif difficulty == "hard":
            return f"{base_instructions} This is an advanced quiz requiring deep understanding and analysis."
        else:
            return f"{base_instructions} This quiz tests your understanding of the material."
    
    def _generate_scoring_guide(self, num_questions: int) -> Dict[str, Any]:
        """Generate scoring guide for the quiz"""
        return {
            "total_points": num_questions,
            "points_per_question": 1,
            "grading_scale": {
                "A": "90-100%",
                "B": "80-89%",
                "C": "70-79%",
                "D": "60-69%",
                "F": "Below 60%"
            }
        }
    
    def save_quiz(self, quiz_data: Dict[str, Any], filename: str) -> str:
        """Save quiz to file"""
        try:
            return save_json_output(quiz_data, f"quiz_{filename}", "quiz")
        except Exception as e:
            raise Exception(f"Error saving quiz: {str(e)}")
    
    def generate_quiz_from_file(self, file_path: str, num_questions: int = 10, difficulty: str = "medium") -> Dict[str, Any]:
        """Generate quiz directly from file"""
        from utils import extract_text_from_file
        
        try:
            # Extract text from file
            text = extract_text_from_file(file_path)
            if not text:
                raise ValueError("Could not extract text from file")
            
            # Generate quiz
            quiz_data = self.generate_quiz(text, num_questions, difficulty)
            
            # Add file metadata
            import os
            quiz_data["quiz_metadata"]["source_file"] = os.path.basename(file_path)
            quiz_data["quiz_metadata"]["file_path"] = file_path
            
            return quiz_data
            
        except Exception as e:
            raise Exception(f"Error processing file {file_path}: {str(e)}")
    
    # Fallback methods for when JSON parsing fails
    def _generate_fallback_multiple_choice(self, text: str, count: int, difficulty: str) -> List[Dict[str, Any]]:
        """Fallback method for multiple choice questions"""
        # Simple fallback implementation
        return []
    
    def _generate_fallback_true_false(self, text: str, count: int, difficulty: str) -> List[Dict[str, Any]]:
        """Fallback method for true/false questions"""
        return []
    
    def _generate_fallback_short_answer(self, text: str, count: int, difficulty: str) -> List[Dict[str, Any]]:
        """Fallback method for short answer questions"""
        return []