"""
Exportação do dataset completo de decisões da Caixa Econômica Federal para consumo por IA.

Formatos de saída:
  1. dataset_caixa_ai.json       → JSON estruturado com metadados + contexto (ideal para RAG/vector stores)
  2. dataset_caixa_ai.jsonl      → JSONL com 1 documento por linha (ideal para embeddings e fine-tuning)
  3. knowledge_base_caixa.md     → Markdown consolidado (ideal para prompting direto / system prompt)
  4. dataset_caixa_summary.json  → Resumo estatístico do dataset para validação
"""

import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config.constants import PROJECT_ROOT, OUTPUT_DIR


# ─── Fontes de dados ───────────────────────────────────────────────────────────

DECISOES_FILE = PROJECT_ROOT / "dados_decisoes_caixa.json"
MINISTROS_FILE = PROJECT_ROOT / "perfil_ministros_sdc_tst.json"
TURMAS_FILE = PROJECT_ROOT / "comportamento_turmas_tst.json"

AI_OUTPUT_DIR = OUTPUT_DIR / "ai_dataset"


# ─── Utilitários ───────────────────────────────────────────────────────────────

def _load_json(path: Path) -> Any:
    """Carrega JSON de um arquivo, retorna [] se não existir."""
    if path.is_file():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _sha256_id(text: str) -> str:
    """Gera um hash curto para servir de ID de chunk."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _clean_for_ai(text: str) -> str:
    """Remove artefatos de formatação que atrapalham modelos de IA."""
    if not text:
        return ""
    # Remove emojis de seção (📑 📜 ⚖️)
    text = re.sub(r"[📑📜⚖️]+\s*", "", text)
    # Normaliza múltiplas quebras de linha
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove espaços em excesso
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def _normalize_date(raw: str) -> str:
    """Extrai apenas a data ISO (YYYY-MM-DD) de strings variáveis."""
    if not raw:
        return ""
    match = re.match(r"(\d{4}-\d{2}-\d{2})", raw)
    return match.group(1) if match else raw


# ─── Geração do dataset estruturado (JSON para RAG) ───────────────────────────

def build_ai_documents(decisoes: List[Dict]) -> List[Dict]:
    """
    Converte cada decisão em um documento otimizado para sistemas de IA/RAG.

    Cada documento contém:
      - metadata: campos estruturados para filtragem e busca facetada
      - content: texto integral limpo para indexação semântica
      - summary: resumo curto para preview / re-ranking
    """
    documents = []

    for d in decisoes:
        content_clean = _clean_for_ai(d.get("conteudoLimpo", ""))
        if not content_clean:
            continue

        doc_id = d.get("id", _sha256_id(content_clean))
        cnj = d.get("cnj", "")
        data_pub = _normalize_date(d.get("dataPublicacao", ""))

        # Metadados estruturados para filtragem
        metadata = {
            "id": doc_id,
            "cnj": cnj,
            "numero_formatado": d.get("numFormatado", ""),
            "classe_processual": d.get("classe", ""),
            "relator": d.get("relator", ""),
            "data_publicacao": data_pub,
            "polo_caixa": d.get("poloCaixa", ""),
            "partes_contrarias": d.get("partesContrarias", ""),
            "desfecho": d.get("desfecho", ""),
            "temas": d.get("temas", []),
            "tipo_documento": d.get("docType", ""),
            "link_pje": d.get("linkPje", ""),
            "is_flagship": d.get("is_flagship", False),
            "fonte": "TST - Tribunal Superior do Trabalho",
            "dataset": "Radar Dissídio Coletivo ACT Caixa 2026-2028",
        }

        # Detalhes adicionais da liminar (quando houver)
        if d.get("detalhesLiminar"):
            metadata["detalhes_liminar"] = d["detalhesLiminar"]

        # Argumentos econômico-financeiros e atuariais (quando houver)
        if d.get("argumentosFinanceiros"):
            metadata["argumentos_financeiros"] = d["argumentosFinanceiros"]

        # Resumo para re-ranking
        summary = d.get("resumoImpacto", "")

        # Conteúdo com cabeçalho contextual para melhor retrieval
        header = (
            f"[{d.get('classe', 'Processo')}] {cnj}\n"
            f"Relator: {d.get('relator', 'N/A')} | Data: {data_pub}\n"
            f"Polo Caixa: {d.get('poloCaixa', 'N/A')} | Desfecho: {d.get('desfecho', 'N/A')}\n"
            f"Temas: {', '.join(d.get('temas', []))}\n"
            f"---\n"
        )

        documents.append({
            "metadata": metadata,
            "content": header + content_clean,
            "summary": summary,
            "char_count": len(content_clean),
            "word_count": len(content_clean.split()),
        })

    return documents


# ─── Geração do Knowledge Base em Markdown ─────────────────────────────────────

def build_markdown_kb(
    decisoes: List[Dict],
    ministros: List[Dict],
    turmas: List[Dict],
) -> str:
    """
    Gera um knowledge base consolidado em Markdown para uso direto como
    system prompt ou contexto de chat.
    """
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines.append("# 📚 Base de Conhecimento: Decisões da Caixa Econômica Federal no TST")
    lines.append(f"\n> Gerado automaticamente em {now}")
    lines.append(f"> Dataset: Radar Dissídio Coletivo ACT Caixa 2026-2028")
    lines.append(f"> Total de decisões: {len(decisoes)}")
    lines.append("")

    # ─── Seção 1: Resumo executivo
    lines.append("## 1. Resumo Executivo")
    lines.append("")

    classes = {}
    desfechos = {}
    temas_count = {}
    relatores = {}
    for d in decisoes:
        c = d.get("classe", "N/A")
        classes[c] = classes.get(c, 0) + 1
        de = d.get("desfecho", "N/A")
        desfechos[de] = desfechos.get(de, 0) + 1
        r = d.get("relator", "N/A")
        relatores[r] = relatores.get(r, 0) + 1
        for t in d.get("temas", []):
            temas_count[t] = temas_count.get(t, 0) + 1

    lines.append("### Classes Processuais")
    for k, v in sorted(classes.items(), key=lambda x: -x[1]):
        lines.append(f"- **{k}**: {v} decisões")

    lines.append("")
    lines.append("### Desfechos")
    for k, v in sorted(desfechos.items(), key=lambda x: -x[1]):
        lines.append(f"- **{k}**: {v}")

    lines.append("")
    lines.append("### Temas Mais Frequentes")
    for k, v in sorted(temas_count.items(), key=lambda x: -x[1]):
        lines.append(f"- **{k}**: {v} ocorrências")

    lines.append("")
    lines.append("### Relatores")
    for k, v in sorted(relatores.items(), key=lambda x: -x[1]):
        lines.append(f"- **{k}**: {v} decisões")

    # ─── Seção 2: Decisões Emblemáticas (flagships)
    lines.append("")
    lines.append("## 2. Decisões Emblemáticas")
    lines.append("")

    flagships = [d for d in decisoes if d.get("is_flagship")]
    if flagships:
        for d in flagships:
            lines.append(f"### {d.get('numFormatado', 'N/A')}")
            lines.append(f"- **Relator**: {d.get('relator', 'N/A')}")
            lines.append(f"- **Data**: {_normalize_date(d.get('dataPublicacao', ''))}")
            lines.append(f"- **Desfecho**: {d.get('desfecho', 'N/A')}")
            lines.append(f"- **Temas**: {', '.join(d.get('temas', []))}")
            lines.append(f"- **Impacto**: {d.get('resumoImpacto', '')}")
            if d.get("detalhesLiminar"):
                dl = d["detalhesLiminar"]
                lines.append(f"- **Contingente pedido pela Caixa**: {dl.get('pedidoCaixaContingente', 'N/A')}")
                lines.append(f"- **Contingente deferido**: {dl.get('deferidoGodinhoContingente', 'N/A')}")
                lines.append(f"- **Multa**: {dl.get('multaDescumprimento', 'N/A')}")
                lines.append(f"- **Próximos passos**: {dl.get('proximosPassos', 'N/A')}")
            if d.get("argumentosFinanceiros"):
                af = d["argumentosFinanceiros"]
                lines.append("")
                lines.append("#### Fundamentos Econômico-Financeiros e Atuariais da Caixa:")
                lines.append(f"- **Teto Estatutário da Folha**: {af.get('tetoEstatutarioFolha', 'N/A')}")
                lines.append(f"- **Déficit Acumulado Saúde Caixa**: {af.get('deficitAcumuladoSaude', 'N/A')}")
                lines.append(f"- **Impacto Modelo 70/30 (Pretensão Sindical)**: {af.get('impactoModelo7030', 'N/A')}")
                lines.append(f"- **Proposta de Mensalidade Sustentável**: {af.get('propostaMensalidadeSaude', 'N/A')}")
                lines.append(f"- **Compromisso Pós-2027**: {af.get('compromissoPos2027', 'N/A')}")
                lines.append(f"- **Cláusula 87 (Dias Parados)**: {af.get('clausula87DiasParados', 'N/A')}")
                lines.append(f"- **Regras da PLR**: {af.get('regrasPLR', 'N/A')}")
            lines.append("")
            lines.append("**Conteúdo integral:**")
            lines.append("```")
            lines.append(_clean_for_ai(d.get("conteudoLimpo", ""))[:3000])
            lines.append("```")
            lines.append("")
    else:
        lines.append("Nenhuma decisão emblemática catalogada neste ciclo.")

    # ─── Seção 3: Todas as decisões (resumo tabular)
    lines.append("")
    lines.append("## 3. Catálogo Completo de Decisões")
    lines.append("")
    lines.append("| # | CNJ | Classe | Relator | Data | Desfecho | Temas |")
    lines.append("|---|-----|--------|---------|------|----------|-------|")

    for i, d in enumerate(decisoes, 1):
        cnj = d.get("cnj", "N/A")
        classe = d.get("classe", "N/A")[:20]
        relator = d.get("relator", "N/A")[:25]
        data = _normalize_date(d.get("dataPublicacao", ""))[:10]
        desfecho = d.get("desfecho", "N/A")[:35]
        temas = ", ".join(d.get("temas", []))[:40]
        lines.append(f"| {i} | {cnj} | {classe} | {relator} | {data} | {desfecho} | {temas} |")

    # ─── Seção 4: Conteúdo integral de cada decisão
    lines.append("")
    lines.append("## 4. Conteúdo Integral das Decisões")
    lines.append("")

    for i, d in enumerate(decisoes, 1):
        cnj = d.get("cnj", "N/A")
        lines.append(f"### 4.{i}. [{d.get('classe', 'N/A')}] {cnj}")
        lines.append(f"**Relator**: {d.get('relator', 'N/A')} | "
                      f"**Data**: {_normalize_date(d.get('dataPublicacao', ''))} | "
                      f"**Desfecho**: {d.get('desfecho', 'N/A')}")
        lines.append(f"**Temas**: {', '.join(d.get('temas', []))}")
        lines.append(f"**Resumo**: {d.get('resumoImpacto', '')}")
        lines.append("")
        content = _clean_for_ai(d.get("conteudoLimpo", ""))
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")

    # ─── Seção 5: Perfil dos Ministros da SDC
    if ministros:
        lines.append("## 5. Perfil Jurimétrico dos Ministros da SDC")
        lines.append("")
        lines.append("| Ministro(a) | Total Julgamentos | Greves Abusivas | Taxa Abusividade | Sentenças Normativas | Homologações | Perfil |")
        lines.append("|-------------|-------------------|-----------------|------------------|---------------------|--------------|--------|")

        for m in ministros:
            nome = m.get("Ministro(a) Relator(a)", "N/A")[:30]
            total = m.get("Total Julgamentos Estatais", 0)
            abusivas = m.get("Greves Declaradas Abusivas", 0)
            taxa = m.get("Taxa de Abusividade (%)", 0)
            sent = m.get("Sentenças Normativas", 0)
            homol = m.get("Homologações de Acordo", 0)
            perfil = m.get("Perfil / Tendência Decisória", "N/A")[:50]
            lines.append(f"| {nome} | {total} | {abusivas} | {taxa:.1f}% | {sent} | {homol} | {perfil} |")
        lines.append("")

    # ─── Seção 6: Comportamento das Turmas
    if turmas:
        lines.append("## 6. Comportamento das Turmas do TST")
        lines.append("")
        lines.append("| Turma | Total Julgamentos | Pró-Empresa (%) | Pró-Trabalhador (%) | Súmula 126 (%) | Tendência |")
        lines.append("|-------|-------------------|-----------------|---------------------|----------------|-----------|")

        for t in turmas:
            turma = t.get("Turma do TST", "N/A")
            total = t.get("Total de Julgamentos Analisados", 0)
            pro_emp = t.get("Taxa Desconto Mantido / Pró-Empresa (%)", 0)
            pro_trab = t.get("Taxa Devolução/Compensação / Pró-Trabalhador (%)", 0)
            sum126 = t.get("Aplicação da Súmula 126 / Óbice Fático (%)", 0)
            tend = t.get("Tendência Jurisprudencial Predominante", "N/A")[:60]
            lines.append(f"| {turma} | {total} | {pro_emp:.1f}% | {pro_trab:.1f}% | {sum126:.1f}% | {tend} |")
        lines.append("")

    return "\n".join(lines)


# ─── Geração do sumário estatístico ────────────────────────────────────────────

def build_summary(decisoes: List[Dict], documents: List[Dict]) -> Dict:
    """Gera um resumo estatístico do dataset para validação."""
    total_chars = sum(d["char_count"] for d in documents)
    total_words = sum(d["word_count"] for d in documents)

    classes = {}
    desfechos = {}
    temas = {}
    relatores = {}
    anos = {}

    for d in decisoes:
        c = d.get("classe", "N/A")
        classes[c] = classes.get(c, 0) + 1
        de = d.get("desfecho", "N/A")
        desfechos[de] = desfechos.get(de, 0) + 1
        r = d.get("relator", "N/A")
        relatores[r] = relatores.get(r, 0) + 1
        data = _normalize_date(d.get("dataPublicacao", ""))
        if data:
            ano = data[:4]
            anos[ano] = anos.get(ano, 0) + 1
        for t in d.get("temas", []):
            temas[t] = temas.get(t, 0) + 1

    return {
        "gerado_em": datetime.now().isoformat(),
        "dataset": "Radar Dissídio Coletivo ACT Caixa 2026-2028",
        "fonte": "TST - Tribunal Superior do Trabalho",
        "total_decisoes": len(decisoes),
        "total_documentos_ai": len(documents),
        "total_caracteres": total_chars,
        "total_palavras": total_words,
        "media_palavras_por_doc": total_words // max(len(documents), 1),
        "classes_processuais": dict(sorted(classes.items(), key=lambda x: -x[1])),
        "desfechos": dict(sorted(desfechos.items(), key=lambda x: -x[1])),
        "temas": dict(sorted(temas.items(), key=lambda x: -x[1])),
        "relatores": dict(sorted(relatores.items(), key=lambda x: -x[1])),
        "distribuicao_por_ano": dict(sorted(anos.items())),
        "formatos_exportados": [
            "dataset_caixa_ai.json (RAG / Vector Store)",
            "dataset_caixa_ai.jsonl (Embeddings / Fine-tuning)",
            "knowledge_base_caixa.md (Prompting direto)",
            "dataset_caixa_summary.json (Validação)",
        ],
    }


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print(" 🤖 Exportação do Dataset para IA — Decisões da Caixa no TST")
    print("=" * 70)

    # Carregar fontes
    decisoes = _load_json(DECISOES_FILE)
    ministros = _load_json(MINISTROS_FILE)
    turmas = _load_json(TURMAS_FILE)

    if not decisoes:
        print("❌ Nenhuma decisão encontrada. Execute extract_caixa_jurimetria.py primeiro.")
        return

    print(f"\n📊 Decisões carregadas: {len(decisoes)}")
    print(f"📊 Perfis de ministros: {len(ministros)}")
    print(f"📊 Perfis de turmas: {len(turmas)}")

    # Criar diretório de saída
    AI_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. JSON estruturado (para RAG / Vector Stores)
    print("\n[1/4] Gerando dataset_caixa_ai.json (RAG)...")
    documents = build_ai_documents(decisoes)
    ai_json = {
        "metadata": {
            "dataset": "Radar Dissídio Coletivo ACT Caixa 2026-2028",
            "fonte": "TST - Tribunal Superior do Trabalho",
            "gerado_em": datetime.now().isoformat(),
            "total_documentos": len(documents),
            "descricao": (
                "Dataset estruturado de decisões judiciais da Caixa Econômica Federal "
                "no TST, otimizado para sistemas de Retrieval-Augmented Generation (RAG). "
                "Cada documento contém metadados estruturados para filtragem facetada, "
                "conteúdo integral limpo para indexação semântica, e resumo para re-ranking."
            ),
        },
        "context": {
            "perfil_ministros_sdc": ministros,
            "comportamento_turmas": turmas,
        },
        "documents": documents,
    }

    out_json = AI_OUTPUT_DIR / "dataset_caixa_ai.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(ai_json, f, ensure_ascii=False, indent=2)
    print(f"   ✅ {out_json} ({out_json.stat().st_size / 1024:.1f} KB)")

    # 2. JSONL (para Embeddings / Fine-tuning)
    print("[2/4] Gerando dataset_caixa_ai.jsonl (Embeddings)...")
    out_jsonl = AI_OUTPUT_DIR / "dataset_caixa_ai.jsonl"
    with open(out_jsonl, "w", encoding="utf-8") as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    print(f"   ✅ {out_jsonl} ({out_jsonl.stat().st_size / 1024:.1f} KB)")

    # 3. Markdown Knowledge Base (para Prompting direto)
    print("[3/4] Gerando knowledge_base_caixa.md (Prompting)...")
    md_content = build_markdown_kb(decisoes, ministros, turmas)
    out_md = AI_OUTPUT_DIR / "knowledge_base_caixa.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"   ✅ {out_md} ({out_md.stat().st_size / 1024:.1f} KB)")

    # 4. Sumário estatístico
    print("[4/4] Gerando dataset_caixa_summary.json (Validação)...")
    summary = build_summary(decisoes, documents)
    out_summary = AI_OUTPUT_DIR / "dataset_caixa_summary.json"
    with open(out_summary, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"   ✅ {out_summary} ({out_summary.stat().st_size / 1024:.1f} KB)")

    # Copiar também para a raiz (para acesso fácil pelo GitHub Pages)
    for src in [out_json, out_summary]:
        dst = PROJECT_ROOT / src.name
        with open(dst, "w", encoding="utf-8") as f:
            with open(src, "r", encoding="utf-8") as s:
                f.write(s.read())

    # Resumo final
    print("\n" + "=" * 70)
    print(" ✅ EXPORTAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print(f"\n📁 Diretório de saída: {AI_OUTPUT_DIR}")
    print(f"\n📋 Estatísticas do dataset:")
    print(f"   • Total de decisões: {summary['total_decisoes']}")
    print(f"   • Total de documentos IA: {summary['total_documentos_ai']}")
    print(f"   • Total de palavras: {summary['total_palavras']:,}")
    print(f"   • Média de palavras/doc: {summary['media_palavras_por_doc']:,}")
    print(f"\n📦 Arquivos gerados:")
    print(f"   1. dataset_caixa_ai.json    → RAG / Vector Store (LangChain, LlamaIndex)")
    print(f"   2. dataset_caixa_ai.jsonl   → Embeddings / Fine-tuning")
    print(f"   3. knowledge_base_caixa.md  → Prompting direto (Gemini, ChatGPT, Claude)")
    print(f"   4. dataset_caixa_summary.json → Validação e estatísticas")
    print(f"\n💡 Para usar em IA:")
    print(f"   • Cole o knowledge_base_caixa.md no system prompt de qualquer LLM")
    print(f"   • Indexe o dataset_caixa_ai.json em um vector store (Pinecone, ChromaDB)")
    print(f"   • Use o .jsonl para criar embeddings com OpenAI/Gemini API")


if __name__ == "__main__":
    main()
