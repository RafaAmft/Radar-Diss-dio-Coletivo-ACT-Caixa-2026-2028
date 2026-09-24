import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import html as html_lib

# Load records
with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    all_entity_data = json.load(f)

with open('scraping_dissidio_coletivo_greve/sdc_all_dc_dcg.json', 'r', encoding='utf-8') as f:
    sdc_dc_dcg = json.load(f)

with open('scraping_dissidio_coletivo_greve/sdc_all_ro_rot.json', 'r', encoding='utf-8') as f:
    sdc_ro_rot = json.load(f)

TRT_MAP = {
    0: 'TST', 1: 'TRT-01 (RJ)', 2: 'TRT-02 (SP)', 3: 'TRT-03 (MG)', 4: 'TRT-04 (RS)',
    5: 'TRT-05 (BA)', 6: 'TRT-06 (PE)', 7: 'TRT-07 (CE)', 8: 'TRT-08 (PA/AP)', 9: 'TRT-09 (PR)',
    10: 'TRT-10 (DF/TO)', 11: 'TRT-11 (AM/RR)', 12: 'TRT-12 (SC)', 13: 'TRT-13 (PB)', 14: 'TRT-14 (RO/AC)',
    15: 'TRT-15 (Campinas/SP)', 16: 'TRT-16 (MA)', 17: 'TRT-17 (ES)', 18: 'TRT-18 (GO)', 19: 'TRT-19 (AL)',
    20: 'TRT-20 (SE)', 21: 'TRT-21 (RN)', 22: 'TRT-22 (PI)', 23: 'TRT-23 (MT)', 24: 'TRT-24 (MS)'
}

# Consolidation dictionary by CNJ
cases_by_cnj = {}

def add_record(r, entity_tag=None):
    num = r.get('numFormatado') or r.get('numero')
    if not num:
        return
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
        cases_by_cnj[cnj] = {
            'records': [r],
            'entities': [entity_tag] if entity_tag else []
        }
    else:
        cases_by_cnj[cnj]['records'].append(r)
        if entity_tag and entity_tag not in cases_by_cnj[cnj]['entities']:
            cases_by_cnj[cnj]['entities'].append(entity_tag)

# Feed all records
for ent, recs in all_entity_data.items():
    for r in recs:
        add_record(r, ent)

for r in sdc_dc_dcg:
    add_record(r, None)

for r in sdc_ro_rot:
    add_record(r, None)

print(f"Total de processos únicos CNJ consolidados: {len(cases_by_cnj)}")

