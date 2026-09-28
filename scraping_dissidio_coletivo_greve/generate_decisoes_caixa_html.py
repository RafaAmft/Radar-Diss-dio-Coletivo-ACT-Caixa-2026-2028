"""
Gera o painel interativo HTML exclusivo da Caixa no TST (decisoes_caixa.html)
com design moderno, filtros por tema, relator e desfecho, visualizador de ementas/despachos
e painel preditivo de Inteligência Artificial para o julgamento da SDC.
"""

import json
from pathlib import Path

# Carregar dados processados
CANDIDATE_PATHS = [
    Path("dados_decisoes_caixa.json"),
    Path("../dados_decisoes_caixa.json"),
    Path("output/dados_decisoes_caixa.json"),
]

data_file = next((p for p in CANDIDATE_PATHS if p.is_file()), None)
if not data_file:
    raise FileNotFoundError("Não foi possível encontrar dados_decisoes_caixa.json")

with open(data_file, "r", encoding="utf-8") as f:
    decisions = json.load(f)

json_str = json.dumps(decisions, ensure_ascii=False)
total_decisoes = len(decisions)

html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jurimetria Caixa no TST — {total_decisoes} Decisões Coletivas Mapeadas</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {{
      --background: #000000;
      --card: #0d1117;
      --content: #161b22;
      --border: #30363d;
      --foreground: #f0f6fc;
      --muted-foreground: #8b949e;
      --primary: #3b82f6;
      --primary-foreground: #ffffff;
    }}
    html, body {{
      background-color: #000000 !important;
      color: #f0f6fc !important;
    }}
    .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }}
    .fade-in {{ animation: fadeIn 0.25s ease-out; }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .glow-blue {{ box-shadow: 0 0 16px rgba(59, 130, 246, 0.15); }}
    .glow-green {{ box-shadow: 0 0 16px rgba(34, 197, 94, 0.15); }}
    .glow-red {{ box-shadow: 0 0 16px rgba(239, 68, 68, 0.2); }}
    .glow-purple {{ box-shadow: 0 0 20px rgba(168, 85, 247, 0.2); }}
    .badge {{ display: inline-flex; align-items: center; gap: 4px; padding: 2px 10px; border-radius: 9999px; font-size: 11px; font-weight: 600; }}
    .filter-btn {{ transition: all 0.2s ease; cursor: pointer; }}
    .filter-btn.active {{ background: var(--primary); color: #ffffff; font-weight: 600; border-color: var(--primary); }}
    .sticky-top-container {{
      position: sticky;
      top: 0;
      z-index: 100;
      background-color: #000000;
    }}
    /* Custom scrollbar */
    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-track {{ background: #000000; }}
    ::-webkit-scrollbar-thumb {{ background: #30363d; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #484f58; }}
  </style>
</head>
<body class="bg-[#000000] text-[#f0f6fc] antialiased">

  <!-- CABEÇALHO FIXO COM FUNDO PRETO SÓLIDO (Z-INDEX 100) -->
  <div class="sticky-top-container border-b border-[#30363d]">
    <header class="px-4 sm:px-6 py-3.5 bg-[#000000]">
      <div class="max-w-[1300px] mx-auto flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <span class="text-2xl">🏛️</span>
          <div>
            <div class="flex flex-wrap items-center gap-2">
              <h1 class="text-base sm:text-lg md:text-xl font-bold tracking-tight text-white">
                Jurimetria Exclusiva da CAIXA no TST
              </h1>
              <span class="badge bg-blue-500/20 text-blue-400 border border-blue-500/30 text-[10px] sm:text-xs">
                {total_decisoes} Decisões Coletivas Mapeadas (2016–2026)
              </span>
            </div>
            <p class="text-[11px] sm:text-xs text-[#8b949e] mt-0.5">
              Base oficial de Dissídios Coletivos de Greve (DCG), Econômicos (DC) e Recursos na SDC
            </p>
          </div>
        </div>

        <!-- Links de Navegação entre Painéis -->
        <div class="flex flex-wrap items-center gap-2">
          <a href="index.html" class="text-xs bg-[#161b22] hover:bg-[#30363d] border border-[#30363d] rounded-lg px-2.5 py-1.5 font-medium transition-colors flex items-center gap-1.5 text-white">
            <span>🌡️</span>
            <span>Termômetro ACT 2026</span>
          </a>
          <a href="dashboard_geral_estatais.html" class="text-xs bg-[#161b22] hover:bg-[#30363d] border border-[#30363d] rounded-lg px-2.5 py-1.5 font-medium transition-colors flex items-center gap-1.5 text-white">
            <span>📊</span>
            <span>48 Estatais</span>
          </a>
        </div>
      </div>
    </header>
  </div>

  <!-- CONTEÚDO PRINCIPAL -->
  <main class="max-w-[1300px] mx-auto px-4 sm:px-6 py-4 sm:py-6 relative z-10 space-y-6">

    <!-- CARD FLAGSHIP: PROCESSO VIVO DE 2026 (MIN. GODINHO DELGADO) -->
    <div class="card glow-red border-red-500/40 bg-gradient-to-r from-red-500/10 via-transparent to-transparent">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-[var(--border)]">
        <div>
          <div class="flex flex-wrap items-center gap-2 mb-1.5">
            <span class="badge bg-red-500 text-white font-bold animate-pulse">PROCESSO ATIVO • SDC / TST</span>
            <span class="text-xs font-mono text-red-300">DCG 1000975-72.2026.5.00.0000</span>
            <span class="badge bg-green-500/20 text-green-400 border border-green-500/40">Liminar Deferida em 24/09 (20:57)</span>
          </div>
          <h2 class="text-lg sm:text-xl font-bold text-white">
            Decisão Liminar: Min. Mauricio Godinho Delgado no Dissídio Coletivo da Caixa
          </h2>
          <p class="text-xs text-[var(--muted-foreground)] mt-1 max-w-4xl">
            O Relator indeferiu o pedido da Caixa de 80% e fixou contingenciamento mínimo de <strong>60% por agência</strong> (presencial ou remoto), garantindo <strong>40% da categoria em greve legítima</strong>. Garantiu a <strong>prorrogação integral do ACT 2024/2026 (incluindo Saúde Caixa)</strong>, rejeitou a proibição de piquetes e <strong>derrubou o segredo de justiça</strong> (salvo a Nota Técnica Atuarial GESAD nº 10336/2026).
          </p>
        </div>

        <div class="flex flex-col sm:flex-row items-center gap-2 flex-shrink-0">
          <a href="https://pje.tst.jus.br/pjekz/validacao/26092420574531700000207281146?instancia=3" target="_blank" class="w-full sm:w-auto text-xs bg-red-600 hover:bg-red-500 text-white px-3.5 py-2 rounded-lg font-bold transition-colors flex items-center justify-center gap-2">
            <span>📄</span>
            <span>Validar Liminar no PJe</span>
          </a>
        </div>
      </div>

      <!-- Métricas da Decisão Liminar -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 text-xs">
        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <span class="text-[10px] text-green-400 font-bold uppercase block mb-0.5">Contingenciamento</span>
          <strong class="text-white text-sm">60% do Efetivo</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-0.5">Caixa pediu 80%; Godinho fixou 60% com multa diária de R$ 100 mil.</p>
        </div>
        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <span class="text-[10px] text-blue-400 font-bold uppercase block mb-0.5">Saúde Caixa & Benefícios</span>
          <strong class="text-white text-sm">ACT Prorrogado</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-0.5">Cláusulas normativas anteriores vigentes até julgamento de mérito.</p>
        </div>
        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <span class="text-[10px] text-amber-400 font-bold uppercase block mb-0.5">Piquetes e Acesso</span>
          <strong class="text-white text-sm">Pedido Indeferido</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-0.5">Sem provas de violência; competência é das Varas do Trabalho.</p>
        </div>
        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <span class="text-[10px] text-purple-400 font-bold uppercase block mb-0.5">Pauta da SDC</span>
          <strong class="text-white text-sm">Terça (29/09) • 14:30</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-0.5">Defesa sindical até sábado 13h; julgamento definitivo na terça.</p>
        </div>
      </div>
    </div>

    <!-- SEÇÃO: PREVISÃO DE IA & JURIMETRIA PREDITIVA (DEEPSEEK R1/V3 + SDC/TST) -->
    <div class="card glow-purple border-purple-500/40 bg-gradient-to-br from-[#130d24] via-[var(--card)] to-[var(--card)] space-y-4">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-[var(--border)]">
        <div class="flex items-center gap-3">
          <span class="text-2xl p-2 bg-purple-500/20 rounded-xl border border-purple-500/30">🧠</span>
          <div>
            <div class="flex flex-wrap items-center gap-2">
              <span class="badge bg-purple-500/20 text-purple-300 border border-purple-500/40 font-bold">PREVISÃO DE IA • SDC / TST</span>
              <span class="text-xs text-[var(--muted-foreground)]">Modelo: DeepSeek R1/V3 + Base TST ({total_decisoes} Decisões)</span>
              <span class="badge bg-green-500/20 text-green-400 border border-green-500/30">Sessão SDC: 29/09 às 14:30</span>
            </div>
            <h2 class="text-base sm:text-lg font-bold text-white mt-1">
              Prognóstico Preditivo da Sentença de Mérito: Min. Mauricio Godinho Delgado
            </h2>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <a href="output/ai_dataset/analise_previsao_sentenca_godinho.md" target="_blank" class="text-xs bg-purple-600 hover:bg-purple-500 text-white font-semibold px-3 py-1.5 rounded-lg border border-purple-400/30 transition-colors flex items-center gap-1.5">
            <span>📄</span>
            <span>Relatório de IA (.md)</span>
          </a>
        </div>
      </div>

      <!-- Veredito Antecipado -->
      <div class="p-3.5 bg-black/60 rounded-xl border border-purple-500/30">
        <div class="text-[10px] text-purple-400 font-bold uppercase tracking-wider mb-1 flex items-center gap-1.5">
          <span>⚡</span>
          <span>Veredito Antecipado da Inteligência Artificial (Probabilidade Estimada: 85%+)</span>
        </div>
        <p class="text-xs sm:text-sm text-white leading-relaxed">
          "A probabilidade de Godinho manter as balizas da liminar e proferir uma sentença desfavorável às reivindicações financeiras máximas dos sindicatos é <strong>alta (85%+)</strong>, adotando uma abordagem de ponderação: <strong>confirmar garantias básicas</strong>, <strong>restringir excessos sindicais</strong> e <strong>preservar a higidez econômico-atuarial da Caixa</strong> (contingente de 60%, manutenção do teto de 6,5% e compensação em 180 dias pela Cláusula 87)."
        </p>
      </div>

      <!-- Grade de Probabilidades por Tema -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 text-xs">
        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] text-green-400 font-bold uppercase">Contingente Mínimo</span>
            <span class="badge bg-green-500/20 text-green-300 text-[10px]">95% • Muito Alto</span>
          </div>
          <strong class="text-white text-xs block">60% do Efetivo Mantido</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Rejeição definitiva dos 80% pleiteados pela Caixa. Assegura 40% em greve legítima.</p>
        </div>

        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] text-blue-400 font-bold uppercase">ACT Anterior</span>
            <span class="badge bg-blue-500/20 text-blue-300 text-[10px]">95% • Muito Alto</span>
          </div>
          <strong class="text-white text-xs block">Sem Ultratividade Definitiva</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Prorrogação provisória até celebração de novo acordo, sem conferir vigência perpétua.</p>
        </div>

        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] text-amber-400 font-bold uppercase">Piquetes e Acesso</span>
            <span class="badge bg-amber-500/20 text-amber-300 text-[10px]">90% • Muito Alto</span>
          </div>
          <strong class="text-white text-xs block">Interdito Indeferido</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Piquetes pacíficos de convencimento preservados. Eventuais abusos apurados no 1º grau.</p>
        </div>

        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] text-purple-400 font-bold uppercase">Dias Parados</span>
            <span class="badge bg-purple-500/20 text-purple-300 text-[10px]">85% • Alto</span>
          </div>
          <strong class="text-white text-xs block">Compensação em 180 Dias</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Acolhimento da Cláusula 87 da Caixa ou partilha 50/50. Desconto apenas se não compensado.</p>
        </div>

        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] text-rose-400 font-bold uppercase">Teto Saúde Caixa</span>
            <span class="badge bg-rose-500/20 text-rose-300 text-[10px]">80% • Alto</span>
          </div>
          <strong class="text-white text-xs block">Teto de 6,5% Preservado</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Rejeição do modelo 70/30 por impacto financeiro e LRF. Avaliação de ampliação pós-2027.</p>
        </div>

        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] text-cyan-400 font-bold uppercase">Mensalidade e Cota</span>
            <span class="badge bg-cyan-500/20 text-cyan-300 text-[10px]">75% • Médio-Alto</span>
          </div>
          <strong class="text-white text-xs block">3,7% + R$ 560 (Teto 9%)</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Manutenção da estrutura da Caixa com ajustes marginais e proteção às faixas menores.</p>
        </div>

        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] text-emerald-400 font-bold uppercase">Regras da PLR</span>
            <span class="badge bg-emerald-500/20 text-emerald-300 text-[10px]">80% • Alto</span>
          </div>
          <strong class="text-white text-xs block">Redutor Linear Mantido</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Preservação dos critérios de distribuição com exigência de transparência nas metas.</p>
        </div>

        <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)]">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] text-indigo-400 font-bold uppercase">Tendência Geral</span>
            <span class="badge bg-indigo-500/20 text-indigo-300 text-[10px]">SDC / TST</span>
          </div>
          <strong class="text-white text-xs block">Ponderação Institucional</strong>
          <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Proteção à população usuária dos serviços Caixa sem desidratar o direito de greve.</p>
        </div>
      </div>

      <!-- Fundamentos Econômico-Financeiros e Atuariais dos Autos -->
      <div class="p-3.5 bg-[#161b22] rounded-xl border border-[var(--border)] space-y-2">
        <div class="text-[11px] font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
          <span>📊</span>
          <span>Fundamentos Econômico-Atuariais nos Autos (Doc. 03 e Doc. 04 - Nota Técnica GESAD nº 10336/2026)</span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2 text-xs">
          <div class="bg-black/40 p-2.5 rounded-lg border border-[var(--border)]">
            <span class="text-[10px] text-[var(--muted-foreground)] block">Déficit Histórico (desde 2016)</span>
            <strong class="text-rose-400 text-sm">R$ 1,86 Bilhão</strong>
            <p class="text-[10px] text-[var(--muted-foreground)] mt-0.5">Déficit estrutural acumulado no custeio do plano Saúde Caixa.</p>
          </div>
          <div class="bg-black/40 p-2.5 rounded-lg border border-[var(--border)]">
            <span class="text-[10px] text-[var(--muted-foreground)] block">Impacto do Modelo 70/30</span>
            <strong class="text-amber-400 text-sm">- R$ 11,01 Bilhões</strong>
            <p class="text-[10px] text-[var(--muted-foreground)] mt-0.5">Pretensão sindical que derrubaria o Índice de Basileia abaixo do piso prudencial.</p>
          </div>
          <div class="bg-black/40 p-2.5 rounded-lg border border-[var(--border)]">
            <span class="text-[10px] text-[var(--muted-foreground)] block">Teto Estatutário da Folha</span>
            <strong class="text-blue-400 text-sm">6,5% Limite Máximo</strong>
            <p class="text-[10px] text-[var(--muted-foreground)] mt-0.5">Vedação estatutária e submissão estrita ao art. 22 da Lei de Responsabilidade Fiscal.</p>
          </div>
          <div class="bg-black/40 p-2.5 rounded-lg border border-[var(--border)]">
            <span class="text-[10px] text-[var(--muted-foreground)] block">Cláusula 87 (Compensação)</span>
            <strong class="text-green-400 text-sm">Até 180 Dias</strong>
            <p class="text-[10px] text-[var(--muted-foreground)] mt-0.5">Prazo estendido para quitação de horas sem desconto imediato em folha.</p>
          </div>
        </div>
      </div>

      <!-- Checklist de Aferição Pós-Julgamento (29/09) -->
      <div class="p-3 bg-black/40 rounded-xl border border-[var(--border)]">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center gap-1.5 text-xs font-bold text-white">
            <span>🎯</span>
            <span>Matriz de Aferição Pós-Julgamento (Sessão SDC de 29/09 às 14:30)</span>
          </div>
          <span class="badge bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px]">Aguardando Acórdão Oficial</span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 text-[11px]">
          <div class="flex items-center justify-between p-2 bg-[var(--content)] rounded-lg border border-[var(--border)]">
            <span>1. Contingente 60% confirmado</span>
            <span class="badge bg-gray-500/20 text-gray-400 border border-gray-500/30">⏳ Em Julgamento</span>
          </div>
          <div class="flex items-center justify-between p-2 bg-[var(--content)] rounded-lg border border-[var(--border)]">
            <span>2. ACT prorrogado sem ultratividade</span>
            <span class="badge bg-gray-500/20 text-gray-400 border border-gray-500/30">⏳ Em Julgamento</span>
          </div>
          <div class="flex items-center justify-between p-2 bg-[var(--content)] rounded-lg border border-[var(--border)]">
            <span>3. Piquetes pacíficos preservados</span>
            <span class="badge bg-gray-500/20 text-gray-400 border border-gray-500/30">⏳ Em Julgamento</span>
          </div>
          <div class="flex items-center justify-between p-2 bg-[var(--content)] rounded-lg border border-[var(--border)]">
            <span>4. Compensação 180 dias (Cl. 87)</span>
            <span class="badge bg-gray-500/20 text-gray-400 border border-gray-500/30">⏳ Em Julgamento</span>
          </div>
          <div class="flex items-center justify-between p-2 bg-[var(--content)] rounded-lg border border-[var(--border)]">
            <span>5. Teto 6,5% do Saúde Caixa mantido</span>
            <span class="badge bg-gray-500/20 text-gray-400 border border-gray-500/30">⏳ Em Julgamento</span>
          </div>
          <div class="flex items-center justify-between p-2 bg-[var(--content)] rounded-lg border border-[var(--border)]">
            <span>6. Critérios de PLR preservados</span>
            <span class="badge bg-gray-500/20 text-gray-400 border border-gray-500/30">⏳ Em Julgamento</span>
          </div>
        </div>
      </div>
    </div>

    <!-- CARDS DE ESTATÍSTICAS JURIMÉTRICAS GERAIS DA CAIXA -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
      <div class="card p-4">
        <div class="text-[11px] text-[var(--muted-foreground)] font-semibold uppercase">Total de Processos Mapeados</div>
        <div class="text-2xl sm:text-3xl font-bold mt-1 text-white">{total_decisoes}</div>
        <p class="text-[11px] text-blue-400 mt-1">Dissídios Coletivos e Recursos na SDC</p>
      </div>

      <div class="card p-4">
        <div class="text-[11px] text-[var(--muted-foreground)] font-semibold uppercase">Taxa de Acordo Homologado</div>
        <div class="text-2xl sm:text-3xl font-bold mt-1 text-green-400">37,3%</div>
        <p class="text-[11px] text-[var(--muted-foreground)] mt-1">19 processos resolvidos por autocomposição</p>
      </div>

      <div class="card p-4">
        <div class="text-[11px] text-[var(--muted-foreground)] font-semibold uppercase">Maior Relator Histórico</div>
        <div class="text-2xl sm:text-3xl font-bold mt-1 text-purple-400">Godinho (15)</div>
        <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Quase 30% das decisões na SDC</p>
      </div>

      <div class="card p-4">
        <div class="text-[11px] text-[var(--muted-foreground)] font-semibold uppercase">Sentença Normativa / Mérito</div>
        <div class="text-2xl sm:text-3xl font-bold mt-1 text-amber-400">13,7%</div>
        <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Recursos e sentenças com fixação de cláusulas</p>
      </div>
    </div>

    <!-- BARRA DE PESQUISA E FILTROS INTERATIVOS -->
    <div class="card space-y-4">
      <div class="flex flex-col md:flex-row gap-3 items-center justify-between">
        <!-- Campo de Busca -->
        <div class="w-full md:w-1/2 relative">
          <input 
            type="text" 
            id="searchInput" 
            placeholder="Buscar por CNJ, relator, sindicato, tema (ex: saúde caixa, horas, dias parados)..."
            class="w-full bg-[var(--content)] border border-[var(--border)] rounded-xl px-4 py-2.5 text-xs text-white placeholder-[#8b949e] focus:outline-none focus:border-blue-500 transition-colors"
            oninput="renderDecisions()"
          />
          <span class="absolute right-3.5 top-2.5 text-[#8b949e] text-sm">🔍</span>
        </div>

        <!-- Filtros Suspensos de Apoio -->
        <div class="flex flex-wrap items-center gap-2 w-full md:w-auto">
          <select 
            id="relatorFilter" 
            class="bg-[var(--content)] border border-[var(--border)] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
            onchange="renderDecisions()"
          >
            <option value="todos">Todos os Relatores</option>
            <option value="Mauricio Godinho Delgado">Min. Mauricio Godinho Delgado</option>
            <option value="Katia Magalhaes Arruda">Min. Kátia Arruda</option>
            <option value="Ives Gandra">Min. Ives Gandra</option>
            <option value="Maria Cristina Irigoyen Peduzzi">Min. Cristina Peduzzi</option>
            <option value="Dora Maria Da Costa">Min. Dora Maria da Costa</option>
          </select>

          <select 
            id="desfechoFilter" 
            class="bg-[var(--content)] border border-[var(--border)] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
            onchange="renderDecisions()"
          >
            <option value="todos">Todos os Desfechos</option>
            <option value="Acordo Homologado">Acordo Homologado</option>
            <option value="Liminar">Decisão Liminar</option>
            <option value="Sentença Normativa">Sentença Normativa</option>
            <option value="Recurso">Recursos Providos / Desprovidos</option>
            <option value="Extinto">Extinto sem Resolução</option>
          </select>
        </div>
      </div>

      <!-- Filtros Rápidos por Tema (Pills) -->
      <div class="flex flex-wrap items-center gap-1.5 pt-2 border-t border-[var(--border)]">
        <span class="text-[11px] text-[var(--muted-foreground)] mr-1">Filtrar por Tema:</span>
        <button class="filter-btn active text-xs px-2.5 py-1 rounded-lg border border-[var(--border)] bg-[var(--content)]" onclick="filterByTema('todos', this)">Todos ({total_decisoes})</button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-[var(--border)] bg-[var(--content)] text-[var(--muted-foreground)]" onclick="filterByTema('Dias Parados & Greve', this)">Dias Parados & Greve</button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-[var(--border)] bg-[var(--content)] text-[var(--muted-foreground)]" onclick="filterByTema('Saúde Caixa', this)">Saúde Caixa</button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-[var(--border)] bg-[var(--content)] text-[var(--muted-foreground)]" onclick="filterByTema('Contingenciamento Mínimo', this)">Contingenciamento</button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-[var(--border)] bg-[var(--content)] text-[var(--muted-foreground)]" onclick="filterByTema('PLR & PLR Social', this)">PLR</button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-[var(--border)] bg-[var(--content)] text-[var(--muted-foreground)]" onclick="filterByTema('Reajuste Salarial', this)">Reajuste Salarial</button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-[var(--border)] bg-[var(--content)] text-[var(--muted-foreground)]" onclick="filterByTema('Advogados & Honorários da CEF', this)">Advogados CEF</button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-[var(--border)] bg-[var(--content)] text-[var(--muted-foreground)]" onclick="filterByTema('Comum Acordo Constitucional', this)">Comum Acordo</button>
      </div>
    </div>

    <!-- CONTADOR E LISTA DE CARDS DE DECISÕES -->
    <div class="flex items-center justify-between text-xs text-[var(--muted-foreground)] px-1">
      <span id="counterText">Exibindo todas as decisões</span>
      <span>Ordem: Mais Recentes Primeiro</span>
    </div>

    <!-- CONTAINER ONDE OS CARDS SÃO RENDERIZADOS VIA JAVASCRIPT -->
    <div id="decisionsContainer" class="space-y-4">
      <!-- Inserido dinamicamente -->
    </div>

  </main>

  <!-- RODAPÉ -->
  <footer class="border-t border-[var(--border)] bg-[#000000] py-6 mt-12 text-center text-xs text-[var(--muted-foreground)]">
    <div class="max-w-[1300px] mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
      <div>
        <span>📡 Radar de Dissídios Coletivos e ACT Caixa (2026–2028)</span>
      </div>
      <div>
        <span>Dados oficiais raspados via API pública do Tribunal Superior do Trabalho (TST)</span>
      </div>
    </div>
  </footer>

  <!-- DADOS EMBUTIDOS E LÓGICA JAVASCRIPT -->
  <script>
    const DECISOES = {json_str};
    let activeTema = 'todos';

    function filterByTema(tema, btn) {{
      activeTema = tema;
      document.querySelectorAll('.filter-btn').forEach(b => {{
        b.classList.remove('active');
        b.classList.add('text-[var(--muted-foreground)]');
      }});
      if (btn) {{
        btn.classList.add('active');
        btn.classList.remove('text-[var(--muted-foreground)]');
      }}
      renderDecisions();
    }}

    function getDesfechoBadge(desfecho) {{
      if (desfecho.includes('Acordo Homologado')) {{
        return '<span class="badge bg-green-500/20 text-green-400 border border-green-500/30">🤝 Acordo Homologado</span>';
      }} else if (desfecho.includes('Liminar')) {{
        return '<span class="badge bg-blue-500/20 text-blue-400 border border-blue-500/30">⚡ Liminar Deferida</span>';
      }} else if (desfecho.includes('Sentença Normativa')) {{
        return '<span class="badge bg-amber-500/20 text-amber-400 border border-amber-500/30">⚖️ Sentença Normativa</span>';
      }} else if (desfecho.includes('Provido')) {{
        return '<span class="badge bg-purple-500/20 text-purple-400 border border-purple-500/30">🔄 Recurso Julgado</span>';
      }} else if (desfecho.includes('Extinto')) {{
        return '<span class="badge bg-gray-500/20 text-gray-400 border border-gray-500/30">❌ Extinto sem Resolução</span>';
      }}
      return '<span class="badge bg-gray-500/20 text-gray-300 border border-gray-500/30">📋 ' + desfecho + '</span>';
    }}

    function toggleEmenta(id) {{
      const el = document.getElementById('ementa-' + id);
      const btn = document.getElementById('btn-ementa-' + id);
      const d = DECISOES[id];
      const isEmenta = d && d.docType && d.docType.includes('Ementa');
      const label = isEmenta ? 'Ementa do Acórdão' : 'Teor do Despacho/Decisão';
      
      if (el.classList.contains('hidden')) {{
        el.classList.remove('hidden');
        btn.innerText = '🔼 Ocultar ' + label;
      }} else {{
        el.classList.add('hidden');
        btn.innerText = (isEmenta ? '📜 Ver ' : '📑 Ver ') + label;
      }}
    }}

    function renderDecisions() {{
      const search = document.getElementById('searchInput').value.toLowerCase().trim();
      const relator = document.getElementById('relatorFilter').value;
      const desfechoFilter = document.getElementById('desfechoFilter').value;
      const container = document.getElementById('decisionsContainer');

      const filtered = DECISOES.filter(d => {{
        // Busca textual
        const textToSearch = (d.cnj + ' ' + d.numFormatado + ' ' + d.relator + ' ' + d.partesContrarias + ' ' + d.temas.join(' ') + ' ' + d.conteudoLimpo + ' ' + d.resumoImpacto).toLowerCase();
        if (search && !textToSearch.includes(search)) return false;

        // Filtro por relator
        if (relator !== 'todos' && !d.relator.includes(relator)) return false;

        // Filtro por desfecho
        if (desfechoFilter !== 'todos' && !d.desfecho.includes(desfechoFilter)) return false;

        // Filtro por tema
        if (activeTema !== 'todos' && !d.temas.includes(activeTema)) return false;

        return true;
      }});

      document.getElementById('counterText').innerHTML = `Exibindo <strong>${{filtered.length}}</strong> de <strong>${{DECISOES.length}}</strong> decisões coletivas da CAIXA`;

      if (filtered.length === 0) {{
        container.innerHTML = `
          <div class="card text-center py-12 text-[var(--muted-foreground)]">
            <span class="text-4xl block mb-2">🔍</span>
            <p class="font-bold text-white text-sm">Nenhuma decisão encontrada com esses filtros</p>
            <p class="text-xs mt-1">Tente remover alguns filtros ou buscar por outros termos.</p>
          </div>
        `;
        return;
      }}

      let html = '';
      filtered.forEach((d, idx) => {{
        const isFlagship = d.is_flagship;
        const borderGlow = isFlagship ? 'border-red-500/50 glow-red' : 'border-[var(--border)]';
        const isEmenta = d.docType && d.docType.includes('Ementa');
        const buttonLabel = isEmenta ? '📜 Ver Ementa do Acórdão' : '📑 Ver Teor do Despacho/Decisão';
        
        let tagsHtml = d.temas.map(t => 
          `<span class="text-[10px] bg-[var(--content)] border border-[var(--border)] text-[#c9d1d9] px-2 py-0.5 rounded-md">${{t}}</span>`
        ).join(' ');

        html += `
          <div class="card ${{borderGlow}} fade-in space-y-3">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-[var(--border)]">
              <div class="flex flex-wrap items-center gap-2">
                <span class="text-xs font-mono font-bold text-blue-400">${{d.numFormatado}}</span>
                <span class="badge bg-[#161b22] text-[#8b949e] border border-[var(--border)]">${{d.classe}}</span>
                <span class="badge bg-purple-500/15 text-purple-300 border border-purple-500/30">${{d.docType}}</span>
                <span class="text-xs text-[var(--muted-foreground)]">📅 ${{d.dataPublicacao}}</span>
              </div>
              <div class="flex items-center gap-2">
                ${{getDesfechoBadge(d.desfecho)}}
              </div>
            </div>

            <!-- Dados Principais do Processo -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
              <div>
                <span class="text-[10px] text-[var(--muted-foreground)] uppercase block">Relator(a)</span>
                <strong class="text-white">${{d.relator}}</strong>
              </div>
              <div>
                <span class="text-[10px] text-[var(--muted-foreground)] uppercase block">Polo da Caixa</span>
                <span class="text-blue-300 font-medium">${{d.poloCaixa}}</span>
              </div>
              <div>
                <span class="text-[10px] text-[var(--muted-foreground)] uppercase block">Parte Contrária</span>
                <span class="text-[var(--foreground)] truncate block" title="${{d.partesContrarias}}">${{d.partesContrarias}}</span>
              </div>
            </div>

            <!-- Temas Discutidos -->
            <div class="flex flex-wrap gap-1.5 items-center pt-1">
              <span class="text-[10px] text-[var(--muted-foreground)] mr-1">Temas:</span>
              ${{tagsHtml}}
            </div>

            <!-- Impacto Prático no Empregado -->
            <div class="bg-[var(--content)] p-3 rounded-lg border border-[var(--border)] text-xs">
              <div class="text-[10px] text-green-400 font-bold uppercase mb-1">Impacto Prático no Empregado Caixa:</div>
              <p class="text-[var(--foreground)] leading-relaxed">${{d.resumoImpacto}}</p>
            </div>

            <!-- Botões de Ação -->
            <div class="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
              <button 
                id="btn-ementa-${{idx}}" 
                onclick="toggleEmenta(${{idx}})" 
                class="text-xs text-blue-400 hover:text-blue-300 font-medium transition-colors flex items-center gap-1.5 bg-[#161b22] px-3 py-1.5 rounded-lg border border-[var(--border)]"
              >
                ${{buttonLabel}}
              </button>
              
              <a 
                href="${{d.linkPje}}" 
                target="_blank" 
                class="text-xs bg-[#161b22] hover:bg-[#30363d] border border-[var(--border)] px-3 py-1.5 rounded-lg text-white font-medium transition-colors flex items-center justify-center gap-1.5"
              >
                <span>🔗</span>
                <span>Consultar no PJe / TST</span>
              </a>
            </div>

            <!-- Bloco oculto com a Ementa ou Despacho Limpo -->
            <div id="ementa-${{idx}}" class="hidden p-3.5 bg-black/70 rounded-lg border border-[var(--border)] text-[11px] text-[var(--foreground)] font-mono whitespace-pre-wrap leading-relaxed">
${{d.conteudoLimpo}}
            </div>
          </div>
        `;
      }});

      container.innerHTML = html;
    }}

    // Iniciar na carga da página
    document.addEventListener('DOMContentLoaded', () => {{
      renderDecisions();
    }});
  </script>
</body>
</html>
"""

# Salvar no diretório atual e no diretório pai (se existir)
output_targets = [
    Path("decisoes_caixa.html"),
    Path("../decisoes_caixa.html"),
]

for target in output_targets:
    try:
        with open(target, "w", encoding="utf-8") as f:
            f.write(html_template)
        print(f"Salvo com sucesso em: {target}")
    except Exception as e:
        print(f"Aviso ao salvar {target}: {e}")

if __name__ == "__main__":
    print("Geração do painel concluída com sucesso!")
