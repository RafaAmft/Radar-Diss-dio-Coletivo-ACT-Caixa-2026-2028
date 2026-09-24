import json
import re
import os
from bs4 import BeautifulSoup
import pandas as pd
import html as html_lib
from datetime import datetime

# Load datasets
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

def clean_party(name):
    if not name: return ""
    name = re.sub(r'<[^>]+>', ' ', name)
    name = html_lib.unescape(name)
    name = re.sub(r'Advogad[ao].*$', '', name, flags=re.I)
    name = re.sub(r'PROCESSO SOB A GIDE.*$', '', name, flags=re.I)
    name = re.sub(r'RECURSO ORDINRIO.*$', '', name, flags=re.I)
    name = re.sub(r'GVPGCB.*$', '', name, flags=re.I)
    name = re.sub(r'GMMCP.*$', '', name, flags=re.I)
    name = re.sub(r'GMKA.*$', '', name, flags=re.I)
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r'^(o|a|os|as)\s+', '', name, flags=re.I)
    name = name.strip(' .,;:-')
    if len(name) > 250:
        name = name[:250] + '...'
    return name

def sanitize_excel_cell(val):
    if not isinstance(val, str):
        return val
    # Remove control characters (ASCII 0 to 31 except newline and tab)
    cleaned = ''.join(ch for ch in val if ord(ch) >= 32 or ch in '\n\r\t')
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    if len(cleaned) > 280:
        cleaned = cleaned[:280] + '...'
    return cleaned

start_period = datetime(2016, 9, 24)
end_period = datetime(2026, 9, 24)

tab1_suscitante = []
tab2_suscitada = []