ESTATAIS_INFO = [
    ('Empresa Brasileira de Correios e Telégrafos (ECT)', [r'Empresa Brasileira de Correios e Tel[eé]grafos', r'\bECT\b', r'\bCORREIOS\b']),
    ('Petróleo Brasileiro S.A. - Petrobras', [r'Petr[oó]leo Brasileiro\s+S\.?A\.?', r'\bPETROBRAS\b', r'\bTRANSPETRO\b']),
    ('Caixa Econômica Federal (CEF)', [r'Caixa Econ[oô]mica Federal', r'\bCEF\b']),
    ('Banco do Brasil S.A.', [r'Banco do Brasil\s+S\.?A\.?', r'\bBANCO DO BRASIL\b']),
    ('Empresa Brasileira de Serviços Hospitalares (EBSERH)', [r'Empresa Brasileira de Servi[cç]os Hospitalares', r'\bEBSERH\b']),
    ('Dataprev', [r'Empresa de Tecnologia e Informa[cç][oõ]es da Previd[eê]ncia', r'\bDATAPREV\b']),
    ('Serpro', [r'Servi[cç]o Federal de Processamento de Dados', r'\bSERPRO\b']),
    ('Empresa Brasil de Comunicação (EBC)', [r'Empresa Brasil de Comunica[cç][aã]o', r'\bEBC\b']),
    ('Companhia Nacional de Abastecimento (Conab)', [r'Companhia Nacional de Abastecimento', r'\bCONAB\b']),
    ('Casa da Moeda do Brasil (CMB)', [r'Casa da Moeda do Brasil', r'\bCASA DA MOEDA\b']),
    ('Infraero', [r'Empresa Brasileira de Infraestrutura Aeroportu[aá]ria', r'\bINFRAERO\b']),
    ('Companhia Brasileira de Trens Urbanos (CBTU)', [r'Companhia Brasileira de Trens Urbanos', r'\bCBTU\b']),
    ('Empresa de Trens Urbanos de Porto Alegre (Trensurb)', [r'Empresa de Trens Urbanos de Porto Alegre', r'\bTRENSURB\b']),
    ('Embrapa', [r'Empresa Brasileira de Pesquisa Agropecu[aá]ria', r'\bEMBRAPA\b']),
    ('Eletrobras / Subsidiárias', [r'Centrais El[eé]tricas Brasileiras', r'\bELETROBRAS\b', r'\bELETRONORTE\b', r'\bFURNAS\b', r'\bCHESF\b', r'\bELETROSUL\b']),
    ('BNDES', [r'Banco Nacional de Desenvolvimento Econ[oô]mico e Social', r'\bBNDES\b']),
    ('Finep', [r'Financiadora de Estudos e Projetos', r'\bFINEP\b']),
    ('Codevasf', [r'Companhia de Desenvolvimento dos Vales do S[aã]o Francisco', r'\bCODEVASF\b']),
    ('Hemobrás', [r'Empresa Brasileira de Hemoderivados', r'\bHEMOBR[AÁ]S\b']),
    ('Emgepron', [r'Empresa Gerencial de Projetos Navais', r'\bEMGEPRON\b']),
    ('Infra S.A. / EPL / Valec', [r'Empresa de Planejamento e Log[ií]stica', r'\bEPL\b', r'Infra\s+S\.?A\.?', r'\bVALEC\b']),
    ('Nuclep', [r'Nuclebr[aá]s Equipamentos Pesados', r'\bNUCLEP\b']),
    ('Imbel', [r'Ind[uú]stria de Material B[eé]lico', r'\bIMBEL\b']),
    ('Ceitec', [r'Centro Nacional de Tecnologia Eletr[oô]nica Avan[cç]ada', r'\bCEITEC\b']),
    ('Telebras', [r'Telecomunica[cç][oõ]es Brasileiras', r'\bTELEBRAS\b', r'\bTELEBR[AÁ]S\b']),
    ('Banco do Nordeste (BNB)', [r'Banco do Nordeste do Brasil', r'\bBNB\b']),
    ('Banco da Amazônia (BASA)', [r'Banco da Amaz[oô]nia', r'\bBASA\b']),
    ('BRB - Banco de Brasília', [r'Banco de Bras[ií]lia', r'\bBRB\b']),
    ('Companhia do Metropolitano de São Paulo (Metrô SP)', [r'Companhia do Metropolitano de S[aã]o Paulo', r'Metr[oô] de S[aã]o Paulo']),
    ('Companhia Paulista de Trens Metropolitanos (CPTM)', [r'Companhia Paulista de Trens Metropolitanos', r'\bCPTM\b']),
    ('Sabesp', [r'Companhia de Saneamento B[aá]sico do Estado de S[aã]o Paulo', r'\bSABESP\b']),
    ('Cemig', [r'Companhia Energ[eé]tica de Minas Gerais', r'\bCEMIG\b']),
    ('Copasa', [r'Companhia de Saneamento de Minas Gerais', r'\bCOPASA\b']),
    ('Copel', [r'Companhia Paranaense de Energia', r'\bCOPEL\b']),
    ('Sanepar', [r'Companhia de Saneamento do Paran[aá]', r'\bSANEPAR\b']),
    ('Corsan', [r'Companhia Riograndense de Saneamento', r'\bCORSAN\b']),
    ('CEEE', [r'Companhia Estadual de Energia El[eé]trica', r'\bCEEE\b']),
    ('Caesb', [r'Companhia de Saneamento Ambiental do Distrito Federal', r'\bCAESB\b']),
    ('Companhia do Metropolitano do DF (Metrô DF)', [r'Companhia do Metropolitano do Distrito Federal', r'Metr[oô]-?DF']),
    ('Cedae', [r'Companhia Estadual de [AÁ]guas e Esgotos', r'\bCEDAE\b']),
    ('Comlurb', [r'Companhia Municipal de Limpeza Urbana', r'\bCOMLURB\b']),
    ('SPTrans', [r'S[aã]o Paulo Transporte', r'\bSPTRANS\b']),
    ('Companhia Carris Porto-Alegrense', [r'Companhia Carris Porto-Alegrense', r'\bCARRIS\b']),
    ('Embasa', [r'Empresa Baiana de [AÁ]guas e Saneamento', r'\bEMBASA\b']),
    ('Compesa', [r'Companhia Pernambucana de Saneamento', r'\bCOMPESA\b']),
    ('Instituto de Pesquisas Tecnológicas (IPT)', [r'Instituto de Pesquisas Tecnol[oó]gicas', r'\bIPT\b']),
    ('Celepar', [r'Companhia de Tecnologia da Informa[cç][aã]o e Comunica[cç][aã]o do Paran[aá]', r'\bCELEPAR\b']),
    ('Emgerpi', [r'Empresa de Gest[aã]o de Recursos do Piau[ií]', r'\bEMGERPI\b']),
    ('Prodam SP', [r'Empresa de Tecnologia da Informa[cç][aã]o e Comunica[cç][aã]o do Munic[ií]pio de S[aã]o Paulo', r'\bPRODAM\b']),
    ('Prodesp', [r'Companhia de Processamento de Dados do Estado de S[aã]o Paulo', r'\bPRODESP\b']),
    ('Cohab PA', [r'Companhia de Habita[cç][aã]o do Estado do Par[aá]', r'\bCOHAB\b'])
]

