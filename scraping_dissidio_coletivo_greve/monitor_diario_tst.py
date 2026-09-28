"""
Monitoramento diário de movimentações e decisões recentes de dissídios coletivos envolvendo a Caixa Econômica Federal no TST.
"""

import json
import logging
from datetime import datetime
from config.constants import PROJECT_ROOT, OUTPUT_DIR
from utils.html_utils import clean_html
from utils.tst_api import TstApiClient

logger = logging.getLogger("monitor_diario")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def monitor_caixa_dissidio():
    """
    Rastreia despachos, acórdãos e movimentações recentes de dissídios coletivos
    envolvendo a Caixa Econômica Federal no TST.
    """
    client = TstApiClient()
    queries = [
        "Caixa Econômica Federal dissídio",
        "Caputo Bastos Caixa",
        "Contraf Caixa dissídio",
        "1000422-59.2025",
        "1000975-72.2026",
    ]

    found_movements = []
    seen_ids = set()

    logger.info("Iniciando varredura diária no TST para a Caixa Econômica Federal...")

    for q in queries:
        payload = {
            "ou": "", "e": q, "termoExato": "", "naoContem": "", "ementa": "", "dispositivo": "",
            "numeracaoUnica": {"numero": "", "ano": "", "digito": "", "orgao": "5", "tribunal": "", "vara": ""},
            "orgaosJudicantes": [],
            "ministros": [], "convocados": [],
            "classesProcessuais": [],
            "codigosClassesPrecedentes": [], "indicadores": [], "assuntos": [],
            "tipos": ["DESPACHO", "ACORDAO"], "orgao": "TST",
            "publicacaoInicial": None, "publicacaoFinal": None,
            "julgamentoInicial": None, "julgamentoFinal": None,
            "ordenacao": "data"
        }

        data = client.fetch_page(offset=1, page_size=15, payload=payload)
        if not data:
            continue

        for reg in data.get("registros", []):
            rec = reg.get("registro", {})
            num = rec.get("numFormatado") or rec.get("id")
            txt = clean_html(rec.get("txtConteudoDecisao") or rec.get("ementa") or "")

            if num and num not in seen_ids and any(
                k in txt.lower() for k in ["caixa econômica", "cef", "contraf", "dissídio", "acordo coletivo"]
            ):
                seen_ids.add(num)
                found_movements.append({
                    "numero": num,
                    "tipo": rec.get("tipo", {}).get("nome") if isinstance(rec.get("tipo"), dict) else str(rec.get("tipo", "")),
                    "orgao": rec.get("orgaoJudicante", {}).get("descricao", ""),
                    "relator": rec.get("nomRelator", ""),
                    "data_publicacao": rec.get("dtaPublicacao", ""),
                    "data_julgamento": rec.get("dtaJulgamento", ""),
                    "resumo": txt[:350].strip() + "..." if len(txt) > 350 else txt,
                })

    historico = {
        "ultima_execucao": datetime.now().isoformat(),
        "total_registros_relevantes": len(found_movements),
        "registros": found_movements,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    targets = [
        OUTPUT_DIR / "monitoramento_diario_caixa.json",
        PROJECT_ROOT / "monitoramento_diario_caixa.json",
    ]

    for p in targets:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)

    logger.info("Varredura concluída. %d movimentações catalogadas.", len(found_movements))
    return historico


if __name__ == "__main__":
    monitor_caixa_dissidio()
