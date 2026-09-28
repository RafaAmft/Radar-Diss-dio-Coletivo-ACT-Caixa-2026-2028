"""Cliente HTTP padronizado e resiliente para a API de Jurisprudência do TST."""

import time
import logging
from typing import Dict, Any, List, Optional
import requests
from config.constants import API_BASE_URL, DEFAULT_HEADERS

logger = logging.getLogger("tst_scraper")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class TstApiClient:
    """Cliente para consultas paginadas à API do TST com retries e backoff exponencial."""

    def __init__(self, base_url: str = API_BASE_URL, headers: Optional[Dict[str, str]] = None, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or DEFAULT_HEADERS.copy()
        self.timeout = timeout

    def fetch_page(
        self,
        offset: int,
        page_size: int,
        payload: Dict[str, Any],
        max_retries: int = 3,
        base_delay: float = 2.0
    ) -> Optional[Dict[str, Any]]:
        """
        Executa requisição POST para uma página específica com limite máximo de tentativas.
        """
        url = f"{self.base_url}/{offset}/{page_size}"
        
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=self.headers,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    return response.json()
                
                logger.warning(
                    "Tentativa %d/%d: status %d recebido no offset %d.",
                    attempt, max_retries, response.status_code, offset
                )
            except (requests.RequestException, Exception) as exc:
                logger.warning(
                    "Tentativa %d/%d falhou com erro no offset %d: %s",
                    attempt, max_retries, offset, exc
                )

            if attempt < max_retries:
                wait_time = base_delay * (2 ** (attempt - 1))
                time.sleep(wait_time)

        logger.error("Falha definitiva ao obter offset %d após %d tentativas.", offset, max_retries)
        return None

    def fetch_all(
        self,
        payload: Dict[str, Any],
        page_size: int = 50,
        max_retries: int = 3,
        page_delay: float = 0.5,
        total_limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Itera por todas as páginas da pesquisa até atingir totalRegistros ou o limite configurado.
        Retorna a lista de registros extraídos.
        """
        all_records = []
        current_offset = 1
        total_expected = None

        logger.info("Iniciando coleta paginada da API TST...")

        while True:
            data = self.fetch_page(current_offset, page_size, payload, max_retries=max_retries)
            if not data:
                logger.error("Encerrando paginação antecipadamente devido a erro irrecuperável no offset %d.", current_offset)
                break

            if total_expected is None:
                total_expected = data.get("totalRegistros", 0)
                logger.info("Total de registros informados pelo TST: %d", total_expected)

            regs = data.get("registros", [])
            if not regs:
                logger.info("Nenhum registro adicional retornado no offset %d. Paginação concluída.", current_offset)
                break

            for item in regs:
                rec = item.get("registro", {})
                if rec:
                    all_records.append(rec)

            logger.info("Progresso: %d / %d coletados (offset=%d)", len(all_records), total_expected or 0, current_offset)

            if total_limit and len(all_records) >= total_limit:
                logger.info("Limite configurado atingido (%d registros).", total_limit)
                break

            if total_expected and len(all_records) >= total_expected:
                break

            current_offset += page_size
            time.sleep(page_delay)

        logger.info("Coleta concluída com sucesso. Total coletado: %d registros.", len(all_records))
        return all_records
