import json
import re

with open('scraping_dissidio_coletivo_greve/sdc_all_ro_rot.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

print(f"Total registros RO/ROT carregados: {len(records)}")

targets = {
    'ECT / Correios': [r'\bECT\b', r'Correios', r'Empresa Brasileira de Correios'],
    'Petrobras': [r'Petrobras', r'Petr[oó]leo Brasileiro', r'Transpetro'],
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
    'Trensurb': [r'Trensurb', r'Empresa de Trens Urbanos de Porto Alegre'],
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
    'Metrô SP': [r'Companhia do Metropolitano de S[aã]o Paulo', r'Metr[oô] de S[aã]o Paulo', r'\bMetr[oô]\b.*S[aã]o Paulo'],
    'CPTM': [r'\bCPTM\b', r'Companhia Paulista de Trens Metropolitanos'],
    'Sabesp': [r'Sabesp', r'Companhia de Saneamento B[aá]sico do Estado de S[aã]o Paulo'],
    'Cemig': [r'Cemig', r'Companhia Energ[eé]tica de Minas Gerais'],
    'Copasa': [r'Copasa', r'Companhia de Saneamento de Minas Gerais'],
    'Copel': [r'Copel', r'Companhia Paranaense de Energia'],
    'Sanepar': [r'Sanepar', r'Companhia de Saneamento do Paran[aá]'],
    'Corsan': [r'Corsan', r'Companhia Riograndense de Saneamento'],
    'CEEE': [r'\bCEEE\b', r'Companhia Estadual de Energia El[eé]trica'],
    'Caesb': [r'Caesb', r'Companhia de Saneamento Ambiental do Distrito Federal'],
    'Metrô DF': [r'Metr[oô] do Distrito Federal', r'Metr[oô]-?DF'],
    'Cedae': [r'Cedae', r'Companhia Estadual de [AÁ]guas e Esgotos'],
    'Comlurb': [r'Comlurb', r'Companhia Municipal de Limpeza Urbana'],
    'SPTrans': [r'SPTrans', r'S[aã]o Paulo Transporte'],
    'Carris': [r'Carris', r'Companhia Carris Porto-Alegrense'],
    'Embasa': [r'Embasa', r'Empresa Baiana de [AÁ]guas e Saneamento'],
    'Compesa': [r'Compesa', r'Companhia Pernambucana de Saneamento']
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
            'ementa': ementa
        })

print(f"Total de registros RO/ROT com entidades estatais identificadas: {len(matched_cases)}")
ent_counts = {}
for m in matched_cases:
    for e in m['entities']:
        ent_counts[e] = ent_counts.get(e, 0) + 1

for e, c in sorted(ent_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {e}: {c} decisões")

with open('scraping_dissidio_coletivo_greve/matched_ro_entities.json', 'w', encoding='utf-8') as f:
    json.dump(matched_cases, f, ensure_ascii=False, indent=2)
