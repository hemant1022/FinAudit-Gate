import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def ask_llm(system_prompt: str, user_prompt: str, model: str = "gemini-2.5-flash") -> str:
    """
    Generic wrapper to call Gemini API using the google-genai SDK.
    Requires GEMINI_API_KEY to be set in environment or .env file.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: GEMINI_API_KEY not found in environment."
        
    client = genai.Client(api_key=api_key)
    
    config = genai.types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.2
    )
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=config
        )
        return response.text
    except Exception as e:
        return f"ERROR calling Gemini: {e}"
