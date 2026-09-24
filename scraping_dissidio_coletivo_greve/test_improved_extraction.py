import json
import re
from datetime import datetime

with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    all_entity_data = json.load(f)

with open('scraping_dissidio_coletivo_greve/sdc_all_dc_dcg.json', 'r', encoding='utf-8') as f:
    sdc_dc_dcg = json.load(f)

with open('scraping_dissidio_coletivo_greve/sdc_all_ro_rot.json', 'r', encoding='utf-8') as f:
    sdc_ro_rot = json.load(f)

cases_by_cnj = {}
def add_record(r, entity_tag=None):
    num = r.get('numFormatado') or r.get('numero')
    if not num: return
    cnj_match = re.search(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', str(num))
    if cnj_match:
        cnj = cnj_match.group(1)
    else:
        nu = r.get('numeracaoUnica')
        if isinstance(nu, dict) and nu.get('numero'):
            cnj = f"{nu['numero']:07d}-{nu['digito']:02d}.{nu['ano']}.{nu['orgao']}.{nu['tribunal']:02d}.{nu['vara']:04d}"
        else:
            return
    if cnj not in cases_by_cnj:
        cases_by_cnj[cnj] = {'records': [r], 'entities': [entity_tag] if entity_tag else []}
    else:
        cases_by_cnj[cnj]['records'].append(r)
        if entity_tag and entity_tag not in cases_by_cnj[cnj]['entities']:
            cases_by_cnj[cnj]['entities'].append(entity_tag)

for ent, recs in all_entity_data.items():
    for r in recs: add_record(r, ent)
for r in sdc_dc_dcg: add_record(r, None)
for r in sdc_ro_rot: add_record(r, None)

print(f"Total casos agregados: {len(cases_by_cnj)}")

ESTATAIS_INFO = [
    ('Empresa Brasileira de Correios e Telégrafos (ECT)', [r'Empresa Brasileira de Correios', r'\bECT\b', r'\bCORREIOS\b']),
    ('Petróleo Brasileiro S.A. - Petrobras', [r'Petr[oó\ufffd]leo Brasileiro', r'\bPETROBRAS\b', r'\bTRANSPETRO\b']),
    ('Caixa Econômica Federal (CEF)', [r'Caixa Econ[oô\ufffd]mica Federal', r'\bCEF\b']),
    ('Banco do Brasil S.A.', [r'Banco do Brasil', r'\bCOBRA TECNOLOGIA\b', r'\bBB TECNOLOGIA\b']),
    ('Empresa Brasileira de Serviços Hospitalares (EBSERH)', [r'Empresa Brasileira de Servi[cç\ufffd]os Hospitalares', r'\bEBSERH\b']),
    ('Dataprev', [r'Empresa de Tecnologia e Informa[cç\ufffd][oõ\ufffd]es da Previd[eê\ufffd]ncia', r'\bDATAPREV\b']),
    ('Serpro', [r'Servi[cç\ufffd]o Federal de Processamento de Dados', r'\bSERPRO\b']),
    ('Empresa Brasil de Comunicação (EBC)', [r'Empresa Brasil de Comunica[cç\ufffd][aã\ufffd]o', r'\bEBC\b']),
    ('Companhia Nacional de Abastecimento (Conab)', [r'Companhia Nacional de Abastecimento', r'\bCONAB\b']),
    ('Casa da Moeda do Brasil (CMB)', [r'Casa da Moeda', r'\bCMB\b']),
    ('Infraero', [r'Empresa Brasileira de Infraestrutura Aeroportu[aá\ufffd]ria', r'\bINFRAERO\b']),
    ('Companhia Brasileira de Trens Urbanos (CBTU)', [r'Companhia Brasileira de Trens Urbanos', r'\bCBTU\b']),
    ('Empresa de Trens Urbanos de Porto Alegre (Trensurb)', [r'Empresa de Trens Urbanos de Porto Alegre', r'\bTRENSURB\b']),
    ('Embrapa', [r'Empresa Brasileira de Pesquisa Agropecu[aá\ufffd]ria', r'\bEMBRAPA\b']),
    ('Eletrobras / Subsidiárias', [r'Centrais El[eé\ufffd]tricas Brasileiras', r'\bELETROBRAS\b', r'\bELETRONORTE\b', r'\bFURNAS\b', r'\bCHESF\b', r'\bELETROSUL\b']),
    ('BNDES', [r'Banco Nacional de Desenvolvimento Econ[oô\ufffd]mico e Social', r'\bBNDES\b']),
    ('Finep', [r'Financiadora de Estudos e Projetos', r'\bFINEP\b']),
    ('Codevasf', [r'Companhia de Desenvolvimento dos Vales do S[aã\ufffd]o Francisco', r'\bCODEVASF\b']),
    ('Hemobrás', [r'Empresa Brasileira de Hemoderivados', r'\bHEMOBR[AÁ\ufffd]S\b']),
    ('Emgepron', [r'Empresa Gerencial de Projetos Navais', r'\bEMGEPRON\b']),
    ('Infra S.A. / EPL / Valec', [r'Empresa de Planejamento e Log[ií\ufffd]stica', r'\bEPL\b', r'Infra\s+S\.?A\.?', r'\bVALEC\b']),
    ('Nuclep', [r'Nuclebr[aá\ufffd]s Equipamentos Pesados', r'\bNUCLEP\b']),
    ('Imbel', [r'Ind[uú\ufffd]stria de Material B[eé\ufffd]lico', r'\bIMBEL\b']),
    ('Ceitec', [r'Centro Nacional de Tecnologia Eletr[oô\ufffd]nica Avan[cç\ufffd]ada', r'\bCEITEC\b']),
    ('Telebras', [r'Telecomunica[cç\ufffd][oõ\ufffd]es Brasileiras', r'\bTELEBRAS\b', r'\bTELEBR[AÁ\ufffd]S\b']),
    ('Banco do Nordeste (BNB)', [r'Banco do Nordeste do Brasil', r'\bBNB\b']),
    ('Banco da Amazônia (BASA)', [r'Banco da Amaz[oô\ufffd]nia', r'\bBASA\b']),
    ('BRB - Banco de Brasília', [r'Banco de Bras[ií\ufffd]lia', r'\bBRB\b']),
    ('Companhia do Metropolitano de São Paulo (Metrô SP)', [r'Companhia do Metropolitano de S[aã\ufffd]o Paulo', r'Metr[oô\ufffd] de S[aã\ufffd]o Paulo', r'\bMETR[OÔ\ufffd]\b.*S[aã\ufffd]o Paulo']),
    ('Companhia Paulista de Trens Metropolitanos (CPTM)', [r'Companhia Paulista de Trens Metropolitanos', r'\bCPTM\b']),
    ('Sabesp', [r'Companhia de Saneamento B[aá\ufffd]sico do Estado de S[aã\ufffd]o Paulo', r'\bSABESP\b']),
    ('Cemig', [r'Companhia Energ[eé\ufffd]tica de Minas Gerais', r'\bCEMIG\b']),
    ('Copasa', [r'Companhia de Saneamento de Minas Gerais', r'\bCOPASA\b']),
    ('Copel', [r'Companhia Paranaense de Energia', r'\bCOPEL\b']),
    ('Sanepar', [r'Companhia de Saneamento do Paran[aá\ufffd]', r'\bSANEPAR\b']),
    ('Corsan', [r'Companhia Riograndense de Saneamento', r'\bCORSAN\b']),
    ('CEEE', [r'Companhia Estadual de Energia El[eé\ufffd]trica', r'\bCEEE\b']),
    ('Caesb', [r'Companhia de Saneamento Ambiental do Distrito Federal', r'\bCAESB\b']),
    ('Companhia do Metropolitano do DF (Metrô DF)', [r'Companhia do Metropolitano do Distrito Federal', r'Metr[oô\ufffd]-?DF']),
    ('Cedae', [r'Companhia Estadual de [AÁ\ufffd]guas e Esgotos', r'\bCEDAE\b']),
    ('Comlurb', [r'Companhia Municipal de Limpeza Urbana', r'\bCOMLURB\b']),
    ('SPTrans', [r'S[aã\ufffd]o Paulo Transporte', r'\bSPTRANS\b']),
    ('Companhia Carris Porto-Alegrense', [r'Companhia Carris Porto-Alegrense', r'\bCARRIS\b']),
    ('Embasa', [r'Empresa Baiana de [AÁ\ufffd]guas e Saneamento', r'\bEMBASA\b']),
    ('Compesa', [r'Companhia Pernambucana de Saneamento', r'\bCOMPESA\b']),
    ('Instituto de Pesquisas Tecnológicas (IPT)', [r'Instituto de Pesquisas Tecnol[oó\ufffd]gicas', r'\bIPT\b']),
    ('Celepar', [r'Companhia de Tecnologia da Informa[cç\ufffd][aã\ufffd]o e Comunica[cç\ufffd][aã\ufffd]o do Paran[aá\ufffd]', r'\bCELEPAR\b']),
    ('Emgerpi', [r'Empresa de Gest[aã\ufffd]o de Recursos do Piau[ií\ufffd]', r'\bEMGERPI\b']),
    ('Prodam SP', [r'Empresa de Tecnologia da Informa[cç\ufffd][aã\ufffd]o e Comunica[cç\ufffd][aã\ufffd]o do Munic[ií\ufffd]pio de S[aã\ufffd]o Paulo', r'\bPRODAM\b']),
    ('Prodesp', [r'Companhia de Processamento de Dados do Estado de S[aã\ufffd]o Paulo', r'\bPRODESP\b']),
    ('Cohab PA', [r'Companhia de Habita[cç\ufffd][aã\ufffd]o do Estado do Par[aá\ufffd]', r'\bCOHAB\b'])
]

def check_entity_match(text):
    if not text: return None
    for formal_name, pats in ESTATAIS_INFO:
        for p in pats:
            if re.search(p, text, re.I):
                return formal_name
    return None

tab1 = []
tab2 = []

for cnj, info in cases_by_cnj.items():
    # Year filter
    ano_m = re.search(r'\.\d{2}\.(\d{4})\.5\.', cnj)
    ano_proc = int(ano_m.group(1)) if ano_m else None
    if ano_proc and (ano_proc < 2016 or ano_proc > 2026):
        continue
    
    # Concatenate texts of all records for this CNJ
    full_text_blocks = []
    for r in info['records']:
        t = r.get('inteiroTeorHtml') or r.get('txtConteudoDecisao') or r.get('txtConteudoDecisaoHighlight') or ''
        if t:
            clean = re.sub(r'<[^>]+>', ' ', t)
            clean = re.sub(r'\s+', ' ', clean)
            full_text_blocks.append(clean)
        em = r.get('ementa') or ''
        if em:
            full_text_blocks.append(em)
    
    combined_text = "\n".join(full_text_blocks)
    if not combined_text:
        continue
    
    # Try multiple patterns for Suscitante and Suscitado
    susc = ""
    suscd = ""
    
    # Pattern 1: SUSCITANTE: ... e são SUSCITADOS ...
    m1 = re.search(r'SUSCITANTE[:\s]+([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|[A-Z\s]{4,}))\s+e\s+(?:s[aã\ufffd]o|[eé\ufffd\?])\s+SUSCITADO[S]?[:\s]+([^,;\n\r.]+)', combined_text, re.I)
    
    # Pattern 2: SUSCITANTE: ... SUSCITADO: ...
    m2 = re.search(r'SUSCITANTE\s*:\s*([^\n\r]+?)(?:SUSCITAD[AO][S]?|REQUERID[AO]|\n|\r)', combined_text, re.I)
    m2_d = re.search(r'SUSCITAD[AO][S]?\s*:\s*([^\n\r]+?)(?:DESPACHO|AC[OÓ\ufffd]RD[AÃ\ufffd]O|RELAT[OÓ\ufffd]RIO|TERCEIRO|\n|\r)', combined_text, re.I)
    
    # Pattern 3: DISSÍDIO COLETIVO ... INSTAURADO/AJUIZADO PELO/PELA X EM FACE DE Y
    m3 = re.search(r'DISS[IÍ\ufffd]DIO COLETIVO[\s\w-]{0,30}?(?:INSTAURADO|AJUIZADO|SUSCITADO|PROPOSTO)\s*PEL[AO]\s*([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ\ufffd][AÃ\ufffd]O[^\n\r,;.]+?|[A-Z\s]{4,}))\s*(?:EM FACE\s*(?:DE|DO|DA)|CONTRA)\s*([^\n\r;.]+)', combined_text, re.I)

    # Pattern 4: Recurso Ordinário pelo X, suscitante/suscitado na ação de dissídio coletivo ajuizada pela Y
    m4 = re.search(r'(?:Cuidam os autos|Trata-se) de recurso ordin[aá\ufffd]rio[\s\w\d.,-]{0,60}?pelo[a]?\s+([^\n\r,;.]+?(?:S\.?A\.?|LTDA|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ\ufffd][AÃ\ufffd]O[^\n\r,;.]+?|[A-Z\s]{4,}))\s*,\s*(suscitante|suscitad[ao])[\s\w\d.,-]{0,40}?ajuizada\s+pela[o]?\s+([^\n\r;.]+)', combined_text, re.I)

    if m1:
        susc = m1.group(1).strip()
        suscd = m1.group(2).strip()
    elif m2 and m2_d:
        susc = m2.group(1).strip()
        suscd = m2_d.group(1).strip()
    elif m4:
        p1 = m4.group(1).strip()
        role1 = m4.group(2).lower()
        p2 = m4.group(3).strip()
        if 'suscitante' in role1:
            susc = p1
            suscd = p2
        else:
            susc = p2
            suscd = p1
    elif m3:
        susc = m3.group(1).strip()
        suscd = m3.group(2).strip()
    
    # Match entities
    est_susc = check_entity_match(susc)
    est_suscd = check_entity_match(suscd)
    
    # Fallback if only one party was found
    if not est_susc and not est_suscd:
        # Check if ementa says "INSTAURADO PELA EMPRESA X"
        m_inst = re.search(r'DISS[IÍ\ufffd]DIO COLETIVO[\s\w-]{0,30}?(?:INSTAURADO|AJUIZADO|SUSCITADO|PROPOSTO)\s*PEL[AO]\s*([^\n\r.,;]+)', combined_text[:2000], re.I)
        if m_inst:
            mat = check_entity_match(m_inst.group(1))
            if mat:
                est_susc = mat
                susc = m_inst.group(1).strip()
                suscd = "Entidades Sindicais Representativas dos Trabalhadores"
    
    if est_susc:
        tab1.append((cnj, est_susc, susc, suscd))
    elif est_suscd:
        tab2.append((cnj, est_suscd, susc, suscd))

print(f"\nResultados após regex aprimorada:")
print(f"Tab 1 (Estatal Suscitante): {len(tab1)}")
print(f"Tab 2 (Estatal Suscitada):  {len(tab2)}")

from collections import Counter
c1 = Counter([x[1] for x in tab1])
print("\nTab 1 por entidade:")
for k, v in c1.most_common():
    print(f"  {k}: {v}")
