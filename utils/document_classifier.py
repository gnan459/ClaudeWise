import google.generativeai as genai

# Set your Gemini API key
GOOGLE_API_KEY = "AIzaSyAz1IufdDxClKN3ni_HfdC24F2a4JjLNUg"
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini 1.5 Flash model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def classify_document(document_text: str) -> str:
    """
    Classifies the document type using Gemini API.
    Returns the most likely document type label.
    """
    prompt = f"""Analyze the following document content and classify the document type from among:
    ["Agreement", "Invoice", "Resume", "Policy Document", "Legal Notice", "Report", "Other"].

    Document:
    \"\"\"
    {document_text}
    \"\"\"

    Output only the most likely document type label.
    """
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, 'text') else str(response)