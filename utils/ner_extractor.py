import google.generativeai as genai
import dotenv
import os
import json
import re

# Load environment variables
dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.5-pro")

def extract_entities(document_text: str) -> dict:
    prompt = f"""
You are a document analysis assistant.

Extract named entities from the document below and organize them by type using the following categories (only if present):
- PERSON
- ORGANIZATION
- LOCATION
- DATE
- MONEY
- PERCENT
- LAW
- GPE (Countries, Cities, States)
- PRODUCT
- EVENT
- OTHER

Return the result strictly as a valid JSON object. Do not include explanations or any extra text.

Document:
\"\"\"
{document_text}
\"\"\"
"""

    response = model.generate_content(prompt)
    raw_output = response.text if hasattr(response, "text") else str(response)

    try:
        # Try to isolate the first JSON-like object in the response
        json_match = re.search(r'\{[\s\S]*\}', raw_output)
        if json_match:
            cleaned_json = json_match.group(0)
            return json.loads(cleaned_json)
        else:
            return {"error": "No JSON object found", "raw_output": raw_output}
    except Exception as e:
        return {"error": str(e), "raw_output": raw_output}