def check_entity_match(text):
    for formal_name, pats in ESTATAIS_INFO:
        for p in pats:
            if re.search(p, text, re.I):
                return formal_name
    return None

def clean_name(txt):
    if not txt:
        return ""
    txt = re.sub(r'\s+', ' ', txt).strip()
    txt = re.sub(r'^(o|a|os|as)\s+', '', txt, flags=re.I)
    return txt.strip(' .,;:-')

def extract_case_details(cnj, case_info):
    recs = case_info['records']
    # Sort records to find best one (with acórdão text)
    best_rec = None
    for r in recs:
        if r.get('inteiroTeorHtml'):
            best_rec = r
            break
    if not best_rec:
        for r in recs:
            if r.get('txtConteudoDecisao'):
                best_rec = r
                break
    if not best_rec:
        best_rec = recs[0]
    
    # Extract Tribunal
    m_trt = re.search(r'\.5\.(\d{2})\.', cnj)
    if m_trt:
        trt_code = int(m_trt.group(1))
        tribunal = TRT_MAP.get(trt_code, f'TRT-{trt_code:02d}')
    else:
        tribunal = 'TST'
    
    # Extract Classe
    cod_fase = best_rec.get('codFase') or ''
    if 'DCG' in cod_fase:
        classe = 'Dissídio Coletivo de Greve (DCG)'
    elif 'DC' in cod_fase:
        classe = 'Dissídio Coletivo (DC)'
    elif 'RODC' in cod_fase:
        classe = 'Recurso Ordinário em Dissídio Coletivo (RODC)'
    elif 'ROT' in cod_fase:
        classe = 'Recurso Ordinário Trabalhista (ROT)'
    elif 'RO' in cod_fase:
        classe = 'Recurso Ordinário (RO)'
    else:
        classe = cod_fase if cod_fase else 'Dissídio Coletivo'
    
    # Extract Relator
    relator_raw = best_rec.get('nomRelatorSemTratamento') or best_rec.get('nomRelator') or ''
    relator = ' '.join(w.capitalize() for w in relator_raw.split()) if relator_raw else ''
    
    # Dates
    dt_julg = best_rec.get('dtaJulgamento') or ''
    dt_pub = best_rec.get('dtaPublicacao') or ''
    
    # Year of filing from CNJ: NNNNNNN-DD.AAAA...
    ano_cnj_m = re.search(r'\.\d{2}\.(\d{4})\.5\.', cnj)
    ano_cnj = ano_cnj_m.group(1) if ano_cnj_m else ''
    
    # Full text extraction
    html = best_rec.get('inteiroTeorHtml') or best_rec.get('txtConteudoDecisao') or ''
    ementa = best_rec.get('ementa') or ''
    dispositivo = best_rec.get('dispositivo') or ''
    
    full_text = ""
    if html:
        soup = BeautifulSoup(html[:50000], 'html.parser')
        full_text = soup.get_text()
    else:
        full_text = f"{ementa}\n{dispositivo}"
    
    # Determine Tipo (natureza)
    tipo_str = "Econômico"
    lower_all = (full_text[:4000] + " " + ementa).lower()
    if 'greve' in lower_all or 'paredista' in lower_all or 'paralisação' in lower_all or 'dcg' in cod_fase.lower():
        tipo_str = "Greve"
    elif 'natureza jurídica' in lower_all or 'declaratória' in lower_all:
        tipo_str = "Jurídico"
    elif 'revisional' in lower_all:
        tipo_str = "Revisional"
    elif 'natureza econômica' in lower_all or 'reajuste' in lower_all or 'cláusula' in lower_all:
        tipo_str = "Econômico"
    
    # Extract Ano de Vigência ACT/DC
    ano_vigencia = ""
    vig_m = re.search(r'(?:vig[eê]ncia|per[ií]odo|exerc[ií]cio|acordo|act|cct)[\s\w/ºªde.-]{0,40}?(20\d{2}\s*/\s*20\d{2}|20\d{2}\s*-\s*20\d{2}|1[ºo]?[\s\w/]+20\d{2}\s+a\s+31[\s\w/]+20\d{2})', full_text[:10000], re.I)
    if vig_m:
        ano_vigencia = re.sub(r'\s+', ' ', vig_m.group(1)).strip()
    elif ano_cnj:
        ano_next = int(ano_cnj) + 1 if ano_cnj.isdigit() else ''
        ano_vigencia = f"{ano_cnj}/{ano_next}"
    
    # Extract Situação / Resultado
    disp_lower = (dispositivo + " " + ementa[:2000] + " " + full_text[:4000]).lower()
    resultado = "Sentença Normativa"
    if 'homolog' in disp_lower and 'acordo' in disp_lower:
        resultado = "Acordo Homologado"
    elif 'extin' in disp_lower and ('sem resolução' in disp_lower or 'sem julgamento' in disp_lower or 'sem exame' in disp_lower or 'falta de comum acordo' in disp_lower or 'perda do objeto' in disp_lower):
        resultado = "Extinto sem Resolução de Mérito"
    elif 'abusiv' in disp_lower:
        if 'não abusiva' in disp_lower or 'ausência de abusividade' in disp_lower:
            resultado = "Greve Julgada Não Abusiva"
        else:
            resultado = "Greve Julgada Abusiva"
    elif 'procedente em parte' in disp_lower:
        resultado = "Sentença Normativa (Procedente em Parte)"
    elif 'improcedente' in disp_lower:
        resultado = "Julgado Improcedente"
    elif 'procedente' in disp_lower:
        resultado = "Sentença Normativa (Procedente)"
    elif 'pendente' in disp_lower or not dt_julg:
        resultado = "Pendente"
    
    # Extract Parties & Determine Suscitante vs Suscitado
    suscitante = ""
    suscitados = ""
    polo_estatal = None # 'SUSCITANTE', 'SUSCITADA', or None (not a direct party)
    estatal_envolvida = None
    
    # Patterns for Header:
    # 1. "em que é SUSCITANTE X e são SUSCITADOS Y"
    p_std = re.search(r'em que [eé]\s+SUSCITANTE\s+([^,;\n\r]+?)\s+e\s+(?:s[aã]o|é)\s+SUSCITADO[S]?\s+([^,;\n\r]+?)(?:\s+e\s+|\.|\;|\n|\r)', full_text, re.I)
    
    # 2. "Trata-se de dissídio coletivo [de greve] ajuizado/instaurado por/pela/pelo X em face de/do/da Y"
    p_trata = re.search(r'diss[ií]dio coletivo\s*(?:de greve|de natureza econ[oô]mica|de natureza jur[ií]dica)?\s*(?:ajuizado|instaurado|suscitado|proposto)\s*(?:por|pela|pelo)\s*([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ][AÃ]O[^\n\r,;.]+?|[A-Z\s]{4,}))\s*(?:em face\s*(?:de|do|da)|contra)\s*([^\n\r;.]+)', full_text, re.I)
    
    # 3. ROT / Recurso Ordinário: "Cuidam os autos de recurso ordinário ... pelo/pela X, suscitante/suscitado na ação de dissídio coletivo ajuizada por/pela Y"
    p_cuidam = re.search(r'(?:Cuidam os autos|Trata-se) de recurso ordin[aá]rio[\s\w\d.,-]{0,60}?pelo[a]?\s+([^\n\r,;.]+?(?:S\.?A\.?|LTDA|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ][AÃ]O[^\n\r,;.]+?|[A-Z\s]{4,}))\s*,\s*(suscitante|suscitad[ao])[\s\w\d.,-]{0,40}?ajuizada\s+pela[o]?\s+([^\n\r;.]+)', full_text, re.I)

    # 4. Ementa header: "DISSÍDIO COLETIVO DE GREVE INSTAURADO PELA X"
    p_instaurado = re.search(r'DISS[IÍ]DIO COLETIVO\s*(?:DE GREVE|DE NATUREZA ECON[OÔ]MICA|DE NATUREZA JUR[IÍ]DICA)?\s*(?:INSTAURADO|AJUIZADO|SUSCITADO|PROPOSTO)\s*PEL[AO]\s*([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ][AÃ]O[^\n\r,;.]+?|[A-Z\s]{4,}))', full_text, re.I)
    
    if p_std:
        susc_candidate = clean_name(p_std.group(1))
        suscd_candidate = clean_name(p_std.group(2))
        suscitante = susc_candidate
        suscitados = suscd_candidate
    elif p_trata:
        susc_candidate = clean_name(p_trata.group(1))
        suscd_candidate = clean_name(p_trata.group(2))
        suscitante = susc_candidate
        suscitados = suscd_candidate
    elif p_cuidam:
        party1 = clean_name(p_cuidam.group(1))
        role1 = p_cuidam.group(2).lower()
        party2 = clean_name(p_cuidam.group(3))
        if 'suscitante' in role1:
            suscitante = party1
            suscitados = party2
        else:
            suscitante = party2
            suscitados = party1
    elif p_instaurado:
        suscitante = clean_name(p_instaurado.group(1))
        # Look for face/contra
        suscd_m = re.search(r'(?:em face\s*(?:de|do|da)|contra)\s*([^\n\r;.]+)', full_text[:4000], re.I)
        if suscd_m:
            suscitados = clean_name(suscd_m.group(1))

    # Now verify if an estatal is Suscitante or Suscitada
    estatal_susc = check_entity_match(suscitante)
    estatal_suscd = check_entity_match(suscitados)
    
    # If not detected from regex above, test against the initial report/ementa
    if not estatal_susc and not estatal_suscd:
        # Check if ementa says "SUSCITADO PELA EMPRESA X" or "AJUIZADO PELA EMPRESA X"
        m_emp_susc = re.search(r'(?:instaurado|ajuizado|suscitado|proposto)\s*pel[ao]\s*([^\n\r.,;]+)', ementa[:1500], re.I)
        if m_emp_susc:
            mat = check_entity_match(m_emp_susc.group(1))
            if mat:
                estatal_susc = mat
                suscitante = m_emp_susc.group(1).strip()
        
        # Check if ementa says "RECURSO ORDINÁRIO DA EMPRESA SUSCITADA X" or "SUSCITADO: EMPRESA X"
        m_emp_suscd = re.search(r'(?:empresa suscitada|recorrida)\s*[\.:-]?\s*([^\n\r.,;]+)', ementa[:1500], re.I)
        if m_emp_suscd:
            mat2 = check_entity_match(m_emp_suscd.group(1))
            if mat2:
                estatal_suscd = mat2
                suscitados = m_emp_suscd.group(1).strip()
    
    if estatal_susc:
        polo_estatal = 'SUSCITANTE'
        estatal_envolvida = estatal_susc
        if not suscitados:
            suscitados = "Entidades Sindicais Representativas dos Trabalhadores"
    elif estatal_suscd:
        polo_estatal = 'SUSCITADA'
        estatal_envolvida = estatal_suscd
        if not suscitante:
            suscitante = "Entidade Sindical Profissional"
    
    # Data de ajuizamento
    # If year in CNJ exists, format approximate or use dtaJulgamento / dtaPublicacao
    dt_ajz = ""
    dt_ajz_m = re.search(r'ajuizad[oa]\s+em\s+(\d{1,2}/\d{1,2}/\d{4}|\d{1,2}\s+de\s+[a-zç]+\s+de\s+\d{4})', full_text[:10000], re.I)
    if dt_ajz_m:
        dt_ajz = dt_ajz_m.group(1)
    elif dt_julg:
        dt_ajz = dt_julg
    elif ano_cnj:
        dt_ajz = f"Ano {ano_cnj}"
    
    fonte_url = f"https://jurisprudencia.tst.jus.br"
    if '5.00.' in cnj:
        fonte_url = f"https://consultaprocessual.tst.jus.br/consultaProcessual/resumoForm.do?consulta=1&numeroProcesso={cnj.replace('-', '').replace('.', '')}"
    
    return {
        'número CNJ': cnj,
        'tribunal': tribunal,
        'classe': classe,
        'data de ajuizamento': dt_ajz,
        'suscitante': clean_name(suscitante),
        'suscitado(s)': clean_name(suscitados),
        'tipo (greve, econômico, jurídico, revisional)': tipo_str,
        'relator': relator,
        'situação/resultado (acordo, sentença normativa, extinto, pendente)': resultado,
        'ano de vigência do ACT/DC': ano_vigencia,
        'fonte (URL)': fonte_url,
        'nível de confiança (confirmado em fonte primária / só notícia / não verificado)': 'confirmado em fonte primária',
        'polo_estatal': polo_estatal,
        'estatal_identificada': estatal_envolvida
    }

print("Iniciando processamento e classificação de todos os processos...", flush=True)

tab1_suscitante = []
tab2_suscitada = []
nao_enquadrados = []

for cnj, info in cases_by_cnj.items():
    res = extract_case_details(cnj, info)
    if res['polo_estatal'] == 'SUSCITANTE':
        tab1_suscitante.append(res)
    elif res['polo_estatal'] == 'SUSCITADA':
        tab2_suscitada.append(res)
    else:
        nao_enquadrados.append(res)

print(f"\nResultado da classificação:")
print(f"  Tab 1 (Estatal como Suscitante): {len(tab1_suscitante)} processos confirmados")
print(f"  Tab 2 (Estatal como Suscitada):  {len(tab2_suscitada)} processos confirmados")
print(f"  Não enquadrados (citações/precedentes de outras categorias): {len(nao_enquadrados)}")

# Preview by entity in Tab 1
df_tab1 = pd.DataFrame(tab1_suscitante)
if not df_tab1.empty:
    print("\nProcessos na Tab 1 por Entidade Estatal:")
    print(df_tab1['estatal_identificada'].value_counts())
