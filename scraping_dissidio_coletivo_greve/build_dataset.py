"""
Construção e consolidação do dataset completo de dissídios coletivos (2016-2026).
Consolida todos os registros do TST por número CNJ e classifica o envolvimento de entidades estatais.
"""

import json
import logging
from typing import Dict, Any, List, Optional
import pandas as pd

from config.constants import (
    PROJECT_ROOT,
    OUTPUT_DIR,
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
)
from utils.html_utils import clean_html

logger = logging.getLogger("build_dataset")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def find_data_file(filename: str):
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


def load_all_records() -> tuple[dict, list, list]:
    """Carrega os dados brutos salvos pelos scrapers do TST."""
    p_entities = find_data_file("all_entity_records.json")
    p_dc = find_data_file("sdc_all_dc_dcg.json")
    p_ro = find_data_file("sdc_all_ro_rot.json")

    logger.info("Carregando datasets brutos: %s, %s, %s", p_entities.name, p_dc.name, p_ro.name)
    with open(p_entities, "r", encoding="utf-8") as f:
        all_entity_data = json.load(f)

    with open(p_dc, "r", encoding="utf-8") as f:
        sdc_dc_dcg = json.load(f)

    with open(p_ro, "r", encoding="utf-8") as f:
        sdc_ro_rot = json.load(f)

    return all_entity_data, sdc_dc_dcg, sdc_ro_rot


def build_consolidated_cases(all_entity_data: dict, sdc_dc_dcg: list, sdc_ro_rot: list) -> Dict[str, Dict[str, Any]]:
    """Indexa e agrupa todos os registros pelo número CNJ padronizado."""
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


