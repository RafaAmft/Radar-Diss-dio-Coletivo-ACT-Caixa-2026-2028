"""
Script que injeta a seção e a aba de Previsão de IA (DeepSeek R1/V3) diretamente no index.html
e adiciona o anchor id="previsao-ia" em decisoes_caixa.html.
"""

from pathlib import Path

INDEX_PATH = Path("../index.html")
DECISOES_HTML_PATH = Path("../decisoes_caixa.html")
DECISOES_LOCAL_PATH = Path("decisoes_caixa.html")


def update_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Atualizar o link no cabeçalho
    old_link = '<span>57 Decisões Caixa</span>'
    new_link = '<span class="w-1.5 h-1.5 rounded-full bg-purple-400 animate-pulse"></span><span>🤖 Previsão IA & Decisões</span>'
    if old_link in content:
        content = content.replace(old_link, new_link)

    # 2. Adicionar o botão da aba no <nav>
    old_nav_marker = '<button class="tab-btn px-3.5 py-3 text-xs sm:text-sm whitespace-nowrap" onclick="showTab(\'sdc\')" id="tab-sdc">\n          🏛️ Se Fracassar (SDC)\n        </button>'
    new_tab_btn = (
        '<button class="tab-btn px-3.5 py-3 text-xs sm:text-sm whitespace-nowrap" onclick="showTab(\'sdc\')" id="tab-sdc">\n'
        '          🏛️ Se Fracassar (SDC)\n'
        '        </button>\n'
        '        <button class="tab-btn px-3.5 py-3 text-xs sm:text-sm whitespace-nowrap text-purple-300 font-bold flex items-center gap-1.5 border-b-2 border-purple-500/0 hover:border-purple-400" onclick="showTab(\'previsao-ia\')" id="tab-previsao-ia">\n'
        '          <span>🧠</span>\n'
        '          <span>Previsão IA (DeepSeek)</span>\n'
        '          <span class="badge bg-purple-500/20 text-purple-300 text-[10px] ml-1">SDC 29/09</span>\n'
        '        </button>'
    )

    if 'id="tab-previsao-ia"' not in content and old_nav_marker in content:
        content = content.replace(old_nav_marker, new_tab_btn)

    # 3. Adicionar o Banner de Destaque logo no início do <main>
    banner_html = """
    <!-- BANNER DE DESTAQUE: PREVISÃO DE IA (DEEPSEEK R1/V3) -->
    <div class="card glow-purple border-purple-500/40 bg-gradient-to-r from-purple-500/20 via-[#130d24] to-transparent p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
      <div class="flex items-center gap-3">
        <span class="text-2xl p-2 bg-purple-500/20 rounded-xl border border-purple-500/40">🧠</span>
        <div>
          <div class="flex flex-wrap items-center gap-2">
            <span class="badge bg-purple-500/30 text-purple-300 border border-purple-500/50 text-[10px] font-bold">DESTAQUE • PREVISÃO DE IA (DEEPSEEK R1/V3)</span>
            <span class="badge bg-green-500/20 text-green-400 border border-green-500/30 text-[10px]">Sessão da SDC: 29/09 às 14:30</span>
          </div>
          <h3 class="text-sm sm:text-base font-bold text-white mt-1">
            Prognóstico Antecipado da Sentença de Mérito do Min. Mauricio Godinho Delgado
          </h3>
          <p class="text-xs text-[var(--muted-foreground)] mt-0.5">
            Probabilidade de 85%+ de procedência parcial: 60% contingente, ACT provisório sem ultratividade, compensação de dias parados em 180d e teto de 6,5% do Saúde Caixa.
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2 flex-shrink-0">
        <button onclick="showTab('previsao-ia')" class="text-xs bg-purple-600 hover:bg-purple-500 text-white font-bold px-3.5 py-2 rounded-lg transition-colors flex items-center gap-1.5 shadow-lg shadow-purple-600/30">
          <span>Ver Prognóstico na Aba</span>
          <span>➔</span>
        </button>
        <a href="decisoes_caixa.html#previsao-ia" class="text-xs bg-[#161b22] hover:bg-[#30363d] border border-purple-500/40 text-purple-300 px-3 py-2 rounded-lg transition-colors flex items-center gap-1.5">
          <span>Abrir no Painel de Decisões</span>
          <span>➔</span>
        </a>
      </div>
    </div>
"""

    main_start = '<main class="max-w-[1300px] mx-auto px-4 sm:px-6 py-4 sm:py-6 relative z-10">'
    if 'DESTAQUE • PREVISÃO DE IA' not in content and main_start in content:
        content = content.replace(main_start, main_start + "\n" + banner_html)

    # 4. Adicionar o painel completo de Previsão de IA antes de </main>
    panel_previsao_html = """
    <!-- ==================== ABA 6: PREVISÃO DE IA (DEEPSEEK R1/V3) ==================== -->
    <div id="panel-previsao-ia" class="fade-in space-y-6 hidden">
      <div class="card glow-purple border-purple-500/40 bg-gradient-to-br from-[#130d24] via-[var(--card)] to-[var(--card)] space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-[var(--border)]">
          <div class="flex items-center gap-3">
            <span class="text-3xl p-2 bg-purple-500/20 rounded-xl border border-purple-500/30">🧠</span>
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <span class="badge bg-purple-500/20 text-purple-300 border border-purple-500/40 font-bold">PREVISÃO DE IA • SDC / TST</span>
                <span class="text-xs text-[var(--muted-foreground)]">Modelo: DeepSeek R1/V3 + Base TST (51 Decisões)</span>
                <span class="badge bg-green-500/20 text-green-400 border border-green-500/30">Sessão SDC: 29/09 às 14:30</span>
              </div>
              <h2 class="text-base sm:text-xl font-bold text-white mt-1">
                Prognóstico Preditivo da Sentença de Mérito: Min. Mauricio Godinho Delgado
              </h2>
            </div>
          </div>

          <div class="flex items-center gap-2">
            <a href="output/ai_dataset/analise_previsao_sentenca_godinho.md" target="_blank" class="text-xs bg-purple-600 hover:bg-purple-500 text-white font-semibold px-3 py-1.5 rounded-lg border border-purple-400/30 transition-colors flex items-center gap-1.5">
              <span>📄</span>
              <span>Baixar Relatório (.md)</span>
            </a>
          </div>
        </div>

        <!-- Veredito Antecipado -->
        <div class="p-4 bg-black/60 rounded-xl border border-purple-500/30">
          <div class="text-[10px] text-purple-400 font-bold uppercase tracking-wider mb-1 flex items-center gap-1.5">
            <span>⚡</span>
            <span>Veredito Antecipado da Inteligência Artificial (Probabilidade Estimada: 85%+)</span>
          </div>
          <p class="text-xs sm:text-sm text-white leading-relaxed">
            "A probabilidade de Godinho manter as balizas da liminar e proferir uma sentença desfavorável às reivindicações financeiras máximas dos sindicatos é <strong>alta (85%+)</strong>, adotando uma abordagem de ponderação constitucional: <strong>confirmar garantias básicas</strong>, <strong>restringir excessos sindicais</strong> e <strong>preservar a higidez econômico-atuarial da Caixa</strong> (contingente de 60%, manutenção do teto de 6,5% e compensação em 180 dias pela Cláusula 87)."
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
        <div class="p-3.5 bg-black/40 rounded-xl border border-[var(--border)]">
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
    </div>
"""

    if 'id="panel-previsao-ia"' not in content:
        content = content.replace("</main>", panel_previsao_html + "\n  </main>")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("index.html atualizado com a Previsão de IA (Banner + Aba + Painel)!")


def update_decisoes_html_anchors():
    for p in [DECISOES_HTML_PATH, DECISOES_LOCAL_PATH]:
        if p.is_file():
            with open(p, "r", encoding="utf-8") as f:
                c = f.read()
            # Assegura id="previsao-ia" no card de previsão
            c = c.replace(
                '<!-- SEÇÃO: PREVISÃO DE IA & JURIMETRIA PREDITIVA (DEEPSEEK R1/V3 + SDC/TST) -->\n    <div class="card glow-purple',
                '<!-- SEÇÃO: PREVISÃO DE IA & JURIMETRIA PREDITIVA (DEEPSEEK R1/V3 + SDC/TST) -->\n    <div id="previsao-ia" class="card glow-purple'
            )
            with open(p, "w", encoding="utf-8") as f:
                f.write(c)
            print(f"Anchor id='previsao-ia' adicionado em {p}")


if __name__ == "__main__":
    update_index()
    update_decisoes_html_anchors()
