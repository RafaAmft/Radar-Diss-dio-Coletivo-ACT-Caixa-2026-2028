import requests
import json

url = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual/1/5'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

payload = {
    'ou': '', 'e': '', 'termoExato': 'dias parados greve', 'naoContem': '', 'ementa': '', 'dispositivo': '',
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

r = requests.post(url, json=payload, headers=headers, timeout=20)
print('Status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    print('Total registros:', data.get('totalRegistros'))
    for reg in data.get('registros', []):
        rec = reg.get('registro', {})
        print(rec.get('orgaoJudicante'), '|', rec.get('nomRelator'), '|', rec.get('tipo'), '|', rec.get('numFormatado'))
