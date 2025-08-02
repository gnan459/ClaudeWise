import google.generativeai as genai
import dotenv
import os
import json

# Load environment variables
dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set your Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini 2.5 Pro model
model = genai.GenerativeModel(model_name="gemini-2.5-pro")

def clean_json_response(raw):
    # Remove code block markers and any leading text before the first '{'
    raw = raw.strip()
    if raw.startswith("```"):
        # Remove code block markers
        raw = raw.split("```")[-2].strip() if "```" in raw else raw
    # Find the first '{' and last '}' to extract JSON
    start = raw.find('{')
    end = raw.rfind('}')
    if start != -1 and end != -1:
        raw = raw[start:end+1]
    return raw

def analyze_insurance_policy_from_clauses(simplified_clauses: list):
    clauses_text = "\n".join(simplified_clauses)
    prompt = f"""
You are an expert legal assistant. Read the following simplified insurance policy clauses and return ONLY valid JSON as specified below, with no explanations, markdown, or code blocks.
Return ONLY valid JSON. Do NOT include any explanations, markdown, or code blocks. If you do, your answer will be ignored.
Return in this format:
{{
  "rating": "x / 5",
  "benefits": ["..."],
  "drawbacks": ["..."]
}}

Simplified Clauses:
{clauses_text}
"""
    response = model.generate_content(prompt)
    raw = clean_json_response(response.text)
    try:
        result = json.loads(raw)
        return result["rating"], result["benefits"], result["drawbacks"]
    except Exception:
        # Optional: print raw for debugging
        # print("Gemini raw output:", raw)
        return "N/A", ["Failed to parse benefits"], ["Failed to parse drawbacks"]

def analyze_insurance_policy(text: str):
    """
    Analyze an insurance policy using the raw document text.
    Returns: rating, benefits, drawbacks
    """
    prompt = f"""
You are an expert legal assistant. Read the following insurance policy document and return ONLY valid JSON as specified below, with no explanations, markdown, or code blocks.
Return ONLY valid JSON. Do NOT include any explanations, markdown, or code blocks. If you do, your answer will be ignored.
Return in this format:
{{
  "rating": "x / 5",
  "benefits": ["..."],
  "drawbacks": ["..."]
}}

Document:
{text[:15000]}
"""
    response = model.generate_content(prompt)
    raw = clean_json_response(response.text)
    try:
        result = json.loads(raw)
        return result["rating"], result["benefits"], result["drawbacks"]
    except Exception:
        # Optional: print raw for debugging
        # print("Gemini raw output:", raw)
        return "N/A", ["Failed to parse benefits"], ["Failed to parse drawbacks"]

def classify_and_analyze(document_text: str, simplified_clauses: list = None):
    """
    Classifies the document and analyzes insurance policies.
    If simplified_clauses is provided and document is an insurance policy, uses clause-based analysis.
    """
    doc_type = classify_document(document_text)
    if doc_type.lower() == "insurance policy":
        if simplified_clauses:
            rating, benefits, drawbacks = analyze_insurance_policy_from_clauses(simplified_clauses)
        else:
            rating, benefits, drawbacks = analyze_insurance_policy(document_text)
        return {
            "type": doc_type,
            "analysis": {
                "rating": rating,
                "benefits": benefits,
                "drawbacks": drawbacks
            }
        }
    else:
        return {"type": doc_type}

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