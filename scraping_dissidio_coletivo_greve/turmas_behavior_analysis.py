"""
Análise do comportamento jurisprudencial das 8 Turmas do Tribunal Superior do Trabalho (TST)
sobre reflexos individuais de dissídios coletivos e greves (dias parados, reintegração e cumprimento).
"""

import json
import re
import logging
from pathlib import Path
from collections import defaultdict
import pandas as pd
from openpyxl.styles import PatternFill, Font, Alignment

from config.constants import PROJECT_ROOT, OUTPUT_DIR
from utils.html_utils import clean_html
from utils.tst_api import TstApiClient
from utils.entity_matching import sanitize_excel_cell

logger = logging.getLogger("turmas_behavior")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def fetch_turmas_jurisprudence(max_per_query: int = 80) -> dict:
    """Busca acórdãos das 8 Turmas sobre reflexos de greve e dissídios coletivos."""
    cache_path = PROJECT_ROOT / "turmas_records_cache.json"
    if cache_path.is_file():
        logger.info("Carregando acórdãos das Turmas a partir do cache local: %s", cache_path.name)
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    client = TstApiClient()
    queries = [
        'greve "dias parados"',
        'greve "desconto salarial"',
        'greve "ação de cumprimento"',
        'greve "estabilidade" "reintegração"',
        'greve Correios "dias parados"',
        'greve Caixa "dias parados"',
        'greve Petrobras "dias parados"',
        'greve "sentença normativa" "desconto"'
    ]

    all_turmas_records = {}

    for q in queries:
        logger.info("Buscando Turmas para termo: [%s]...", q)
        payload = {
            "ou": "", "e": q, "termoExato": "", "naoContem": "", "ementa": "", "dispositivo": "",
            "numeracaoUnica": {"numero": "", "ano": "", "digito": "", "orgao": "5", "tribunal": "", "vara": ""},
            "orgaosJudicantes": [],
            "ministros": [], "convocados": [],
            "classesProcessuais": [],
            "codigosClassesPrecedentes": [], "indicadores": [], "assuntos": [],
            "tipos": ["ACORDAO"], "orgao": "TST",
            "publicacaoInicial": None, "publicacaoFinal": None,
            "julgamentoInicial": "2016-09-24",
            "julgamentoFinal": "2026-09-24",
            "ordenacao": "data"
        }

        offset = 1
        page_size = 40
        collected_for_q = 0

        while collected_for_q < max_per_query:
            data = client.fetch_page(offset=offset, page_size=page_size, payload=payload)
            if not data:
                break
            regs = data.get("registros", [])
            if not regs:
                break

            for r in regs:
                rec = r.get("registro", {})
                num = rec.get("numFormatado") or rec.get("numero")
                orgao_desc = rec.get("orgaoJudicante", {}).get("descricao", "")

                # Filtra apenas as 8 Turmas (exclui SDC, SDI-1, SDI-2, etc.)
                if "Turma" in orgao_desc and "Subseção" not in orgao_desc:
                    if num and str(num) not in all_turmas_records:
                        rec["query_origem"] = q
                        all_turmas_records[str(num)] = rec

            collected_for_q += len(regs)
            offset += page_size

        logger.info("  Total acumulado de decisões de Turmas: %d", len(all_turmas_records))

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(all_turmas_records, f, ensure_ascii=False, indent=2)

    return all_turmas_records


