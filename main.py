from utils import (
    get_pdf_links,
    download_pdf,
    extract_table_from_pdf,
    replace_abbreviations,
    save_csv,
    create_zip_file
)
import os

def main():
    site_url = (
        "https://www.gov.br/ans/pt-br/acesso-a-informacao/"
        "participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    )
    
    try:
        pdf_info = get_pdf_links(site_url) 
        
        if not pdf_info:
            return
        
        for (text, href) in pdf_info:
            print("----")

        anexo_i_link = None
        for (text, href) in pdf_info:
            if ("anexo i" in text) or ("rol de procedimentos e eventos em saúde" in text):
                anexo_i_link = href
                break
        
        if not anexo_i_link:
            return
        
        
        pdf_name = "Anexo_I.pdf"
        download_pdf(anexo_i_link, pdf_name)
        
        data_df = extract_table_from_pdf(pdf_name)
        
        data_df = replace_abbreviations(data_df)
        
        csv_path = "Dados_Combinados.csv"
        save_csv(data_df, csv_path)
        
        zip_file_name = "Teste_Ikaro.zip"
        create_zip_file(csv_path, zip_file_name)
        
        if os.path.exists(csv_path):
            os.remove(csv_path)
        

    except Exception as e:
        print("Ocorreu um erro:", e)

if __name__ == "__main__":
    main()
