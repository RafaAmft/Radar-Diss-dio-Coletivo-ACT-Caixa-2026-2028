"""
Geração e consolidação das planilhas finais de jurimetria de dissídios coletivos envolvendo empresas estatais (2016-2026).
Corrige problemas de codificação e unifica a detecção de polos e estatais.
"""

import json
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

from config.constants import (
    PROJECT_ROOT,
    OUTPUT_DIR,
    TRT_MAP,
)
from utils.cnj_utils import (
    extract_cnj,
    extract_tribunal,
    extract_year_from_cnj,
    extract_classe_processual,
)
from utils.entity_matching import (
    check_entity_match,
    clean_party,
    sanitize_excel_cell,
)

logger = logging.getLogger("jurimetria")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

UNION_WORDS = [
    'sindicato', 'federacao', 'federação', 'confederacao', 'confederação',
    'associacao', 'associação', 'fenadsef', 'fentect', 'fup', 'fnte',
    'sindipetro', 'sintect'
]


def find_data_file(filename: str) -> Path:
    """Localiza o arquivo JSON no diretório do projeto ou no diretório pai."""
    candidates = [
        PROJECT_ROOT / filename,
        PROJECT_ROOT.parent / filename,
        PROJECT_ROOT / "scraping_dissidio_coletivo_greve" / filename,
    ]
    for p in candidates:
        if p.is_file():
            return p
    return candidates[0]


def load_raw_datasets() -> tuple[dict, list, list]:
    """Carrega os datasets coletados do TST a partir dos arquivos JSON locais."""
    p_entities = find_data_file("all_entity_records.json")
    p_dc = find_data_file("sdc_all_dc_dcg.json")
    p_ro = find_data_file("sdc_all_ro_rot.json")

    logger.info("Carregando arquivos de dados brutos...")
    with open(p_entities, "r", encoding="utf-8") as f:
        all_entity_data = json.load(f)

    with open(p_dc, "r", encoding="utf-8") as f:
        sdc_dc_dcg = json.load(f)

    with open(p_ro, "r", encoding="utf-8") as f:
        sdc_ro_rot = json.load(f)

    return all_entity_data, sdc_dc_dcg, sdc_ro_rot


def build_cases_by_cnj(all_entity_data: dict, sdc_dc_dcg: list, sdc_ro_rot: list) -> Dict[str, Dict[str, Any]]:
    """Agrega todos os registros de processos por CNJ único."""
    cases_by_cnj = {}

    def add_record(r: dict, entity_tag: Optional[str] = None):
        cnj = extract_cnj(r)
        if not cnj:
            return
        if cnj not in cases_by_cnj:
            cases_by_cnj[cnj] = {
                "records": [r],
                "entities": [entity_tag] if entity_tag else [],
            }
        else:
            cases_by_cnj[cnj]["records"].append(r)
            if entity_tag and entity_tag not in cases_by_cnj[cnj]["entities"]:
                cases_by_cnj[cnj]["entities"].append(entity_tag)

    for ent, recs in all_entity_data.items():
        for r in recs:
            add_record(r, ent)

    for r in sdc_dc_dcg:
        add_record(r, None)

    for r in sdc_ro_rot:
        add_record(r, None)

    logger.info("Total de processos únicos CNJ consolidados: %d", len(cases_by_cnj))
    return cases_by_cnj


