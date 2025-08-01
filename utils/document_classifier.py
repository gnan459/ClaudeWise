# Install Gemini client
#pip install -q google-generativeai

# Import libraries
import google.generativeai as genai

# Set your Gemini API key
GOOGLE_API_KEY = "AIzaSyAz1IufdDxClKN3ni_HfdC24F2a4JjLNUg"
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini 1.5 Flash model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Sample document content (replace with any actual doc text)
document_text = """
This agreement is made between ABC Corporation and John Doe for the licensing of intellectual property
related to the ABC software suite. The licensee agrees to pay a fee of $10,000 per annum...
"""

# Prompt to classify the document type
prompt = f"""Analyze the following document content and classify the document type from among:
["Agreement", "Invoice", "Resume", "Policy Document", "Legal Notice", "Report", "Other"].

Document:
\"\"\"
{document_text}
\"\"\"

Output only the most likely document type label.
"""

# Generate response
response = model.generate_content(prompt)

# Print predicted document type
print("Predicted Document Type:", response.text.strip())