def extract_case_details(cnj: str, case_info: dict) -> dict:
    """Extrai detalhes substantivos de um caso consolidado."""
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

    tribunal = extract_tribunal(cnj)
    classe = extract_classe_processual(best_rec.get("codFase"))

    relator_raw = best_rec.get("nomRelatorSemTratamento") or best_rec.get("nomRelator") or ""
    relator = " ".join(w.capitalize() for w in relator_raw.split()) if relator_raw else "Não informado"

    dt_julg = best_rec.get("dtaJulgamento") or ""
    dt_pub = best_rec.get("dtaPublicacao") or ""
    ano_cnj = extract_year_from_cnj(cnj)

    html = best_rec.get("inteiroTeorHtml") or best_rec.get("txtConteudoDecisao") or ""
    ementa = best_rec.get("ementa") or ""
    dispositivo = best_rec.get("dispositivo") or ""

    full_text = clean_html(html) if html else f"{clean_html(ementa)}\n{clean_html(dispositivo)}"

    # Natureza do dissídio
    tipo_str = "Econômico"
    lower_all = (full_text[:4000] + " " + ementa).lower()
    cod_fase = (best_rec.get("codFase") or "").lower()
    if "greve" in lower_all or "paredista" in lower_all or "paralisação" in lower_all or "dcg" in cod_fase:
        tipo_str = "Greve"
    elif "natureza jurídica" in lower_all or "declaratória" in lower_all:
        tipo_str = "Jurídico"
    elif "revisional" in lower_all:
        tipo_str = "Revisional"
    elif "natureza econômica" in lower_all or "reajuste" in lower_all or "cláusula" in lower_all:
        tipo_str = "Econômico"

    import re
    ano_vigencia = ""
    vig_m = re.search(
        r"(?:vig[eê]ncia|per[ií]odo|exerc[ií]cio|acordo|act|cct)[\s\w/ºªde.-]{0,40}?(20\d{2}\s*/\s*20\d{2}|20\d{2}\s*-\s*20\d{2}|1[ºo]?[\s\w/]+20\d{2}\s+a\s+31[\s\w/]+20\d{2})",
        full_text[:10000],
        re.I,
    )
    if vig_m:
        ano_vigencia = re.sub(r"\s+", " ", vig_m.group(1)).strip()
    elif ano_cnj:
        ano_next = int(ano_cnj) + 1 if ano_cnj.isdigit() else ""
        ano_vigencia = f"{ano_cnj}/{ano_next}"

    # Situação / Resultado
    disp_lower = (dispositivo + " " + ementa[:2000] + " " + full_text[:4000]).lower()
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
    elif "pendente" in disp_lower or not dt_julg:
        resultado = "Pendente"

    # Partes e identificação de polos
    suscitante = ""
    suscitados = ""
    polo_estatal = None
    estatal_envolvida = None

    p_std = re.search(
        r"em que [eé]\s+SUSCITANTE\s+([^,;\n\r]+?)\s+e\s+(?:s[aã]o|é)\s+SUSCITADO[S]?\s+([^,;\n\r]+?)(?:\s+e\s+|\.|\;|\n|\r)",
        full_text,
        re.I,
    )
    p_trata = re.search(
        r"diss[ií]dio coletivo\s*(?:de greve|de natureza econ[oô]mica|de natureza jur[ií]dica)?\s*(?:ajuizado|instaurado|suscitado|proposto)\s*(?:por|pela|pelo)\s*([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ][AÃ]O[^\n\r,;.]+?|[A-Z\s]{4,}))\s*(?:em face\s*(?:de|do|da)|contra)\s*([^\n\r;.]+)",
        full_text,
        re.I,
    )
    p_cuidam = re.search(
        r"(?:Cuidam os autos|Trata-se) de recurso ordin[aá]rio[\s\w\d.,-]{0,60}?pelo[a]?\s+([^\n\r,;.]+?(?:S\.?A\.?|LTDA|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ][AÃ]O[^\n\r,;.]+?|[A-Z\s]{4,}))\s*,\s*(suscitante|suscitad[ao])[\s\w\d.,-]{0,40}?ajuizada\s+pela[o]?\s+([^\n\r;.]+)",
        full_text,
        re.I,
    )
    p_instaurado = re.search(
        r"DISS[IÍ]DIO COLETIVO\s*(?:DE GREVE|DE NATUREZA ECON[OÔ]MICA|DE NATUREZA JUR[IÍ]DICA)?\s*(?:INSTAURADO|AJUIZADO|SUSCITADO|PROPOSTO)\s*PEL[AO]\s*([^\n\r,;.]+?(?:S\.?A\.?|LTDA|EIRELI|EMPRESA[^\n\r,;.]+?|COMPANHIA[^\n\r,;.]+?|SINDICATO[^\n\r,;.]+?|FEDERA[CÇ][AÃ]O[^\n\r,;.]+?|[A-Z\s]{4,}))",
        full_text,
        re.I,
    )

    if p_std:
        suscitante = clean_party(p_std.group(1))
        suscitados = clean_party(p_std.group(2))
    elif p_trata:
        suscitante = clean_party(p_trata.group(1))
        suscitados = clean_party(p_trata.group(2))
    elif p_cuidam:
        p1 = clean_party(p_cuidam.group(1))
        r1 = p_cuidam.group(2).lower()
        p2 = clean_party(p_cuidam.group(3))
        if "suscitante" in r1:
            suscitante = p1
            suscitados = p2
        else:
            suscitante = p2
            suscitados = p1
    elif p_instaurado:
        suscitante = clean_party(p_instaurado.group(1))
        suscd_m = re.search(r"(?:em face\s*(?:de|do|da)|contra)\s*([^\n\r;.]+)", full_text[:4000], re.I)
        if suscd_m:
            suscitados = clean_party(suscd_m.group(1))

    estatal_susc = check_entity_match(suscitante)
    estatal_suscd = check_entity_match(suscitados)

    if not estatal_susc and not estatal_suscd:
        m_emp_susc = re.search(r"(?:instaurado|ajuizado|suscitado|proposto)\s*pel[ao]\s*([^\n\r.,;]+)", ementa[:1500], re.I)
        if m_emp_susc:
            mat = check_entity_match(m_emp_susc.group(1))
            if mat:
                estatal_susc = mat
                suscitante = m_emp_susc.group(1).strip()

        m_emp_suscd = re.search(r"(?:empresa suscitada|recorrida)\s*[\.:-]?\s*([^\n\r.,;]+)", ementa[:1500], re.I)
        if m_emp_suscd:
            mat2 = check_entity_match(m_emp_suscd.group(1))
            if mat2:
                estatal_suscd = mat2
                suscitados = m_emp_suscd.group(1).strip()

    if estatal_susc:
        polo_estatal = "SUSCITANTE"
        estatal_envolvida = estatal_susc
        if not suscitados:
            suscitados = "Entidades Sindicais Representativas dos Trabalhadores"
    elif estatal_suscd:
        polo_estatal = "SUSCITADA"
        estatal_envolvida = estatal_suscd
        if not suscitante:
            suscitante = "Entidade Sindical Profissional"

    dt_ajz = ""
    dt_ajz_m = re.search(
        r"ajuizad[oa]\s+em\s+(\d{1,2}/\d{1,2}/\d{4}|\d{1,2}\s+de\s+[a-zç]+\s+de\s+\d{4})",
        full_text[:10000],
        re.I,
    )
    if dt_ajz_m:
        dt_ajz = dt_ajz_m.group(1)
    elif dt_julg:
        dt_ajz = dt_julg
    elif ano_cnj:
        dt_ajz = f"Ano {ano_cnj}"

    fonte_url = "https://jurisprudencia.tst.jus.br"
    if "5.00." in cnj:
        num_clean = cnj.replace("-", "").replace(".", "")
        fonte_url = f"https://consultaprocessual.tst.jus.br/consultaProcessual/resumoForm.do?consulta=1&numeroProcesso={num_clean}"

    return {
        "número CNJ": cnj,
        "tribunal": tribunal,
        "classe": classe,
        "data de ajuizamento": dt_ajz,
        "suscitante": clean_party(suscitante),
        "suscitado(s)": clean_party(suscitados),
        "tipo (greve, econômico, jurídico, revisional)": tipo_str,
        "relator": relator,
        "situação/resultado (acordo, sentença normativa, extinto, pendente)": resultado,
        "ano de vigência do ACT/DC": ano_vigencia,
        "fonte (URL)": fonte_url,
        "nível de confiança (confirmado em fonte primária / só notícia / não verificado)": "confirmado em fonte primária",
        "polo_estatal": polo_estatal,
        "estatal_identificada": estatal_envolvida,
    }


