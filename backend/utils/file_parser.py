"""File parsing utilities for resumes."""

import io
import fitz  # PyMuPDF
from docx import Document


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    text = ""
    doc = Document(io.BytesIO(file_bytes))
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text.strip()


def parse_resume(filename: str, file_bytes: bytes) -> str:
    """Parse resume based on file extension."""
    
    filename_lower = filename.lower()
    
    if filename_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    
    elif filename_lower.endswith((".docx", ".doc")):
        # Note: .doc parsing via python-docx is limited, but keeping for compatibility
        return extract_text_from_docx(file_bytes)
        
    else:
        # Fallback for .txt or other formats
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return ""
