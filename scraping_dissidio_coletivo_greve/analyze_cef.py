import json
import pandas as pd
from collections import Counter
from bs4 import BeautifulSoup
import re

# 1. CEF records in SDC (all_entity_records.json)
with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cef_procs = []
for k in data.keys():
    if 'caixa' in k.lower() or 'cef' in k.lower():
        print(f"Entity key: [{k}] -> {len(data[k])} records")
        cef_procs = data[k]

print(f"\n=== CEF SDC RECORDS: {len(cef_procs)} ===")
for p in cef_procs[:3]:
    print(p.get('numFormatado'), '|', p.get('nomRelator'), '|', p.get('dtaJulgamento'))

# Relatores
print('\nRelatores CEF na SDC:')
relatores = Counter(p.get('nomRelator') for p in cef_procs)
for r, c in relatores.most_common():
    print(f"  {r}: {c}")

# Classes
print('\nClasses CEF:')
classes = Counter()
for p in cef_procs:
    t = p.get('tipo', '')
    if isinstance(t, dict):
        classes[t.get('nome', 'N/A')] += 1
    else:
        classes[str(t)] += 1
for cl, c in classes.most_common():
    print(f"  {cl}: {c}")

# Temporal
print('\nAnos de julgamento CEF:')
anos = Counter()
for p in cef_procs:
    dj = p.get('dtaJulgamento', '')
    if dj and len(dj) >= 4:
        anos[dj[:4]] += 1
for a, c in sorted(anos.items()):
    print(f"  {a}: {c}")

# 2. CEF in main suscitante/suscitada dataset
xl = pd.ExcelFile('dissidios_coletivos_estatais_2016_2026.xlsx')
df_susc = xl.parse('Estatal Suscitante')
df_suscitada = xl.parse('Estatal Suscitada')

cef_susc = df_susc[df_susc['suscitante'].str.contains('Caixa|CEF', case=False, na=False)]
print(f"\n=== CEF como Suscitante: {len(cef_susc)} ===")
if len(cef_susc) > 0:
    for _, row in cef_susc.iterrows():
        print(row.get('número CNJ', ''), '|', row.get('classe', ''), '|', row.get('relator', ''))

cef_suscitada = df_suscitada[df_suscitada.apply(lambda r: 'caixa' in str(r).lower() or 'cef' in str(r).lower(), axis=1)]
print(f"\n=== CEF como Suscitada: {len(cef_suscitada)} ===")

# 3. CEF in turmas cache
with open('scraping_dissidio_coletivo_greve/turmas_records_cache.json', 'r', encoding='utf-8') as f:
    turmas = json.load(f)

cef_turmas = []
for num, rec in turmas.items():
    txt = (rec.get('ementa') or '') + ' ' + (rec.get('inteiroTeorHtml') or '')
    if 'caixa' in txt.lower() or 'cef' in txt.lower():
        cef_turmas.append(rec)
print(f"\n=== CEF nas Turmas: {len(cef_turmas)} ===")
for t in cef_turmas[:5]:
    print(t.get('numFormatado'), '|', t.get('orgaoJudicante', {}).get('descricao', ''), '|', t.get('nomRelator'))

# 4. Sample CEF full-text content analysis
print('\n=== AMOSTRA DE CONTEUDO CEF SDC ===')
def clean_html(text):
    if not text:
        return ""
    if "<" in text and ">" in text:
        return BeautifulSoup(text, 'html.parser').get_text(separator=' ')
    return text

for p in cef_procs[:3]:
    txt = clean_html(p.get('txtConteudoDecisao', '') or '')
    if len(txt) > 200:
        # Find key legal terms
        mentions = []
        for term in ['greve', 'abusiv', 'dias parados', 'desconto', 'reajuste', 'INPC', 'plano de saúde',
                      'vale', 'tíquete', 'cesta', 'PLR', 'participação nos lucros', 'jornada',
                      'contingente', 'acordo coletivo', 'ACT', 'CCT', 'comum acordo']:
            if term.lower() in txt.lower():
                mentions.append(term)
        if mentions:
            print(f"  {p.get('numFormatado')}: Temas encontrados: {', '.join(mentions)}")
