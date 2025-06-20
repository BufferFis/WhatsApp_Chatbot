import os
import sys
from dotenv import load_dotenv # type: ignore

def load_config():
    """Load configuration from .env file"""
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found!")
        print("Please check your .env file or set the environment variable")
        print("Get your key from: https://ai.google.dev/gemini-api/docs/api-key")
        sys.exit(1)
    
    return {
        'api_key': api_key,
        'model': os.getenv('GEMINI_MODEL', 'gemini-1.5-flash'),
        'max_tokens': int(os.getenv('MAX_TOKENS', '150')),
        'temperature': float(os.getenv('TEMPERATURE', '0.7'))
    }
