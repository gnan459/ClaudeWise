import google.generativeai as genai
import dotenv
import os
dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure your API key (get it from https://makersuite.google.com/app/apikey)

genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini 2.5 Flash model
model = genai.GenerativeModel(model_name="gemini-2.5-pro")

def simplify_clause(clause: str) -> str:
    """Simplifies a legal clause into plain English using Gemini API."""
    prompt = f"Simplify this legal clause into plain English:\n\n\"{clause}\". Just give one response."
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, 'text') else str(response)