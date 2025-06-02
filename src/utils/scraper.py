import requests
import tqdm
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL 
BASE_URL = "http://www.empulia.it/tno-a/empulia/Empulia/SitePages/Guide%20pratiche.aspx"

DOWNLOAD_DIR = "data\PDF"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_pdf_from_page():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    link_pdf = soup.find_all("a", href=True)
    for link in tqdm.tqdm(link_pdf):
        href = link["href"]
        if href.endswith(".pdf"):
            url_pdf = urljoin(BASE_URL, href)
            nome_file = href.split("/")[-1]

            path_destinazione = os.path.join(DOWNLOAD_DIR, nome_file)
            if not os.path.exists(path_destinazione):  
                print(f"Download {nome_file}...")
                pdf_data = requests.get(url_pdf)
                with open(path_destinazione, "wb") as f:
                    f.write(pdf_data.content)
            else:
                print(f"{nome_file} already downloaded.")

if __name__ == "__main__":
    download_pdf_from_page()
