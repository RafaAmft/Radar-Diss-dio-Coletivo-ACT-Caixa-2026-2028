"""Utilitários para correspondência e classificação de empresas estatais e sanitização de dados."""

import re
import html as html_lib
from typing import Optional, List, Tuple, Pattern
from config.constants import ESTATAIS_INFO

# Pré-compilação dos padrões regex para ganho substancial de desempenho em lotes de grande escala
COMPILED_ESTATAIS: List[Tuple[str, List[Pattern]]] = [
    (formal_name, [re.compile(p, re.IGNORECASE) for p in pats])
    for formal_name, pats in ESTATAIS_INFO
]


def check_entity_match(text: Optional[str]) -> Optional[str]:
    """
    Verifica se o texto informado cita alguma das empresas estatais mapeadas.
    Retorna o nome formal da entidade ou None.
    """
    if not text:
        return None
    for formal_name, patterns in COMPILED_ESTATAIS:
        for p in patterns:
            if p.search(text):
                return formal_name
    return None


def clean_party(name: Optional[str]) -> str:
    """
    Limpa e normaliza a string contendo a identificação da parte processual,
    removendo tags HTML, referências a advogados, carimbos de gabinete e artigos iniciais.
    """
    if not name:
        return ""
    
    # Remove eventuais tags HTML e desfaz entidades
    name = re.sub(r"<[^>]+>", " ", str(name))
    name = html_lib.unescape(name)
    
    # Remove anotações burocráticas anexadas ao nome no TST
    name = re.sub(r"Advogad[ao].*$", "", name, flags=re.I)
    name = re.sub(r"PROCESSO SOB A [EÉ]?GIDE.*$", "", name, flags=re.I)
    name = re.sub(r"RECURSO ORDIN[AÁ]RIO.*$", "", name, flags=re.I)
    name = re.sub(r"GVPGCB.*$", "", name, flags=re.I)
    name = re.sub(r"GMMCP.*$", "", name, flags=re.I)
    name = re.sub(r"GMKA.*$", "", name, flags=re.I)
    
    # Normaliza espaços
    name = re.sub(r"\s+", " ", name).strip()
    # Remove artigos iniciais soltos
    name = re.sub(r"^(o|a|os|as)\s+", "", name, flags=re.I)
    name = name.strip(" .,;:-")
    
    # Limita tamanho excessivo para manter tabelas legíveis
    if len(name) > 250:
        name = name[:250] + "..."
    return name


def sanitize_excel_cell(val: any, max_len: int = 280) -> any:
    """
    Remove caracteres de controle ASCII que causam corrupção ao abrir arquivos XLSX gerados
    pelo openpyxl e limita o tamanho máximo do texto por célula.
    """
    if not isinstance(val, str):
        return val
    # Remove caracteres de controle (ASCII 0 a 31 exceto quebra de linha e tabulação)
    cleaned = "".join(ch for ch in val if ord(ch) >= 32 or ch in "\n\r\t")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if max_len and len(cleaned) > max_len:
        cleaned = cleaned[:max_len] + "..."
    return cleaned
