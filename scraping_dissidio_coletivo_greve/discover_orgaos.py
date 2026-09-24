import requests
import json

url = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual/1/200'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

payload = {
    'ou': '', 'e': '', 'termoExato': 'greve', 'naoContem': '', 'ementa': '', 'dispositivo': '',
    'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
    'orgaosJudicantes': [],
    'ministros': [], 'convocados': [],
    'classesProcessuais': [],
    'codigosClassesPrecedentes': [], 'indicadores': [], 'assuntos': [],
    'tipos': ['ACORDAO'], 'orgao': 'TST',
    'publicacaoInicial': None, 'publicacaoFinal': None,
    'julgamentoInicial': '2020-01-01',
    'julgamentoFinal': '2023-12-31',
    'ordenacao': 'data'
}

r = requests.post(url, json=payload, headers=headers, timeout=20)
if r.status_code == 200:
    data = r.json()
    orgaos = {}
    for reg in data.get('registros', []):
        org = reg.get('registro', {}).get('orgaoJudicante', {})
        if org and isinstance(org, dict):
            orgaos[org.get('codigo')] = org.get('descricao')
    print("Órgãos encontrados:")
    for k, v in sorted(orgaos.items(), key=lambda x: str(x[1])):
        print(f"  Código {k}: {v}")
