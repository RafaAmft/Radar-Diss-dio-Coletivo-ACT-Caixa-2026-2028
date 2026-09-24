import json
import re
from bs4 import BeautifulSoup
import pandas as pd

# Load all entity records
with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Also load sdc_all_dc_dcg.json to ensure 100% coverage of all DC/DCG
with open('scraping_dissidio_coletivo_greve/sdc_all_dc_dcg.json', 'r', encoding='utf-8') as f:
    dc_dcg_records = json.load(f)

# List of target state-owned entities patterns for matching
ESTATAIS = [
    # Federais
    ('ECT / Correios', [r'Empresa Brasileira de Correios e Tel[eé]grafos', r'\bECT\b', r'\bCORREIOS\b']),
    ('Petrobras / Transpetro', [r'Petr[oó]leo Brasileiro\s+S\.?A\.?', r'\bPETROBRAS\b', r'\bTRANSPETRO\b']),
    ('Caixa Econômica Federal', [r'Caixa Econ[oô]mica Federal', r'\bCEF\b']),
    ('Banco do Brasil', [r'Banco do Brasil\s+S\.?A\.?', r'\bBANCO DO BRASIL\b']),
    ('EBSERH', [r'Empresa Brasileira de Servi[cç]os Hospitalares', r'\bEBSERH\b']),
    ('Dataprev', [r'Empresa de Tecnologia e Informa[cç][oõ]es da Previd[eê]ncia', r'\bDATAPREV\b']),
    ('Serpro', [r'Servi[cç]o Federal de Processamento de Dados', r'\bSERPRO\b']),
    ('EBC', [r'Empresa Brasil de Comunica[cç][aã]o', r'\bEBC\b']),
    ('Conab', [r'Companhia Nacional de Abastecimento', r'\bCONAB\b']),
    ('Casa da Moeda', [r'Casa da Moeda do Brasil', r'\bCASA DA MOEDA\b']),
    ('Infraero', [r'Empresa Brasileira de Infraestrutura Aeroportu[aá]ria', r'\bINFRAERO\b']),
    ('CBTU', [r'Companhia Brasileira de Trens Urbanos', r'\bCBTU\b']),
    ('Trensurb', [r'Empresa de Trens Urbanos de Porto Alegre', r'\bTRENSURB\b']),
    ('Embrapa', [r'Empresa Brasileira de Pesquisa Agropecu[aá]ria', r'\bEMBRAPA\b']),
    ('Eletrobras', [r'Centrais El[eé]tricas Brasileiras', r'\bELETROBRAS\b', r'\bELETRONORTE\b', r'\bFURNAS\b', r'\bCHESF\b', r'\bELETROSUL\b']),
    ('BNDES', [r'Banco Nacional de Desenvolvimento Econ[oô]mico e Social', r'\bBNDES\b']),
    ('Finep', [r'Financiadora de Estudos e Projetos', r'\bFINEP\b']),
    ('Codevasf', [r'Companhia de Desenvolvimento dos Vales do S[aã]o Francisco', r'\bCODEVASF\b']),
    ('Hemobrás', [r'Empresa Brasileira de Hemoderivados', r'\bHEMOBR[AÁ]S\b']),
    ('Emgepron', [r'Empresa Gerencial de Projetos Navais', r'\bEMGEPRON\b']),
    ('EPL / Infra S.A.', [r'Empresa de Planejamento e Log[ií]stica', r'\bEPL\b', r'Infra\s+S\.?A\.?', r'\bVALEC\b']),
    ('Nuclep', [r'Nuclebr[aá]s Equipamentos Pesados', r'\bNUCLEP\b']),
    ('Imbel', [r'Ind[uú]stria de Material B[eé]lico', r'\bIMBEL\b']),
    ('Ceitec', [r'Centro Nacional de Tecnologia Eletr[oô]nica Avan[cç]ada', r'\bCEITEC\b']),
    ('Telebras', [r'Telecomunica[cç][oõ]es Brasileiras', r'\bTELEBRAS\b', r'\bTELEBR[AÁ]S\b']),
    ('Banco do Nordeste', [r'Banco do Nordeste do Brasil', r'\bBNB\b']),
    ('Banco da Amazônia', [r'Banco da Amaz[oô]nia', r'\bBASA\b']),
    ('BRB', [r'Banco de Bras[ií]lia', r'\bBRB\b']),
    # Estaduais e Municipais
    ('Metrô SP', [r'Companhia do Metropolitano de S[aã]o Paulo', r'Metr[oô] de S[aã]o Paulo']),
    ('CPTM', [r'Companhia Paulista de Trens Metropolitanos', r'\bCPTM\b']),
    ('Sabesp', [r'Companhia de Saneamento B[aá]sico do Estado de S[aã]o Paulo', r'\bSABESP\b']),
    ('Cemig', [r'Companhia Energ[eé]tica de Minas Gerais', r'\bCEMIG\b']),
    ('Copasa', [r'Companhia de Saneamento de Minas Gerais', r'\bCOPASA\b']),
    ('Copel', [r'Companhia Paranaense de Energia', r'\bCOPEL\b']),
    ('Sanepar', [r'Companhia de Saneamento do Paran[aá]', r'\bSANEPAR\b']),
    ('Corsan', [r'Companhia Riograndense de Saneamento', r'\bCORSAN\b']),
    ('CEEE', [r'Companhia Estadual de Energia El[eé]trica', r'\bCEEE\b']),
    ('Caesb', [r'Companhia de Saneamento Ambiental do Distrito Federal', r'\bCAESB\b']),
    ('Metrô DF', [r'Companhia do Metropolitano do Distrito Federal', r'Metr[oô]-?DF']),
    ('Cedae', [r'Companhia Estadual de [AÁ]guas e Esgotos', r'\bCEDAE\b']),
    ('Comlurb', [r'Companhia Municipal de Limpeza Urbana', r'\bCOMLURB\b']),
    ('SPTrans', [r'S[aã]o Paulo Transporte', r'\bSPTRANS\b']),
    ('Carris', [r'Companhia Carris Porto-Alegrense', r'\bCARRIS\b']),
    ('Embasa', [r'Empresa Baiana de [AÁ]guas e Saneamento', r'\bEMBASA\b']),
    ('Compesa', [r'Companhia Pernambucana de Saneamento', r'\bCOMPESA\b']),
    ('IPT', [r'Instituto de Pesquisas Tecnol[oó]gicas', r'\bIPT\b']),
    ('CELEPAR', [r'Companhia de Tecnologia da Informa[cç][aã]o e Comunica[cç][aã]o do Paran[aá]', r'\bCELEPAR\b']),
    ('EMGERPI', [r'Empresa de Gest[aã]o de Recursos do Piau[ií]', r'\bEMGERPI\b']),
    ('PRODAM SP', [r'Empresa de Tecnologia da Informa[cç][aã]o e Comunica[cç][aã]o do Munic[ií]pio de S[aã]o Paulo', r'\bPRODAM\b']),
    ('PRODESP', [r'Companhia de Processamento de Dados do Estado de S[aã]o Paulo', r'\bPRODESP\b'])
]

