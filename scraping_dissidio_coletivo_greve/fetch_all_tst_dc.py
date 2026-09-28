"""
Coleta automatizada de todos os Dissídios Coletivos (DC e DCG) na SDC do TST (2016-2026).
Utiliza TstApiClient com retry exponencial e controle de integridade.
"""

import json
import logging
from config.constants import (
    PROJECT_ROOT,
    SDC_ORGAO_JUDICANTE,
    CLASSES_DISSIDIO,
)
from utils.tst_api import TstApiClient

logger = logging.getLogger("fetch_dc")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def fetch_sdc_dc_records(output_filename: str = "sdc_all_dc_dcg.json"):
    payload = {
        "ou": "", "e": "", "termoExato": "", "naoContem": "", "ementa": "", "dispositivo": "",
        "numeracaoUnica": {"numero": "", "ano": "", "digito": "", "orgao": "5", "tribunal": "", "vara": ""},
        "orgaosJudicantes": SDC_ORGAO_JUDICANTE,
        "ministros": [], "convocados": [],
        "classesProcessuais": CLASSES_DISSIDIO,
        "codigosClassesPrecedentes": [], "indicadores": [], "assuntos": [],
        "tipos": ["ACORDAO", "DESPACHO"], "orgao": "TST",
        "publicacaoInicial": None, "publicacaoFinal": None,
        "julgamentoInicial": "2016-09-24",
        "julgamentoFinal": "2026-09-24",
        "ordenacao": "data"
    }

    client = TstApiClient()
    logger.info("Iniciando coleta de todos os DC/DCG na SDC do TST (2016-2026)...")

    records = client.fetch_all(payload=payload, page_size=50, page_delay=0.4)

    output_path = PROJECT_ROOT / output_filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    logger.info("Salvo com sucesso! Total de registros coletados: %d em %s", len(records), output_path)
    return records


if __name__ == "__main__":
    fetch_sdc_dc_records()
