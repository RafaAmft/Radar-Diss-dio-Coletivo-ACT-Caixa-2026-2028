import requests
import json
import time

url_base = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

# Full list of entities to query
entities_queries = [
    # Federais
    ('Empresa Brasileira de Correios e Telégrafos (ECT / Correios)', ['"Empresa Brasileira de Correios"', 'Correios']),
    ('Caixa Econômica Federal (CEF)', ['"Caixa Econômica Federal"']),
    ('Banco do Brasil (BB)', ['"Banco do Brasil"']),
    ('Petrobras / Transpetro', ['Petrobras', '"Petróleo Brasileiro"', 'Transpetro']),
    ('EBSERH', ['EBSERH', '"Empresa Brasileira de Serviços Hospitalares"']),
    ('Dataprev', ['Dataprev']),
    ('Serpro', ['Serpro', '"Serviço Federal de Processamento de Dados"']),
    ('EBC', ['"Empresa Brasil de Comunicação"']),
    ('Conab', ['Conab', '"Companhia Nacional de Abastecimento"']),
    ('Casa da Moeda do Brasil (CMB)', ['"Casa da Moeda"']),
    ('Infraero', ['Infraero', '"Empresa Brasileira de Infraestrutura Aeroportuária"']),
    ('CBTU', ['CBTU', '"Companhia Brasileira de Trens Urbanos"']),
    ('Trensurb', ['Trensurb', '"Empresa de Trens Urbanos de Porto Alegre"']),
    ('Embrapa', ['Embrapa', '"Empresa Brasileira de Pesquisa Agropecuária"']),
    ('Eletrobras', ['Eletrobras', '"Centrais Elétricas Brasileiras"', 'Eletronorte', 'Furnas', 'Chesf', 'Eletrosul']),
    ('BNDES', ['BNDES', '"Banco Nacional de Desenvolvimento Econômico e Social"']),
    ('Finep', ['Finep', '"Financiadora de Estudos e Projetos"']),
    ('Codevasf', ['Codevasf']),
    ('Hemobrás', ['Hemobrás', 'Hemobras']),
    ('Emgepron', ['Emgepron']),
    ('EPL / Infra S.A.', ['"Infra S.A."', '"Empresa de Planejamento e Logística"', 'Valec']),
    ('Nuclep', ['Nuclep']),
    ('Imbel', ['Imbel', '"Indústria de Material Bélico"']),
    ('Ceitec', ['Ceitec']),
    ('Telebras', ['Telebras', 'Telebrás']),
    ('Banco do Nordeste (BNB)', ['"Banco do Nordeste"']),
    ('Banco da Amazônia (BASA)', ['"Banco da Amazônia"']),
    ('BRB (Banco de Brasília)', ['"Banco de Brasília"']),
    # Estaduais e Municipais
    ('Metrô SP', ['"Companhia do Metropolitano de São Paulo"', '"Metrô de São Paulo"']),
    ('CPTM', ['CPTM', '"Companhia Paulista de Trens Metropolitanos"']),
    ('Sabesp', ['Sabesp', '"Companhia de Saneamento Básico do Estado de São Paulo"']),
    ('Cemig', ['Cemig', '"Companhia Energética de Minas Gerais"']),
    ('Copasa', ['Copasa', '"Companhia de Saneamento de Minas Gerais"']),
    ('Copel', ['Copel', '"Companhia Paranaense de Energia"']),
    ('Sanepar', ['Sanepar', '"Companhia de Saneamento do Paraná"']),
    ('Corsan', ['Corsan', '"Companhia Riograndense de Saneamento"']),
    ('CEEE', ['CEEE', '"Companhia Estadual de Energia Elétrica"']),
    ('Caesb', ['Caesb', '"Companhia de Saneamento Ambiental do Distrito Federal"']),
    ('Metrô DF', ['"Companhia do Metropolitano do Distrito Federal"', '"Metrô-DF"']),
    ('Cedae (RJ)', ['Cedae', '"Companhia Estadual de Águas e Esgotos"']),
    ('Comlurb (RJ)', ['Comlurb', '"Companhia Municipal de Limpeza Urbana"']),
    ('SPTrans (SP)', ['SPTrans', '"São Paulo Transporte"']),
    ('Carris (RS)', ['Carris', '"Companhia Carris Porto-Alegrense"']),
    ('Embasa (BA)', ['Embasa', '"Empresa Baiana de Águas e Saneamento"']),
    ('Compesa (PE)', ['Compesa', '"Companhia Pernambucana de Saneamento"']),
    ('Metrô Rio', ['"Metrô Rio"', '"MetrôRio"', '"Concessão Metroviária do Rio de Janeiro"']),
    ('Prodam SP', ['"Empresa de Tecnologia da Informação e Comunicação do Município de São Paulo"', 'PRODAM']),
    ('Prodesp', ['"Companhia de Processamento de Dados do Estado de São Paulo"', 'PRODESP'])
]

classes = [
    {'codFase': 'DCG', 'desFase': 'Dissídio Coletivo de Greve'},
    {'codFase': 'DC', 'desFase': 'Dissídio Coletivo'},
    {'codFase': 'RO', 'desFase': 'Recurso Ordinário'},
    {'codFase': 'ROT', 'desFase': 'Recurso Ordinário Trabalhista'},
    {'codFase': 'RODC', 'desFase': 'Recurso Ordinário em Dissídio Coletivo'}
]

collected_by_entity = {}
all_unique_records = {}

print("Iniciando varredura full-text na SDC do TST por entidade...", flush=True)

for entity_name, queries in entities_queries:
    collected_by_entity[entity_name] = []
    print(f"\n--- Pesquisando entidade: {entity_name} ---", flush=True)
    seen_in_entity = set()
    
    for q in queries:
        offset = 1
        page_size = 30
        while True:
            payload = {
                'ou': '', 'e': q, 'termoExato': '', 'naoContem': '', 'ementa': '', 'dispositivo': '',
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
            url = f"{url_base}/{offset}/{page_size}"
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=25)
                if r.status_code != 200:
                    print(f"  Query '{q}' offset {offset} status {r.status_code}", flush=True)
                    break
                data = r.json()
                total = data.get('totalRegistros', 0)
                regs = data.get('registros', [])
                if not regs:
                    break
                
                for item in regs:
                    rec = item.get('registro', {})
                    num = rec.get('numFormatado') or rec.get('numero')
                    if not num:
                        continue
                    if num not in seen_in_entity:
                        seen_in_entity.add(num)
                        rec['matched_entity'] = entity_name
                        rec['matched_query'] = q
                        collected_by_entity[entity_name].append(rec)
                    
                    if num not in all_unique_records:
                        all_unique_records[num] = rec
                
                offset += page_size
                if offset > total or offset > 300: # safety cap
                    break
                time.sleep(0.3)
            except Exception as e:
                print(f"  Erro na query '{q}': {e}", flush=True)
                break
        time.sleep(0.3)
    
    print(f"Total únicos para {entity_name}: {len(collected_by_entity[entity_name])}", flush=True)

with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'w', encoding='utf-8') as f:
    json.dump(collected_by_entity, f, ensure_ascii=False, indent=2)

print(f"\nConcluído! Total de entidades pesquisadas: {len(entities_queries)}", flush=True)
print(f"Total de processos únicos consolidados: {len(all_unique_records)}", flush=True)
