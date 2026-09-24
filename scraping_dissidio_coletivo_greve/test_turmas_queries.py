import requests
import json
import time

url_base = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

queries = [
    'greve "dias parados"',
    'greve "desconto salarial"',
    'greve "ação de cumprimento"',
    'greve estatal "sentença normativa"',
    'greve "empresa pública"'
]

for q in queries:
    payload = {
        'ou': '', 'e': '', 'termoExato': q, 'naoContem': '', 'ementa': '', 'dispositivo': '',
        'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
        'orgaosJudicantes': [],
        'ministros': [], 'convocados': [],
        'classesProcessuais': [],
        'codigosClassesPrecedentes': [], 'indicadores': [], 'assuntos': [],
        'tipos': ['ACORDAO'], 'orgao': 'TST',
        'publicacaoInicial': None, 'publicacaoFinal': None,
        'julgamentoInicial': '2016-09-24',
        'julgamentoFinal': '2026-09-24',
        'ordenacao': 'data'
    }
    r = requests.post(f"{url_base}/1/10", json=payload, headers=headers, timeout=20)
    if r.status_code == 200:
        tot = r.json().get('totalRegistros', 0)
        print(f"Query: [{q}] -> Total: {tot} registros")
    else:
        print(f"Query: [{q}] -> Status: {r.status_code}")
    time.sleep(0.5)
