# -*- coding: utf-8 -*-
"""
Script para atualizar o README.md principal (raiz do repositório)
com documentação de nível de produção para publicação no LinkedIn e portfólio.
"""

import os

ROOT_README = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "README.md"))

CONTENT = """# ⚖️ Radar de Dissídios Coletivos & Jurimetria Caixa (TST 2026–2028)

[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-success?style=for-the-badge&logo=github)](https://rafaamft.github.io/Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Jurisprudência TST](https://img.shields.io/badge/Dados-TST%20SDC%20%26%20Turmas-0052cc?style=for-the-badge)](https://jurisprudencia.tst.jus.br/)
[![DeepSeek AI](https://img.shields.io/badge/IA%20Preditiva-DeepSeek%20R1%2FV3-6366f1?style=for-the-badge)](https://deepseek.com)
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=for-the-badge)](LICENSE)

> **Plataforma de Jurimetria Empírica, Engenharia de Dados e Inteligência Artificial Preditiva** aplicada aos conflitos coletivos de trabalho, focada no **Dissídio Coletivo de Greve do ACT Caixa 2026/2028 (DCG 1000975-72.2026.5.00.0000)** e na jurisprudência histórica do Tribunal Superior do Trabalho (TST).

🌐 **Acesse o Dashboard Interativo Online:**  
👉 **[https://rafaamft.github.io/Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028/](https://rafaamft.github.io/Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028/)**

---

## 📌 Visão Geral do Projeto

As campanhas salariais de grandes empresas estatais federais historicamente sofrem com assimetria de informações, volatilidade jurídica e expectativas irreais de ambas as partes.

Este projeto resolve esse problema através da **ciência de dados jurídicos (Jurimetria)** e de **Modelos de Linguagem Avançados (LLMs)**, transformando mais de duas décadas de acórdãos, despachos do PJe e relatórios da Seção Especializada em Dissídios Coletivos (SDC) do TST em:
1. **Predições probabilísticas fundamentadas** sobre a sentença final de cada cláusula.
2. **Matriz de precedentes vinculantes** que condicionam o voto do relator.
3. **Dashboards interativos de alto nível executivo** para negociadores, dirigentes sindicais, advogados e colaboradores.

---

## 🗺️ As 4 Interfaces do Painel Online

| Interface | URL / Página | Objetivo Principal |
|---|---|---|
| ⚡ **Radar Matriz Executivo** | [`index.html`](https://rafaamft.github.io/Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028/) | **Página Principal**: Cruzamento em 3 colunas entre os 5 precedentes históricos do TST, o impasse de 2026 e o veredito antecipado da IA. |
| 📚 **Catálogo Jurimétrico Caixa** | [`decisoes_caixa.html`](https://rafaamft.github.io/Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028/decisoes_caixa.html) | Acervo completo com **51 acórdãos da Caixa (2005–2026)**, filtros instantâneos, ementas completas e módulo de predição DeepSeek. |
| 🏢 **Macrovisão das 48 Estatais** | [`dashboard_geral_estatais.html`](https://rafaamft.github.io/Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028/dashboard_geral_estatais.html) | Radiografia de 700+ processos na SDC de 48 empresas públicas (Correios, Petrobras, Caixa, etc.), perfil dos 16 ministros e das 8 Turmas. |
| ⚙️ **Painel com Abas Detalhadas** | [`index_tabs_backup.html`](https://rafaamft.github.io/Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028/index_tabs_backup.html) | Versão tática profunda dividida em abas temáticas, linha do tempo da greve e proteções do trabalhador grevista. |

---

## 🏛️ O Caso em Julgamento: DCG 1000975-72.2026.5.00.0000

* **Órgão Julgador:** Tribunal Superior do Trabalho — Seção de Dissídios Coletivos (SDC)
* **Relator Oficial:** **Ministro Mauricio Godinho Delgado** *(maior autoridade acadêmica da SDC, com 15 decisões anteriores da Caixa)*
* **Status Atual:** Sessão de julgamento pautada.
* **Liminar Interina Deferida (24/09/2026):**
  * ❌ Rejeitou a pretensão da Caixa de exigir 80% do efetivo em agências.
  * ✅ **Fixou o contingente mínimo em 60% por unidade**, garantindo 40% do efetivo em greve legítima.
  * ✅ **Prorrogou a vigência das cláusulas benéficas do ACT** anterior provisoriamente, afastando a caducidade do Saúde Caixa e auxílios (ultratividade cautelar).

---

## ⚡ A Matriz dos 5 Precedentes que Definem o Dissídio Atual

A Justiça do Trabalho não decide em terreno virgem. O modelo jurimétrico correlaciona cada ponto de travamento do ACT 2026 com os acórdãos paradigma da SDC:

```
┌─────────────────────────────────┐     ┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│     1. PRECEDENTE HISTÓRICO     │ ──> │      2. IMPASSE NO ACT 2026     │ ──> │    3. VEREDITO PREVISTO (IA)    │
│  Acórdão do TST / Tese Jurídica │     │ Posição CEF vs Posição Comando  │     │ Probabilidade & Decisão Final   │
└─────────────────────────────────┘     └─────────────────────────────────┘     └─────────────────────────────────┘
```

```markdown
1. Custeio do Saúde Caixa e Déficit Atuarial
   • Precedente: TST-DC-1000295-05.2017 (Rel. Min. Aloysio Corrêa da Veiga)
   • Tese: SDC veda criação compulsória de plano assistencial sem teto ou em colapso atuarial (CGPAR 52 / Basileia III).
   • Impasse 2026: Sindicatos pedem retorno ao custeio 70/30 sem teto. Caixa propõe 50/50 com teto de 6,5% a 9% da folha.
   • Veredito IA: 70% de probabilidade de manutenção do teto orçamentário da Caixa. O TST não concederá 70/30 na sentença.

2. Tratamento dos 15 Dias de Greve
   • Precedente: TST-RO-1000911-91.2015 (Relª. Minª. Kátia Arruda)
   • Tese: Greves motivadas por impasse de ACT não autorizam corte salarial punitivo; prioridade absoluta para compensação.
   • Impasse 2026: Caixa requereu corte integral de 100% dos salários. Sindicatos pedem compensação em 180 dias (Cláusula 87).
   • Veredito IA: 85% de probabilidade de vitória dos trabalhadores. Godinho fixará compensação sem desconto em folha.

3. Contingente Mínimo de Atendimento
   • Precedente: TST-RO-1001254-87.2015 (Rel. Min. Mauricio Godinho Delgado)
   • Tese: Serviços bancários são essenciais apenas para benefícios sociais e compensação. Exigir > 70% viola a CF/88.
   • Impasse 2026: Caixa ajuizou cautelar requerendo 80% do efetivo. Sindicatos propuseram 30% a 40%.
   • Veredito IA: 95% de certeza de confirmação da liminar: teto de 60% por agência, mantendo 40% do quadro em greve legal.

4. Reajuste Salarial & PLR Social
   • Precedente: TST-RO-240-29.2016 (Relª. Minª. Cristina Peduzzi)
   • Tese: Precedente Normativo nº 37 veda aumento real compulsório em estatais federais sem lastro na SEST/MGI.
   • Impasse 2026: Sindicatos pedem INPC + 2,5% e distribuição linear da PLR Social. Caixa limita à FENABAN e regras SEST.
   • Veredito IA: 90% de chance de fixação estrita de 100% do INPC acumulado. Ganho real condicionado a acordo de mesa.

5. Ultratividade do ACT & Prorrogação de Direitos
   • Precedente: STF ADPF 323 & Tema 1046
   • Tese: O STF revogou a ultratividade automática. Direitos vencem se não houver acordo ou tutela cautelar expressa.
   • Impasse 2026: Para evitar o vácuo de benefícios, a própria Caixa pediu judicialmente a extensão provisória de vigência.
   • Veredito IA: 90% de certeza de manutenção de todas as conquistas do ACT anterior até a publicação do acórdão.
```

---

## 🧠 Módulo de Inteligência Artificial (DeepSeek R1/V3)

O projeto inclui um pipeline de preparação de dados para LLMs no diretório `output/ai_dataset/`:
* `dataset_caixa_ai.json`: Formato estruturado para bancos de vetores e **RAG** (Retrieval-Augmented Generation).
* `dataset_caixa_ai.jsonl`: Formato linha-a-linha com ementas e metadados para **fine-tuning**.
* `knowledge_base_caixa.md`: Base textual condensada com sumário analítico dos 51 julgados.
* `analise_previsao_sentenca_godinho.md`: Relatório preditivo completo gerado pelo modelo DeepSeek R1/V3.

### Métricas de Acordo Histórico na SDC (Caixa Econômica Federal)
* **Total de Julgados Mapeados:** 51
* **Acordos Homologados:** 37,3% (19 acórdãos)
* **Recursos Desprovidos:** 13,7% (7 acórdãos)
* **Processos em Andamento / Despacho:** 25,5% (13 processos)
* **Relator Mais Frequente:** Min. Mauricio Godinho Delgado (15 decisões)

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem & Backend:** Python 3.10+, Pandas, OpenPyXL, Requests, Unittest.
* **Frontend:** Vanilla HTML5, Tailwind CSS, Google Fonts (Inter & JetBrains Mono), design responsivo mobile-first.
* **IA & Jurimetria:** Modelagem preditiva com DeepSeek R1/V3, Engenharia de Prompts Jurídicos, RAG Datasets.
* **DevOps & CI/CD:** GitHub Actions para monitoramento diário do TST e deploy automático via GitHub Pages.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o Repositório
```bash
git clone https://github.com/RafaAmft/Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028.git
cd Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028/scraping_dissidio_coletivo_greve
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar o Dashboard Localmente
```bash
python -m http.server 8000 --directory ..
```
Acesse no seu navegador: `http://localhost:8000/index.html`

### 4. Executar Scripts do Pipeline
* **Gerar a nova página inicial:** `python generate_clean_index.py`
* **Atualizar o catálogo de 51 decisões:** `python generate_decisoes_caixa_html.py`
* **Exportar dataset para IA (JSON, JSONL, Markdown):** `python export_ai_dataset.py`
* **Monitorar novas movimentações no TST:** `python monitor_diario_tst.py`
* **Executar suíte de testes unitários:** `python -m unittest discover tests`

---

## 👤 Autor

**Rafael Augusto Masson Fontes**  
Analista de Dados • Jurimetria • Inteligência Artificial aplicada ao Direito  
🔗 **[Conecte-se comigo no LinkedIn](https://www.linkedin.com/in/rafael-augusto-masson-fontes-94228a27a/)**

---

## 📄 Licença

Este projeto é disponibilizado sob a licença [MIT](LICENSE). Dados públicos extraídos do portal da Justiça do Trabalho em conformidade com a Lei de Acesso à Informação (Lei nº 12.527/2011).
"""

def main():
    print(f"Atualizando README.md raiz em: {ROOT_README}")
    with open(ROOT_README, "w", encoding="utf-8") as f:
        f.write(CONTENT)
    print("README.md raiz atualizado com sucesso!")

if __name__ == "__main__":
    main()
