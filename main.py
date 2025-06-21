from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from config import load_config


config = load_config()

# Initialize FastAPI app
app = FastAPI(
    title="Pneuma WhatsApp FAQ Bot", 
    version="0.1",
    description="Chatbot for Pneuma"
)

# Configure Gemini
genai.configure(api_key=config['api_key'])
model = genai.GenerativeModel(config['model'])

class WhatsAppMessage(BaseModel):
    From: str
    Body: str
    MessageSid: str

class BotResponse(BaseModel):
    message: str
    intent: str
    confidence: str

def classify_intent(message: str) -> tuple[str, str]:
    """Classify user intent and return confidence level"""
    message_lower = message.lower()
    
    # Intent 1: Points Maximization 
    if any(keyword in message_lower for keyword in [
        "maximize", "best value", "worth", "optimize", "sweet spot", 
        "most out of", "strategic", "credit card", "transfer ratio",
        "points transfer", "airline miles", "redemption", "business class",
        "first class", "economy class", "award booking", "points redemption",
        "points strategy", "points value", "points worth", "points maximization",
        "points optimization", "points earning", "points usage", "points strategy",
        "points transfer ratio", "points earning strategy", "points usage strategy",
    ]):
        return "points_maximization", "high"
    
    # Intent 2: Student Travel Benefits
    elif any(keyword in message_lower for keyword in [
        "student", "student discount", "extra baggage", "student fare", "college", "university",
        "extra luggage", "student id", "school", "education", "student benefits",
        "student travel", "student airfare", "student discount airfare",
        "student travel benefits", "student discounts", "student fares",
    ]):
        return "student_travel_benefits", "high"
    
    # Intent 3: Points Transfer & Expiration  
    elif any(keyword in message_lower for keyword in [
        "transfer", "expir", "expire", "ratio", "convert", 
        "move points", "about to lose", "dying"
    ]):
        return "points_transfer", "high"
    
    else:
        return "general", "low"

def get_pneuma_prompt(intent: str, user_message: str) -> str:
    
    base_system = """You are Pneuma's travel rewards assistant. Help users with travel bookings and maximize their benefits.

    Voice & Tone:
    - Plain English, data-backed responses
    - Light wit, never snark
    - No buzzwords like "revolutionize" 
    - Concise but helpful (under 100 words)
    - Focus on actionable advice"""

    intent_prompts = {
        "points_maximization": f"""{base_system}

        Focus on: Transfer ratios, sweet spot redemptions, strategic timing advice.
        Include specific examples like "Chase points transfer 1:1 to United - 70k points for business class to Europe."

        User question: {user_message}""",

        "student_travel_benefits": f"""{base_system}

        Focus on: Student discounts, extra baggage allowances, student fares.
        Include specific examples from airlines like Emirates (10% off + 10kg extra), Air India (20kg extra + discounted price), Singapore Airlines (10% discount), Indigo (10Kgs extra + discounted price + musical instrument).
        Mention verification requirements (student ID, enrollment letter).

        User question: {user_message}""",

        "points_transfer": f"""{base_system}

        Focus on: Transfer partners, expiration rescue strategies, timing best practices.
        Include specific programs like Aeroplan, Air India when relevant.

        User question: {user_message}""",

        "general": f"""{base_system}

        The user's question isn't clearly about travel rewards. Politely redirect them to your expertise areas:
        1. Points maximization strategies
        2. Student travel benefits and discounts
        3. Points transfers and expiration

        User question: {user_message}"""
    }
    
    return intent_prompts.get(intent, intent_prompts["general"])

async def get_gemini_response(prompt: str) -> str:
    """Get response from Gemini API"""
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=config['max_tokens'],
                temperature=config['temperature']
            )
        )
        return response.text.strip()
    except Exception as e:
        return f"I'm having trouble processing that right now. Could you try rephrasing your travel question? (Error: {str(e)[:50]}...)"

@app.post("/webhook", response_model=BotResponse)
async def whatsapp_webhook(message: WhatsAppMessage):
    intent, confidence = classify_intent(message.Body)
    
    
    if confidence == "low":
        bot_response = """I can help with travel rewards! Please be more specific:
        
        1) Points maximization strategies
        2) Student travel benefits  
        3) Points transfers & expiration
        
        What would you like to know about?"""
    else:
        prompt = get_pneuma_prompt(intent, message.Body)
        bot_response = await get_gemini_response(prompt)
    
    return BotResponse(
        message=bot_response,
        intent=intent, 
        confidence=confidence
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "model": config['model'],
        "version": "0.1"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Pneuma WhatsApp FAQ Bot v0.1 - Powered by Gemini",
        "intents": ["points_maximization", "student_travel_benefits", "points_transfer"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
