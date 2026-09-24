import json
from bs4 import BeautifulSoup
import re

with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find records with html
sample_cases = ['ROT - 62-10.2022.5.23.0000', 'ROT - 1001567-09.2019.5.02.0000', 'DC - 1001307-73.2025.5.00.0000', 'DCG - 1000279-36.2026.5.00.0000', 'ROT - 1028102-33.2023.5.02.0000']

for ent, recs in data.items():
    for r in recs:
        num = r.get('numFormatado')
        if any(sc in str(num) for sc in sample_cases):
            html = r.get('inteiroTeorHtml')
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.get_text()
                print(f"\n=================== {num} ===================")
                # Look for "Vistos, relatados"
                idx = text.find("Vistos, relatados")
                if idx != -1:
                    print("--- VISTOS RELATADOS BLOCK ---")
                    print(text[idx:idx+800].replace('\n', ' '))
                else:
                    idx2 = text.find("R E L A T Ó R I O")
                    if idx2 == -1:
                        idx2 = text.find("RELATÓRIO")
                    if idx2 != -1:
                        print("--- RELATORIO BLOCK ---")
                        print(text[idx2:idx2+800].replace('\n', ' '))
                    else:
                        print("Snippet from middle:", text[1000:1800].replace('\n', ' '))
            sample_cases = [sc for sc in sample_cases if sc not in str(num)]
