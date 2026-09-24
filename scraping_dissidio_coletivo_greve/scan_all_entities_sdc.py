import requests
import json
import time

url = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual/1/20'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

entities = [
    ("ECT / Correios", ["Correios", "Empresa Brasileira de Correios e Telégrafos"]),
    ("Petrobras", ["Petrobras", "Petróleo Brasileiro"]),
    ("Caixa Econômica Federal", ["Caixa Econômica Federal", "CEF"]),
    ("Banco do Brasil", ["Banco do Brasil"]),
    ("EBSERH", ["EBSERH", "Empresa Brasileira de Serviços Hospitalares"]),
    ("Dataprev", ["Dataprev", "Empresa de Tecnologia e Informações da Previdência"]),
    ("Serpro", ["Serpro", "Serviço Federal de Processamento de Dados"]),
    ("EBC", ["Empresa Brasil de Comunicação", "EBC"]),
    ("Conab", ["Companhia Nacional de Abastecimento", "Conab"]),
    ("Casa da Moeda", ["Casa da Moeda do Brasil", "Casa da Moeda"]),
    ("Infraero", ["Infraero", "Empresa Brasileira de Infraestrutura Aeroportuária"]),
    ("CBTU", ["Companhia Brasileira de Trens Urbanos", "CBTU"]),
    ("Trensurb", ["Trensurb", "Empresa de Trens Urbanos de Porto Alegre"]),
    ("Embrapa", ["Embrapa", "Empresa Brasileira de Pesquisa Agropecuária"]),
    ("Eletrobras", ["Eletrobras", "Centrais Elétricas Brasileiras", "Eletronorte", "Furnas", "Chesf", "Eletrosul"]),
    ("BNDES", ["BNDES", "Banco Nacional de Desenvolvimento Econômico e Social"]),
    ("Finep", ["Finep", "Financiadora de Estudos e Projetos"]),
    ("Codevasf", ["Codevasf", "Companhia de Desenvolvimento dos Vales do São Francisco"]),
    ("Hemobrás", ["Hemobrás", "Empresa Brasileira de Hemoderivados"]),
    ("Emgepron", ["Emgepron", "Empresa Gerencial de Projetos Navais"]),
    ("EPL / Infra S.A.", ["EPL", "Infra S.A.", "Empresa de Planejamento e Logística", "Valec"]),
    ("Nuclep", ["Nuclep", "Nuclebrás"]),
    ("Imbel", ["Imbel", "Indústria de Material Bélico"]),
    ("Ceitec", ["Ceitec"]),
    ("Telebras", ["Telebras", "Telecomunicações Brasileiras"]),
    ("Banco do Nordeste", ["Banco do Nordeste", "BNB"]),
    ("Banco da Amazônia", ["Banco da Amazônia", "BASA"]),
    ("BRB", ["Banco de Brasília", "BRB"]),
    ("Metrô SP", ["Companhia do Metropolitano de São Paulo", "Metrô de São Paulo"]),
    ("CPTM", ["Companhia Paulista de Trens Metropolitanos", "CPTM"]),
    ("Sabesp", ["Sabesp", "Companhia de Saneamento Básico do Estado de São Paulo"]),
    ("Cemig", ["Cemig", "Companhia Energética de Minas Gerais"]),
    ("Copasa", ["Copasa", "Companhia de Saneamento de Minas Gerais"]),
    ("Copel", ["Copel", "Companhia Paranaense de Energia"]),
    ("Sanepar", ["Sanepar", "Companhia de Saneamento do Paraná"]),
    ("Corsan", ["Corsan", "Companhia Riograndense de Saneamento"]),
    ("CEEE", ["CEEE", "Companhia Estadual de Energia Elétrica"]),
    ("Caesb", ["Caesb", "Companhia de Saneamento Ambiental do Distrito Federal"]),
    ("Metrô DF", ["Companhia do Metropolitano do Distrito Federal", "Metrô DF"]),
    ("Cedae", ["Cedae", "Companhia Estadual de Águas e Esgotos"]),
    ("Comlurb", ["Comlurb", "Companhia Municipal de Limpeza Urbana"]),
    ("SPTrans", ["SPTrans", "São Paulo Transporte"]),
    ("Carris", ["Carris", "Companhia Carris Porto-Alegrense"]),
    ("Embasa", ["Embasa", "Empresa Baiana de Águas e Saneamento"]),
    ("Compesa", ["Compesa", "Companhia Pernambucana de Saneamento"])
]

classes = [
    {'codFase': 'DCG', 'desFase': 'Dissídio Coletivo de Greve'},
    {'codFase': 'DC', 'desFase': 'Dissídio Coletivo'},
    {'codFase': 'RO', 'desFase': 'Recurso Ordinário'},
    {'codFase': 'ROT', 'desFase': 'Recurso Ordinário Trabalhista'}
]

results = {}

for ent_name, terms in entities:
    total_ent = 0
    procs = set()
    for term in terms:
        payload = {
            'ou': '', 'e': term, 'termoExato': '', 'naoContem': '', 'ementa': '', 'dispositivo': '',
            'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
            'orgaosJudicantes': [{'codigo': 47, 'sigla': 'SDC', 'descricao': 'Seção Especializada em Dissídios Coletivos'}],
            'ministros': [], 'convocados': [],
            'classesProcessuais': classes,
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
                data = r.json()
                tot = data.get('totalRegistros', 0)
                regs = data.get('registros', [])
                for reg in regs:
                    item = reg.get('registro', {})
                    num = item.get('numFormatado')
                    if num:
                        procs.add(num)
                print(f"  [{ent_name}] term '{term}' -> {tot} hits (found {len(regs)} in first page)")
            else:
                print(f"  [{ent_name}] term '{term}' -> status {r.status_code}")
        except Exception as e:
            print(f"  [{ent_name}] term '{term}' -> error {e}")
        time.sleep(0.3)
    results[ent_name] = len(procs)

print("\nSUMMARY (unique processes seen in page 1):")
for k, v in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"{k}: {v}")
