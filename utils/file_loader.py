#Load documents of different formats (PDF, DOCX, TXT), extract raw text.
import os
import fitz  # PyMuPDF
import docx


def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def load_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def load_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    elif ext == ".txt":
        return load_txt(file_path)
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