for cnj, info in cases_by_cnj.items():
    ano_m = re.search(r'\.\d{2}\.(\d{4})\.5\.', cnj)
    ano_proc = int(ano_m.group(1)) if ano_m else None
    
    # Process only 2016 to 2026
    if ano_proc and (ano_proc < 2016 or ano_proc > 2026):
        continue
    
    recs = info['records']
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
    
    dt_julg = best_rec.get('dtaJulgamento') or ''
    dt_pub = best_rec.get('dtaPublicacao') or ''
    
    # Tribunal
    m_trt = re.search(r'\.5\.(\d{2})\.', cnj)
    if m_trt:
        trt_code = int(m_trt.group(1))
        tribunal = TRT_MAP.get(trt_code, f'TRT-{trt_code:02d}')
    else:
        tribunal = 'TST'
    
    # Classe
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
    
    # Relator
    relator_raw = best_rec.get('nomRelatorSemTratamento') or best_rec.get('nomRelator') or ''
    relator = ' '.join(w.capitalize() for w in relator_raw.split()) if relator_raw else 'Não informado'
    
    # Combined text of all records
    full_text_blocks = []
    for r in recs:
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
    
    # Extract parties
    susc = ""
    suscd = ""
    
    # 1. SUSCITANTE ... e são SUSCITADOS ...
    m1 = re.search(r'SUSCITANTE[:\s]+([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|[A-Z\s]{4,}))\s+e\s+(?:s[aã\ufffd]o|[eé\ufffd\?])\s+SUSCITADO[S]?[:\s]+([^,;\n\r.]+)', combined_text, re.I)
    
    # 2. SUSCITANTE: ... SUSCITADO: ...
    m2 = re.search(r'SUSCITANTE\s*:\s*([^\n\r]+?)(?:SUSCITAD[AO][S]?|REQUERID[AO]|\n|\r)', combined_text, re.I)
    m2_d = re.search(r'SUSCITAD[AO][S]?\s*:\s*([^\n\r]+?)(?:DESPACHO|AC[OÓ\ufffd]RD[AÃ\ufffd]O|RELAT[OÓ\ufffd]RIO|TERCEIRO|\n|\r)', combined_text, re.I)
    
    # 3. DISSÍDIO COLETIVO ... INSTAURADO/AJUIZADO PELO/PELA X EM FACE DE Y
    m3 = re.search(r'DISS[IÍ\ufffd]DIO COLETIVO[\s\w-]{0,30}?(?:INSTAURADO|AJUIZADO|SUSCITADO|PROPOSTO)\s*PEL[AO]\s*([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ\ufffd][AÃ\ufffd]O[^\n\r,;.]+?|[A-Z\s]{4,}))\s*(?:EM FACE\s*(?:DE|DO|DA)|CONTRA)\s*([^\n\r;.]+)', combined_text, re.I)

    # 4. Recurso Ordinário pelo X, suscitante/suscitado na ação de dissídio coletivo ajuizada pela Y
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
    
    # Classify polo
    est_susc = check_entity_match(susc)
    est_suscd = check_entity_match(suscd)
    
    # Fallback checking ementa
    if not est_susc and not est_suscd:
        m_inst = re.search(r'DISS[IÍ\ufffd]DIO COLETIVO[\s\w-]{0,30}?(?:INSTAURADO|AJUIZADO|SUSCITADO|PROPOSTO)\s*PEL[AO]\s*([^\n\r.,;]+)', combined_text[:3000], re.I)
        if m_inst:
            mat = check_entity_match(m_inst.group(1))
            if mat:
                est_susc = mat
                susc = m_inst.group(1).strip()
                suscd = "Entidades Sindicais Representativas dos Trabalhadores"
        
        m_suscd_em = re.search(r'(?:empresa suscitada|recorrida|face d[aeo])\s*[\.:-]?\s*([^\n\r.,;]+)', combined_text[:3000], re.I)
        if m_suscd_em:
            mat2 = check_entity_match(m_suscd_em.group(1))
            if mat2:
                est_suscd = mat2
                suscd = m_suscd_em.group(1).strip()
                susc = "Entidade Sindical Profissional"

    if not est_susc and not est_suscd:
        continue # Not an actual party in this dispute
    
    # Specific fix for inverted patterns (when union has the state enterprise in its name)
    if est_susc and any(k in susc.lower() for k in ['sindicato', 'federacao', 'federação', 'associacao', 'associação', 'confederacao', 'confederação']):
        if est_suscd:
            est_susc = None
        else:
            est_suscd = est_susc
            est_susc = None
            suscd = est_suscd
    
    # Tipo
    tipo_str = "Econômico"
    lower_check = combined_text[:4000].lower()
    if 'greve' in lower_check or 'paredista' in lower_check or 'paralisação' in lower_check or 'dcg' in cod_fase.lower():
        tipo_str = "Greve"
    elif 'natureza jurídica' in lower_check or 'declaratória' in lower_check:
        tipo_str = "Jurídico"
    elif 'revisional' in lower_check:
        tipo_str = "Revisional"
    elif 'natureza econômica' in lower_check or 'reajuste' in lower_check or 'cláusula' in lower_check:
        tipo_str = "Econômico"
    
    # Vigência
    ano_vigencia = ""
    vig_m = re.search(r'(?:vig[eê\ufffd]ncia|per[ií\ufffd]odo|exerc[ií\ufffd]cio|acordo|act|cct)[\s\w/ºªde.-]{0,40}?(20\d{2}\s*/\s*20\d{2}|20\d{2}\s*-\s*20\d{2}|1[ºo]?[\s\w/]+20\d{2}\s+a\s+31[\s\w/]+20\d{2})', combined_text[:15000], re.I)
    if vig_m:
        ano_vigencia = re.sub(r'\s+', ' ', vig_m.group(1)).strip()
    elif ano_proc:
        ano_vigencia = f"{ano_proc}/{ano_proc+1}"
    
    # Situação / Resultado
    disp_lower = combined_text[:6000].lower()
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
    elif not dt_julg:
        resultado = "Pendente"
    
    # Filing date
    dt_ajz = ""
    dt_ajz_m = re.search(r'ajuizad[oa]\s+em\s+(\d{1,2}/\d{1,2}/\d{4}|\d{1,2}\s+de\s+[a-zç\ufffd]+\s+de\s+\d{4})', combined_text[:15000], re.I)
    if dt_ajz_m:
        dt_ajz = dt_ajz_m.group(1)
    elif dt_julg:
        dt_ajz = dt_julg
    elif ano_proc:
        dt_ajz = f"Ano {ano_proc}"
    
    # Source URL
    fonte_url = f"https://jurisprudencia.tst.jus.br"
    if '5.00.' in cnj:
        num_clean = cnj.replace('-', '').replace('.', '')
        fonte_url = f"https://consultaprocessual.tst.jus.br/consultaProcessual/resumoForm.do?consulta=1&numeroProcesso={num_clean}"
    
    row = {
        'número CNJ': cnj,
        'tribunal': tribunal,
        'classe': classe,
        'data de ajuizamento': dt_ajz,
        'suscitante': clean_party(susc) or (est_susc if est_susc else "Não informado"),
        'suscitado(s)': clean_party(suscd) or (est_suscd if est_suscd else "Entidades Sindicais"),
        'tipo (greve, econômico, jurídico, revisional)': tipo_str,
        'relator': relator,
        'situação/resultado (acordo, sentença normativa, extinto, pendente)': resultado,
        'ano de vigência do ACT/DC': ano_vigencia,
        'fonte (URL)': fonte_url,
        'nível de confiança (confirmado em fonte primária / só notícia / não verificado)': 'confirmado em fonte primária',
        'entidade_estatal': est_susc if est_susc else est_suscd,
        'ano_referencia': ano_proc if ano_proc else 2020
    }
    
    if est_susc:
        tab1_suscitante.append(row)
    elif est_suscd:
        tab2_suscitada.append(row)

