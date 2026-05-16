import os
import PyPDF2
from docx import Document

def read_pdf(file_path):
    """Read and extract text from a PDF file"""
    try:
        path = os.path.expanduser(file_path)
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        if not text.strip():
            return "The PDF appears to be empty or scanned with no extractable text."
        return text[:3000]
    except Exception as e:
        return f"Could not read PDF: {str(e)}"

def read_docx(file_path):
    """Read and extract text from a Word document"""
    try:
        path = os.path.expanduser(file_path)
        doc = Document(path)
        text = "\n".join([para.text for para in doc.paragraphs])
        if not text.strip():
            return "The document appears to be empty."
        return text[:3000]
    except Exception as e:
        return f"Could not read document: {str(e)}"

def read_text_file(file_path):
    """Read a plain text file"""
    try:
        path = os.path.expanduser(file_path)
        with open(path, 'r') as f:
            text = f.read()
        if not text.strip():
            return "The file appears to be empty."
        return text[:3000]
    except Exception as e:
        return f"Could not read file: {str(e)}"

def read_file(file_path):
    """Auto detect file type and read it"""
    file_path = file_path.strip()
    if file_path.endswith('.pdf'):
        return read_pdf(file_path)
    elif file_path.endswith('.docx'):
        return read_docx(file_path)
    else:
        return read_text_file(file_path)

def list_downloads():
    """List files in Downloads folder"""
    try:
        path = os.path.expanduser("~/Downloads")
        files = os.listdir(path)
        if not files:
            return "Your Downloads folder is empty."
        return "Files in your Downloads folder: " + ", ".join(files[:15])
    except Exception as e:
        return f"Could not list downloads: {str(e)}"
