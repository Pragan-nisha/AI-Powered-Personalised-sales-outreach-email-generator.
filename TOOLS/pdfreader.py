import sys
import json
import fitz  # PyMuPDF

def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    doc.close()
    return {"content": text.strip()}

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    data = read_pdf(pdf_path)
    print(json.dumps(data))
