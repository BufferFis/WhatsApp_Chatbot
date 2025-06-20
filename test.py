import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

def test_pneuma_bot():
    """Test all three key intents for Pneuma including new student benefits"""
    
    # Check if server is running
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code != 200:
            print("Bot server is not running. Start it with: python main.py")
            return
    except requests.exceptions.RequestException:
        print("Cannot connect to bot. Make sure it's running on port 8000")
        return
    
    print("Testing Pneuma WhatsApp FAQ Bot v0.1 with Student Benefits\n")
    
    #
    test_cases = [
        {
            "intent": "Points Maximization",
            "message": "How can I maximize my Chase Sapphire points for flights to Europe?"
        },
        {
            "intent": "Student Travel Benefits", 
            "message": "Do airlines offer student discounts and extra baggage for college students?"
        },
        {
            "intent": "Student Travel Benefits",
            "message": "Can I bring my guitar on a plane as a student? Any special policies?"
        },
        {
            "intent": "Points Transfer",
            "message": "My Amex points expire in 2 months, what should I do?"
        },
        {
            "intent": "Off-topic test",
            "message": "What's the weather like today?"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i} - {test_case['intent']}:")
        print(f"Q: {test_case['message']}")
        
        payload = {
            "From": "whatsapp:+1234567890",
            "Body": test_case['message'],
            "MessageSid": f"test_{i:03d}"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/webhook", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"Intent: {result['intent']} (confidence: {result['confidence']})")
                print(f"Response: {result['message']}\n")
                print("-" * 60 + "\n")
            else:
                print(f"❌ Error {response.status_code}: {response.text}\n")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}\n")

if __name__ == "__main__":
    test_pneuma_bot()
