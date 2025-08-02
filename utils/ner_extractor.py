import google.generativeai as genai
import dotenv
import os
import json
import re
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions

# Load environment variables
dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
IBM_API_KEY = os.getenv("IBM_WATSON_API_KEY")
IBM_URL = os.getenv("IBM_WATSON_URL")

# Configure Gemini model
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel(model_name="gemini-2.5-pro")

# Configure IBM Watson NLU
ibm_authenticator = IAMAuthenticator(IBM_API_KEY)
ibm_nlu = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=ibm_authenticator
)
ibm_nlu.set_service_url(IBM_URL)

def extract_entities(document_text: str) -> dict:
    # Step 1: IBM Watson NER extraction
    try:
        ibm_response = ibm_nlu.analyze(
            text=document_text,
            features=Features(entities=EntitiesOptions(sentiment=False, emotion=False, limit=50))
        ).get_result()
        ibm_entities = ibm_response.get("entities", [])
    except Exception as e:
        ibm_entities = []
    
    # Organize IBM entities by type
    ibm_entity_dict = {}
    for ent in ibm_entities:
        ent_type = ent.get("type", "OTHER")
        ent_text = ent.get("text", "")
        ibm_entity_dict.setdefault(ent_type, []).append(ent_text)

    # Step 2: Enhance with Gemini
    prompt = f"""
You are a document analysis assistant.

Given the following named entities extracted from IBM Watson, enhance and organize them by type using these categories (only if present):
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

IBM Watson Entities:
{json.dumps(ibm_entity_dict, ensure_ascii=False, indent=2)}

Document:
\"\"\"
{document_text}
\"\"\"
"""
    response = gemini_model.generate_content(prompt)
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