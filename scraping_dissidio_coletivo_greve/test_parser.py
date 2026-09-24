import json
import re
from bs4 import BeautifulSoup

with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Flatten all unique records by process number
unique_records = {}
for ent, recs in data.items():
    for r in recs:
        num = r.get('numFormatado') or r.get('numero')
        if not num:
            continue
        # Extract pure CNJ number
        cnj_match = re.search(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', str(num))
        if not cnj_match:
            # Try construct from numeracaoUnica
            nu = r.get('numeracaoUnica')
            if isinstance(nu, dict) and nu.get('numero'):
                cnj_str = f"{nu['numero']:07d}-{nu['digito']:02d}.{nu['ano']}.{nu['orgao']}.{nu['tribunal']:02d}.{nu['vara']:04d}"
            else:
                cnj_str = str(num)
        else:
            cnj_str = cnj_match.group(1)
        
        if cnj_str not in unique_records:
            unique_records[cnj_str] = r
            unique_records[cnj_str]['matched_entities'] = [ent]
        else:
            if ent not in unique_records[cnj_str]['matched_entities']:
                unique_records[cnj_str]['matched_entities'].append(ent)
            # If current record has HTML full text and existing doesn't, prefer this one
            if len(r.get('inteiroTeorHtml') or '') > len(unique_records[cnj_str].get('inteiroTeorHtml') or ''):
                ents = unique_records[cnj_str]['matched_entities']
                unique_records[cnj_str] = r
                unique_records[cnj_str]['matched_entities'] = ents

print(f"Total processos CNJ únicos consolidados: {len(unique_records)}")

# Test parsing on first 20 records
parsed_samples = []
for cnj, r in list(unique_records.items())[:20]:
    html = r.get('inteiroTeorHtml') or r.get('txtConteudoDecisao') or ''
    ementa = r.get('ementa') or ''
    dispositivo = r.get('dispositivo') or ''
    full_text = ""
    if html:
        soup = BeautifulSoup(html[:20000], 'html.parser')
        full_text = soup.get_text()
    else:
        full_text = f"{ementa}\n{dispositivo}"
    
    # Try extract Suscitante
    susc_match = re.search(r'(?:SUSCITANTE(?:[S\s:]|:\s*|[\s]+))([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ][AÃ]O[^\n\r,;.]+?|[A-Z\s]{4,}))(?:(?:\s+e\s+|\s*,\s*|\s+s[aã]o\s+)(?:SUSCITADO|RECORRIDO)|[\n\r;])', full_text, re.I)
    
    # Also look for standard header: "em que é SUSCITANTE ... e são SUSCITADOS ..."
    susc_std = re.search(r'em que [eé]\s+SUSCITANTE\s+([^,;\n\r]+?)\s+e\s+(?:s[aã]o|é)\s+SUSCITADO[S]?\s+([^,;\n\r]+?)(?:\s+e\s+|\.|\;|\n|\r)', full_text, re.I)
    
    print(f"\nCNJ: {cnj} | Classe: {r.get('codFase')} | Entidades: {r.get('matched_entities')}")
    if susc_std:
        print(f"  STD -> Suscitante: {susc_std.group(1).strip()[:80]}")
        print(f"         Suscitado:  {susc_std.group(2).strip()[:80]}")
    elif susc_match:
        print(f"  REGEX -> Suscitante: {susc_match.group(1).strip()[:80]}")
    else:
        print("  Partes não extraídas pelo padrão direto. Ementa snippet:", ementa[:120].replace('\n', ' '))
