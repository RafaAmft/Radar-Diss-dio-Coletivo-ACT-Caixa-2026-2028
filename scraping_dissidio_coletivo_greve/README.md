# Radar de Dissídios Coletivos e Greves em Empresas Estatais (TST: 2016–2026)

Este projeto implementa uma solução integral de **raspagem de dados (scraping), processamento analítico, saneamento de dados e jurimetria empírica** aplicada aos dissídios coletivos e greves envolvendo empresas estatais federais, estaduais e distritais perante o **Tribunal Superior do Trabalho (TST)** no decênio de 2016 a 2026.

---

## 🎯 Objetivos do Projeto

1. **Coleta Abrangente na SDC e Turmas**: Extração de decisões, acórdãos e despachos da Seção Especializada em Dissídios Coletivos (SDC) e das 8 Turmas do TST.
2. **Classificação Automatizada de Polos**: Identificação precisa de quando a empresa estatal figura como **Suscitante** (autora de ação de dissídio de greve/tutela de urgência) ou como **Suscitada** (ré em dissídios econômicos ou jurídicos ajuizados por sindicatos).
3. **Jurimetria Temática**: Mapeamento de teses críticas como desconto de dias parados (OJ 10 da SDC / Tema 435 do STF), compensação de horas, contingenciamento mínimo em atividades bancárias/essenciais, Saúde Caixa, PLR e ultratividade de acordos coletivos (ACTs).
4. **Perfil Decisório de Ministros e Turmas**: Apuração empírica do perfil decisório dos ministros relatores e das 8 Turmas em matéria paredista.

---

## 🏗️ Arquitetura do Repositório

```plaintext
scraping_dissidio_coletivo_greve/
├── config/
│   ├── __init__.py
│   ├── constants.py              # Catálogo canônico de 50+ estatais, TRTs, URLs da API e classes
│   └── flagship_cases.json       # Casos emblemáticos e decisões liminares recentes configuráveis
├── utils/
│   ├── __init__.py
│   ├── html_utils.py             # Limpeza de HTML e remoção de cabeçalhos burocráticos
│   ├── cnj_utils.py              # Extração/validação de padrão CNJ, TRTs e classes
│   ├── entity_matching.py        # Casamento de estatais pré-compilado, clean_party e sanitização de planilhas
│   └── tst_api.py                # Cliente HTTP padronizado com retry exponencial e controle de falhas
├── output/                       # Diretório centralizado de saídas consolidadas
│   ├── dissidios_coletivos_estatais_2016_2026.xlsx
│   ├── dissidios_estatais_suscitantes.csv
│   ├── dissidios_estatais_suscitadas.csv
│   ├── perfil_ministros_sdc_tst.xlsx / .json
│   ├── comportamento_turmas_tst.xlsx / .json
│   ├── dados_decisoes_caixa.json
│   └── ai_dataset/               # Formatos RAG, Fine-Tuning e Knowledge Base
│       ├── dataset_caixa_ai.json
│       ├── dataset_caixa_ai.jsonl
│       ├── knowledge_base_caixa.md
│       └── analise_previsao_sentenca_godinho.md
├── tests/
│   ├── test_html_utils.py        # Testes de limpeza de tags e parsing de despachos
│   ├── test_cnj_utils.py         # Testes de números CNJ e mapeamento de tribunais
│   └── test_entity_matching.py   # Testes de casamento de regex e sanitização para Excel
├── fetch_all_tst_dc.py           # Coleta de Dissídios Coletivos (DC/DCG)
├── fetch_all_tst_ro.py           # Coleta de Recursos Ordinários (RO/ROT/RODC)
├── scan_all_entities_sdc.py      # Varredura quantitativa preliminar de estatais
├── monitor_diario_tst.py         # Monitor diário com janela deslizante de decisões da Caixa
├── build_dataset.py              # Construção e consolidação analítica do dataset
├── generate_final_spreadsheets.py# Geração definitiva de XLSX/CSV com saneamento de polos
├── clean_and_finalize_data.py    # Validação e auditoria de integridade das planilhas
├── extract_caixa_jurimetria.py   # Extração analítica dos dissídios e liminares da Caixa
├── export_ai_dataset.py          # Exportação do dataset nos padrões RAG / Fine-Tuning para LLMs
├── generate_clean_index.py       # Geração da nova homepage executiva (Matriz Precedente ➔ Veredito)
├── generate_decisoes_caixa_html.py# Geração do catálogo interativo com as 51 decisões da Caixa
├── sdc_ministers_profile.py      # Jurimetria e mapa decisório dos Ministros da SDC
├── turmas_behavior_analysis.py   # Análise do comportamento jurisprudencial das 8 Turmas
├── requirements.txt              # Dependências do projeto
└── README.md                     # Documentação de uso
```

