"""Utilitários para limpeza e extração estruturada de conteúdo HTML/textual de decisões do TST."""

import re
import html as html_lib
from bs4 import BeautifulSoup


def clean_html(raw_html: str) -> str:
    """
    Remove scripts, styles, tags HTML e entidades especiais,
    retornando texto plano limpo com espaços normalizados.
    """
    if not raw_html:
        return ""
    
    import warnings
    from bs4 import MarkupResemblesLocatorWarning
    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

    # Tratamento preliminar para entidades HTML
    raw_html = html_lib.unescape(raw_html)
    
    if "<" not in raw_html:
        return re.sub(r"\s+", " ", raw_html).strip()

    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()
        
    text = soup.get_text(separator=" ")
    # Normalização de espaços e quebras redundantes
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_clean_document(reg: dict) -> tuple[str, str]:
    """
    Extrai a Ementa Oficial formatada ou o texto substantivo do Despacho/Decisão,
    removendo cabeçalhos burocráticos (PODER JUDICIÁRIO, SUSCITANTE, ADVOGADO, etc.).
    Retorna (tipo_documento, texto_limpo).
    """
    ementa = (reg.get("ementa") or "").strip()
    disp = (reg.get("dispositivo") or "").strip()
    
    if ementa:
        doc_type = "Ementa do Acórdão"
        clean_em = clean_html(ementa)
        clean_text = f"📜 EMENTA OFICIAL:\n{clean_em}"
        if disp:
            clean_disp = clean_html(disp)
            clean_text += f"\n\n⚖️ DISPOSITIVO:\n{clean_disp}"
        return doc_type, clean_text
    
    # Caso seja Despacho ou Decisão Monocrática
    tipo_info = reg.get("tipo", {})
    tipo_nome = tipo_info.get("nome") if isinstance(tipo_info, dict) else "Decisão Monocrática"
    doc_type = f"{tipo_nome} do Relator"
    
    raw_html = reg.get("txtConteudoDecisao") or reg.get("txtConteudoDecisaoHighlight") or ""
    soup = BeautifulSoup(raw_html, "html.parser")
    for s in soup(["script", "style", "noscript"]):
        s.extract()
    raw_text = soup.get_text(separator="\n")
    
    # Filtra linhas burocráticas no início
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    substantive_lines = []
    ignoring_header = True
    
    header_patterns = [
        r"^poder judici[aá]rio",
        r"^justi[cç]a do trabalho",
        r"^tribunal superior do trabalho",
        r"^processo n[ºo]?",
        r"^suscitante",
        r"^suscitad[ao]",
        r"^advogad[ao]",
        r"^relator",
        r"^classe:",
        r"^d\s*e\s*s\s*p\s*a\s*c\s*h\s*o",
        r"^d\s*e\s*c\s*i\s*s\s*[aã]\s*o",
    ]
    
    for line in lines:
        if ignoring_header:
            if any(re.search(pat, line, re.I) for pat in header_patterns):
                continue
            # Quando encontrar a fundamentação ou relatório
            if len(line) > 50 or re.search(r"^(vistos|trata-se|relat[oó]rio|cuida-se|o diss[ií]dio|por meio da)", line, re.I):
                ignoring_header = False
                substantive_lines.append(line)
        else:
            substantive_lines.append(line)
            
    final_content = "\n\n".join(substantive_lines) if substantive_lines else clean_html(raw_html)
    return doc_type, final_content
