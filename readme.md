# Pneuma Whatsapp FAQ Bot v0.1

A prototype chatbot for travel reward queries. Powered by Google's Gemini AI and 

## Project Structure

```
pneuma-whatsapp-bot/  
├── main.py # FastAPI application with intent classification  
├── config.py # Configuration management (.env file loading)  
├── test.py # Automated tests  
├── chat_now.py # Interactive chat  
├── .env.example # Environment variables example file  
├── .gitignore # Git ignore rules
├── requirements.txt # Required dependencies  
└── README.md # This file
```

## Setup

### Prerequisites 
- Python 3.8+ (tested with Python 3.13)
- Gemini API key
- Requirements.txt contains rest of the requirements

### Installation Steps

1. Clone the project then: `cd WhatsApp_Chatbot`
2. Activate your virtual environment:  `source ~/path/to/myenv/bin/activate # Linux/macOS` 
	b. For Windows: 
3. Install dependencies : `pip install -r requirements.txt`
4. Set up environmental variables (API key)
5. Create .env file while following the example of example env file in the directory.


## Running the Bot

### Starting the server
- the server will start on 'http://localhost:8000' when ran with `python main.py`
- Run chat_now file to talk to the bot using `python chat_now.py`

### Testing the bot
- Automated test are setup in `test.py` which can be modified whenever needed, once server is running just run `python test.py` to run the automated tests.

## Extending the bot
### Adding a new Intent
1. Update intent Classification in `main.py`:
	- Example, adding a new intent with using a elif statement.
	- `elif any(keyword in message_lower for keyword in [  
"hotel", "accommodation", "stay", "overnight"  
]):  
return "hotel_bookings", "high"` 

2. Add Intent Prompts in `get_pneuma_prompt()`:
	 - In the prompts dictionary add new key value pair like given below
	 - `"hotel_bookings": f"""{base_system}
Focus on: Hotel loyalty programs, point values, status benefits.  
Include specific examples when possible.
User question: {user_message}""" `

3. Testing the new Intent
	- Add to test.py ` {  
"intent": "Hotel Bookings",  
"message": "How do I book hotels with Marriott points?"  
} ` 

### Customisation for responses

Modify the `base_system` prompt in `get_pneuma_prompt()` to adjust:
 - Voice and tone
 -   Response length
 -   Specific knowledge areas
 -   Brand personality

## Limitations

- Cannot access real-time award inventory (would need airline API integration) 
- Limited to pre-trained FAQ patterns (expansion requires code updates) 
- No transaction processing capability (compliance considerations) 
- Responses are AI-generated and should be verified for accuracy
 
	
