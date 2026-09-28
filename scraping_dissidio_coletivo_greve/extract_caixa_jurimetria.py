"""
Extração aperfeiçoada e jurimetria estruturada de decisões da Caixa Econômica Federal no TST.
Lê os casos emblemáticos de config/flagship_cases.json e processa o acervo de dissídios coletivos.
"""

import json
import re
import logging
from pathlib import Path
from typing import Dict, Any, List

from config.constants import PROJECT_ROOT, OUTPUT_DIR
from utils.html_utils import clean_html, extract_clean_document
from utils.cnj_utils import extract_cnj, extract_classe_processual

logger = logging.getLogger("caixa_jurimetria")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def load_flagship_cases() -> List[Dict[str, Any]]:
    """Carrega os casos emblemáticos vivos configurados em JSON."""
    flagship_file = PROJECT_ROOT / "config" / "flagship_cases.json"
    if flagship_file.is_file():
        with open(flagship_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def process_caixa_record(reg: dict) -> Dict[str, Any]:
    """Classifica e extrai temas, desfecho e impacto de um registro processual da Caixa."""
    doc_type, clean_content = extract_clean_document(reg)
    cnj = extract_cnj(reg) or reg.get("numFormatado") or reg.get("numero") or ""
    num_formatado = reg.get("numFormatado") or cnj

    # Relator
    relator_raw = reg.get("nomRelatorSemTratamento") or reg.get("nomRelator") or ""
    relator = " ".join(w.capitalize() for w in relator_raw.split()) if relator_raw else "Tribunal Superior do Trabalho"

    # Partes e polos
    partes = reg.get("partes", [])
    polo_caixa = "Interessada / Citada"
    parte_contraria = "Entidades Sindicais dos Bancários"

    if partes:
        caixa_found = False
        sindicato_found = False
        sind_nomes = []
        for p in partes:
            nome = p.get("nome", "")
            polo = p.get("polo", "")
            if re.search(r"caixa econ[oô]mica federal|\bcef\b", nome, re.I):
                caixa_found = True
                if polo == "A" or "suscitante" in p.get("tipoParte", "").lower():
                    polo_caixa = "Suscitante (Autora da Ação)"
                elif polo == "P" or "suscitad" in p.get("tipoParte", "").lower():
                    polo_caixa = "Suscitada (Ré / Alvo da Greve)"
            else:
                if any(w in nome.lower() for w in ["sindicato", "federa", "confedera", "contraf", "contec"]):
                    sindicato_found = True
                    sind_nomes.append(clean_html(nome))
        if sind_nomes:
            parte_contraria = " / ".join(sind_nomes[:2])

    data_pub = reg.get("dtaPublicacao") or reg.get("dtaJulgamento") or "2024-09-01"

    # Classe Processual
    cod_fase = reg.get("codFase") or ""
    classe = extract_classe_processual(cod_fase)

    full_text = clean_content.lower()

    # Identificação de Temas
    temas = []
    if re.search(r"sa[uú]de\s+caixa|plano\s+de\s+sa[uú]de|assist[eê]ncia\s+m[eé]dica", full_text):
        temas.append("Saúde Caixa")
    if re.search(r"dias\s+parados|desconto.*sal[aá]ri|compensa[cç][aã]o\s+de\s+horas|greve", full_text):
        temas.append("Dias Parados & Greve")
    if re.search(r"plr|participa[cç][aã]o\s+nos\s+lucros|plr\s+social", full_text):
        temas.append("PLR & PLR Social")
    if re.search(r"7[aª]\s+e\s+8[aª]\s+hora|jornada|cargo\s+de\s+confian[cç]a|fun[cç][aã]o\s+gratificada|art\.?\s*224", full_text):
        temas.append("Jornada & 7ª/8ª Hora")
    if re.search(r"contingente|efetivo\s+m[ií]nimo|servi[cç]o\s+essencial|60%|70%|80%", full_text):
        temas.append("Contingenciamento Mínimo")
    if re.search(r"vale[\s-]?alimenta|vale[\s-]?refei|aux[ií]lio[\s-]?alimenta|cesta", full_text):
        temas.append("Auxílio Alimentação & Cesta")
    if re.search(r"reajuste|inpc|ipca|perda\s+inflacion[aá]ria|aumento\s+real", full_text):
        temas.append("Reajuste Salarial")
    if re.search(r"teletrabalho|home\s*office|trabalho\s+remoto|h[ií]brido", full_text):
        temas.append("Teletrabalho & Regime Híbrido")
    if re.search(r"piquete|interdito|turba[cç][aã]o|livre\s+acesso", full_text):
        temas.append("Piquetes & Acesso")
    if re.search(r"advogado|honor[aá]rio|advocef", full_text):
        temas.append("Advogados & Honorários da CEF")
    if re.search(r"comum\s+acordo|art\.?\s*114.*§\s*2", full_text):
        temas.append("Comum Acordo Constitucional")
    if not temas:
        temas = ["Cláusulas Gerais do ACT"]

    # Desfecho
    disp = clean_html(reg.get("dispositivo", "")).lower()
    desfecho = "Em Andamento / Despacho"
    if "homolog" in disp or "acordo" in disp:
        desfecho = "Acordo Homologado"
    elif "negar-lhe provimento" in disp or "negou-se provimento" in disp:
        desfecho = "Recurso Desprovido (Mantida Decisão Anterior)"
    elif "dar-lhe provimento" in disp or "deu-se provimento" in disp:
        desfecho = "Recurso Provido pelo TST"
    elif re.search(r"homolog[ao]|homologa[cç][aã]o|acordo\s+coletivo\s+homologado|autocomposi[cç][aã]o", full_text):
        desfecho = "Acordo Homologado"
    elif re.search(r"senten[cç]a\s+normativa|julgado\s+procedente|julgado\s+improcedente|fixa-se\s+a\s+cl[aá]usula", full_text):
        desfecho = "Sentença Normativa Fixada"
    elif re.search(r"defiro\s+parcialmente|defiro\s+o\s+pedido\s+liminar|concedo\s+a\s+tutela|medida\s+liminar", full_text):
        desfecho = "Liminar Deferida (Parcial ou Total)"
    elif re.search(r"indefiro\s+o\s+pedido|indefiro\s+a\s+liminar|denego", full_text):
        desfecho = "Liminar Indeferida"
    elif re.search(r"extin[cç][aã]o\s+do\s+processo|sem\s+resolu[cç][aã]o\s+de\s+m[eé]rito|falta\s+de\s+comum\s+acordo|perda\s+de\s+objeto", full_text):
        desfecho = "Extinto sem Resolução de Mérito"

    # Contextualização do Impacto
    if "Acordo Homologado" in desfecho:
        impacto = "Conquista homologada: as cláusulas negociadas entre a Caixa e os sindicatos ganharam força executiva judicial, resguardando direitos e benefícios acordados sem risco de anulação."
    elif "Liminar" in desfecho:
        impacto = "Medida cautelar de urgência: fixação de contingente de trabalho e garantia de vigência provisória de direitos até a decisão colegiada final."
    elif "Sentença Normativa" in desfecho:
        impacto = "Decisão judicial impositiva da SDC: fixação compulsória de cláusulas pelo TST com vigência legal para os empregados da Caixa."
    elif "Recurso Provido" in desfecho:
        impacto = "Reforma no TST: acolhimento da tese recursal pelo Tribunal Superior, adequando a decisão regional ao entendimento consolidado da corte."
    elif "Recurso Desprovido" in desfecho:
        impacto = "Decisão mantida no TST: a corte rejeitou o recurso, confirmando o julgado anterior favorável à jurisprudência pacífica da SDC."
    elif "dias parados" in full_text and "desconto" in full_text:
        impacto = "Discussão direta sobre a legalidade do desconto de salários de greve e a aplicação de compensação de jornada em favor dos empregados."
    elif "plr" in full_text:
        impacto = "Disputa coletiva envolvendo o pagamento e as regras de distribuição da PLR e PLR Social da Caixa."
    elif "saúde caixa" in full_text:
        impacto = "Acompanhamento de regras de custeio, coparticipação e sustentabilidade do plano de assistência médica Saúde Caixa."
    else:
        impacto = "Acompanhamento processual de direitos coletivos dos empregados da Caixa no TST."

    link_pje = f"https://pje.tst.jus.br/consultaprocessual/detalhe-processo/{cnj.replace('-', '').replace('.', '')}" if cnj else ""

    return {
        "id": reg.get("id", ""),
        "cnj": cnj,
        "numFormatado": num_formatado,
        "classe": classe,
        "relator": relator,
        "dataPublicacao": data_pub,
        "poloCaixa": polo_caixa,
        "partesContrarias": parte_contraria[:120],
        "desfecho": desfecho,
        "temas": temas,
        "docType": doc_type,
        "resumoImpacto": impacto,
        "conteudoLimpo": clean_content,
        "linkPje": link_pje,
    }


def main():
    logger.info("Iniciando extração jurimétrica aperfeiçoada com limpeza estrutural de ementas e despachos...")

    all_decisions = []
    seen_cnjs = set()

    # 1. Carrega casos emblemáticos configurados no JSON
    flagships = load_flagship_cases()
    for fc in flagships:
        all_decisions.append(fc)
        seen_cnjs.add(fc.get("cnj"))
    logger.info("Casos emblemáticos carregados: %d", len(flagships))

    # 2. Carrega do cache local completo com mais de 50 decisões reais da Caixa
    cache_candidates = [
        PROJECT_ROOT / "all_entity_records.json",
        PROJECT_ROOT.parent / "all_entity_records.json",
        PROJECT_ROOT / "scraping_dissidio_coletivo_greve" / "all_entity_records.json",
    ]
    cache_file = next((p for p in cache_candidates if p.is_file()), None)

    if cache_file:
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                all_records_by_entity = json.load(f)

            caixa_raw_records = []
            for k, recs in all_records_by_entity.items():
                if "caixa econ" in k.lower() or "cef" in k.lower():
                    caixa_raw_records.extend(recs)
            logger.info("Registros da Caixa encontrados no cache: %d", len(caixa_raw_records))

            for reg in caixa_raw_records:
                parsed = process_caixa_record(reg)
                cnj = parsed.get("cnj")
                if cnj and cnj in seen_cnjs:
                    continue
                if cnj:
                    seen_cnjs.add(cnj)
                all_decisions.append(parsed)
        except Exception as e:
            logger.error("Erro ao carregar cache de entidades: %s", e)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_paths = [
        OUTPUT_DIR / "dados_decisoes_caixa.json",
        PROJECT_ROOT / "dados_decisoes_caixa.json",
    ]

    for p in out_paths:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(all_decisions, f, ensure_ascii=False, indent=2)

    logger.info("Extração concluída com sucesso! Total de decisões catalogadas: %d", len(all_decisions))


if __name__ == "__main__":
    main()