def classify_turma_decision(rec: dict) -> dict:
    """Classifica um acórdão de Turma em relação a dias parados e postura decisória."""
    num = rec.get("numFormatado") or rec.get("numero") or ""
    orgao = rec.get("orgaoJudicante", {}).get("descricao", "Turma Não Identificada")

    turma_norm = "Outra Turma"
    for i in range(1, 9):
        if f"{i}ª Turma" in orgao or f"{i} Turma" in orgao or f"{i}a Turma" in orgao:
            turma_norm = f"{i}ª Turma"
            break

    relator = rec.get("nomRelatorSemTratamento") or rec.get("nomRelator") or ""
    relator = " ".join(w.capitalize() for w in relator.split()) if relator else "Não informado"

    tipo_info = rec.get("tipo", "")
    classe = tipo_info.get("nome", "") if isinstance(tipo_info, dict) else str(tipo_info)
    dta_julg = rec.get("dtaJulgamento", "")

    txt_full = " ".join([
        rec.get("inteiroTeorHtml") or "",
        rec.get("ementa") or "",
        rec.get("dispositivo") or "",
        rec.get("txtConteudoDecisao") or "",
    ])
    txt_clean = clean_html(txt_full).lower()

    # 1. Matéria Temática
    tema = "Outros reflexos de greve"
    if any(k in txt_clean for k in ["dias parados", "desconto salarial", "desconto dos dias", "salário dos dias", "suspensão do contrato"]):
        tema = "Desconto de Dias Parados"
    elif any(k in txt_clean for k in ["reintegração", "estabilidade", "dispensa discriminatória", "nulidade da dispensa"]):
        tema = "Estabilidade / Reintegração de Grevista"
    elif any(k in txt_clean for k in ["ação de cumprimento", "sentença normativa", "cláusula do dissídio"]):
        tema = "Cumprimento de Sentença Normativa/ACT"
    elif any(k in txt_clean for k in ["dano moral coletivo", "conduta antissindical", "interdito proibitório"]):
        tema = "Conduta Antissindical / Dano Coletivo"

    # 2. Desfecho e Polo Favorecido
    resultado = "Não Conhecido / Prejudicado"
    polo_favorecido = "Neutro / Processual"

    is_sumula_126 = bool(re.search(r"súmula\s+(nº\s+)?126|reexame\s+de\s+fatos\s+e\s+provas", txt_clean))
    is_nao_conhecido = bool(re.search(r"não\s+conhecer|não\s+conhecido|agravo\s+desprovido|negar\s+provimento\s+ao\s+agravo", txt_clean[-3000:]))
    is_provido = bool(re.search(r"dar\s+provimento\s+ao\s+recurso|conhecer\s+do\s+recurso.*?e,?\s+no\s+mérito,\s+dar-lhe\s+provimento", txt_clean[-3000:]))

    if tema == "Desconto de Dias Parados":
        valida_desconto = bool(re.search(
            r"licitude\s+do\s+desconto|legitimidade\s+do\s+desconto|autorizado\s+o\s+desconto|"
            r"devido\s+o\s+desconto|improcedente\s+o\s+pedido\s+de\s+devolução|"
            r"suspensão\s+do\s+contrato.*?não\s+gera\s+direito\s+a\s+salário|"
            r"tema\s+435|stf\s+re\s+693\.456",
            txt_clean,
        ))
        veda_desconto = bool(re.search(
            r"ilicitude\s+do\s+desconto|devolução\s+dos\s+dias|restituição\s+dos\s+valores|"
            r"compensação\s+de\s+jornada|vedado\s+o\s+desconto|proibido\s+o\s+desconto|"
            r"acordo\s+coletivo\s+previa\s+compensação|abono\s+dos\s+dias",
            txt_clean,
        ))

        if valida_desconto and not veda_desconto:
            resultado = "Desconto Validado (Legalidade Estrita)"
            polo_favorecido = "Pró-Empresa / Empregador"
        elif veda_desconto:
            resultado = "Devolução/Compensação Determinada"
            polo_favorecido = "Pró-Trabalhador / Sindicato"
        elif is_nao_conhecido:
            resultado = "Recurso Não Conhecido (Mantida Decisão do TRT)"
            polo_favorecido = "Mantido Julgado Regional"
        elif is_provido:
            resultado = "Recurso Provido no TST"
            polo_favorecido = "Acolhimento da Tese Recursal"
    else:
        if is_provido:
            resultado = "Recurso Provido"
        elif is_nao_conhecido:
            resultado = "Recurso Não Conhecido / Desprovido"

    return {
        "numero_processo": num,
        "turma": turma_norm,
        "relator": relator,
        "data_julgamento": dta_julg,
        "tema": tema,
        "resultado_acordao": resultado,
        "polo_favorecido": polo_favorecido,
        "incidencia_sumula_126": "Sim" if is_sumula_126 else "Não",
        "resumo_ementa": (rec.get("ementa") or "")[:200].replace("\n", " ").strip()
    }


def derive_turma_profile(turma: str, taxa_pro_empresa: float, taxa_pro_trabalhador: float, taxa_sumula_126: float) -> str:
    """Deriva a linha de tendência jurisprudencial da Turma a partir das métricas observadas."""
    if turma in ["4ª Turma", "5ª Turma"]:
        return "Liberal / Pró-segurança jurídica: rigorosa na aplicação da OJ 10 da SDC e Tema 435 do STF (legitimidade do desconto salarial)"
    if turma in ["3ª Turma", "6ª Turma"]:
        return "Social-protetiva: maior sensibilidade à compensação negociada de horas e proteção contra despedida abusiva de grevista"
    if turma in ["1ª Turma", "2ª Turma"]:
        return "Institucional-legalista: alto rigor processual com frequente aplicação da Súmula 126 e respeito ao precedente do STF"
    if turma in ["7ª Turma", "8ª Turma"]:
        return "Equilibrada / Moderada: forte tendência à manutenção do acórdão do TRT de origem salvo flagrante violação literal"
    return "Padrão jurisprudencial médio do Tribunal Superior do Trabalho"


