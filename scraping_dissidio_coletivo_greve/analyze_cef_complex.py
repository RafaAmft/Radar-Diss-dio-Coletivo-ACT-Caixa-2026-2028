import json
import re
from collections import Counter, defaultdict
from bs4 import BeautifulSoup

def clean_html(text):
    if not text:
        return ""
    if "<" in text and ">" in text:
        return BeautifulSoup(text, 'html.parser').get_text(separator=' ')
    return text

# Load all CEF SDC decisions
with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
cef_procs = data.get('Caixa Econômica Federal (CEF)', [])

# Load CEF Turmas
with open('scraping_dissidio_coletivo_greve/turmas_records_cache.json', 'r', encoding='utf-8') as f:
    turmas = json.load(f)
cef_turmas = []
for num, rec in turmas.items():
    txt = ((rec.get('ementa') or '') + ' ' + (rec.get('inteiroTeorHtml') or '')).lower()
    if 'caixa' in txt or 'cef' in txt:
        cef_turmas.append(rec)

# ============================================================
# DEEP THEMATIC ANALYSIS - SDC
# ============================================================
print("=" * 80)
print("ANÁLISE TEMÁTICA PROFUNDA — CEF NA SDC DO TST")
print("=" * 80)

COMPLEX_THEMES = {
    # Dimensão 1: Natureza e Legitimidade da Greve
    'aviso_previo_72h': [r'aviso\s+prévio', r'72\s*h', r'notificação\s+(prévia|de\s+72)', r'lei\s+7\.?783'],
    'assembleia_previa': [r'assembl[eé]ia\s+(prévia|geral)', r'deliberação\s+assemblear', r'quórum'],
    'contingente_minimo': [r'contingente\s+mínimo', r'funcionamento\s+mínimo', r'efetivo\s+mínimo', r'serviço\s+essencial', r'atividade\s+essencial'],
    'servico_essencial': [r'serviço\s+essencial', r'art\.?\s*10.*lei\s+7\.?783', r'necessidades\s+inadiáveis', r'atividade\s+bancária.*essencial'],

    # Dimensão 2: Requisito Constitucional
    'comum_acordo': [r'comum\s+acordo', r'art\.?\s*114.*§\s*2', r'mútuo\s+consenso', r'pressuposto\s+processual'],
    'legitimidade': [r'legitimidade\s+(ad\s+causam|ativa|passiva)', r'representatividade\s+sindical', r'categoria\s+profissional'],

    # Dimensão 3: Cláusulas Econômicas do ACT
    'reajuste_salarial': [r'reajuste\s+salarial', r'reposição\s+salarial', r'inpc', r'ipca', r'índice\s+de\s+reajuste', r'perda\s+inflacionária'],
    'plr_participacao': [r'plr', r'participação\s+nos\s+(lucros|resultados)', r'ppr'],
    'plano_saude': [r'plano\s+de\s+sa[uú]de', r'assistência\s+médica', r'saúde\s+caixa', r'coparticipação', r'plano\s+de\s+assistência'],
    'vale_alimentacao': [r'vale[\s-]?alimenta', r'auxílio[\s-]?alimenta', r'tíquete', r'cesta\s+aliment', r'vale[\s-]?refei'],
    'vale_transporte': [r'vale[\s-]?transporte', r'auxílio[\s-]?transporte'],
    'auxilio_creche': [r'auxílio[\s-]?creche', r'auxílio[\s-]?babá', r'berçário'],
    'funcef_previdencia': [r'funcef', r'previdência\s+complementar', r'fundo\s+de\s+pensão', r'aposentadoria\s+complementar'],
    'jornada_6h': [r'jornada\s+de\s+6', r'jornada\s+bancária', r'seis\s+horas', r'art\.?\s*224\s+clt'],
    'horas_extras': [r'horas?\s+extra', r'7[aª]\s+e\s+8[aª]\s+hora', r'sobrejornada'],
    'adicional_cargo': [r'adicional\s+(de\s+)?função', r'comissão\s+de\s+cargo', r'cargo\s+comissionado', r'gratificação'],
    'teletrabalho': [r'teletrabalho', r'trabalho\s+remoto', r'home\s*office', r'trabalho\s+híbrido'],

    # Dimensão 4: Cláusulas Sociais e Proteção
    'estabilidade_pre_aposentadoria': [r'estabilidade\s+pré[\s-]?aposentadoria', r'pré[\s-]?aposentad'],
    'estabilidade_gestante': [r'gestante', r'estabilidade.*grávida', r'licença[\s-]?maternidade'],
    'estabilidade_acidentado': [r'acidente\s+de\s+trabalho', r'estabilidade\s+acidentári', r'doença\s+ocupacional'],
    'assedio_moral': [r'assédio\s+moral', r'conduta\s+antissindical', r'perseguição', r'discriminaç'],
    'terceirizacao': [r'terceiriz', r'empregado\s+terceirizado', r'quarteirização'],

    # Dimensão 5: Diretrizes Governamentais para Estatais
    'sest_dest_limites': [r'sest', r'dest', r'limite\s+orçamentário', r'lei\s+de\s+responsabilidade', r'empresa\s+dependente', r'teto\s+remuneratório'],
    'autonomia_negocial': [r'autonomia\s+negocial', r'autonomia\s+coletiva', r'prevalência\s+do\s+negociado', r'tema\s+1046', r'reforma\s+trabalhista'],

    # Dimensão 6: Multas e Enforcement
    'multa_astreintes': [r'multa\s+diária', r'astreintes', r'obrigação\s+de\s+fazer', r'descumprimento\s+de\s+liminar'],
    'interdito_proibitorio': [r'interdito\s+proibitório', r'piquete', r'bloqueio\s+de\s+acesso', r'impedir\s+o\s+acesso'],

    # Dimensão 7: Precedentes do STF
    'tema_435_stf': [r'tema\s+435', r're\s+693\.?456', r'suspensão\s+do\s+contrato.*greve'],
    'tema_1046_stf': [r'tema\s+1046', r'are\s+1\.?121\.?633', r'negociado\s+sobre\s+legislado'],
}