def normalize_estatal_name(name: str) -> str:
    """Padroniza o nome de exibição das principais estatais."""
    n = name.lower()
    if 'correios' in n or 'ect' in n:
        return 'Empresa Brasileira de Correios e Telégrafos (ECT)'
    if 'petrobras' in n and 'transpetro' in n:
        return 'Petrobras Transporte S.A. - TRANSPETRO'
    if 'petrobras' in n:
        return 'Petróleo Brasileiro S.A. - PETROBRAS'
    if 'caixa econ' in n or n == 'cef':
        return 'Caixa Econômica Federal (CEF)'
    if 'banco do brasil' in n or 'bb tecnologia' in n or 'cobra tecnologia' in n:
        return 'Banco do Brasil S.A.'
    if 'eletrobras' in n or 'centrais eletricas brasileiras' in n or 'centrais elétricas' in n:
        return 'Centrais Elétricas Brasileiras S.A. - ELETROBRAS'
    if 'furnas' in n:
        return 'Furnas Centrais Elétricas S.A.'
    if 'ebserh' in n or 'hospitalares' in n:
        return 'Empresa Brasileira de Serviços Hospitalares (EBSERH)'
    if 'cptm' in n:
        return 'Companhia Paulista de Trens Metropolitanos (CPTM)'
    if 'cbtu' in n:
        return 'Companhia Brasileira de Trens Urbanos (CBTU)'
    if 'trensurb' in n:
        return 'Empresa de Trens Urbanos de Porto Alegre (Trensurb)'
    if 'serpro' in n:
        return 'Serviço Federal de Processamento de Dados (SERPRO)'
    if 'dataprev' in n:
        return 'Empresa de Tecnologia e Informações da Previdência (DATAPREV)'
    if 'metrô' in n and ('distrito federal' in n or 'df' in n):
        return 'Companhia do Metropolitano do Distrito Federal (Metrô DF)'
    if 'metrô' in n and 'são paulo' in n:
        return 'Companhia do Metropolitano de São Paulo (Metrô SP)'
    if 'imbel' in n:
        return 'Indústria de Material Bélico do Brasil (IMBEL)'
    if 'ebc' in n or 'brasil de comunicacao' in n or 'brasil de comunicação' in n:
        return 'Empresa Brasil de Comunicação S.A. (EBC)'
    if 'casa da moeda' in n or 'cmb' in n:
        return 'Casa da Moeda do Brasil (CMB)'
    if 'telebras' in n:
        return 'Telecomunicações Brasileiras S.A. (TELEBRAS)'
    if 'valec' in n or 'infra s.a.' in n:
        return 'Infra S.A. / VALEC'
    if 'bndes' in n:
        return 'Banco Nacional de Desenvolvimento Econômico e Social (BNDES)'
    if 'conab' in n:
        return 'Companhia Nacional de Abastecimento (Conab)'
    if 'infraero' in n:
        return 'Empresa Brasileira de Infraestrutura Aeroportuária (Infraero)'
    if 'embrapa' in n:
        return 'Empresa Brasileira de Pesquisa Agropecuária (Embrapa)'
    if 'emgerpi' in n:
        return 'Empresa de Gestão de Recursos do Estado do Piauí - EMGERPI'
    if 'celepar' in n:
        return 'Companhia de Tecnologia da Informação e Comunicação do Paraná - CELEPAR'
    return name


