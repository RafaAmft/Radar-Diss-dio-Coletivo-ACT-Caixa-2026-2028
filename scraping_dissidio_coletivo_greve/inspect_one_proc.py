import json

with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for ent, recs in data.items():
    for r in recs:
        if r.get('numFormatado') == 'DC - 1001307-73.2025.5.00.0000':
            print("Found DC - 1001307-73.2025.5.00.0000:")
            for k, v in r.items():
                if v and not str(v).startswith('{') and len(str(v)) < 500:
                    print(f"  {k}: {v}")
                elif v and len(str(v)) >= 500:
                    print(f"  {k} (len {len(str(v))}): {str(v)[:300]}...")
            break