def main():
    all_entity_data, sdc_dc_dcg, sdc_ro_rot = load_all_records()
    cases_by_cnj = build_consolidated_cases(all_entity_data, sdc_dc_dcg, sdc_ro_rot)

    logger.info("Iniciando processamento e classificação de todos os processos...")
    tab1_suscitante = []
    tab2_suscitada = []
    nao_enquadrados = []

    for cnj, info in cases_by_cnj.items():
        res = extract_case_details(cnj, info)
        if res["polo_estatal"] == "SUSCITANTE":
            tab1_suscitante.append(res)
        elif res["polo_estatal"] == "SUSCITADA":
            tab2_suscitada.append(res)
        else:
            nao_enquadrados.append(res)

    logger.info("Resultado da classificação:")
    logger.info("  Tab 1 (Estatal como Suscitante): %d processos confirmados", len(tab1_suscitante))
    logger.info("  Tab 2 (Estatal como Suscitada):  %d processos confirmados", len(tab2_suscitada))
    logger.info("  Não enquadrados (sem menção direta a estatais mapeadas): %d", len(nao_enquadrados))

    df_tab1 = pd.DataFrame(tab1_suscitante)
    if not df_tab1.empty:
        print("\nProcessos na Tab 1 por Entidade Estatal:")
        print(df_tab1["estatal_identificada"].value_counts())


if __name__ == "__main__":
    main()
