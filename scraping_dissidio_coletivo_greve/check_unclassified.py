import json
import re

with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    all_entity_data = json.load(f)

# Look at records for Petrobras, Metrô SP, Sabesp, Caixa, Banco do Brasil
target_check = ['Petrobras / Transpetro', 'Metrô SP', 'Sabesp', 'Caixa Econômica Federal (CEF)', 'Banco do Brasil (BB)', 'Conab', 'Infraero', 'Casa da Moeda do Brasil (CMB)']

for ent in target_check:
    recs = all_entity_data.get(ent, [])
    print(f"\n================ Entidade: {ent} (Total {len(recs)} registros) ================")
    for r in recs[:4]:
        num = r.get('numFormatado')
        ementa = r.get('ementa') or ''
        print(f"Proc: {num}")
        print(f"Ementa snippet: {ementa[:250].replace('\n', ' ')}")
        html = r.get('inteiroTeorHtml') or ''
        # Look for "Suscitante" in html
        for m in re.finditer(r'suscitante', html, re.I):
            print("   HTML match around suscitante:", html[max(0, m.start()-40):min(len(html), m.end()+150)].replace('\n', ' '))
            break
