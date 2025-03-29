import requests
import pandas as pd
import zipfile
import os
from bs4 import BeautifulSoup

def get_pdf_links(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        raise Exception("Falha ao acessar a página (status_code != 200).")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = []
    
    for link in soup.find_all('a', href=True):
        href = link['href'].strip()
        text = link.get_text(strip=True).lower()
        if href.lower().endswith('.pdf'):
            if href.startswith('/'):
                href = "https://www.gov.br" + href
            pdf_links.append((text, href))
    
    return pdf_links

def download_pdf(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"[OK] PDF baixado: {save_path}")
    else:
        raise Exception(f"Falha ao baixar o arquivo de {url} (status_code={response.status_code})")

def extract_table_from_pdf(pdf_path):
    import pdfplumber
    import pandas as pd
    
    tables_list = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                table = page.extract_table()
                
                if not table or len(table) < 2:
                    continue
                
                raw_headers = table[0]
                data_rows = table[1:]
                
                num_cols = len(raw_headers)
                filtered_data_rows = [row for row in data_rows if len(row) == num_cols]

                headers = []
                count_map = {}
                for col in raw_headers:
                    if col not in count_map:
                        count_map[col] = 1
                        headers.append(col)
                    else:
                        count_map[col] += 1
                        headers.append(f"{col}_{count_map[col]}")
                
                df = pd.DataFrame(filtered_data_rows, columns=headers)
                tables_list.append(df)
    except Exception as e:
        raise ValueError(
            f"Falha ao abrir/extrair do PDF '{pdf_path}'. "
            f"Verifique se o arquivo está corrompido ou se é um PDF válido.\n"
            f"Erro original: {e}"
        )
    
    if tables_list:
        combined_df = pd.concat(tables_list, ignore_index=True)
        return combined_df
    else:
        raise ValueError(f"Nenhuma tabela válida foi encontrada no PDF '{pdf_path}'.")

def replace_abbreviations(df):
    mapping_OD = {
        "OD": "Seg. Odontológica"
    }
    mapping_AMB = {
        "AMB": "Seg. Ambulatorial"
    }
    
    if "OD" in df.columns:
        df["OD"] = df["OD"].replace(mapping_OD)
    if "AMB" in df.columns:
        df["AMB"] = df["AMB"].replace(mapping_AMB)
    
    return df

def save_csv(df, csv_path):
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

def create_zip_file(file_to_zip, zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_to_zip, arcname=os.path.basename(file_to_zip))
    print(f"[OK] Arquivo ZIP criado: {zip_file_name}")
