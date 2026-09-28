import requests
import json
import re
from bs4 import BeautifulSoup

url_base = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

payload = {
    'ou': '',
    'e': '"Caixa Econômica Federal"',
    'termoExato': '',
    'naoContem': '',
    'ementa': '',
    'dispositivo': '',
    'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
    'orgaosJudicantes': [{'codigo': 47, 'sigla': 'SDC', 'descricao': 'Seção Especializada em Dissídios Coletivos'}],
    'ministros': [],
    'convocados': [],
    'classesProcessuais': [
        {'codFase': 'DCG'}, {'codFase': 'DC'}, {'codFase': 'RO'}, {'codFase': 'ROT'}, {'codFase': 'RODC'}
    ],
    'codigosClassesPrecedentes': [],
    'indicadores': [],
    'assuntos': [],
    'tipos': ['ACORDAO', 'DESPACHO'],
    'orgao': 'TST',
    'publicacaoInicial': None,
    'publicacaoFinal': None,
    'julgamentoInicial': '2016-01-01',
    'julgamentoFinal': '2026-09-25',
    'ordenacao': 'data'
}

r = requests.post(f'{url_base}/1/50', json=payload, headers=headers, timeout=25)
res = r.json()
print('Total registros retornados:', res.get('totalRegistros'))
records = res.get('registros', [])
print(f'Recebidos na página 1: {len(records)}')

valid_cef = []
for item in records:
    reg = item.get('registro', {})
    html = reg.get('txtConteudoDecisao', '') or reg.get('txtConteudoDecisaoHighlight', '')
    text = BeautifulSoup(html, 'html.parser').get_text(separator=' ')
    
    # Check if Caixa is party in text
    polo = None
    if re.search(r'(suscitante|recorrente|autor|requerente)\s*:\s*[^;\n\r]*caixa\s+econ[oô]mica\s+federal', text, re.IGNORECASE):
        polo = 'Suscitante / Recorrente (Autora)'
    elif re.search(r'(suscitad[oa]s?|recorrid[oa]s?|r[eé]u|requerid[oa])\s*:\s*[^;\n\r]*caixa\s+econ[oô]mica\s+federal', text, re.IGNORECASE):
        polo = 'Suscitada / Recorrida (Ré)'
    elif re.search(r'(em\s+face\s+da|contra\s+a)\s+caixa\s+econ[oô]mica\s+federal', text[:3000], re.IGNORECASE):
        polo = 'Suscitada / Requerida'
    elif re.search(r'caixa\s+econ[oô]mica\s+federal', text[:1200], re.IGNORECASE):
        polo = 'Parte Qualificada no Cabeçalho'
        
    if polo:
        num = reg.get('numFormatado')
        rel = reg.get('nomRelator')
        dt = reg.get('dtaPublicacao')
        valid_cef.append({'num': num, 'polo': polo, 'relator': rel, 'data': dt})

print(f'Total identificados com Caixa como parte: {len(valid_cef)}')
for v in valid_cef:
    print(' ', v['num'], '|', v['polo'], '| Relator:', v['relator'], '| Data:', v['data'])
