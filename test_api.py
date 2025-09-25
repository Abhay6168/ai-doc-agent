#!/usr/bin/env python3
"""
Test script to verify API key is working for both summarization and quiz generation
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import config
from summarizer import DocumentSummarizer
from quiz_generator import QuizGenerator

def test_api_connection():
    """Test if API key works for both components"""
    
    sample_text = """
    Artificial Intelligence (AI) is a rapidly growing field in computer science. 
    AI systems can perform tasks that typically require human intelligence, such as 
    visual perception, speech recognition, decision-making, and language translation. 
    Machine learning is a subset of AI that enables computers to learn and improve 
    from experience without being explicitly programmed. Deep learning, a subset 
    of machine learning, uses neural networks with multiple layers to model and 
    understand complex patterns in data.
    """
    
    print("🧪 Testing API Connection...")
    print(f"📋 API Key: {config.GEMINI_API_KEY[:20]}...")
    print(f"🤖 Model: {config.MODEL_NAME}")
    print("-" * 50)
    
    try:
        # Test Summarizer
        print("📄 Testing Summarizer...")
        summarizer = DocumentSummarizer()
        summary_result = summarizer.generate_summary(sample_text, "brief")
        print("✅ Summarizer API call successful!")
        print(f"📊 Summary length: {len(summary_result['summary'])} characters")
        
        # Test Quiz Generator  
        print("\n📝 Testing Quiz Generator...")
        quiz_generator = QuizGenerator()
        quiz_result = quiz_generator.generate_quiz(sample_text, 3, "medium")
        print("✅ Quiz Generator API call successful!")
        print(f"📊 Questions generated: {len(quiz_result['questions'])}")
        
        print("\n🎉 SUCCESS: Both components are using your API key correctly!")
        print("\n📋 Summary Preview:")
        print(summary_result['summary'][:200] + "...")
        
        print("\n📋 Quiz Preview:")
        if quiz_result['questions']:
            q1 = quiz_result['questions'][0]
            print(f"Q1: {q1.get('question', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: API call failed - {str(e)}")
        print("\n💡 Possible issues:")
        print("   1. Invalid API key")
        print("   2. API quota exceeded")
        print("   3. Network connection issue")
        print("   4. Missing dependencies")
        return False

if __name__ == "__main__":
    test_api_connection()