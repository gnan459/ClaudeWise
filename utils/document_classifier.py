import google.generativeai as genai
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set your Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini 2.5 Pro model
model = genai.GenerativeModel(model_name="gemini-2.5-pro")

def classify_document(document_text: str) -> str:
    prompt = f"""Analyze the following document content and classify it into one of the following document types:

["Employment Contract", "Rental/Lease Agreement", "Non-Disclosure Agreement (NDA)", "Insurance Policy", "Service Agreement", "Invoice", "Resume", "Legal Notice", "Report", "Other"]

Document:
\"\"\"
{document_text}
\"\"\"

Output only the most likely document type label from the list above. Do not explain or elaborate—just return the label.
"""
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, 'text') else str(response)