---

## 🚀 Instalação e Configuração

### 1. Pré-requisitos
- Python 3.10 ou superior instalado.

### 2. Instalação das Dependências
No terminal do projeto, execute:
```bash
pip install -r requirements.txt
```

---

## 💻 Guia de Execução

### 1. Geração das Planilhas Consolidadas (Recomendado)
Gera a planilha Excel oficial com as abas **"Estatal Suscitante"** e **"Estatal Suscitada"**, aplicando deduplicação e normalização de partes:
```bash
python generate_final_spreadsheets.py
```
*Saídas geradas em:* `output/dissidios_coletivos_estatais_2016_2026.xlsx` e arquivos CSV correspondentes.

### 2. Jurimetria da Caixa Econômica Federal
Extrai o conjunto analítico de decisões envolvendo a Caixa (incluindo o caso emblemático do DCG 2026 e a liminar do Min. Godinho):
```bash
python extract_caixa_jurimetria.py
```
*Saída gerada em:* `output/dados_decisoes_caixa.json`.

### 3. Perfil Decisório dos Ministros da SDC
Processa centenas de decisões substantivas para calcular taxas empíricas de desconto salarial, acordos homologados e declaração de abusividade por relator:
```bash
python sdc_ministers_profile.py
```
*Saídas geradas em:* `output/perfil_ministros_sdc_tst.xlsx` e `output/perfil_ministros_sdc_tst.json`.

### 4. Análise de Comportamento das 8 Turmas do TST
Analisa o padrão decisório das Turmas recursais quanto ao desconto de dias parados e à incidência de óbices como a Súmula 126 do TST:
```bash
python turmas_behavior_analysis.py
```
*Saídas geradas em:* `output/comportamento_turmas_tst.xlsx` e `output/comportamento_turmas_tst.json`.

### 5. Monitoramento Diário de Movimentações
Executa varredura diária no TST para monitorar novos andamentos e despachos:
```bash
python monitor_diario_tst.py
```

### 6. Execução dos Testes Automatizados
Para rodar a suíte de testes unitários:
```bash
python -m unittest discover tests
```

---

## 📊 Dicionário de Dados das Planilhas

A planilha `dissidios_coletivos_estatais_2016_2026.xlsx` possui as seguintes colunas padronizadas:

| Coluna | Descrição |
|---|---|
| `número CNJ` | Numeração única padrão CNJ (`NNNNNNN-DD.AAAA.5.TR.OOOO`). |
| `tribunal` | Tribunal competente (TST ou TRT de origem regional). |
| `classe` | Classe processual formal (ex: DCG, DC, RODC, ROT). |
| `data de ajuizamento` | Data em que a ação coletiva foi ajuizada. |
| `suscitante` | Nome limpo da parte que instaurou o dissídio. |
| `suscitado(s)` | Entidades sindicais ou patronais suscitadas. |
| `tipo` | Natureza do dissídio: Greve, Econômico, Jurídico ou Revisional. |
| `relator` | Ministro ou Desembargador relator da decisão. |
| `situação/resultado` | Acordo Homologado, Sentença Normativa, Extinto sem Resolução de Mérito, etc. |
| `ano de vigência do ACT/DC` | Período de vigência do instrumento coletivo normativo. |
| `fonte (URL)` | Link direto para consulta processual oficial no TST. |
| `nível de confiança` | Grau de confirmação documental ("confirmado em fonte primária"). |

---

## 🛡️ Robustez e Boas Práticas Implementadas

- **Codificação UTF-8 Limpa**: Correção de caracteres de substituição corrompidos (`\ufffd`) que existiam em scripts legados.
- **Proteção OpenPyXL**: Tratamento sistemático de caracteres de controle ASCII (< 32) que causavam `IllegalCharacterError` no Excel.
- **Resiliência de Caminhos**: Uso de `pathlib.Path` dinâmico em todos os módulos, permitindo execução a partir de qualquer diretório de trabalho.
- **Tratamento de Falhas HTTP**: O `TstApiClient` implementa limite máximo de tentativas com backoff exponencial, eliminando risco de loops infinitos em caso de instabilidade na API do Tribunal.