TRT_MAP = {
    0: 'TST', 1: 'TRT-01 (RJ)', 2: 'TRT-02 (SP)', 3: 'TRT-03 (MG)', 4: 'TRT-04 (RS)',
    5: 'TRT-05 (BA)', 6: 'TRT-06 (PE)', 7: 'TRT-07 (CE)', 8: 'TRT-08 (PA/AP)', 9: 'TRT-09 (PR)',
    10: 'TRT-10 (DF/TO)', 11: 'TRT-11 (AM/RR)', 12: 'TRT-12 (SC)', 13: 'TRT-13 (PB)', 14: 'TRT-14 (RO/AC)',
    15: 'TRT-15 (Campinas/SP)', 16: 'TRT-16 (MA)', 17: 'TRT-17 (ES)', 18: 'TRT-18 (GO)', 19: 'TRT-19 (AL)',
    20: 'TRT-20 (SE)', 21: 'TRT-21 (RN)', 22: 'TRT-22 (PI)', 23: 'TRT-23 (MT)', 24: 'TRT-24 (MS)'
}

def extract_cnj(record):
    num = record.get('numFormatado') or record.get('numero')
    if num:
        m = re.search(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', str(num))
        if m:
            return m.group(1)
    nu = record.get('numeracaoUnica')
    if isinstance(nu, dict) and nu.get('numero'):
        return f"{nu['numero']:07d}-{nu['digito']:02d}.{nu['ano']}.{nu['orgao']}.{nu['tribunal']:02d}.{nu['vara']:04d}"
    return None

def extract_tribunal(cnj):
    if not cnj:
        return 'TST'
    m = re.search(r'\.5\.(\d{2})\.', cnj)
    if m:
        trt_num = int(m.group(1))
        return TRT_MAP.get(trt_num, f'TRT-{trt_num:02d}')
    return 'TST'

print("Mapeamento e regexes prontos.", flush=True)
