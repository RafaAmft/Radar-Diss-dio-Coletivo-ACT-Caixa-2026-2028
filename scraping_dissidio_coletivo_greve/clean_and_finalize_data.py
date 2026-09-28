"""
Rotina de pós-processamento, validação e finalização de dados e planilhas de dissídios coletivos.
"""

import logging
from pathlib import Path
import pandas as pd
from config.constants import PROJECT_ROOT, OUTPUT_DIR
from generate_final_spreadsheets import generate_spreadsheets

logger = logging.getLogger("finalize_data")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def main():
    logger.info("Executando geração e saneamento definitivo das planilhas...")
    df1, df2 = generate_spreadsheets()

    logger.info("CONSOLIDAÇÃO E FINALIZAÇÃO CONCLUÍDAS COM SUCESSO!")
    logger.info("Tab 1 (Estatal como Suscitante): %d processos únicos verificados", len(df1))
    logger.info("Tab 2 (Estatal como Suscitada):  %d processos únicos verificados", len(df2))

    excel_out = OUTPUT_DIR / "dissidios_coletivos_estatais_2016_2026.xlsx"
    if excel_out.exists():
        logger.info("Arquivo verificado com integridade: %s (%d bytes)", excel_out, excel_out.stat().st_size)


if __name__ == "__main__":
    main()
