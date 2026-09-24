import json
import re

with open('scraping_dissidio_coletivo_greve/sdc_all_dc_dcg.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

print(f"Total registros DC/DCG carregados: {len(records)}")

# Target entities keywords
targets = {
    'ECT / Correios': [r'\bECT\b', r'Correios', r'Empresa Brasileira de Correios'],
    'Petrobras': [r'Petrobras', r'Petr[oó]leo Brasileiro'],
    'Caixa Econômica Federal': [r'Caixa Econ[oô]mica Federal', r'\bCEF\b'],
    'Banco do Brasil': [r'Banco do Brasil'],
    'EBSERH': [r'EBSERH', r'Empresa Brasileira de Servi[cç]os Hospitalares'],
    'Dataprev': [r'Dataprev'],
    'Serpro': [r'Serpro', r'Servi[cç]o Federal de Processamento de Dados'],
    'EBC': [r'\bEBC\b', r'Empresa Brasil de Comunica[cç][aã]o'],
    'Conab': [r'Conab', r'Companhia Nacional de Abastecimento'],
    'Casa da Moeda': [r'Casa da Moeda'],
    'Infraero': [r'Infraero'],
    'CBTU': [r'\bCBTU\b', r'Companhia Brasileira de Trens Urbanos'],
    'Trensurb': [r'Trensurb'],
    'Embrapa': [r'Embrapa'],
    'Eletrobras': [r'Eletrobras', r'Centrais El[eé]tricas Brasileiras', r'Eletronorte', r'Furnas', r'Chesf', r'Eletrosul'],
    'BNDES': [r'\bBNDES\b'],
    'Finep': [r'Finep'],
    'Codevasf': [r'Codevasf'],
    'Hemobrás': [r'Hemobr[aá]s'],
    'Emgepron': [r'Emgepron'],
    'EPL / Infra S.A.': [r'\bEPL\b', r'Infra S\.?A\.?', r'Valec'],
    'Nuclep': [r'Nuclep'],
    'Imbel': [r'Imbel'],
    'Ceitec': [r'Ceitec'],
    'Telebras': [r'Telebras', r'Telecomunica[cç][oõ]es Brasileiras'],
    'Banco do Nordeste': [r'Banco do Nordeste', r'\bBNB\b'],
    'Banco da Amazônia': [r'Banco da Amaz[oô]nia', r'\bBASA\b'],
    'BRB': [r'\bBRB\b', r'Banco de Bras[ií]lia'],
    'Metrô SP': [r'Companhia do Metropolitano de S[aã]o Paulo', r'Metr[oô] de S[aã]o Paulo'],
    'CPTM': [r'\bCPTM\b', r'Companhia Paulista de Trens Metropolitanos'],
    'Sabesp': [r'Sabesp'],
    'Cemig': [r'Cemig'],
    'Copasa': [r'Copasa'],
    'Copel': [r'Copel'],
    'Sanepar': [r'Sanepar'],
    'Corsan': [r'Corsan'],
    'CEEE': [r'\bCEEE\b'],
    'Caesb': [r'Caesb'],
    'Metrô DF': [r'Metr[oô] do Distrito Federal', r'Metr[oô]-?DF'],
    'Cedae': [r'Cedae'],
    'Comlurb': [r'Comlurb'],
    'SPTrans': [r'SPTrans']
}

matched_cases = []

for rec in records:
    num = rec.get('numFormatado') or rec.get('numero')
    cod_fase = rec.get('codFase')
    dt_julg = rec.get('dtaJulgamento')
    dt_pub = rec.get('dtaPublicacao')
    relator = rec.get('nomRelator')
    ementa = rec.get('ementa') or ''
    dispositivo = rec.get('dispositivo') or ''
    full_search_text = f"{num} {ementa} {dispositivo}"
    
    found_entities = []
    for ent, patterns in targets.items():
        for pat in patterns:
            if re.search(pat, full_search_text, re.IGNORECASE):
                found_entities.append(ent)
                break
    
    if found_entities:
        matched_cases.append({
            'num': num,
            'cod_fase': cod_fase,
            'dt_julg': dt_julg,
            'dt_pub': dt_pub,
            'relator': relator,
            'entities': found_entities,
            'ementa_snippet': ementa[:250].replace('\n', ' ')
        })

print(f"Total de registros DC/DCG com entidades estatais identificadas: {len(matched_cases)}")
# Count by entity
ent_counts = {}
for m in matched_cases:
    for e in m['entities']:
        ent_counts[e] = ent_counts.get(e, 0) + 1

for e, c in sorted(ent_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {e}: {c} decisões")

# Show sample of cases
print("\nExemplo de 5 casos encontrados:")
for m in matched_cases[:5]:
    print(f"[{m['entities']}] {m['num']} | Julg: {m['dt_julg']} | Relator: {m['relator']}")
    print(f"   Ementa: {m['ementa_snippet'][:180]}...")
