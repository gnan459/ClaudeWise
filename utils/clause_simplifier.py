import google.generativeai as genai

# Configure your API key (get it from https://makersuite.google.com/app/apikey)
GOOGLE_API_KEY = "AIzaSyAz1IufdDxClKN3ni_HfdC24F2a4JjLNUg"
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini 2.5 Flash model
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

def simplify_clause(clause: str) -> str:
    """Simplifies a legal clause into plain English using Gemini API."""
    prompt = f"Simplify this legal clause into plain English:\n\n\"{clause}\". Just give one response."
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, 'text') else str(response)