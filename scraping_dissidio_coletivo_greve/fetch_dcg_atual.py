import json
from bs4 import BeautifulSoup

# 1. Check in all_entity_records.json
with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

target = '1000422-59.2025'
found_entity = None
for ent, procs in data.items():
    for p in procs:
        num = p.get('numFormatado', '') or p.get('numeracaoUnica', '')
        if target in str(num):
            found_entity = p
            print(f"ENCONTRADO em all_entity_records: {ent}")
            print(f"  numFormatado: {p.get('numFormatado')}")
            print(f"  nomRelator: {p.get('nomRelator')}")
            print(f"  dtaJulgamento: {p.get('dtaJulgamento')}")
            print(f"  dtaPublicacao: {p.get('dtaPublicacao')}")
            print(f"  tipo: {p.get('tipo')}")
            print(f"  orgaoJudicante: {p.get('orgaoJudicante')}")
            print(f"  codFase: {p.get('codFase')}")
            txt = p.get('txtConteudoDecisao', '') or ''
            print(f"  txtConteudoDecisao length: {len(txt)}")
            if txt:
                clean = BeautifulSoup(txt, 'html.parser').get_text(separator=' ') if '<' in txt else txt
                print(f"\n=== CONTEÚDO COMPLETO ===\n")
                print(clean[:5000])
                if len(clean) > 5000:
                    print(f"\n... [truncado, total: {len(clean)} chars] ...\n")
                    print(clean[-2000:])
            break

# 2. Check in sdc_all_dc_dcg.json
with open('scraping_dissidio_coletivo_greve/sdc_all_dc_dcg.json', 'r', encoding='utf-8') as f:
    dcg = json.load(f)

for p in dcg:
    num = p.get('numFormatado', '') or ''
    if target in num:
        print(f"\nENCONTRADO em sdc_all_dc_dcg.json:")
        print(f"  numFormatado: {p.get('numFormatado')}")
        print(f"  nomRelator: {p.get('nomRelator')}")
        txt = p.get('txtConteudoDecisao', '') or ''
        if txt:
            clean = BeautifulSoup(txt, 'html.parser').get_text(separator=' ') if '<' in txt else txt
            print(f"\n=== CONTEÚDO ===\n")
            print(clean[:5000])

# 3. Try API directly
import requests
print("\n\n=== BUSCANDO NA API DO TST ===")
url = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual/1/10'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
payload = {
    'ou': '', 'e': '', 'termoExato': '1000422-59.2025', 'naoContem': '', 'ementa': '', 'dispositivo': '',
    'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
    'orgaosJudicantes': [],
    'ministros': [], 'convocados': [],
    'classesProcessuais': [],
    'codigosClassesPrecedentes': [], 'indicadores': [], 'assuntos': [],
    'tipos': ['ACORDAO', 'DESPACHO'], 'orgao': 'TST',
    'publicacaoInicial': None, 'publicacaoFinal': None,
    'julgamentoInicial': None, 'julgamentoFinal': None,
    'ordenacao': 'data'
}
r = requests.post(url, json=payload, headers=headers, timeout=20)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data_api = r.json()
    print(f"Total registros: {data_api.get('totalRegistros')}")
    for reg in data_api.get('registros', []):
        rec = reg.get('registro', {})
        print(f"  Num: {rec.get('numFormatado')}")
        print(f"  Relator: {rec.get('nomRelator')}")
        txt = rec.get('txtConteudoDecisao', '') or rec.get('conteudoDecisao', '') or ''
        if txt:
            clean = BeautifulSoup(txt, 'html.parser').get_text(separator=' ') if '<' in txt else txt
            print(f"  Texto ({len(clean)} chars):")
            print(clean[:3000])

# 4. Try by numeracaoUnica
print("\n\n=== BUSCANDO POR NUMERAÇÃO ÚNICA ===")
payload2 = {
    'ou': '', 'e': '', 'termoExato': '', 'naoContem': '', 'ementa': '', 'dispositivo': '',
    'numeracaoUnica': {'numero': '1000422', 'ano': '2025', 'digito': '59', 'orgao': '5', 'tribunal': '00', 'vara': '0000'},
    'orgaosJudicantes': [],
    'ministros': [], 'convocados': [],
    'classesProcessuais': [],
    'codigosClassesPrecedentes': [], 'indicadores': [], 'assuntos': [],
    'tipos': ['ACORDAO', 'DESPACHO'], 'orgao': 'TST',
    'publicacaoInicial': None, 'publicacaoFinal': None,
    'julgamentoInicial': None, 'julgamentoFinal': None,
    'ordenacao': 'data'
}
r2 = requests.post(url, json=payload2, headers=headers, timeout=20)
print(f"Status: {r2.status_code}")
if r2.status_code == 200:
    data2 = r2.json()
    print(f"Total registros: {data2.get('totalRegistros')}")
    for reg in data2.get('registros', []):
        rec = reg.get('registro', {})
        print(f"  Num: {rec.get('numFormatado')}")
        print(f"  Tipo: {rec.get('tipo')}")
        print(f"  Relator: {rec.get('nomRelator')}")
        txt = rec.get('txtConteudoDecisao', '') or ''
        if txt:
            clean = BeautifulSoup(txt, 'html.parser').get_text(separator=' ') if '<' in txt else txt
            print(f"\n  TEXTO ({len(clean)} chars):\n")
            print(clean[:8000])