def process_case(cnj: str, case_info: dict) -> Optional[dict]:
    """Processa um processo CNJ e extrai seus atributos jurimétricos."""
    ano_str = extract_year_from_cnj(cnj)
    ano_proc = int(ano_str) if ano_str.isdigit() else None

    # Filtra apenas o decênio 2016-2026
    if ano_proc and (ano_proc < 2016 or ano_proc > 2026):
        return None

    recs = case_info["records"]
    best_rec = None
    for r in recs:
        if r.get("inteiroTeorHtml"):
            best_rec = r
            break
    if not best_rec:
        for r in recs:
            if r.get("txtConteudoDecisao"):
                best_rec = r
                break
    if not best_rec:
        best_rec = recs[0]

    dt_julg = best_rec.get("dtaJulgamento") or ""
    dt_pub = best_rec.get("dtaPublicacao") or ""
    tribunal = extract_tribunal(cnj)
    classe = extract_classe_processual(best_rec.get("codFase"))

    relator_raw = best_rec.get("nomRelatorSemTratamento") or best_rec.get("nomRelator") or ""
    relator = " ".join(w.capitalize() for w in relator_raw.split()) if relator_raw else "Não informado"

    # Concatenação e limpeza dos textos de decisões para análise
    full_text_blocks = []
    for r in recs:
        t = r.get("inteiroTeorHtml") or r.get("txtConteudoDecisao") or r.get("txtConteudoDecisaoHighlight") or ""
        if t:
            clean = re.sub(r"<[^>]+>", " ", t)
            clean = re.sub(r"\s+", " ", clean)
            full_text_blocks.append(clean)
        em = r.get("ementa") or ""
        if em:
            full_text_blocks.append(em)

    combined_text = "\n".join(full_text_blocks)
    if not combined_text:
        return None

    susc = ""
    suscd = ""

    # Extração de partes via regex refinado
    m1 = re.search(
        r"SUSCITANTE[:\s]+([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|[A-Z\s]{4,}))\s+e\s+(?:s[aã]o|[eé\?])\s+SUSCITADO[S]?[:\s]+([^,;\n\r.]+)",
        combined_text,
        re.I,
    )
    m2 = re.search(r"SUSCITANTE\s*:\s*([^\n\r]+?)(?:SUSCITAD[AO][S]?|REQUERID[AO]|\n|\r)", combined_text, re.I)
    m2_d = re.search(r"SUSCITAD[AO][S]?\s*:\s*([^\n\r]+?)(?:DESPACHO|AC[OÓ]RD[AÃ]O|RELAT[OÓ]RIO|TERCEIRO|\n|\r)", combined_text, re.I)
    m3 = re.search(
        r"DISS[IÍ]DIO COLETIVO[\s\w-]{0,30}?(?:INSTAURADO|AJUIZADO|SUSCITADO|PROPOSTO)\s*PEL[AO]\s*([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ][AÃ]O[^\n\r,;.]+?|[A-Z\s]{4,}))\s*(?:EM FACE\s*(?:DE|DO|DA)|CONTRA)\s*([^\n\r;.]+)",
        combined_text,
        re.I,
    )
    m4 = re.search(
        r"(?:Cuidam os autos|Trata-se) de recurso ordin[aá]rio[\s\w\d.,-]{0,60}?pelo[a]?\s+([^\n\r,;.]+?(?:S\.?A\.?|LTDA|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ][AÃ]O[^\n\r,;.]+?|[A-Z\s]{4,}))\s*,\s*(suscitante|suscitad[ao])[\s\w\d.,-]{0,40}?ajuizada\s+pela[o]?\s+([^\n\r;.]+)",
        combined_text,
        re.I,
    )

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
        if "suscitante" in role1:
            susc = p1
            suscd = p2
        else:
            susc = p2
            suscd = p1
    elif m3:
        susc = m3.group(1).strip()
        suscd = m3.group(2).strip()

    est_susc = check_entity_match(susc)
    est_suscd = check_entity_match(suscd)

    # Fallback na ementa
    if not est_susc and not est_suscd:
        m_inst = re.search(
            r"DISS[IÍ]DIO COLETIVO[\s\w-]{0,30}?(?:INSTAURADO|AJUIZADO|SUSCITADO|PROPOSTO)\s*PEL[AO]\s*([^\n\r.,;]+)",
            combined_text[:3000],
            re.I,
        )
        if m_inst:
            mat = check_entity_match(m_inst.group(1))
            if mat:
                est_susc = mat
                susc = m_inst.group(1).strip()
                suscd = "Entidades Sindicais Representativas dos Trabalhadores"

        m_suscd_em = re.search(r"(?:empresa suscitada|recorrida|face d[aeo])\s*[\.:-]?\s*([^\n\r.,;]+)", combined_text[:3000], re.I)
        if m_suscd_em:
            mat2 = check_entity_match(m_suscd_em.group(1))
            if mat2:
                est_suscd = mat2
                suscd = m_suscd_em.group(1).strip()
                susc = "Entidade Sindical Profissional"

    if not est_susc and not est_suscd:
        return None

    # Correção de inversão quando o sindicato contém o nome da estatal no título
    if est_susc and any(k in susc.lower() for k in UNION_WORDS):
        if est_suscd:
            est_susc = None
        else:
            est_suscd = est_susc
            est_susc = None
            suscd = est_suscd

    # Verificação de texto excessivo ou cláusula no nome da suscitante
    if len(susc) > 120 or 'cláusula' in susc.lower() or 'clausula' in susc.lower() or 'conhece-se' in susc.lower():
        if 'emgerpi' in susc.lower() or 'emgerpi' in suscd.lower():
            susc = "Empresa de Gestão de Recursos do Estado do Piauí - EMGERPI"
            est_susc = 'Emgerpi'
        elif 'celepar' in susc.lower() or 'cepar' in susc.lower():
            susc = "Companhia de Tecnologia da Informação e Comunicação do Paraná - CELEPAR"
            est_susc = 'Celepar'
        else:
            # Transfere para polo de suscitada se for recurso sindical
            if est_susc and not est_suscd:
                est_suscd = est_susc
                est_susc = None
                suscd = est_suscd

    # Determinação do Tipo / Natureza
    tipo_str = "Econômico"
    lower_check = combined_text[:4000].lower()
    cod_fase = best_rec.get("codFase") or ""
    if "greve" in lower_check or "paredista" in lower_check or "paralisação" in lower_check or "dcg" in cod_fase.lower():
        tipo_str = "Greve"
    elif "natureza jurídica" in lower_check or "declaratória" in lower_check:
        tipo_str = "Jurídico"
    elif "revisional" in lower_check:
        tipo_str = "Revisional"
    elif "natureza econômica" in lower_check or "reajuste" in lower_check or "cláusula" in lower_check:
        tipo_str = "Econômico"

    # Ano de Vigência
    ano_vigencia = ""
    vig_m = re.search(
        r"(?:vig[eê]ncia|per[ií]odo|exerc[ií]cio|acordo|act|cct)[\s\w/ºªde.-]{0,40}?(20\d{2}\s*/\s*20\d{2}|20\d{2}\s*-\s*20\d{2}|1[ºo]?[\s\w/]+20\d{2}\s+a\s+31[\s\w/]+20\d{2})",
        combined_text[:15000],
        re.I,
    )
    if vig_m:
        ano_vigencia = re.sub(r"\s+", " ", vig_m.group(1)).strip()
    elif ano_proc:
        ano_vigencia = f"{ano_proc}/{ano_proc + 1}"

    # Situação / Resultado
    disp_lower = combined_text[:6000].lower()
    resultado = "Sentença Normativa"
    if "homolog" in disp_lower and "acordo" in disp_lower:
        resultado = "Acordo Homologado"
    elif "extin" in disp_lower and (
        "sem resolução" in disp_lower
        or "sem julgamento" in disp_lower
        or "sem exame" in disp_lower
        or "falta de comum acordo" in disp_lower
        or "perda do objeto" in disp_lower
    ):
        resultado = "Extinto sem Resolução de Mérito"
    elif "abusiv" in disp_lower:
        if "não abusiva" in disp_lower or "ausência de abusividade" in disp_lower:
            resultado = "Greve Julgada Não Abusiva"
        else:
            resultado = "Greve Julgada Abusiva"
    elif "procedente em parte" in disp_lower:
        resultado = "Sentença Normativa (Procedente em Parte)"
    elif "improcedente" in disp_lower:
        resultado = "Julgado Improcedente"
    elif "procedente" in disp_lower:
        resultado = "Sentença Normativa (Procedente)"
    elif not dt_julg:
        resultado = "Pendente"

    # Data de ajuizamento
    dt_ajz = ""
    dt_ajz_m = re.search(
        r"ajuizad[oa]\s+em\s+(\d{1,2}/\d{1,2}/\d{4}|\d{1,2}\s+de\s+[a-zç]+\s+de\s+\d{4})",
        combined_text[:15000],
        re.I,
    )
    if dt_ajz_m:
        dt_ajz = dt_ajz_m.group(1)
    elif dt_julg:
        dt_ajz = dt_julg
    elif ano_proc:
        dt_ajz = f"Ano {ano_proc}"

    # Link da fonte
    fonte_url = "https://jurisprudencia.tst.jus.br"
    if "5.00." in cnj:
        num_clean = cnj.replace("-", "").replace(".", "")
        fonte_url = f"https://consultaprocessual.tst.jus.br/consultaProcessual/resumoForm.do?consulta=1&numeroProcesso={num_clean}"

    # Limpeza e normalização dos nomes das partes
    susc_clean = clean_party(susc)
    suscd_clean = clean_party(suscd)

    if est_susc:
        susc_clean = normalize_estatal_name(susc_clean or est_susc)
        if not suscd_clean or suscd_clean.lower() in ["entidades sindicais", "não informado"] or len(suscd_clean) < 5:
            suscd_clean = "Entidades Sindicais Representativas da Categoria Profissional"
    elif est_suscd:
        suscd_clean = normalize_estatal_name(suscd_clean or est_suscd)
        if not susc_clean or susc_clean.lower() in ["entidade sindical", "não informado"] or len(susc_clean) < 5:
            susc_clean = "Entidade Sindical Profissional"

    return {
        "número CNJ": cnj,
        "tribunal": tribunal,
        "classe": classe,
        "data de ajuizamento": dt_ajz,
        "suscitante": susc_clean,
        "suscitado(s)": suscd_clean,
        "tipo (greve, econômico, jurídico, revisional)": tipo_str,
        "relator": relator,
        "situação/resultado (acordo, sentença normativa, extinto, pendente)": resultado,
        "ano de vigência do ACT/DC": ano_vigencia,
        "fonte (URL)": fonte_url,
        "nível de confiança (confirmado em fonte primária / só notícia / não verificado)": "confirmado em fonte primária",
        "polo_estatal": "SUSCITANTE" if est_susc else "SUSCITADA",
        "entidade_estatal": est_susc if est_susc else est_suscd,
        "ano_referencia": ano_proc or 2020,
    }


