"""
PDF Parser Tool - Extract text from PDF files
"""

from pypdf import PdfReader


def parse_pdf(pdf_path: str) -> dict:
    """
    Extract text from a PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        dict: Extracted text and metadata
    """
    try:
        reader = PdfReader(pdf_path)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return {
            "type": "pdf_content",
            "success": True,
            "num_pages": len(reader.pages),
            "text": text.strip(),
            "char_count": len(text)
        }
    except Exception as e:
        return {
            "type": "pdf_content",
            "success": False,
            "error": str(e)
        }


def get_pdf_metadata(pdf_path: str) -> dict:
    """
    Get PDF metadata
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        dict: PDF metadata
    """
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        
        return {
            "type": "pdf_metadata",
            "success": True,
            "title": metadata.get("/Title", "N/A"),
            "author": metadata.get("/Author", "N/A"),
            "pages": len(reader.pages)
        }
    except Exception as e:
        return {
            "type": "pdf_metadata",
            "success": False,
            "error": str(e)
        }


