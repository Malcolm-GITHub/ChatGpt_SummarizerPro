import os
from docx import Document

def read_file(uploaded_file):
    """Reads and returns the text from .txt or .docx"""
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""

def get_clean_filename(name):
    """Strip and sanitize file names for saving"""
    base = os.path.basename(name)
    return base.replace(" ", "_").replace(".docx", "").replace(".txt", "")

def save_summary(text, filename):
    """Save summary text to file"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
