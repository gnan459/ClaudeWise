# Install the Gemini API client
#!pip install -q google-generativeai

# Import required libraries
import google.generativeai as genai

# Configure your API key (get it from https://makersuite.google.com/app/apikey)
GOOGLE_API_KEY = "AIzaSyAz1IufdDxClKN3ni_HfdC24F2a4JjLNUg"
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini 2.5 Flash model
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# Sample complex clause to simplify
clause = """In the event that the user fails to comply with the terms and conditions set forth herein, 
the company reserves the right, without prior notice, to suspend or terminate the user’s access 
to the platform, notwithstanding any prior agreements."""

# Prompt for simplification
prompt = f"Simplify this legal clause into plain English:\n\n\"{clause}, just give one response.\""

# Generate the simplified version
response = model.generate_content(prompt)

# Print the simplified clause
print("Simplified Clause:\n", response.text)
