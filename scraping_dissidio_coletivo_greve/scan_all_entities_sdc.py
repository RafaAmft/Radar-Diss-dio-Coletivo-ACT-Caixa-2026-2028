"""
Varredura automatizada na SDC do TST para quantificação preliminar de dissídios por empresa estatal.
Utiliza o catálogo canônico de ESTATAIS_INFO e o cliente TstApiClient.
"""

import logging
from typing import Dict, Set
from config.constants import (
    ESTATAIS_INFO,
    SDC_ORGAO_JUDICANTE,
    CLASSES_DISSIDIO,
    CLASSES_RECURSO,
)
from utils.tst_api import TstApiClient

logger = logging.getLogger("scan_entities")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def scan_entities_sample(max_terms_per_entity: int = 2) -> Dict[str, int]:
    """
    Executa busca rápida para cada estatal mapeada e retorna a contagem de processos únicos na página inicial.
    """
    client = TstApiClient()
    all_classes = CLASSES_DISSIDIO + CLASSES_RECURSO
    results: Dict[str, int] = {}

    logger.info("Iniciando varredura rápida de processos na SDC por entidade estatal...")

    for formal_name, patterns in ESTATAIS_INFO:
        unique_procs: Set[str] = set()
        # Filtra termos simplificados para a query da API a partir dos padrões
        # Ex: r'\bECT\b' -> 'ECT'
        search_terms = []
        for p in patterns:
            term = p.replace(r'\b', '').replace(r'\s+', ' ').replace(r'S\.?A\.?', 'S/A')
            # remove caracteres regex complexos
            clean_term = "".join(c for c in term if c.isalnum() or c in " /.-").strip()
            if clean_term and len(clean_term) >= 3 and clean_term not in search_terms:
                search_terms.append(clean_term)

        for term in search_terms[:max_terms_per_entity]:
            payload = {
                "ou": "", "e": term, "termoExato": "", "naoContem": "", "ementa": "", "dispositivo": "",
                "numeracaoUnica": {"numero": "", "ano": "", "digito": "", "orgao": "5", "tribunal": "", "vara": ""},
                "orgaosJudicantes": SDC_ORGAO_JUDICANTE,
                "ministros": [], "convocados": [],
                "classesProcessuais": all_classes,
                "codigosClassesPrecedentes": [], "indicadores": [], "assuntos": [],
                "tipos": ["ACORDAO", "DESPACHO"], "orgao": "TST",
                "publicacaoInicial": None, "publicacaoFinal": None,
                "julgamentoInicial": "2016-09-24",
                "julgamentoFinal": "2026-09-24",
                "ordenacao": "data"
            }

            data = client.fetch_page(offset=1, page_size=20, payload=payload)
            if data:
                tot = data.get("totalRegistros", 0)
                regs = data.get("registros", [])
                for reg in regs:
                    item = reg.get("registro", {})
                    num = item.get("numFormatado") or item.get("numero")
                    if num:
                        unique_procs.add(str(num))
                logger.info("  [%s] termo '%s' -> %d ocorrências totais (amostra de %d na primeira página)",
                            formal_name, term, tot, len(regs))

        results[formal_name] = len(unique_procs)

    print("\nRESUMO DA VARREDURA (Processos únicos na primeira página):")
    for k, v in sorted(results.items(), key=lambda x: x[1], reverse=True):
        if v > 0:
            print(f"  {k}: {v}")

    return results


if __name__ == "__main__":
    scan_entities_sample()
