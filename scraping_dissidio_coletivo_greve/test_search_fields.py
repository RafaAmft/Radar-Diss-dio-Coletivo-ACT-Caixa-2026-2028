import requests
import json

url_base = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

tests = [
    {'termoExato': 'greve dias parados'},
    {'e': 'greve "dias parados"'},
    {'ementa': 'greve "dias parados"'},
    {'dispositivo': 'greve'},
    {'termoExato': 'Empresa Brasileira de Correios e Telégrafos greve'}
]

for t in tests:
    payload = {
        'ou': t.get('ou', ''),
        'e': t.get('e', ''),
        'termoExato': t.get('termoExato', ''),
        'naoContem': '',
        'ementa': t.get('ementa', ''),
        'dispositivo': t.get('dispositivo', ''),
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
    r = requests.post(f"{url_base}/1/5", json=payload, headers=headers, timeout=20)
    if r.status_code == 200:
        data = r.json()
        print(f"Test {t} -> Total: {data.get('totalRegistros')}")
        regs = data.get('registros', [])
        if regs:
            first = regs[0].get('registro', {})
            print(f"   First: {first.get('numFormatado')} | {first.get('orgaoJudicante', {}).get('descricao')}")
    else:
        print(f"Test {t} -> Status: {r.status_code}")
