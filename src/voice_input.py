import speech_recognition as sr
import time
from typing import Optional, Dict, Any
import config

class VoiceInputHandler:
    def __init__(self):
        """Initialize voice input handler"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        self._calibrate_microphone()
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            print("Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone calibrated successfully!")
        except Exception as e:
            print(f"Warning: Could not calibrate microphone: {str(e)}")
    
    def listen_for_command(self, timeout: int = 10, phrase_time_limit: int = 5) -> Optional[str]:
        """
        Listen for voice input and convert to text
        
        Args:
            timeout (int): Seconds to wait for speech to start
            phrase_time_limit (int): Maximum seconds for each phrase
            
        Returns:
            str: Transcribed text or None if failed
        """
        try:
            print("Listening for voice input...")
            
            with self.microphone as source:
                # Listen for audio input
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            print("Processing speech...")
            
            # Use Google's speech recognition
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error during voice input: {str(e)}")
            return None
    
    def listen_continuously(self, callback_function, stop_phrase: str = "stop listening"):
        """
        Listen continuously for voice commands
        
        Args:
            callback_function: Function to call when speech is recognized
            stop_phrase: Phrase to stop continuous listening
        """
        print(f"Starting continuous listening... Say '{stop_phrase}' to stop.")
        
        while True:
            try:
                text = self.listen_for_command(timeout=1, phrase_time_limit=3)
                
                if text:
                    if stop_phrase.lower() in text.lower():
                        print("Stopping continuous listening...")
                        break
                    
                    # Call the callback function with the recognized text
                    callback_function(text)
                
                time.sleep(0.1)  # Small delay to prevent overwhelming
                
            except KeyboardInterrupt:
                print("\nStopped by user")
                break
            except Exception as e:
                print(f"Error in continuous listening: {str(e)}")
                time.sleep(1)  # Wait before retrying
    
    def get_voice_parameters(self) -> Optional[Dict[str, Any]]:
        """
        Get quiz/summary parameters through voice input
        
        Returns:
            dict: Parameters for quiz/summary generation
        """
        parameters = {}
        
        try:
            # Get number of questions for quiz
            print("How many questions would you like in the quiz? (Say a number)")
            while True:
                text = self.listen_for_command()
                if text:
                    # Extract number from text
                    num_questions = self._extract_number(text)
                    if num_questions and 1 <= num_questions <= 50:
                        parameters['num_questions'] = num_questions
                        print(f"Set number of questions to: {num_questions}")
                        break
                    else:
                        print("Please say a number between 1 and 50")
                else:
                    print("Please try again")
            
            # Get difficulty level
            print("What difficulty level? (Say: easy, medium, or hard)")
            while True:
                text = self.listen_for_command()
                if text:
                    difficulty = self._extract_difficulty(text.lower())
                    if difficulty:
                        parameters['difficulty'] = difficulty
                        print(f"Set difficulty to: {difficulty}")
                        break
                    else:
                        print("Please say: easy, medium, or hard")
                else:
                    print("Please try again")
            
            # Get summary type
            print("What type of summary? (Say: brief, comprehensive, or detailed)")
            while True:
                text = self.listen_for_command()
                if text:
                    summary_type = self._extract_summary_type(text.lower())
                    if summary_type:
                        parameters['summary_type'] = summary_type
                        print(f"Set summary type to: {summary_type}")
                        break
                    else:
                        print("Please say: brief, comprehensive, or detailed")
                else:
                    print("Please try again")
            
            return parameters
            
        except Exception as e:
            print(f"Error getting voice parameters: {str(e)}")
            return None
    
    def _extract_number(self, text: str) -> Optional[int]:
        """Extract number from text"""
        import re
        
        # Common number words
        number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
            'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20
        }
        
        # Look for digits
        digits = re.findall(r'\d+', text)
        if digits:
            return int(digits[0])
        
        # Look for number words
        words = text.lower().split()
        for word in words:
            if word in number_words:
                return number_words[word]
        
        return None
    
    def _extract_difficulty(self, text: str) -> Optional[str]:
        """Extract difficulty level from text"""
        if 'easy' in text:
            return 'easy'
        elif 'medium' in text:
            return 'medium'
        elif 'hard' in text or 'difficult' in text:
            return 'hard'
        return None
    
    def _extract_summary_type(self, text: str) -> Optional[str]:
        """Extract summary type from text"""
        if 'brief' in text or 'short' in text:
            return 'brief'
        elif 'comprehensive' in text or 'complete' in text:
            return 'comprehensive'
        elif 'detailed' in text or 'long' in text:
            return 'detailed'
        return None
    
    def confirm_action(self, message: str) -> bool:
        """
        Get voice confirmation for an action
        
        Args:
            message (str): Message to speak/display
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        print(f"{message} (Say 'yes' or 'no')")
        
        while True:
            text = self.listen_for_command()
            if text:
                text_lower = text.lower()
                if 'yes' in text_lower or 'yeah' in text_lower or 'okay' in text_lower:
                    return True
                elif 'no' in text_lower or 'nope' in text_lower:
                    return False
                else:
                    print("Please say 'yes' or 'no'")
            else:
                print("Please try again")
    
    def test_microphone(self) -> bool:
        """Test if microphone is working properly"""
        try:
            print("Testing microphone... Please say something:")
            text = self.listen_for_command(timeout=5)
            
            if text:
                print(f"✓ Microphone test successful! You said: '{text}'")
                return True
            else:
                print("✗ Microphone test failed - no speech detected")
                return False
                
        except Exception as e:
            print(f"✗ Microphone test failed: {str(e)}")
            return False