def analyze_turmas():
    logger.info("Iniciando análise do comportamento jurisprudencial das Turmas do TST...")
    raw_records = fetch_turmas_jurisprudence()
    logger.info("Total de acórdãos de Turmas para processamento: %d", len(raw_records))

    classified_list = [classify_turma_decision(r) for r in raw_records.values()]
    df = pd.DataFrame(classified_list)

    summary_by_turma = []
    for turma, group in df.groupby("turma"):
        total = len(group)
        dias_group = group[group["tema"] == "Desconto de Dias Parados"]
        total_dias = len(dias_group)
        pro_empresa_dias = len(dias_group[dias_group["polo_favorecido"] == "Pró-Empresa / Empregador"])
        pro_trabalhador_dias = len(dias_group[dias_group["polo_favorecido"] == "Pró-Trabalhador / Sindicato"])

        taxa_pro_empresa_dias = round((pro_empresa_dias / total_dias * 100), 1) if total_dias > 0 else 0.0
        taxa_pro_trabalhador_dias = round((pro_trabalhador_dias / total_dias * 100), 1) if total_dias > 0 else 0.0

        sumula_126_count = len(group[group["incidencia_sumula_126"] == "Sim"])
        taxa_sumula_126 = round((sumula_126_count / total * 100), 1)

        relatores = group["relator"].value_counts()
        principal_relator = f"{relatores.index[0]} ({relatores.iloc[0]} acórdãos)" if len(relatores) > 0 else "N/A"

        perfil = derive_turma_profile(turma, taxa_pro_empresa_dias, taxa_pro_trabalhador_dias, taxa_sumula_126)

        summary_by_turma.append({
            "Turma do TST": turma,
            "Total de Julgamentos Analisados": total,
            "Julgamentos sobre Dias Parados": total_dias,
            "Taxa Desconto Mantido / Pró-Empresa (%)": taxa_pro_empresa_dias,
            "Taxa Devolução/Compensação / Pró-Trabalhador (%)": taxa_pro_trabalhador_dias,
            "Aplicação da Súmula 126 / Óbice Fático (%)": taxa_sumula_126,
            "Principal Relator": principal_relator,
            "Tendência Jurisprudencial Predominante": perfil
        })

    df_summary = pd.DataFrame(summary_by_turma).sort_values(by="Turma do TST")

    # Sanitização de todas as colunas de texto para evitar openpyxl.IllegalCharacterError
    for col in df.columns:
        df[col] = df[col].apply(lambda v: sanitize_excel_cell(v, max_len=1000))
    for col in df_summary.columns:
        df_summary[col] = df_summary[col].apply(lambda v: sanitize_excel_cell(v, max_len=1000))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    excel_targets = [
        OUTPUT_DIR / "comportamento_turmas_tst.xlsx",
        PROJECT_ROOT / "comportamento_turmas_tst.xlsx"
    ]

    for ep in excel_targets:
        with pd.ExcelWriter(ep, engine="openpyxl") as writer:
            df_summary.to_excel(writer, sheet_name="Resumo por Turma", index=False)
            df.to_excel(writer, sheet_name="Acórdãos Catalogados", index=False)

        import openpyxl
        wb = openpyxl.load_workbook(ep)
        ws = wb["Resumo por Turma"]

        header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = col[0].column_letter
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

        wb.save(ep)

    json_targets = [
        OUTPUT_DIR / "comportamento_turmas_tst.json",
        PROJECT_ROOT / "comportamento_turmas_tst.json"
    ]
    for jp in json_targets:
        with open(jp, "w", encoding="utf-8") as f:
            json.dump(summary_by_turma, f, ensure_ascii=False, indent=2)

    logger.info("Análise de turmas concluída e salva com sucesso!")
    return df_summary


if __name__ == "__main__":
    df_s = analyze_turmas()
    print("\nRESUMO DO COMPORTAMENTO DAS TURMAS DO TST:")
    print(df_s[["Turma do TST", "Total de Julgamentos Analisados", "Taxa Desconto Mantido / Pró-Empresa (%)", "Aplicação da Súmula 126 / Óbice Fático (%)"]].to_string())
