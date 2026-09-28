# -*- coding: utf-8 -*-
"""
Script para gerar o novo index.html baseado na Alternativa 1:
'Radar Matriz: Precedente TST ➔ Dissídio 2026 ➔ Veredito da IA'
Foco absoluto nas decisões e sentenças históricas que impactaram a Caixa
e sua conexão direta com a sentença do dissídio atual (DCG 2026).
"""

import json
import os

OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index.html"))

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Radar Dissídio Caixa 2026 — Precedentes TST & Previsão da Sentença</title>
  <meta name="description" content="Análise jurimétrica executiva conectando os acórdãos históricos do TST com o Dissídio Coletivo da Caixa 2026/2028 (DCG 1000975-72.2026.5.00.0000).">
  
  <!-- Tailwind CSS & Fonts -->
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">

  <style>
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #090d13;
      color: #e6edf3;
    }
    .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }
    .glass-card {
      background: rgba(18, 24, 38, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(48, 54, 61, 0.6);
      border-radius: 14px;
    }
    .matrix-card {
      background: #0f1623;
      border: 1px solid #1f293d;
      border-radius: 16px;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .matrix-card:hover {
      border-color: #3b82f6;
      box-shadow: 0 10px 30px -10px rgba(59, 130, 246, 0.2);
      transform: translateY(-2px);
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.02em;
    }
    .badge-blue { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-purple { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    .badge-green { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
    .badge-red { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    
    .pill-filter {
      cursor: pointer;
      transition: all 0.2s ease;
      font-size: 12px;
      font-weight: 500;
      padding: 6px 14px;
      border-radius: 9999px;
      border: 1px solid #30363d;
      background: #161b22;
      color: #8b949e;
    }
    .pill-filter.active, .pill-filter:hover {
      background: #2563eb;
      color: #ffffff;
      border-color: #3b82f6;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-blue-600 selection:text-white">

  <!-- Top Navbar -->
  <header class="sticky top-0 z-50 bg-[#090d13]/90 backdrop-blur-md border-b border-[#21262d] px-4 lg:px-8 py-3.5">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
          ⚖️
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-sm sm:text-base font-bold text-white tracking-tight">Radar Jurimétrico Caixa</h1>
            <span class="badge badge-purple text-[10px] py-0.5">DCG 2026/2028</span>
          </div>
          <p class="text-xs text-[#8b949e] hidden sm:block">Precedentes do TST vs. Sentença do Dissídio Coletivo</p>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav class="flex items-center gap-2">
        <a href="decisoes_caixa.html" class="text-xs bg-[#161b22] hover:bg-[#21262d] text-blue-300 hover:text-white border border-blue-500/30 px-3 py-1.5 rounded-lg font-medium transition-all flex items-center gap-1.5 shadow-sm">
          <span>📚 Catálogo (51 Acórdãos)</span>
        </a>
        <a href="dashboard_geral_estatais.html" class="text-xs bg-[#161b22] hover:bg-[#21262d] text-gray-300 hover:text-white border border-[#30363d] px-3 py-1.5 rounded-lg font-medium transition-all hidden md:flex items-center gap-1.5">
          <span>🏢 48 Estatais no TST</span>
        </a>
        <a href="index_tabs_backup.html" class="text-xs bg-[#161b22] hover:bg-[#21262d] text-gray-400 hover:text-white border border-[#30363d] px-2.5 py-1.5 rounded-lg transition-all" title="Ver painel analítico com abas detalhadas">
          <span>⚙️ Modo Abas</span>
        </a>
      </nav>
    </div>
  </header>

  <!-- Main Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-6 space-y-8">

    <!-- HERO SECTION: O PROCESSO ATIVO E O RELATOR -->
    <section class="glass-card p-5 sm:p-7 relative overflow-hidden border-blue-500/30">
      <div class="absolute -right-16 -top-16 w-64 h-64 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -left-16 -bottom-16 w-64 h-64 bg-purple-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <div class="space-y-3 max-w-3xl">
          <div class="flex flex-wrap items-center gap-2">
            <span class="badge badge-green text-xs flex items-center gap-1.5 py-1 px-3">
              <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
              Sessão de Julgamento Pautada
            </span>
            <span class="badge badge-blue text-xs py-1 px-3 font-mono">
              DCG 1000975-72.2026.5.00.0000
            </span>
            <span class="text-xs text-[#8b949e]">TST • Seção de Dissídios Coletivos (SDC)</span>
          </div>

          <h2 class="text-xl sm:text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
            Como os Precedentes do TST Definem a Sentença do Dissídio da Caixa
          </h2>
          
          <p class="text-sm text-[#8b949e] leading-relaxed">
            A Justiça do Trabalho não decide em terreno virgem. O julgamento do ACT Caixa 2026/2028 é a consequência direta de 
            <strong class="text-blue-400">20 anos de jurisprudência</strong>, 
            da doutrina do relator <strong class="text-purple-300">Min. Mauricio Godinho Delgado</strong> e de balizas do STF. 
            Abaixo, correlacionamos as sentenças históricas com os temas centrais do conflito atual.
          </p>
        </div>

        <!-- Relator & Decisão Interina Card -->
        <div class="bg-[#161b22]/90 border border-blue-500/30 rounded-xl p-4 sm:p-5 flex-shrink-0 lg:w-80 space-y-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-purple-500/20 border border-purple-500/40 flex items-center justify-center text-lg">
              👨‍⚖️
            </div>
            <div>
              <div class="text-xs text-purple-400 font-semibold uppercase tracking-wider">Relator Designado</div>
              <div class="text-sm font-bold text-white">Min. Mauricio Godinho</div>
              <div class="text-[11px] text-[#8b949e]">15 julgamentos da Caixa no TST</div>
            </div>
          </div>
          
          <div class="pt-2 border-t border-[#30363d]/80 text-xs space-y-1.5">
            <div class="flex justify-between text-[#8b949e]">
              <span>Liminar deferida:</span>
              <span class="text-green-400 font-semibold">24/Setembro/2026</span>
            </div>
            <div class="flex justify-between text-[#8b949e]">
              <span>Contingente fixado:</span>
              <span class="text-white font-mono font-bold">60% em agências</span>
            </div>
            <div class="flex justify-between text-[#8b949e]">
              <span>Vigência do ACT:</span>
              <span class="text-blue-400 font-semibold">Mantido provisoriamente</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Metrics Strip -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-6 mt-6 border-t border-[#21262d]">
        <div class="bg-[#121824] border border-[#21262d] rounded-xl p-3 text-center">
          <div class="text-xs text-[#8b949e] font-medium">Acórdãos Mapeados</div>
          <div class="text-xl sm:text-2xl font-extrabold text-blue-400 font-mono mt-0.5">51</div>
          <div class="text-[11px] text-[#6e7681]">Base histórica 2005–2026</div>
        </div>
        <div class="bg-[#121824] border border-[#21262d] rounded-xl p-3 text-center">
          <div class="text-xs text-[#8b949e] font-medium">Taxa de Acordos SDC</div>
          <div class="text-xl sm:text-2xl font-extrabold text-green-400 font-mono mt-0.5">37,3%</div>
          <div class="text-[11px] text-[#6e7681]">19 pactos homologados</div>
        </div>
        <div class="bg-[#121824] border border-[#21262d] rounded-xl p-3 text-center">
          <div class="text-xs text-[#8b949e] font-medium">Pedido Cautelar CEF</div>
          <div class="text-xl sm:text-2xl font-extrabold text-amber-400 font-mono mt-0.5">80% ➔ 60%</div>
          <div class="text-[11px] text-[#6e7681]">Rejeição do teto abusivo</div>
        </div>
        <div class="bg-[#121824] border border-[#21262d] rounded-xl p-3 text-center">
          <div class="text-xs text-[#8b949e] font-medium">Previsão IA (DeepSeek)</div>
          <div class="text-xl sm:text-2xl font-extrabold text-purple-400 font-mono mt-0.5">Equilíbrio</div>
          <div class="text-[11px] text-[#6e7681]">Vitórias parciais mútuas</div>
        </div>
      </div>
    </section>

    <!-- SECTION TITLE & FILTERS -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h3 class="text-lg font-bold text-white flex items-center gap-2">
          <span>⚡ Matriz Comparativa: Precedente Histórico ➔ Impasse 2026 ➔ Veredito da Sentença</span>
        </h3>
        <p class="text-xs text-[#8b949e]">Veja como cada cláusula que travou a negociação já tem desfecho delineado pela jurisprudência da SDC.</p>
      </div>

      <!-- Quick Category Filter Pills -->
      <div class="flex flex-wrap items-center gap-1.5" id="filter-pills">
        <button class="pill-filter active" onclick="filterCards('all', this)">Todos (5)</button>
        <button class="pill-filter" onclick="filterCards('saude', this)">Saúde Caixa</button>
        <button class="pill-filter" onclick="filterCards('greve', this)">Greve & Dias Parados</button>
        <button class="pill-filter" onclick="filterCards('salario', this)">Salário & PLR</button>
        <button class="pill-filter" onclick="filterCards('ultratividade', this)">Ultratividade</button>
      </div>
    </div>

    <!-- THE 5 MATRIX CARDS -->
    <div class="space-y-6" id="matrix-container">

      <!-- CARD 1: SAÚDE CAIXA -->
      <article class="matrix-card p-5 sm:p-6" data-category="saude">
        <!-- Card Header -->
        <div class="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-[#21262d]">
          <div class="flex items-center gap-2.5">
            <span class="w-8 h-8 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 flex items-center justify-center font-bold text-sm">
              🏥
            </span>
            <div>
              <h4 class="text-base font-bold text-white">1. Custeio do Saúde Caixa e Déficit Atuarial</h4>
              <p class="text-xs text-[#8b949e]">Proporção 70/30 vs 50/50, teto orçamentário da folha e coparticipação</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="badge badge-amber text-xs">Cláusula mais sensível da mesa</span>
          </div>
        </div>

        <!-- 3 Columns Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 pt-4">
          <!-- Col 1: O Precedente no TST -->
          <div class="bg-[#121824] border border-[#21262d] rounded-xl p-4 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">🏛️ O Precedente no TST</span>
              <span class="badge badge-blue text-[10px]">DC 1000295-05.2017</span>
            </div>
            <div class="text-xs font-semibold text-white">Rel. Min. Aloysio Corrêa da Veiga • SDC</div>
            <p class="text-xs text-[#8b949e] leading-relaxed">
              O TST fixou que em empresas estatais federais, a Justiça do Trabalho <strong>não pode criar benefício assistencial ilimitado</strong> por sentença normativa que comprometa o erário e desborde das resoluções da CGPAR/SEST. A concessão exige estrito equilíbrio atuarial comprovado.
            </p>
            <div class="text-[11px] text-blue-300 font-mono bg-blue-950/40 p-2 rounded border border-blue-800/30">
              Tese: "A autonomia negocial coletiva subordina-se aos limites orçamentários do ente controlador federal."
            </div>
          </div>

          <!-- Col 2: O Embate no ACT 2026 -->
          <div class="bg-[#121824] border border-[#21262d] rounded-xl p-4 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">⚔️ A Disputa no ACT 2026</span>
              <span class="badge badge-amber text-[10px]">Impasse Central</span>
            </div>
            <div class="text-xs font-semibold text-white">Caixa Econômica vs. FENABAN/Sindicatos</div>
            <div class="text-xs space-y-2 text-[#8b949e]">
              <div>
                <strong class="text-gray-300">Posição da Caixa:</strong> Manutenção do teto orçamentário de gastos em 6,5% a 9% da folha e coparticipação adicional de 3,7% do titular para cobrir déficit histórico.
              </div>
              <div>
                <strong class="text-gray-300">Posição dos Sindicatos:</strong> Retorno integral à proporção 70/30 com cobertura de 100% dos déficits pelo banco, rejeitando a taxa de 3,7%.
              </div>
            </div>
          </div>

          <!-- Col 3: O Veredito Preditivo IA -->
          <div class="bg-gradient-to-b from-[#19152b] to-[#121824] border border-purple-500/30 rounded-xl p-4 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-purple-300 uppercase tracking-wider">🎯 Veredito da Sentença (IA)</span>
              <span class="text-xs font-bold text-purple-400 font-mono">70% de Chance</span>
            </div>

            <!-- Probability Bar -->
            <div class="w-full bg-[#21262d] rounded-full h-2 overflow-hidden">
              <div class="bg-purple-500 h-2 rounded-full" style="width: 70%"></div>
            </div>

            <p class="text-xs text-purple-200/90 leading-relaxed">
              <strong>Tendência de Godinho:</strong> Preservará a operabilidade do plano e os direitos dos aposentados, mas <strong>rejeitará a imposição de custeio patronal 70/30 irrestrito</strong>, validando o teto orçamentário da Caixa sob pena de colapso de solvência (Basileia III).
            </p>
            <div class="text-[11px] text-green-400 bg-green-950/40 p-2 rounded border border-green-800/30 flex items-center gap-1.5">
              <span>✅</span>
              <span><strong>Desfecho Previsto:</strong> Manutenção da estrutura com teto e mediação de aporte extraordinário.</span>
            </div>
          </div>
        </div>
      </article>

      <!-- CARD 2: DIAS PARADOS E COMPENSAÇÃO -->
      <article class="matrix-card p-5 sm:p-6" data-category="greve">
        <!-- Card Header -->
        <div class="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-[#21262d]">
          <div class="flex items-center gap-2.5">
            <span class="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-sm">
              🛑
            </span>
            <div>
              <h4 class="text-base font-bold text-white">2. Tratamento dos 15 Dias Parados de Greve</h4>
              <p class="text-xs text-[#8b949e]">Desconto salarial imediato em folha vs. Compensação em banco de horas</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="badge badge-green text-xs">Proteção Salarial do Grevista</span>
          </div>
        </div>

        <!-- 3 Columns Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 pt-4">
          <!-- Col 1: O Precedente no TST -->
          <div class="bg-[#121824] border border-[#21262d] rounded-xl p-4 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">🏛️ O Precedente no TST</span>
              <span class="badge badge-blue text-[10px]">RO 1000911-91.2015</span>
            </div>
            <div class="text-xs font-semibold text-white">Relª. Minª. Kátia Arruda • SDC</div>
            <p class="text-xs text-[#8b949e] leading-relaxed">
              A SDC consolidou que greves não declaradas abusivas decorrentes de impasse genuíno em negociação <strong>não devem ensejar corte de ponto sumário</strong>. O padrão histórico do tribunal em bancos públicos é a compensação em 50% dos dias parados com abono dos demais, ou quitação em 180 dias.
            </p>
            <div class="text-[11px] text-blue-300 font-mono bg-blue-950/40 p-2 rounded border border-blue-800/30">
              Tese: "A compensação de horas resguarda o caráter alimentar dos salários e a higidez do serviço bancário."
            </div>
          </div>

          <!-- Col 2: O Embate no ACT 2026 -->
          <div class="bg-[#121824] border border-[#21262d] rounded-xl p-4 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">⚔️ A Disputa no ACT 2026</span>
              <span class="badge badge-amber text-[10px]">Risco Financeiro</span>
            </div>
            <div class="text-xs font-semibold text-white">Caixa Econômica vs. Sindicatos</div>
            <div class="text-xs space-y-2 text-[#8b949e]">
              <div>
                <strong class="text-gray-300">Posição da Caixa:</strong> Desconto de 100% dos salários dos 15 dias de greve, além de reflexos em 13º salário e férias.
              </div>
              <div>
                <strong class="text-gray-300">Posição dos Sindicatos:</strong> Aplicação estrita da Cláusula 87 do ACT anterior: compensação integral de jornada sem qualquer desconto financeiro.
              </div>
            </div>
          </div>

          <!-- Col 3: O Veredito Preditivo IA -->
          <div class="bg-gradient-to-b from-[#19152b] to-[#121824] border border-purple-500/30 rounded-xl p-4 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-purple-300 uppercase tracking-wider">🎯 Veredito da Sentença (IA)</span>
              <span class="text-xs font-bold text-green-400 font-mono">85% de Chance</span>
            </div>

            <!-- Probability Bar -->
            <div class="w-full bg-[#21262d] rounded-full h-2 overflow-hidden">
              <div class="bg-green-500 h-2 rounded-full" style="width: 85%"></div>
            </div>

            <p class="text-xs text-purple-200/90 leading-relaxed">
              <strong>Tendência de Godinho:</strong> Autor de consagrada doutrina de proteção salarial, Godinho <strong>afastará o corte punitivo de ponto</strong>. A sentença fixará a compensação em banco de horas ampliado (180 dias) com limite diário de até 1 hora extra.
            </p>
            <div class="text-[11px] text-green-400 bg-green-950/40 p-2 rounded border border-green-800/30 flex items-center gap-1.5">
              <span>✅</span>
              <span><strong>Desfecho Previsto:</strong> Vitória dos empregados. Compensação sem desconto em contracheque.</span>
            </div>
          </div>
        </div>
      </article>

      <!-- CARD 3: CONTINGENTE MÍNIMO -->
      <article class="matrix-card p-5 sm:p-6" data-category="greve">
        <!-- Card Header -->
        <div class="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-[#21262d]">
          <div class="flex items-center gap-2.5">
            <span class="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-sm">
              🛡️
            </span>
            <div>
              <h4 class="text-base font-bold text-white">3. Contingente Mínimo de Atendimento em Agências</h4>
              <p class="text-xs text-[#8b949e]">Pedido de 80% do efetivo pela Caixa vs. Fixação em 60% por Godinho</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="badge badge-purple text-xs">Liminar Já Concedida</span>
          </div>
        </div>

        <!-- 3 Columns Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 pt-4">
          <!-- Col 1: O Precedente no TST -->
          <div class="bg-[#121824] border border-[#21262d] rounded-xl p-4 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">🏛️ O Precedente no TST</span>
              <span class="badge badge-blue text-[10px]">RO 1001254-87.2015</span>
            </div>
            <div class="text-xs font-semibold text-white">Rel. Min. Mauricio Godinho Delgado • SDC</div>
            <p class="text-xs text-[#8b949e] leading-relaxed">
              O TST fixou que bancos prestam serviços de utilidade pública, mas <strong>não são serviços 100% inadiáveis</strong> (art. 10 da Lei 7.783/89). Exigir mais de 70% ou 80% equivale a cassar o direito constitucional de greve por via judicial oblíqua.
            </p>
            <div class="text-[11px] text-blue-300 font-mono bg-blue-950/40 p-2 rounded border border-blue-800/30">
              Tese: "O contingenciamento deve ser estritamente proporcional às necessidades inadiáveis sociais."
            </div>
          </div>

          <!-- Col 2: O Embate no ACT 2026 -->
          <div class="bg-[#121824] border border-[#21262d] rounded-xl p-4 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">⚔️ A Disputa no ACT 2026</span>
              <span class="badge badge-amber text-[10px]">Medida Cautelar</span>
            </div>
            <div class="text-xs font-semibold text-white">Caixa Econômica vs. Comando Bancário</div>
            <div class="text-xs space-y-2 text-[#8b949e]">
              <div>
                <strong class="text-gray-300">Posição da Caixa:</strong> Exigência de 80% do efetivo trabalhando para manter FGTS, PIS, Bolsa Família e pagamentos judiciais.
              </div>
              <div>
                <strong class="text-gray-300">Posição dos Sindicatos:</strong> Oferta de 30% de atendimento, alegando que os canais digitais absorvem as demandas.
              </div>
            </div>
          </div>

          <!-- Col 3: O Veredito Preditivo IA -->
          <div class="bg-gradient-to-b from-[#19152b] to-[#121824] border border-purple-500/30 rounded-xl p-4 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-purple-300 uppercase tracking-wider">🎯 Veredito da Sentença (IA)</span>
              <span class="text-xs font-bold text-green-400 font-mono">95% de Certeza</span>
            </div>

            <!-- Probability Bar -->
            <div class="w-full bg-[#21262d] rounded-full h-2 overflow-hidden">
              <div class="bg-green-500 h-2 rounded-full" style="width: 95%"></div>
            </div>

            <p class="text-xs text-purple-200/90 leading-relaxed">
              <strong>Tendência de Godinho:</strong> A liminar proferida em 24/09 <strong>já estabeleceu os 60%</strong> e será integralmente mantida pelo colegiado da SDC, assegurando que 40% do efetivo continue resguardado na greve legal.
            </p>
            <div class="text-[11px] text-green-400 bg-green-950/40 p-2 rounded border border-green-800/30 flex items-center gap-1.5">
              <span>✅</span>
              <span><strong>Desfecho Previsto:</strong> Manutenção definitiva dos 60% por unidade bancária.</span>
            </div>
          </div>
        </div>
      </article>

      <!-- CARD 4: REAJUSTE SALARIAL E PLR -->
      <article class="matrix-card p-5 sm:p-6" data-category="salario">
        <!-- Card Header -->
        <div class="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-[#21262d]">
          <div class="flex items-center gap-2.5">
            <span class="w-8 h-8 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 flex items-center justify-center font-bold text-sm">
              💰
            </span>
            <div>
              <h4 class="text-base font-bold text-white">4. Reajuste Salarial & Teto de PLR Social</h4>
              <p class="text-xs text-[#8b949e]">Reposição pelo INPC vs Aumento Real e diretrizes da SEST/DEST</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="badge badge-blue text-xs">Cláusula Econômica</span>
          </div>
        </div>

        <!-- 3 Columns Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 pt-4">
          <!-- Col 1: O Precedente no TST -->
          <div class="bg-[#121824] border border-[#21262d] rounded-xl p-4 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">🏛️ O Precedente no TST</span>
              <span class="badge badge-blue text-[10px]">RO 240-29.2016</span>
            </div>
            <div class="text-xs font-semibold text-white">Relª. Minª. Cristina Peduzzi • SDC</div>
            <p class="text-xs text-[#8b949e] leading-relaxed">
              O TST consolidou que em sede de sentença normativa de estatais <strong>não há concessão de ganho real de salários</strong> sem anuência do Ministério do Planejamento/SEST. A concessão jurisdicional é estritamente vinculada a 100% da variação do INPC (Precedente Normativo nº 37).
            </p>
            <div class="text-[11px] text-blue-300 font-mono bg-blue-950/40 p-2 rounded border border-blue-800/30">
              Tese: "É vedado ao poder normativo da Justiça do Trabalho conceder reajustes reais não pactuados."
            </div>
          </div>

          <!-- Col 2: O Embate no ACT 2026 -->
          <div class="bg-[#121824] border border-[#21262d] rounded-xl p-4 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">⚔️ A Disputa no ACT 2026</span>
              <span class="badge badge-amber text-[10px]">Tabela Salarial</span>
            </div>
            <div class="text-xs font-semibold text-white">Caixa Econômica vs. Sindicatos</div>
            <div class="text-xs space-y-2 text-[#8b949e]">
              <div>
                <strong class="text-gray-300">Posição da Caixa:</strong> Reajuste restrito ao índice inflacionário pactuado pela FENABAN, sem gatilho real, e trava na PLR Social.
              </div>
              <div>
                <strong class="text-gray-300">Posição dos Sindicatos:</strong> Reivindicação de INPC + 2,5% de aumento real, além de distribuição linear de 4% do lucro líquido na PLR Social.
              </div>
            </div>
          </div>

          <!-- Col 3: O Veredito Preditivo IA -->
          <div class="bg-gradient-to-b from-[#19152b] to-[#121824] border border-purple-500/30 rounded-xl p-4 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-purple-300 uppercase tracking-wider">🎯 Veredito da Sentença (IA)</span>
              <span class="text-xs font-bold text-purple-400 font-mono">90% de Chance</span>
            </div>

            <!-- Probability Bar -->
            <div class="w-full bg-[#21262d] rounded-full h-2 overflow-hidden">
              <div class="bg-purple-500 h-2 rounded-full" style="width: 90%"></div>
            </div>

            <p class="text-xs text-purple-200/90 leading-relaxed">
              <strong>Tendência da SDC:</strong> O tribunal <strong>deferirá exatamente 100% do INPC</strong> sobre salários e tíquetes alimentação/refeição. O pleito de ganho real será indeferido pela jurisprudência vinculante da SDC.
            </p>
            <div class="text-[11px] text-green-400 bg-green-950/40 p-2 rounded border border-green-800/30 flex items-center gap-1.5">
              <span>✅</span>
              <span><strong>Desfecho Previsto:</strong> Reposição de 100% da inflação; ganho real apenas em acordo de mesa.</span>
            </div>
          </div>
        </div>
      </article>

      <!-- CARD 5: ULTRATIVIDADE E RISCO DE CADUCIDADE -->
      <article class="matrix-card p-5 sm:p-6" data-category="ultratividade">
        <!-- Card Header -->
        <div class="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-[#21262d]">
          <div class="flex items-center gap-2.5">
            <span class="w-8 h-8 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center font-bold text-sm">
              ⚖️
            </span>
            <div>
              <h4 class="text-base font-bold text-white">5. Ultratividade do ACT & Prorrogação de Direitos</h4>
              <p class="text-xs text-[#8b949e]">Fim da ultratividade automática pelo STF e a tutela cautelar concedida</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="badge badge-purple text-xs">ADPF 323 / STF</span>
          </div>
        </div>

        <!-- 3 Columns Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 pt-4">
          <!-- Col 1: O Precedente no TST -->
          <div class="bg-[#121824] border border-[#21262d] rounded-xl p-4 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">🏛️ O Precedente no STF/TST</span>
              <span class="badge badge-blue text-[10px]">ADPF 323 & Tema 1046</span>
            </div>
            <div class="text-xs font-semibold text-white">STF • Efeito Vinculante Nacional</div>
            <p class="text-xs text-[#8b949e] leading-relaxed">
              O STF julgou inconstitucional a Súmula 277 do TST, determinando que <strong>cláusulas convencionais não se incorporam ao contrato</strong> de trabalho após a data-base. Se o acordo expira sem renovação, há risco de corte de benefícios voluntários caso não haja tutela judicial expressa.
            </p>
            <div class="text-[11px] text-blue-300 font-mono bg-blue-950/40 p-2 rounded border border-blue-800/30">
              Tese: "Cláusulas normativas têm eficácia restrita ao seu prazo de vigência, vedada ultratividade legal."
            </div>
          </div>

          <!-- Col 2: O Embate no ACT 2026 -->
          <div class="bg-[#121824] border border-[#21262d] rounded-xl p-4 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">⚔️ A Disputa no ACT 2026</span>
              <span class="badge badge-amber text-[10px]">Vácuo Normativo</span>
            </div>
            <div class="text-xs font-semibold text-white">Caixa Econômica vs. Sindicatos</div>
            <div class="text-xs space-y-2 text-[#8b949e]">
              <div>
                <strong class="text-gray-300">A Cautelar da Caixa:</strong> Para evitar o vácuo e manter estabilidade operacional, a própria Caixa pediu judicialmente a extensão provisória de benefícios até o julgamento.
              </div>
              <div>
                <strong class="text-gray-300">Efeito Prático:</strong> Todos os direitos (auxílio alimentação, jornada, gratificações) seguem garantidos durante o dissídio coletivo.
              </div>
            </div>
          </div>

          <!-- Col 3: O Veredito Preditivo IA -->
          <div class="bg-gradient-to-b from-[#19152b] to-[#121824] border border-purple-500/30 rounded-xl p-4 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-purple-300 uppercase tracking-wider">🎯 Veredito da Sentença (IA)</span>
              <span class="text-xs font-bold text-green-400 font-mono">90% de Certeza</span>
            </div>

            <!-- Probability Bar -->
            <div class="w-full bg-[#21262d] rounded-full h-2 overflow-hidden">
              <div class="bg-green-500 h-2 rounded-full" style="width: 90%"></div>
            </div>

            <p class="text-xs text-purple-200/90 leading-relaxed">
              <strong>Tendência de Godinho:</strong> Min. Godinho <strong>prorrogou a vigência das cláusulas vigentes</strong> na liminar. Essa blindagem será mantida até a data de publicação do acórdão definitivo, pacificando as relações no banco.
            </p>
            <div class="text-[11px] text-green-400 bg-green-950/40 p-2 rounded border border-green-800/30 flex items-center gap-1.5">
              <span>✅</span>
              <span><strong>Desfecho Previsto:</strong> Manutenção integral da vigência das cláusulas até a sentença.</span>
            </div>
          </div>
        </div>
      </article>

    </div>

    <!-- BALANCE OF OUTCOMES / PLACAR ANTECIPADO -->
    <section class="glass-card p-6 border-purple-500/30 space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <span>⚖️ O Equilíbrio da Sentença Final: Quem Leva o Quê no TST</span>
          </h3>
          <p class="text-xs text-[#8b949e]">Síntese estratégica do veredito previsto pela jurimetria e pelo modelo DeepSeek R1.</p>
        </div>
        <span class="badge badge-purple text-xs">Previsão Jurimétrica</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
        <!-- Vitórias Prováveis da Caixa -->
        <div class="bg-[#121824] border border-blue-500/30 rounded-xl p-4 space-y-3">
          <div class="flex items-center gap-2 text-blue-400 font-bold text-sm">
            <span>🏛️</span>
            <span>Ganhos Esperados pela Caixa Econômica</span>
          </div>
          <ul class="text-xs space-y-2 text-[#8b949e]">
            <li class="flex items-start gap-2">
              <span class="text-blue-400 font-bold">•</span>
              <span><strong>Teto no Saúde Caixa:</strong> O TST não concederá o retorno ao modelo 70/30 ilimitado sem teto de gastos.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-blue-400 font-bold">•</span>
              <span><strong>Teto Inflacionário:</strong> A SDC indeferirá aumento real acima da inflação oficial (100% INPC).</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-blue-400 font-bold">•</span>
              <span><strong>Contingente em 60%:</strong> Atendimento nas agências permanece garantido para serviços sociais essenciais.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-blue-400 font-bold">•</span>
              <span><strong>Limites da SEST:</strong> A SDC não criará novas fórmulas de PLR além das aprovadas pelos órgãos federais.</span>
            </li>
          </ul>
        </div>

        <!-- Vitórias Prováveis dos Sindicatos e Empregados -->
        <div class="bg-[#121824] border border-green-500/30 rounded-xl p-4 space-y-3">
          <div class="flex items-center gap-2 text-green-400 font-bold text-sm">
            <span>✊</span>
            <span>Ganhos Esperados pelos Sindicatos & Empregados</span>
          </div>
          <ul class="text-xs space-y-2 text-[#8b949e]">
            <li class="flex items-start gap-2">
              <span class="text-green-400 font-bold">•</span>
              <span><strong>Compensação dos 15 Dias de Greve:</strong> Afastamento do corte de ponto punitivo pretendido pelo banco.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-green-400 font-bold">•</span>
              <span><strong>Rejeição do Contingente de 80%:</strong> O banco não conseguiu forçar retorno de 80% do quadro funcional.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-green-400 font-bold">•</span>
              <span><strong>Prorrogação de Todos os Benefícios:</strong> Manutenção da ultratividade judicial de auxílios e direitos.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-green-400 font-bold">•</span>
              <span><strong>Reposição Integral do INPC:</strong> Blindagem do poder de compra dos salários contra perdas inflacionárias.</span>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- EXPLORE MORE MODULES BANNER -->
    <section class="bg-gradient-to-r from-blue-900/20 via-purple-900/20 to-blue-900/20 border border-blue-500/30 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-5">
      <div class="space-y-1.5 text-center md:text-left">
        <h4 class="text-base font-bold text-white">Quer pesquisar os acórdãos na íntegra ou ver outras estatais?</h4>
        <p class="text-xs text-[#8b949e]">Explore a base de dados com 51 decisões catalogadas da Caixa ou o ranking com 48 empresas públicas brasileiras no TST.</p>
      </div>
      <div class="flex flex-wrap items-center justify-center gap-3">
        <a href="decisoes_caixa.html" class="bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs px-4 py-2.5 rounded-xl shadow-lg shadow-blue-600/30 transition-all flex items-center gap-2">
          <span>📚 Explorar 51 Acórdãos da Caixa</span>
          <span>→</span>
        </a>
        <a href="dashboard_geral_estatais.html" class="bg-[#161b22] hover:bg-[#21262d] text-gray-200 border border-[#30363d] font-semibold text-xs px-4 py-2.5 rounded-xl transition-all">
          <span>🏢 Painel 48 Estatais</span>
        </a>
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="border-t border-[#21262d] bg-[#090d13] py-6 px-4 text-center text-xs text-[#6e7681]">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
      <div>
        <strong>Radar Dissídio Coletivo Caixa (2026–2028)</strong> • Dados extraídos da Seção de Dissídios Coletivos (SDC / TST)
      </div>
      <div class="flex items-center gap-4">
        <a href="decisoes_caixa.html" class="hover:text-blue-400">Jurisprudência</a>
        <a href="decisoes_caixa.html#previsao-ia" class="hover:text-purple-400">Previsão DeepSeek</a>
        <a href="index_tabs_backup.html" class="hover:text-gray-400">Modo Detalhado</a>
      </div>
    </div>
  </footer>

  <!-- Filter Script -->
  <script>
    function filterCards(category, btnElement) {
      // Toggle button active state
      document.querySelectorAll('.pill-filter').forEach(btn => btn.classList.remove('active'));
      btnElement.classList.add('active');

      const cards = document.querySelectorAll('#matrix-container .matrix-card');
      cards.forEach(card => {
        const cardCat = card.getAttribute('data-category');
        if (category === 'all' || cardCat === category) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    }
  </script>

</body>
</html>
"""

def main():
    print(f"Escrevendo novo index.html em: {OUTPUT_PATH}")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print("Sucesso! Novo index.html gerado com base na Alternativa 1.")

if __name__ == "__main__":
    main()