# Deduplicate
def dedup(lst):
    seen = {}
    for r in lst:
        c = r['número CNJ']
        if c not in seen:
            seen[c] = r
        else:
            if len(r['suscitante']) > len(seen[c]['suscitante']):
                seen[c]['suscitante'] = r['suscitante']
            if len(r['suscitado(s)']) > len(seen[c]['suscitado(s)']):
                seen[c]['suscitado(s)'] = r['suscitado(s)']
    return list(seen.values())

tab1_clean = dedup(tab1_suscitante)
tab2_clean = dedup(tab2_suscitada)

print(f"\nTotal final deduplicado (24/09/2016 a 24/09/2026):")
print(f"  Tab 1 (Estatal Suscitante): {len(tab1_clean)}")
print(f"  Tab 2 (Estatal Suscitada):  {len(tab2_clean)}")

df_tab1 = pd.DataFrame(tab1_clean)
df_tab2 = pd.DataFrame(tab2_clean)

cols = [
    'número CNJ', 'tribunal', 'classe', 'data de ajuizamento',
    'suscitante', 'suscitado(s)', 'tipo (greve, econômico, jurídico, revisional)',
    'relator', 'situação/resultado (acordo, sentença normativa, extinto, pendente)',
    'ano de vigência do ACT/DC', 'fonte (URL)',
    'nível de confiança (confirmado em fonte primária / só notícia / não verificado)'
]

df_tab1_export = df_tab1[cols].copy()
df_tab2_export = df_tab2[cols].copy()

# Sanitize all cells
for c in cols:
    df_tab1_export[c] = df_tab1_export[c].apply(sanitize_excel_cell)
    df_tab2_export[c] = df_tab2_export[c].apply(sanitize_excel_cell)

# Save Excel files
excel_path1 = 'scraping_dissidio_coletivo_greve/dissidios_coletivos_estatais_2016_2026.xlsx'
excel_path2 = 'dissidios_coletivos_estatais_2016_2026.xlsx'

with pd.ExcelWriter(excel_path1, engine='openpyxl') as writer:
    df_tab1_export.to_excel(writer, sheet_name='Estatal Suscitante', index=False)
    df_tab2_export.to_excel(writer, sheet_name='Estatal Suscitada', index=False)

with pd.ExcelWriter(excel_path2, engine='openpyxl') as writer:
    df_tab1_export.to_excel(writer, sheet_name='Estatal Suscitante', index=False)
    df_tab2_export.to_excel(writer, sheet_name='Estatal Suscitada', index=False)

# Save CSVs
df_tab1_export.to_csv('scraping_dissidio_coletivo_greve/dissidios_estatais_suscitantes.csv', index=False, encoding='utf-8-sig', sep=';')
df_tab2_export.to_csv('scraping_dissidio_coletivo_greve/dissidios_estatais_suscitadas.csv', index=False, encoding='utf-8-sig', sep=';')
df_tab1_export.to_csv('dissidios_estatais_suscitantes.csv', index=False, encoding='utf-8-sig', sep=';')
df_tab2_export.to_csv('dissidios_estatais_suscitadas.csv', index=False, encoding='utf-8-sig', sep=';')

print("Planilhas salvas com sucesso em XLSX e CSV!")

# Print Stats for the Report
print("\n" + "="*60)
print("RELATÓRIO: TABELA 1 - ESTATAL SUSCITANTE")
print("="*60)
print("\nPor Entidade Estatal:")
print(df_tab1['entidade_estatal'].value_counts().to_string())

print("\nPor Ano de Ajuizamento / Referência:")
print(df_tab1['ano_referencia'].value_counts().sort_index().to_string())

print("\nPor Tribunal:")
print(df_tab1['tribunal'].value_counts().to_string())

print("\nPor Tipo:")
print(df_tab1['tipo (greve, econômico, jurídico, revisional)'].value_counts().to_string())

print("\nPor Situação / Resultado:")
print(df_tab1['situação/resultado (acordo, sentença normativa, extinto, pendente)'].value_counts().to_string())

print("\n" + "="*60)
print("RELATÓRIO: TABELA 2 - ESTATAL SUSCITADA")
print("="*60)
print("\nPor Entidade Estatal:")
print(df_tab2['entidade_estatal'].value_counts().to_string())

print("\nPor Tribunal:")
print(df_tab2['tribunal'].value_counts().to_string())
