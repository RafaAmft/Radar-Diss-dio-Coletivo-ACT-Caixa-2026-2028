import requests
import json

url = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual/1/10'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

payload = {
    'ou': '', 'e': 'Caputo Bastos Caixa', 'termoExato': '', 'naoContem': '', 'ementa': '', 'dispositivo': '',
    'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
    'orgaosJudicantes': [],
    'ministros': [], 'convocados': [],
    'classesProcessuais': [],
    'codigosClassesPrecedentes': [], 'indicadores': [], 'assuntos': [],
    'tipos': ['DESPACHO', 'ACORDAO'], 'orgao': 'TST',
    'publicacaoInicial': None, 'publicacaoFinal': None,
    'julgamentoInicial': '2024-01-01',
    'julgamentoFinal': '2026-09-24',
    'ordenacao': 'data'
}
r = requests.post(url, json=payload, headers=headers, timeout=20)
print('Status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    print('Total:', data.get('totalRegistros'))
    for reg in data.get('registros', []):
        rec = reg.get('registro', {})
        print(rec.get('numFormatado'), '|', rec.get('orgaoJudicante', {}).get('descricao'), '|', rec.get('nomRelator'), '|', rec.get('dtaPublicacao'))
        txt = (rec.get('txtConteudoDecisao') or rec.get('ementa') or '')[:300]
        print('  Snippet:', txt[:150])
