"""Utilitários para validação, extração e normalização de números de processo padrão CNJ e tribunais."""

import re
from typing import Optional, Dict, Any
from config.constants import TRT_MAP


def extract_cnj(record: Dict[str, Any]) -> Optional[str]:
    """
    Extrai o número padronizado CNJ (NNNNNNN-DD.AAAA.5.TR.OOOO) a partir de um registro bruto do TST.
    Tenta primeiro numFormatado/numero e recorre ao objeto numeracaoUnica se necessário.
    """
    if not record or not isinstance(record, dict):
        return None

    # Tentativa direta em campos formatados
    num = record.get("numFormatado") or record.get("numero")
    if num:
        match = re.search(r"(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})", str(num))
        if match:
            return match.group(1)

    # Tentativa no dicionário numeracaoUnica
    nu = record.get("numeracaoUnica")
    if isinstance(nu, dict) and nu.get("numero"):
        try:
            return (
                f"{int(nu['numero']):07d}-{int(nu['digito']):02d}."
                f"{int(nu['ano'])}.{int(nu['orgao'])}."
                f"{int(nu['tribunal']):02d}.{int(nu['vara']):04d}"
            )
        except (ValueError, TypeError, KeyError):
            pass

    return None


def extract_tribunal(cnj: Optional[str]) -> str:
    """
    Identifica o tribunal de origem a partir do código do TRT no CNJ (.5.XX.).
    Se for .5.00. ou não especificado, retorna 'TST'.
    """
    if not cnj:
        return "TST"
    m_trt = re.search(r"\.5\.(\d{2})\.", cnj)
    if m_trt:
        trt_code = int(m_trt.group(1))
        return TRT_MAP.get(trt_code, f"TRT-{trt_code:02d}")
    return "TST"


def extract_year_from_cnj(cnj: Optional[str]) -> str:
    """
    Extrai o ano de ajuizamento a partir da numeração padrão CNJ (campo AAAA).
    Exemplo: 1000975-72.2026.5.00.0000 -> '2026'
    """
    if not cnj:
        return ""
    m = re.search(r"\.\d{2}\.(\d{4})\.5\.", cnj)
    if m:
        return m.group(1)
    # Fallback caso a estrutura CNJ tenha pequenas variações
    m2 = re.search(r"-?\d{2}\.(\d{4})\.", cnj)
    return m2.group(1) if m2 else ""


def extract_classe_processual(cod_fase: Optional[str]) -> str:
    """
    Normaliza a sigla ou código de fase para o nome descritivo padronizado da classe processual.
    """
    cf = (cod_fase or "").upper()
    if "DCG" in cf:
        return "Dissídio Coletivo de Greve (DCG)"
    if "DC" in cf and "RO" not in cf:
        return "Dissídio Coletivo (DC)"
    if "RODC" in cf:
        return "Recurso Ordinário em Dissídio Coletivo (RODC)"
    if "ROT" in cf:
        return "Recurso Ordinário Trabalhista (ROT)"
    if "RO" in cf:
        return "Recurso Ordinário (RO)"
    return cod_fase if cod_fase else "Dissídio Coletivo"
