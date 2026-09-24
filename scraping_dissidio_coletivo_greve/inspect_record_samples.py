import json
import re

with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total entidades no json: {len(data)}")

total_recs = 0
for ent, recs in data.items():
    total_recs += len(recs)
print(f"Total registros somados: {total_recs}")

# Inspect structure of first 5 records across different entities
sample_ents = ['Empresa Brasileira de Correios e Telégrafos (ECT / Correios)', 'Petrobras / Transpetro', 'EBSERH', 'Metrô SP', 'CPTM']
for ent in sample_ents:
    recs = data.get(ent, [])
    if recs:
        r = recs[0]
        print(f"\n=================== Sample: {ent} ===================")
        print("numFormatado:", r.get('numFormatado'))
        print("numero:", r.get('numero'))
        print("numeracaoUnica:", r.get('numeracaoUnica'))
        print("codFase:", r.get('codFase'))
        print("dtaJulgamento:", r.get('dtaJulgamento'))
        print("nomRelator:", r.get('nomRelator'))
        print("ementaHtml len:", len(r.get('ementaHtml') or ''))
        print("ementa len:", len(r.get('ementa') or ''))
        print("Ementa start:", (r.get('ementa') or '')[:300].replace('\n', ' '))
