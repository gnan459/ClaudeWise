import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Set up the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-2.5-pro")


def extract_clauses(document_text):
    """Extract clauses from a legal document using Gemini Pro."""
    prompt = f"""
You are a legal assistant AI. Extract individual clauses from the following legal document and present each clause as a separate numbered item.

Text:
\"\"\"
{document_text}
\"\"\"
make the headings bold and use markdown formatting for clarity.
Output format:
**Clause 1:** ...
**Clause 2:** ...
...
"""
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        # Optional: split by "Clause X:" to get structured list
        clauses = result.split("Clause ")[1:]  # remove leading text
        clauses = [f"Clause {clause.strip()}" for clause in clauses]
        return clauses
    except Exception as e:
        print("[Gemini] Error extracting clauses:", e)
        return ["Error extracting clauses."]

# # Example Usage
# if _name_ == "_main_":
#     text = """
#     This Agreement is made effective as of the date signed below.
#     The Parties agree to the terms set forth herein.
#     Confidentiality must be maintained at all times.
#     The recipient shall not disclose any confidential information to third parties.
#     This Agreement shall be governed by the laws of the State of California.
#     """
#     clauses = extract_clauses(text)
#     for clause in clauses:
#         print(clause)