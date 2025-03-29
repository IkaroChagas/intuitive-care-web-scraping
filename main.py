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
        print("Buscando links de PDF na página...")
        pdf_info = get_pdf_links(site_url) 
        
        if not pdf_info:
            print("Nenhum PDF encontrado na página.")
            return
        
        print("\n--- PDFs encontrados ---")
        for (text, href) in pdf_info:
            print(f"Texto do link: {text}")
            print(f"URL: {href}")
            print("----")

        anexo_i_link = None
        for (text, href) in pdf_info:
            if ("anexo i" in text) or ("rol de procedimentos e eventos em saúde" in text):
                anexo_i_link = href
                break
        
        if not anexo_i_link:
            print("\nNão foi encontrado link do Anexo I usando os critérios atuais.")
            print("Verifique os PDFs listados acima e ajuste a condição de filtragem, se necessário.")
            return
        
        print(f"\n[OK] Link do Anexo I selecionado: {anexo_i_link}")
        
        pdf_name = "Anexo_I.pdf"
        download_pdf(anexo_i_link, pdf_name)
        
        data_df = extract_table_from_pdf(pdf_name)
        
        data_df = replace_abbreviations(data_df)
        
        csv_path = "Dados_Combinados.csv"
        save_csv(data_df, csv_path)
        print(f"[OK] CSV gerado: {csv_path}")
        
        zip_file_name = "Teste_Ikaro.zip"
        create_zip_file(csv_path, zip_file_name)
        
        if os.path.exists(csv_path):
            os.remove(csv_path)
            print(f"[INFO] CSV '{csv_path}' removido. Agora só existe '{zip_file_name}'.")
        
        print("\nProcesso concluído com sucesso!")
    
    except Exception as e:
        print("Ocorreu um erro:", e)

if __name__ == "__main__":
    main()
