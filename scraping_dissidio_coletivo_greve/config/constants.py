"""Constantes globais do projeto de jurimetria de dissídios coletivos do TST."""

from pathlib import Path

# Diretórios estruturais
CONFIG_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CONFIG_DIR.parent
DATA_DIR = PROJECT_ROOT
OUTPUT_DIR = PROJECT_ROOT / "output"

# Mapeamento oficial de TRTs da Justiça do Trabalho (código do ramo no CNJ: .5.XX.)
TRT_MAP = {
    0: 'TST',
    1: 'TRT-01 (RJ)',
    2: 'TRT-02 (SP)',
    3: 'TRT-03 (MG)',
    4: 'TRT-04 (RS)',
    5: 'TRT-05 (BA)',
    6: 'TRT-06 (PE)',
    7: 'TRT-07 (CE)',
    8: 'TRT-08 (PA/AP)',
    9: 'TRT-09 (PR)',
    10: 'TRT-10 (DF/TO)',
    11: 'TRT-11 (AM/RR)',
    12: 'TRT-12 (SC)',
    13: 'TRT-13 (PB)',
    14: 'TRT-14 (RO/AC)',
    15: 'TRT-15 (Campinas/SP)',
    16: 'TRT-16 (MA)',
    17: 'TRT-17 (ES)',
    18: 'TRT-18 (GO)',
    19: 'TRT-19 (AL)',
    20: 'TRT-20 (SE)',
    21: 'TRT-21 (RN)',
    22: 'TRT-22 (PI)',
    23: 'TRT-23 (MT)',
    24: 'TRT-24 (MS)',
}

# Configurações de API do TST
API_BASE_URL = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

SDC_ORGAO_JUDICANTE = [
    {'codigo': 47, 'sigla': 'SDC', 'descricao': 'Seção Especializada em Dissídios Coletivos'}
]

CLASSES_DISSIDIO = [
    {'codFase': 'DCG', 'desFase': 'Dissídio Coletivo de Greve'},
    {'codFase': 'DC', 'desFase': 'Dissídio Coletivo'}
]

CLASSES_RECURSO = [
    {'codFase': 'RODC', 'desFase': 'Recurso Ordinário em Dissídio Coletivo'},
    {'codFase': 'ROT', 'desFase': 'Recurso Ordinário Trabalhista'},
    {'codFase': 'RO', 'desFase': 'Recurso Ordinário'}
]

