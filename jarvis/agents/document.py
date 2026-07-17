import fitz  # PyMuPDF

class DocumentAgent:
    """Agent for parsing documents like PDFs."""
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Reads a PDF file and extracts its text."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            return text
        except Exception as e:
            return f"Error reading PDF {file_path}: {e}"
