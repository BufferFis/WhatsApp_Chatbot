import requests
import json
import sys
import os
from datetime import datetime

BOT_URL = "http://localhost:8000/webhook"
HEALTH_URL = "http://localhost:8000/health"
CHAT_HISTORY_FILE = "pneuma_chat_history.txt"

class PneumaChat:
    def __init__(self):
        self.chat_history = []
        
    def save_chat_history(self, user_message, bot_response, intent):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(CHAT_HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}] User: {user_message}\n")
            f.write(f"[{timestamp}] Bot ({intent}): {bot_response}\n")
    
    def check_bot_status(self):
        try:
            response = requests.get(HEALTH_URL, timeout=5)
            if response.status_code == 200:
                bot_info = response.json()
                print(f"Connected to {bot_info.get('model', 'Pneuma Bot')} v{bot_info.get('version', '0.1')}")
                return True
            else:
                print(f"Bot server returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            print("Cannot connect to bot. Start server with: python main.py")
            return False
    
    def send_message(self, message):
        """Send message to bot"""
        payload = {
            "From": "chat_user",
            "Body": message,
            "MessageSid": f"chat_{len(self.chat_history):04d}"
        }
        
        try:
            response = requests.post(BOT_URL, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection failed: {str(e)}"}
    
    def print_welcome(self):
        """Print styled welcome message"""
        print("\n" + "="*70)
        print("PNEUMA TRAVEL REWARDS ASSISTANT")
        print("="*70)
        print("Maximize your points • tudent benefits • Transfer strategies")
        print("-"*70)
        print("Commands: 'exit'/'quit' to end, 'help' for examples")
        print("="*70)
    
    def show_help(self):
        """Show example questions"""
        examples = [
            "How can I maximize my Chase Sapphire points?",
            "Do airlines offer student discounts?", 
            "Can I bring my guitar as carry-on?",
            "My points expire next month, what should I do?"
        ]
        
        print("\ntry asking:")
        for i, example in enumerate(examples, 1):
            print(f"   {i}. {example}")
        print()
    
    def start_chat(self):
        """Main chat interface"""
        if not self.check_bot_status():
            return
        
        self.print_welcome()
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                # Handle commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print(f"\nGoodbye! Chat saved to {CHAT_HISTORY_FILE}")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif not user_input:
                    continue
                
                # Send to bot
                print("Pneuma: ", end="", flush=True)
                response = self.send_message(user_input)
                
                if "error" in response:
                    print(f"{response['error']}")
                    continue
                
                # Process response
                bot_message = response.get('message', 'No response')
                intent = response.get('intent', 'general')
                confidence = response.get('confidence', 'unknown')
                
                print(bot_message)
                
                # Show intent detection
                if intent != 'general':
                    intent_display = intent.replace('_', ' ').title()
                    print(f"  Intent: {intent_display} ({confidence} confidence)")
                
                # Save to history
                self.save_chat_history(user_input, bot_message, intent)
                self.chat_history.append({
                    'user': user_input,
                    'bot': bot_message,
                    'intent': intent
                })
                
            except KeyboardInterrupt:
                print(f"\nChat ended. History saved to {CHAT_HISTORY_FILE}")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")

if __name__ == "__main__":
    chat = PneumaChat()
    chat.start_chat()
