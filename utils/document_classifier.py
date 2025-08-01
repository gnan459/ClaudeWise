# utils/document_classifier.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

WATSON_API_KEY = os.getenv("WATSON_API_KEY")
WATSON_PROJECT_ID = os.getenv("WATSON_PROJECT_ID")
WATSON_GRANITE_URL = os.getenv("WATSON_GRANITE_URL")
MODEL_ID = os.getenv("MODEL_ID", "granite-13b-instruct")


def classify_document(document_text: str) -> str:
    prompt = (
        f"Classify the following legal document into one of these types: "
        f"NDA, Lease Agreement, Employment Contract, Service Agreement.\n\n"
        f"Document:\n{document_text}\n\nClassification:"
    )

    headers = {
        "Authorization": f"Bearer {WATSON_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model_id": MODEL_ID,
        "project_id": WATSON_PROJECT_ID,
        "inputs": [prompt]
    }

    try:
        response = requests.post(WATSON_GRANITE_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if "results" in result:
            classification = result["results"][0]["generated_text"].strip()
            return classification
        else:
            return "Unknown (No results)"

    except Exception as e:
        print("Error:", e)
        return "Unknown (Error)"

# Example usage
if __name__ == "__main__":
    sample_doc = """
    This Lease Agreement is made and entered into this 1st day of January, 2024, by and between [Landlord Name] (hereinafter referred to as "Landlord") and [Tenant Name] (hereinafter referred to as "Tenant").
    """

    result = classify_document(sample_doc)
    print("Predicted Document Type:", result)
