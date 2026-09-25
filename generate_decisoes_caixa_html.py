import json

with open('dados_decisoes_caixa.json', 'r', encoding='utf-8') as f:
    decisions = json.load(f)

json_str = json.dumps(decisions, ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jurimetria Caixa no TST — 57 Decisões Coletivas Mapeadas</title>
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
                57 Decisões Coletivas Mapeadas (2016–2026)
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

      <!-- Métricas da Decisão de Ontem -->
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

    <!-- CARDS DE ESTATÍSTICAS JURIMÉTRICAS GERAIS DA CAIXA -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
      <div class="card p-4">
        <div class="text-[11px] text-[var(--muted-foreground)] font-semibold uppercase">Total de Processos Mapeados</div>
        <div class="text-2xl sm:text-3xl font-bold mt-1 text-white">57</div>
        <p class="text-[11px] text-blue-400 mt-1">Dissídios Coletivos e Recursos na SDC</p>
      </div>

      <div class="card p-4">
        <div class="text-[11px] text-[var(--muted-foreground)] font-semibold uppercase">Taxa de Acordo Homologado</div>
        <div class="text-2xl sm:text-3xl font-bold mt-1 text-green-400">52,6%</div>
        <p class="text-[11px] text-[var(--muted-foreground)] mt-1">30 processos resolvidos por autocomposição</p>
      </div>

      <div class="card p-4">
        <div class="text-[11px] text-[var(--muted-foreground)] font-semibold uppercase">Maior Relator Histórico</div>
        <div class="text-2xl sm:text-3xl font-bold mt-1 text-purple-400">Godinho (16)</div>
        <p class="text-[11px] text-[var(--muted-foreground)] mt-1">28% de todas as decisões da Caixa na SDC</p>
      </div>

      <div class="card p-4">
        <div class="text-[11px] text-[var(--muted-foreground)] font-semibold uppercase">Sentença Normativa Pura</div>
        <div class="text-2xl sm:text-3xl font-bold mt-1 text-amber-400">7,0%</div>
        <p class="text-[11px] text-[var(--muted-foreground)] mt-1">Apenas 4 casos foram a julgamento litigioso</p>
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
            <option value="Mauricio Godinho Delgado">Min. Mauricio Godinho Delgado (16)</option>
            <option value="Katia Magalhaes Arruda">Min. Kátia Arruda (12)</option>
            <option value="Ives Gandra">Min. Ives Gandra (9)</option>
            <option value="Maria Cristina Irigoyen Peduzzi">Min. Cristina Peduzzi (5)</option>
            <option value="Dora Maria Da Costa">Min. Dora Maria da Costa (4)</option>
          </select>

          <select 
            id="desfechoFilter" 
            class="bg-[var(--content)] border border-[var(--border)] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500"
            onchange="renderDecisions()"
          >
            <option value="todos">Todos os Desfechos</option>
            <option value="Acordo Homologado">Acordo Homologado (30)</option>
            <option value="Liminar">Decisão Liminar (2)</option>
            <option value="Sentença Normativa">Sentença Normativa (4)</option>
            <option value="Recurso">Recursos Providos/Desprovidos (12)</option>
            <option value="Extinto">Extinto sem Resolução (6)</option>
          </select>
        </div>
      </div>

      <!-- Filtros Rápidos por Tema (Pills) -->
      <div class="flex flex-wrap items-center gap-1.5 pt-2 border-t border-[var(--border)]">
        <span class="text-[11px] text-[var(--muted-foreground)] font-semibold mr-1">Filtrar Tema:</span>
        <button class="filter-btn active text-xs px-2.5 py-1 rounded-lg border border-transparent" onclick="setTemaFilter('todos')" id="tema-todos">
          Todos (57)
        </button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-transparent text-[var(--muted-foreground)]" onclick="setTemaFilter('Saúde Caixa')" id="tema-saude">
          🏥 Saúde Caixa (12)
        </button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-transparent text-[var(--muted-foreground)]" onclick="setTemaFilter('Dias Parados & Greve')" id="tema-greve">
          ✊ Dias Parados & Greve (49)
        </button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-transparent text-[var(--muted-foreground)]" onclick="setTemaFilter('Jornada & 7ª/8ª Hora')" id="tema-jornada">
          ⏰ Jornada & 7ª/8ª Hora (24)
        </button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-transparent text-[var(--muted-foreground)]" onclick="setTemaFilter('Reajuste Salarial')" id="tema-reajuste">
          📈 Reajuste Salarial (18)
        </button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-transparent text-[var(--muted-foreground)]" onclick="setTemaFilter('Contingenciamento Mínimo')" id="tema-contingente">
          🛡️ Contingenciamento (13)
        </button>
        <button class="filter-btn text-xs px-2.5 py-1 rounded-lg border border-transparent text-[var(--muted-foreground)]" onclick="setTemaFilter('PLR & PLR Social')" id="tema-plr">
          💰 PLR Social (3)
        </button>
      </div>

      <div class="flex items-center justify-between text-xs text-[var(--muted-foreground)] pt-1">
        <span id="counterText">Carregando decisões...</span>
        <span class="text-[11px]">Dados obtidos via API Jurisprudência TST & PJe</span>
      </div>
    </div>

    <!-- LISTAGEM DE DECISÕES (RENDERIZADA VIA JAVASCRIPT) -->
    <div id="decisionsContainer" class="space-y-4">
      <!-- Inserido dinamicamente -->
    </div>

  </main>

  <!-- RODAPÉ -->
  <footer class="border-t border-[var(--border)] px-6 py-5 mt-12 bg-[#000000] text-xs text-[var(--muted-foreground)]">
    <div class="max-w-[1300px] mx-auto flex flex-col md:flex-row justify-between items-center gap-2">
      <span>Painel Jurimétrico Exclusivo da Caixa Econômica Federal no TST • Base: 57 Decisões Coletivas (2016–2026)</span>
      <span>Fonte: jurisprudencia-backend.tst.jus.br & PJe TST • Atualizado em 25/09/2026</span>
    </div>
  </footer>

  <!-- SCRIPT COM DADOS EMBUTIDOS E FILTRAGEM REATIVA -->
  <script>
    const DECISOES = {json_str};
    let activeTema = 'todos';

    function setTemaFilter(tema) {{
      activeTema = tema;
      document.querySelectorAll('.filter-btn').forEach(b => {{
        b.classList.remove('active');
        b.classList.add('text-[var(--muted-foreground)]');
      }});
      
      const idMap = {{
        'todos': 'tema-todos',
        'Saúde Caixa': 'tema-saude',
        'Dias Parados & Greve': 'tema-greve',
        'Jornada & 7ª/8ª Hora': 'tema-jornada',
        'Reajuste Salarial': 'tema-reajuste',
        'Contingenciamento Mínimo': 'tema-contingente',
        'PLR & PLR Social': 'tema-plr'
      }};
      const btn = document.getElementById(idMap[tema]);
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

with open('decisoes_caixa.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("decisoes_caixa.html re-gerado com sucesso com limpeza total de ementas e despachos!")
