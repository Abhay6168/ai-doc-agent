import google.generativeai as genai
from typing import Optional, Dict, Any, List
import config
from utils import chunk_text, clean_text, save_json_output
import datetime

class DocumentSummarizer:
    def __init__(self):
        """Initialize the summarizer with Gemini API"""
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
        
    def generate_summary(self, text: str, summary_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Generate summary from text
        
        Args:
            text (str): Input text to summarize
            summary_type (str): Type of summary - 'brief', 'comprehensive', 'detailed'
            
        Returns:
            dict: Summary data with metadata
        """
        try:
            if not text or len(text.strip()) < 50:
                raise ValueError("Text is too short to generate a meaningful summary")
            
            # Clean the text
            cleaned_text = clean_text(text)
            
            # Generate summary based on type
            if summary_type == "brief":
                summary = self._generate_brief_summary(cleaned_text)
            elif summary_type == "detailed":
                summary = self._generate_detailed_summary(cleaned_text)
            else:  # comprehensive
                summary = self._generate_comprehensive_summary(cleaned_text)
            
            # Prepare result
            result = {
                "summary": summary,
                "summary_type": summary_type,
                "original_length": len(text),
                "summary_length": len(summary),
                "compression_ratio": round(len(summary) / len(text), 2),
                "generated_at": datetime.datetime.now().isoformat(),
                "key_points": self._extract_key_points(cleaned_text),
                "word_count": len(summary.split())
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")
    
    def _generate_brief_summary(self, text: str) -> str:
        """Generate a brief summary"""
        prompt = f"""
        Create a brief summary of the following text. The summary should be concise and capture only the most essential points.
        Keep it under 200 words.
        
        Text to summarize:
        {text}
        
        Brief Summary:
        """
        
        return self._call_gemini_api(prompt)
    
    def _generate_comprehensive_summary(self, text: str) -> str:
        """Generate a comprehensive summary"""
        prompt = f"""
        Create a comprehensive summary of the following text. Include:
        - Main topics and themes
        - Key arguments or points
        - Important details and examples
        - Conclusions or outcomes
        
        Keep the summary between 300-800 words, well-structured and informative.
        
        Text to summarize:
        {text}
        
        Comprehensive Summary:
        """
        
        return self._call_gemini_api(prompt)
    
    def _generate_detailed_summary(self, text: str) -> str:
        """Generate a detailed summary"""
        prompt = f"""
        Create a detailed summary of the following text. This should be thorough and include:
        - All major points and sub-points
        - Supporting evidence and examples
        - Context and background information
        - Detailed explanations of complex concepts
        - Step-by-step processes if applicable
        
        The summary should be comprehensive and detailed, around 800-1200 words.
        
        Text to summarize:
        {text}
        
        Detailed Summary:
        """
        
        return self._call_gemini_api(prompt)
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from the text"""
        try:
            prompt = f"""
            Extract the 5-10 most important key points from the following text.
            Return them as a numbered list, each point should be concise but informative.
            
            Text:
            {text}
            
            Key Points:
            """
            
            response = self._call_gemini_api(prompt)
            # Parse the response into a list
            key_points = []
            for line in response.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    # Remove numbering/bullets and add to list
                    clean_point = line.lstrip('0123456789.-• ').strip()
                    if clean_point:
                        key_points.append(clean_point)
            
            return key_points[:10]  # Limit to 10 key points
            
        except Exception:
            return []
    
    def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API with error handling"""
        try:
            # Handle long texts by chunking
            if len(prompt) > 20000:
                # For very long texts, chunk and summarize
                text_start = prompt.find("Text to summarize:") + len("Text to summarize:")
                text_content = prompt[text_start:].strip()
                chunks = chunk_text(text_content, 3000)
                
                chunk_summaries = []
                for chunk in chunks:
                    chunk_prompt = prompt[:text_start] + chunk
                    response = self.model.generate_content(chunk_prompt)
                    chunk_summaries.append(response.text)
                
                # Combine chunk summaries
                combined_prompt = f"""
                Combine and synthesize the following summaries into one coherent summary:
                
                {' '.join(chunk_summaries)}
                
                Final Summary:
                """
                response = self.model.generate_content(combined_prompt)
                return response.text
            else:
                response = self.model.generate_content(prompt)
                return response.text
                
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")
    
    def save_summary(self, summary_data: Dict[str, Any], filename: str) -> str:
        """Save summary to file"""
        try:
            return save_json_output(summary_data, f"summary_{filename}", "summary")
        except Exception as e:
            raise Exception(f"Error saving summary: {str(e)}")
    
    def generate_summary_from_file(self, file_path: str, summary_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Generate summary directly from file
        
        Args:
            file_path (str): Path to the file
            summary_type (str): Type of summary
            
        Returns:
            dict: Summary data with file metadata
        """
        from utils import extract_text_from_file
        
        try:
            # Extract text from file
            text = extract_text_from_file(file_path)
            if not text:
                raise ValueError("Could not extract text from file")
            
            # Generate summary
            summary_data = self.generate_summary(text, summary_type)
            
            # Add file metadata
            import os
            summary_data["source_file"] = os.path.basename(file_path)
            summary_data["file_path"] = file_path
            summary_data["file_size"] = os.path.getsize(file_path)
            
            return summary_data
            
        except Exception as e:
            raise Exception(f"Error processing file {file_path}: {str(e)}")