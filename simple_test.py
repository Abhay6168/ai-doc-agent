#!/usr/bin/env python3
"""
Simple test to verify API key works for both summarization and quiz generation
(without voice input dependencies)
"""

import sys
import os

# Add src to path  
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_api_simple():
    """Simple API test without voice dependencies"""
    
    try:
        # Test basic imports and API key
        import config
        print("🔑 API Key configured:", config.GEMINI_API_KEY[:20] + "...")
        print("🤖 Model:", config.MODEL_NAME)
        
        # Test Google GenAI import
        import google.generativeai as genai
        print("✅ Google GenerativeAI library imported successfully")
        
        # Configure API
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel(config.MODEL_NAME)
        print("✅ API configured successfully")
        
        # Test simple API call
        sample_text = "Artificial Intelligence is transforming many industries."
        prompt = f"Summarize this text in one sentence: {sample_text}"
        
        response = model.generate_content(prompt)
        print("✅ API call successful!")
        print(f"📋 Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Simple API Test")
    print("=" * 40)
    success = test_api_simple()
    
    if success:
        print("\n🎉 SUCCESS: Your API key is working!")
        print("✅ Both summarization and quiz generation will use this API key")
    else:
        print("\n❌ FAILED: Please check your API key")