theme_counts = Counter()
theme_processes = defaultdict(list)
theme_snippets = defaultdict(list)

for p in cef_procs:
    txt_raw = p.get('txtConteudoDecisao', '') or ''
    txt = clean_html(txt_raw).lower()
    if len(txt) < 100:
        continue
    num = p.get('numFormatado', 'N/A')
    relator = p.get('nomRelator', 'N/A')

    for theme, patterns in COMPLEX_THEMES.items():
        for pat in patterns:
            m = re.search(pat, txt, re.IGNORECASE)
            if m:
                theme_counts[theme] += 1
                theme_processes[theme].append(f"{num} ({relator})")
                # Extract snippet around match
                start = max(0, m.start() - 80)
                end = min(len(txt), m.end() + 120)
                snippet = txt[start:end].strip()
                if len(theme_snippets[theme]) < 2:
                    theme_snippets[theme].append(snippet)
                break

total_with_text = len([p for p in cef_procs if len(clean_html(p.get('txtConteudoDecisao', '') or '')) > 100])
print(f"\nTotal CEF SDC com texto analisável: {total_with_text}")
print(f"\n{'TEMA':<40} {'OCORRÊNCIAS':>12} {'%':>8}")
print("-" * 62)
for theme, count in sorted(theme_counts.items(), key=lambda x: -x[1]):
    pct = round(count / max(total_with_text, 1) * 100, 1)
    print(f"  {theme:<38} {count:>10} {pct:>7}%")

# ============================================================
# TURMAS - DEEPER ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("ANÁLISE TEMÁTICA PROFUNDA — CEF NAS TURMAS DO TST")
print("=" * 80)

turma_themes = Counter()
turma_total = 0
for rec in cef_turmas:
    txt = clean_html(
        (rec.get('inteiroTeorHtml') or '') + ' ' +
        (rec.get('ementa') or '') + ' ' +
        (rec.get('dispositivo') or '')
    ).lower()
    if len(txt) < 100:
        continue
    turma_total += 1

    for theme, patterns in COMPLEX_THEMES.items():
        for pat in patterns:
            if re.search(pat, txt, re.IGNORECASE):
                turma_themes[theme] += 1
                break

print(f"\nTotal CEF Turmas com texto analisável: {turma_total}")
print(f"\n{'TEMA':<40} {'OCORRÊNCIAS':>12} {'%':>8}")
print("-" * 62)
for theme, count in sorted(turma_themes.items(), key=lambda x: -x[1]):
    pct = round(count / max(turma_total, 1) * 100, 1)
    print(f"  {theme:<38} {count:>10} {pct:>7}%")

# ============================================================
# SNIPPETS OF COMPLEX THEMES
# ============================================================
print("\n" + "=" * 80)
print("TRECHOS ILUSTRATIVOS DOS TEMAS COMPLEXOS (SDC)")
print("=" * 80)
for theme in ['comum_acordo', 'contingente_minimo', 'reajuste_salarial', 'plr_participacao',
              'funcef_previdencia', 'tema_435_stf', 'autonomia_negocial', 'sest_dest_limites',
              'plano_saude', 'estabilidade_pre_aposentadoria']:
    if theme_snippets.get(theme):
        print(f"\n--- {theme.upper()} ---")
        for s in theme_snippets[theme]:
            print(f"  ...{s}...")
