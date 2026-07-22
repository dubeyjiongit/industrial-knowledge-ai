import os
import re
from typing import Dict, Any

class DocumentParser:
    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()

        text_content = ""
        doc_type = "unknown"

        if ext == ".txt":
            doc_type = "text"
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text_content = f.read()

        elif ext == ".pdf":
            doc_type = "pdf"
            try:
                import pdfplumber
                pages = []
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        t = page.extract_text()
                        if t:
                            pages.append(t)
                text_content = "\n".join(pages)
            except Exception as e:
                print(f"[DocumentParser] pdfplumber failed, trying pypdf fallback: {e}")
                try:
                    import pypdf
                    reader = pypdf.PdfReader(file_path)
                    pages = [page.extract_text() for page in reader.pages if page.extract_text()]
                    text_content = "\n".join(pages)
                except Exception as ex:
                    print(f"[DocumentParser] PDF parsing failed: {ex}")

        elif ext in [".csv", ".xlsx", ".xls"]:
            doc_type = "spreadsheet"
            try:
                import pandas as pd
                if ext == ".csv":
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                text_content = df.to_markdown(index=False)
            except Exception as e:
                print(f"[DocumentParser] Spreadsheet parse error: {e}")

        else:
            doc_type = "raw"
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text_content = f.read()

        # Classify specialized industrial doc types based on content keywords
        content_upper = text_content.upper()
        if "MAINTENANCE" in content_upper or "WORK ORDER" in content_upper or "WO-" in content_upper:
            doc_type = "Maintenance Work Order"
        elif "INSPECTION" in content_upper or "IR-" in content_upper:
            doc_type = "Inspection Report"
        elif "SAFETY" in content_upper or "SP-" in content_upper or "PROCEDURE" in content_upper:
            doc_type = "Safety Procedure"
        elif "SOP" in content_upper or "OPERATING PROCEDURE" in content_upper:
            doc_type = "Standard Operating Procedure"
        elif "P&ID" in content_upper or "DIAGRAM" in content_upper or "PROCESS AREA" in content_upper:
            doc_type = "P&ID Description"

        return {
            "filename": filename,
            "doc_type": doc_type,
            "text": text_content,
            "size": os.path.getsize(file_path)
        }
