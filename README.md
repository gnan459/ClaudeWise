# ClauseWise - Legal Document Analyzer

ClauseWise is an AI-powered legal document analyzer built with Streamlit. It leverages Google Gemini and IBM Watson NLU to classify documents, extract and simplify clauses, analyze insurance policies, and perform advanced named entity recognition (NER).

## Features

- **Document Classification:** Automatically identifies the type of legal document.
- **Clause Extraction:** Extracts key clauses from contracts and agreements.
- **Clause Simplification:** Simplifies complex legal clauses for easier understanding.
- **Insurance Policy Analysis:** Rates insurance policies and summarizes benefits/drawbacks.
- **Entity Extraction:** Uses IBM Watson NLU and Gemini to extract and enhance named entities.
- **RAG Chatbot:** Ask questions about your document using Gemini-powered retrieval-augmented generation.

## Setup

### Prerequisites

- Ubuntu 24.04.2 LTS (dev container)
- Python 3.10+
- Streamlit
- IBM Watson NLU API credentials
- Google Gemini API key

### Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd ClaudeWise
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Create a `.env` file in the root directory:
     ```
     GOOGLE_API_KEY=your_google_gemini_api_key
     IBM_WATSON_API_KEY=your_ibm_watson_api_key
     IBM_WATSON_URL=your_ibm_watson_service_url
     ```

## Usage

1. **Start the Streamlit app:**
   ```sh
   streamlit run app.py
   ```

2. **Open the app in your browser:**
   - The app will provide a local URL (e.g., `http://localhost:8501`)
   - On your dev container, you can use:
     ```sh
     $BROWSER http://localhost:8501
     ```

3. **Upload a legal document** (`.pdf`, `.docx`, `.txt`) and select desired features from the sidebar.

## File Structure

```
ClaudeWise/
├── app.py
├── requirements.txt
├── .env
├── utils/
│   ├── file_loader.py
│   ├── clause_extractor.py
│   ├── clause_simplifier.py
│   ├── document_classifier.py
│   └── ner_extractor.py
```

## Notes

- IBM Watson NLU is used for initial entity extraction; Gemini enhances and organizes entities.
- Insurance policy analysis uses clause simplification for more accurate ratings.
- All AI calls are handled securely using API keys from environment variables.

## License

MIT License

---

**For any issues or feature requests, please open an issue
