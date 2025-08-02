#Load documents of different formats (PDF, DOCX, TXT), extract raw text.
import os
import fitz  # PyMuPDF
import docx


def load_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")


def load_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])


def load_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def load_file(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    uploaded_file.seek(0)  # Ensure pointer is at start
    if ext == ".pdf":
        return load_pdf(uploaded_file)
    elif ext == ".docx":
        return load_docx(uploaded_file)
    elif ext == ".txt":
        return load_txt(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT.")
    
# Example usage:
# if __name__ == "__main__":
#     file_path = "D:/ClauseWise/example.pdf"  # Change to your file path
#     try:
#         text = load_file(file_path)
#         print("File loaded successfully. Text length:", len(text))
#         print(text[:500])  # Print first 500 characters
#     except Exception as e:
#         print("Error loading file:", str(e))
