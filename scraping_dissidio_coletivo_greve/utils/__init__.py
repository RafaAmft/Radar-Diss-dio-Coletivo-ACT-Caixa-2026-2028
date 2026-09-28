"""Módulo de utilitários para parsing, normalização, casamento de entidades e API do TST."""

from .html_utils import clean_html, extract_clean_document
from .cnj_utils import extract_cnj, extract_tribunal, extract_year_from_cnj, extract_classe_processual
from .entity_matching import check_entity_match, clean_party, sanitize_excel_cell
from .tst_api import TstApiClient

__all__ = [
    "clean_html",
    "extract_clean_document",
    "extract_cnj",
    "extract_tribunal",
    "extract_year_from_cnj",
    "extract_classe_processual",
    "check_entity_match",
    "clean_party",
    "sanitize_excel_cell",
    "TstApiClient",
]
