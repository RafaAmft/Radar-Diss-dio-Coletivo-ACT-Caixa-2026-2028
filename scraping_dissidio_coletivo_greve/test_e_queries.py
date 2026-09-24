import requests

url_base = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

queries = [
    'greve "dias parados"',
    'greve "desconto" "sentença normativa"',
    'greve "ação de cumprimento"',
    'greve "abusividade" "recurso de revista"',
    'greve "estabilidade" "reintegração"',
    'greve Correios "dias parados"',
    'greve Petrobras "dias parados"',
    'greve Caixa "dias parados"'
]

for q in queries:
    payload = {
        'ou': '', 'e': q, 'termoExato': '', 'naoContem': '', 'ementa': '', 'dispositivo': '',
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
    r = requests.post(f"{url_base}/1/1", json=payload, headers=headers, timeout=20)
    if r.status_code == 200:
        tot = r.json().get('totalRegistros', 0)
        print(f"e: [{q}] -> {tot} registros")
