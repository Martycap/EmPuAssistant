import os
import fitz  # PyMuPDF
import tqdm

PDF_DIR = "data\PDF"
TEXT_DIR = "data\TEXT"
os.makedirs(TEXT_DIR, exist_ok=True)

def extract_text_pdf():
    for nome_pdf in tqdm.tqdm(os.listdir(PDF_DIR)):
        if nome_pdf.endswith(".pdf"):
            path_pdf = os.path.join(PDF_DIR, nome_pdf)
            path_txt = os.path.join(TEXT_DIR, nome_pdf.replace(".pdf", ".txt"))

            print(f"Extraction from {nome_pdf}")
            with fitz.open(path_pdf) as doc:
                testo = ""
                for pagina in doc:
                    testo += pagina.get_text()

            with open(path_txt, "w", encoding="utf-8") as f:
                f.write(testo)

if __name__ == "__main__":
    extract_text_pdf()