# Catálogo canônico de empresas estatais federais, estaduais e distritais com regexes limpos (UTF-8)
ESTATAIS_INFO = [
    ('Empresa Brasileira de Correios e Telégrafos (ECT)', [
        r'Empresa Brasileira de Correios e Tel[eé]grafos',
        r'Empresa Brasileira de Correios',
        r'\bECT\b',
        r'\bCORREIOS\b'
    ]),
    ('Petróleo Brasileiro S.A. - Petrobras', [
        r'Petr[oó]leo Brasileiro\s+S\.?A\.?',
        r'\bPETROBRAS\b',
        r'\bTRANSPETRO\b'
    ]),
    ('Caixa Econômica Federal (CEF)', [
        r'Caixa Econ[oô]mica Federal',
        r'\bCEF\b'
    ]),
    ('Banco do Brasil S.A.', [
        r'Banco do Brasil\s+S\.?A\.?',
        r'\bBANCO DO BRASIL\b',
        r'\bCOBRA TECNOLOGIA\b',
        r'\bBB TECNOLOGIA\b'
    ]),
    ('Empresa Brasileira de Serviços Hospitalares (EBSERH)', [
        r'Empresa Brasileira de Servi[cç]os Hospitalares',
        r'\bEBSERH\b'
    ]),
    ('Dataprev', [
        r'Empresa de Tecnologia e Informa[cç][oõ]es da Previd[eê]ncia',
        r'\bDATAPREV\b'
    ]),
    ('Serpro', [
        r'Servi[cç]o Federal de Processamento de Dados',
        r'\bSERPRO\b'
    ]),
    ('Empresa Brasil de Comunicação (EBC)', [
        r'Empresa Brasil de Comunica[cç][aã]o',
        r'\bEBC\b'
    ]),
    ('Companhia Nacional de Abastecimento (Conab)', [
        r'Companhia Nacional de Abastecimento',
        r'\bCONAB\b'
    ]),
    ('Casa da Moeda do Brasil (CMB)', [
        r'Casa da Moeda do Brasil',
        r'Casa da Moeda',
        r'\bCASA DA MOEDA\b',
        r'\bCMB\b'
    ]),
    ('Infraero', [
        r'Empresa Brasileira de Infraestrutura Aeroportu[aá]ria',
        r'\bINFRAERO\b'
    ]),
    ('Companhia Brasileira de Trens Urbanos (CBTU)', [
        r'Companhia Brasileira de Trens Urbanos',
        r'\bCBTU\b'
    ]),
    ('Empresa de Trens Urbanos de Porto Alegre (Trensurb)', [
        r'Empresa de Trens Urbanos de Porto Alegre',
        r'\bTRENSURB\b'
    ]),
    ('Embrapa', [
        r'Empresa Brasileira de Pesquisa Agropecu[aá]ria',
        r'\bEMBRAPA\b'
    ]),
    ('Eletrobras / Subsidiárias', [
        r'Centrais El[eé]tricas Brasileiras',
        r'\bELETROBRAS\b',
        r'\bELETRONORTE\b',
        r'\bFURNAS\b',
        r'\bCHESF\b',
        r'\bELETROSUL\b'
    ]),
    ('BNDES', [
        r'Banco Nacional de Desenvolvimento Econ[oô]mico e Social',
        r'\bBNDES\b'
    ]),
    ('Finep', [
        r'Financiadora de Estudos e Projetos',
        r'\bFINEP\b'
    ]),
    ('Codevasf', [
        r'Companhia de Desenvolvimento dos Vales do S[aã]o Francisco',
        r'\bCODEVASF\b'
    ]),
    ('Hemobrás', [
        r'Empresa Brasileira de Hemoderivados',
        r'\bHEMOBR[AÁ]S\b'
    ]),
    ('Emgepron', [
        r'Empresa Gerencial de Projetos Navais',
        r'\bEMGEPRON\b'
    ]),
    ('Infra S.A. / EPL / Valec', [
        r'Empresa de Planejamento e Log[ií]stica',
        r'\bEPL\b',
        r'Infra\s+S\.?A\.?',
        r'\bVALEC\b'
    ]),
    ('Nuclep', [
        r'Nuclebr[aá]s Equipamentos Pesados',
        r'\bNUCLEP\b'
    ]),
    ('Imbel', [
        r'Ind[uú]stria de Material B[eé]lico',
        r'\bIMBEL\b'
    ]),
    ('Ceitec', [
        r'Centro Nacional de Tecnologia Eletr[oô]nica Avan[cç]ada',
        r'\bCEITEC\b'
    ]),
    ('Telebras', [
        r'Telecomunica[cç][oõ]es Brasileiras',
        r'\bTELEBRAS\b',
        r'\bTELEBR[AÁ]S\b'
    ]),
    ('Banco do Nordeste (BNB)', [
        r'Banco do Nordeste do Brasil',
        r'\bBNB\b'
    ]),
    ('Banco da Amazônia (BASA)', [
        r'Banco da Amaz[oô]nia',
        r'\bBASA\b'
    ]),
    ('BRB - Banco de Brasília', [
        r'Banco de Bras[ií]lia',
        r'\bBRB\b'
    ]),
    ('Companhia do Metropolitano de São Paulo (Metrô SP)', [
        r'Companhia do Metropolitano de S[aã]o Paulo',
        r'Metr[oô] de S[aã]o Paulo',
        r'\bMETR[OÔ]\b.*S[aã]o Paulo'
    ]),
    ('Companhia Paulista de Trens Metropolitanos (CPTM)', [
        r'Companhia Paulista de Trens Metropolitanos',
        r'\bCPTM\b'
    ]),
    ('Sabesp', [
        r'Companhia de Saneamento B[aá]sico do Estado de S[aã]o Paulo',
        r'\bSABESP\b'
    ]),
    ('Cemig', [
        r'Companhia Energ[eé]tica de Minas Gerais',
        r'\bCEMIG\b'
    ]),
    ('Copasa', [
        r'Companhia de Saneamento de Minas Gerais',
        r'\bCOPASA\b'
    ]),
    ('Copel', [
        r'Companhia Paranaense de Energia',
        r'\bCOPEL\b'
    ]),
    ('Sanepar', [
        r'Companhia de Saneamento do Paran[aá]',
        r'\bSANEPAR\b'
    ]),
    ('Corsan', [
        r'Companhia Riograndense de Saneamento',
        r'\bCORSAN\b'
    ]),
    ('CEEE', [
        r'Companhia Estadual de Energia El[eé]trica',
        r'\bCEEE\b'
    ]),
    ('Caesb', [
        r'Companhia de Saneamento Ambiental do Distrito Federal',
        r'\bCAESB\b'
    ]),
    ('Companhia do Metropolitano do DF (Metrô DF)', [
        r'Companhia do Metropolitano do Distrito Federal',
        r'Metr[oô]-?DF'
    ]),
    ('Cedae', [
        r'Companhia Estadual de [AÁ]guas e Esgotos',
        r'\bCEDAE\b'
    ]),
    ('Comlurb', [
        r'Companhia Municipal de Limpeza Urbana',
        r'\bCOMLURB\b'
    ]),
    ('SPTrans', [
        r'S[aã]o Paulo Transporte',
        r'\bSPTRANS\b'
    ]),
    ('Companhia Carris Porto-Alegrense', [
        r'Companhia Carris Porto-Alegrense',
        r'\bCARRIS\b'
    ]),
    ('Embasa', [
        r'Empresa Baiana de [AÁ]guas e Saneamento',
        r'\bEMBASA\b'
    ]),
    ('Compesa', [
        r'Companhia Pernambucana de Saneamento',
        r'\bCOMPESA\b'
    ]),
    ('Instituto de Pesquisas Tecnológicas (IPT)', [
        r'Instituto de Pesquisas Tecnol[oó]gicas',
        r'\bIPT\b'
    ]),
    ('Celepar', [
        r'Companhia de Tecnologia da Informa[cç][aã]o e Comunica[cç][aã]o do Paran[aá]',
        r'\bCELEPAR\b'
    ]),
    ('Emgerpi', [
        r'Empresa de Gest[aã]o de Recursos do Piau[ií]',
        r'\bEMGERPI\b'
    ]),
    ('Prodam SP', [
        r'Empresa de Tecnologia da Informa[cç][aã]o e Comunica[cç][aã]o do Munic[ií]pio de S[aã]o Paulo',
        r'\bPRODAM\b'
    ]),
    ('Prodesp', [
        r'Companhia de Processamento de Dados do Estado de S[aã]o Paulo',
        r'\bPRODESP\b'
    ]),
    ('Cohab PA', [
        r'Companhia de Habita[cç][aã]o do Estado do Par[aá]',
        r'\bCOHAB\b'
    ]),
]
