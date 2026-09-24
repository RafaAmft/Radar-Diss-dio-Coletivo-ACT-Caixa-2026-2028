import json
from bs4 import BeautifulSoup
import re

with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect all unique records with inteiroTeorHtml
records_with_html = []
seen = set()
for ent, recs in data.items():
    for r in recs:
        num = r.get('numFormatado')
        html = r.get('inteiroTeorHtml')
        if num and html and num not in seen:
            seen.add(num)
            records_with_html.append(r)

print(f"Total registros com inteiroTeorHtml: {len(records_with_html)}")

for i, r in enumerate(records_with_html[:15]):
    html = r.get('inteiroTeorHtml')
    soup = BeautifulSoup(html[:15000], 'html.parser')
    text = soup.get_text()
    num = r.get('numFormatado')
    
    print(f"\n==================== Case {i+1}: {num} ====================")
    # Search for party sections in the first 4000 characters
    header_chunk = text[:3500]
    lines = [l.strip() for l in header_chunk.split('\n') if l.strip()]
    for l in lines[:25]:
        if any(k in l.lower() for k in ['suscitante', 'suscitad', 'recorrente', 'recorrid', 'autor', 'réu', 'processo']):
            print("  HEADER LINE:", l[:120])