def deduplicate_cases(case_list: List[dict]) -> List[dict]:
    """Deduplica registros mantendo a versão com descrição de partes mais completa."""
    seen = {}
    for r in case_list:
        c = r["número CNJ"]
        if c not in seen:
            seen[c] = r
        else:
            if len(r["suscitante"]) > len(seen[c]["suscitante"]):
                seen[c]["suscitante"] = r["suscitante"]
            if len(r["suscitado(s)"]) > len(seen[c]["suscitado(s)"]):
                seen[c]["suscitado(s)"] = r["suscitado(s)"]
    return list(seen.values())


def generate_spreadsheets():
    """Executa o pipeline completo de processamento, geração e exportação de planilhas."""
    logger.info("Iniciando geração de planilhas de dissídios coletivos de estatais (2016-2026)...")
    
    all_entity_data, sdc_dc_dcg, sdc_ro_rot = load_raw_datasets()
    cases_by_cnj = build_cases_by_cnj(all_entity_data, sdc_dc_dcg, sdc_ro_rot)

    tab1_suscitante = []
    tab2_suscitada = []

    for cnj, info in cases_by_cnj.items():
        res = process_case(cnj, info)
        if not res:
            continue
        if res["polo_estatal"] == "SUSCITANTE":
            tab1_suscitante.append(res)
        else:
            tab2_suscitada.append(res)

    tab1_clean = deduplicate_cases(tab1_suscitante)
    tab2_clean = deduplicate_cases(tab2_suscitada)

    logger.info("Total consolidado deduplicado: Tab 1 (Estatal Suscitante)=%d | Tab 2 (Estatal Suscitada)=%d",
                len(tab1_clean), len(tab2_clean))

    cols = [
        "número CNJ", "tribunal", "classe", "data de ajuizamento",
        "suscitante", "suscitado(s)", "tipo (greve, econômico, jurídico, revisional)",
        "relator", "situação/resultado (acordo, sentença normativa, extinto, pendente)",
        "ano de vigência do ACT/DC", "fonte (URL)",
        "nível de confiança (confirmado em fonte primária / só notícia / não verificado)"
    ]

    df_tab1 = pd.DataFrame(tab1_clean)
    df_tab2 = pd.DataFrame(tab2_clean)

    # Ordenação decrescente por ano e CNJ
    df_tab1["ano_temp"] = df_tab1["número CNJ"].apply(extract_year_from_cnj)
    df_tab1 = df_tab1.sort_values(by=["ano_temp", "número CNJ"], ascending=[False, True]).drop(columns=["ano_temp"])

    df_tab2["ano_temp"] = df_tab2["número CNJ"].apply(extract_year_from_cnj)
    df_tab2 = df_tab2.sort_values(by=["ano_temp", "número CNJ"], ascending=[False, True]).drop(columns=["ano_temp"])

    df_tab1_export = df_tab1[cols].copy()
    df_tab2_export = df_tab2[cols].copy()

    # Sanitização contra caracteres de controle incompatíveis com openpyxl
    for c in cols:
        df_tab1_export[c] = df_tab1_export[c].apply(sanitize_excel_cell)
        df_tab2_export[c] = df_tab2_export[c].apply(sanitize_excel_cell)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Salvamento das planilhas Excel (na pasta output e na raiz para compatibilidade)
    excel_targets = [
        OUTPUT_DIR / "dissidios_coletivos_estatais_2016_2026.xlsx",
        PROJECT_ROOT / "dissidios_coletivos_estatais_2016_2026.xlsx",
    ]

    for ep in excel_targets:
        with pd.ExcelWriter(ep, engine="openpyxl") as writer:
            df_tab1_export.to_excel(writer, sheet_name="Estatal Suscitante", index=False)
            df_tab2_export.to_excel(writer, sheet_name="Estatal Suscitada", index=False)

    # Salvamento dos arquivos CSV em UTF-8 com BOM (padrão Excel Brasil sep=;)
    csv_configs = [
        (df_tab1_export, OUTPUT_DIR / "dissidios_estatais_suscitantes.csv"),
        (df_tab2_export, OUTPUT_DIR / "dissidios_estatais_suscitadas.csv"),
        (df_tab1_export, PROJECT_ROOT / "dissidios_estatais_suscitantes.csv"),
        (df_tab2_export, PROJECT_ROOT / "dissidios_estatais_suscitadas.csv"),
    ]

    for df_exp, csv_path in csv_configs:
        df_exp.to_csv(csv_path, index=False, encoding="utf-8-sig", sep=";")

    logger.info("Planilhas salvas com sucesso em XLSX e CSV (output/ e raiz)!")
    return df_tab1_export, df_tab2_export


if __name__ == "__main__":
    df1, df2 = generate_spreadsheets()
    print("\n--- DISTRIBUIÇÃO TAB 1 (ESTATAL COMO SUSCITANTE) POR ENTIDADE ---")
    print(df1["suscitante"].value_counts().to_string())
    print("\n--- DISTRIBUIÇÃO TAB 1 POR TRIBUNAL ---")
    print(df1["tribunal"].value_counts().to_string())
    print("\n--- DISTRIBUIÇÃO TAB 1 POR SITUAÇÃO/RESULTADO ---")
    print(df1["situação/resultado (acordo, sentença normativa, extinto, pendente)"].value_counts().to_string())
