Whatsapp FAQ Bot v0.1

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
	- `-   elif any(keyword in message_lower for keyword in [“list”, “of”, “keywords”]):
return “Intent”, “confidence”` 

2. Add Intent Prompts in `get_pneuma_prompt()`:
	 - In the prompts dictionary add new key value pair like given below
	 - `“Intent”: f”””{base_system}
Focus on: intent, describe the intent here with telling what to focus on.
User question: {user_message}””” `

3. Testing the new Intent
	- Add in the following format to test.py: 
	-  `
“Intent”: “your intent here”,
“message”: “your test message here”
} ` 

### Customisation for responses

Modify the `base_system` prompt in `get_pneuma_prompt()` to adjust:
 - Voice and tone
 -   Response length
 -   Specific knowledge areas
 -   Brand personality

## Limitations

-   No booking or payment capability
    
-   AI-generated responses should be verified by the company once
    
-   No ability to contact a human helper yet but easily addable as confidence system is implemented as a template now.
    
-   FastAPI handles multiple requests but Gemini API has a rate limit, causing issues for concurrent users
    
-   Keyword bases intent classification may need to be replaced by a ML classifier for complex queries
    
-   Bot provides only general advice, no personalised advice.
    
-   No authentication method or logging.

## Future Enhancements
 
1.  ML based classification: Replace keyword matching with a ML model
    
2.  Context awareness: Conversation memory for the bot
    
3.  User personalization: Account linking
    
4.  Real Whatsapp integration: Business API integration with webhook validation
    
5. Multilingual: Supports multiple languages
