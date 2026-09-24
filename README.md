# Radar Dissídio Coletivo ACT Caixa 2026–2028 ⚖️🏦

> Plataforma de jurimetria, raspagem de dados e inteligência tática sobre dissídios coletivos e greves de estatais brasileiras no Tribunal Superior do Trabalho (TST), com foco especial na campanha salarial e no ACT da Caixa Econômica Federal.

🌐 **Acesse o Dashboard Online:** [https://rafaamft.github.io/Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028/](https://rafaamft.github.io/Radar-Diss-dio-Coletivo-ACT-Caixa-2026-2028/)

---

## 📌 Contexto em Tempo Real (24/09/2026)

Em 24 de setembro de 2026, a Caixa Econômica Federal protocolou pedido de **Dissídio Coletivo de Greve** perante o TST após 15 dias de paralisação nacional e rejeição das propostas anteriores em assembleia.

* **Fase Processual Atual:** Mediação Pré-Processual de Conciliação (Ato GVP nº 01/2019).
* **Condução:** Vice-Presidência do TST — **Ministro Guilherme Augusto Caputo Bastos**.
* **Status de Distribuição:** O processo **ainda não foi distribuído para relator na SDC**; a distribuição para sentença normativa só ocorre se as tentativas de acordo na Vice-Presidência fracassarem.
* **Medida Cautelar da Caixa:** O banco requereu a ultratividade temporária do ACT anterior até 31/08/2026 para assegurar a vigência ininterrupta do **Saúde Caixa** e tíquetes durante as negociações.

---

## 🖥️ Painel Interativo (Dashboard)

O projeto conta com interfaces ricas para visualização dos dados:

1. **`index.html` / `dashboard_cef_empregado.html`**: Painel tático voltado ao empregado da Caixa:
   * **🚨 Radar do Dissídio 2026:** Acompanhamento do status processual, ultratividade e linha do tempo da greve.
   * **🤝 O Mediador (Min. Caputo Bastos):** Como funciona a fase conciliatória e a formulação da Proposta do Tribunal.
   * **🌡️ Termômetro do ACT (4 Camadas):** Saúde Caixa, PLR Social, 7ª e 8ª hora, tíquetes e teletrabalho com comparativo entre Proposta da Caixa, Reivindicação do Comando e Meio-Termo Provável no TST.
   * **⚖️ STF, SEST & Riscos:** Limites orçamentários da SEST/DEST, Temas 435 e 1046 do STF e estabilidades.
   * **🏛️ Se a Mediação Fracassar (SDC):** Quem são os relatores possíveis e os riscos do arbitramento judicial.

2. **`dashboard_geral_estatais.html`**: Visão macro comparativa de 707 acórdãos da SDC e 396 decisões das 8 Turmas abrangendo 48 estatais brasileiras (Correios, Petrobras, Caixa, Banco do Brasil, Eletrobras, etc.).

---

## 📊 Estrutura dos Dados e Jurimetria

Os dados foram minerados diretamente da API de jurisprudência do TST (`jurisprudencia-backend.tst.jus.br`) cobrindo o decênio 2016–2026:

* **SDC (Seção de Dissídios Coletivos):** 707 processos de estatais classificados por Ministro Relator, declaração de abusividade, desconto salarial (OJ 10) e desfecho processual.
* **8 Turmas do TST:** 396 acórdãos mapeados sobre reflexos individuais da greve (desconto de dias, estabilidades, cumprimento de sentença normativa e incidência da Súmula 126).
* **Base Específica da Caixa:** 179 acórdãos catalogados e analisados em 27 dimensões temáticas.

---

## 🛠️ Scripts e Pipeline

* `scraping_dissidio_coletivo_greve/sdc_ministers_profile.py`: Análise e perfilamento decisório dos ministros relatores da SDC.
* `scraping_dissidio_coletivo_greve/turmas_behavior_analysis.py`: Mapeamento comparativo e taxa de provimento nas 8 Turmas.
* `scraping_dissidio_coletivo_greve/analyze_cef_complex.py`: Extração e frequência das 27 cláusulas complexas do ACT Caixa.
* `test_sdc_profile.py` e `test_turmas_behavior.py`: Bateria de testes automatizados unitários garantindo a integridade dos dados e da taxonomia jurídica.

---

## 📄 Arquivos Consolidados

* `dissidios_coletivos_estatais_2016_2026.xlsx`: Base consolidada de dissídios em estatais (Suscitantes e Suscitadas).
* `perfil_ministros_sdc_tst.xlsx` / `.json`: Matriz decisória dos Ministros da SDC.
* `comportamento_turmas_tst.xlsx` / `.json`: Matriz comportamental das 8 Turmas.
* `MAPA_TEMATICO_CEF.md`: Diagnóstico analítico detalhado das cláusulas em disputa.
