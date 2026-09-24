import requests
import json
import time

url = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual/1/10'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

entities_test = [
    "Empresa Brasileira de Correios e Telégrafos",
    "Petrobras",
    "Caixa Econômica Federal",
    "Banco do Brasil",
    "EBSERH",
    "Dataprev",
    "Serpro",
    "Companhia do Metropolitano de São Paulo",
    "Companhia Paulista de Trens Metropolitanos",
    "Sabesp",
    "Cemig",
    "Conab",
    "Infraero",
    "Casa da Moeda",
    "EBC"
]

for ent in entities_test:
    payload = {
        'ou': '', 'e': '', 'termoExato': ent, 'naoContem': '', 'ementa': '', 'dispositivo': '',
        'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
        'orgaosJudicantes': [{'codigo': 47, 'sigla': 'SDC'}],
        'ministros': [], 'convocados': [],
        'classesProcessuais': [], # All classes in SDC
        'codigosClassesPrecedentes': [], 'indicadores': [], 'assuntos': [],
        'tipos': ['ACORDAO', 'DESPACHO'], 'orgao': 'TST',
        'publicacaoInicial': None, 'publicacaoFinal': None,
        'julgamentoInicial': '2016-09-24',
        'julgamentoFinal': '2026-09-24',
        'ordenacao': 'data'
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        if r.status_code == 200:
            tot = r.json().get('totalRegistros', 0)
            print(f"{ent}: {tot} registros na SDC")
        else:
            print(f"{ent}: status {r.status_code}")
    except Exception as e:
        print(f"{ent}: erro {e}")
    time.sleep(0.5)
