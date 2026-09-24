import json
import re
from collections import Counter
from bs4 import BeautifulSoup

def clean_html(text):
    if not text:
        return ""
    if "<" in text and ">" in text:
        return BeautifulSoup(text, 'html.parser').get_text(separator=' ')
    return text

# CEF entity records
with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cef_procs = data.get('Caixa Econômica Federal (CEF)', [])
print(f"Total CEF SDC: {len(cef_procs)}")

# Deep content analysis of ALL CEF SDC records
TOPICS = {
    'greve': ['greve', 'paralisação', 'movimento paredista'],
    'abusividade': ['abusiv', 'não abusiva', 'legalidade da greve'],
    'dias_parados': ['dias parados', 'desconto salarial', 'oj 10', 'oj nº 10', 'suspensão do contrato'],
    'reajuste': ['reajuste salarial', 'reajuste', 'inpc', 'ipca', 'reposição salarial'],
    'plano_saude': ['plano de saúde', 'plano de assistência', 'assistência médica', 'coparticipação'],
    'vale_alimentacao': ['vale alimentação', 'vale-alimentação', 'tíquete', 'cesta alimentação', 'auxílio alimentação', 'auxílio-alimentação'],
    'plr': ['plr', 'participação nos lucros', 'participação nos resultados'],
    'jornada': ['jornada', 'horas extras', 'compensação de jornada', 'banco de horas'],
    'estabilidade': ['estabilidade', 'reintegração', 'dispensa', 'demissão'],
    'contingente': ['contingente mínimo', 'funcionamento mínimo', 'serviço essencial'],
    'comum_acordo': ['comum acordo', '114, § 2', 'art. 114'],
    'act_cct': ['acordo coletivo', 'convenção coletiva', 'act', 'cct', 'norma coletiva'],
    'multa': ['multa', 'astreintes', 'multa diária'],
    'honorarios': ['honorários', 'custas'],
    'adicional': ['adicional', 'periculosidade', 'insalubridade'],
    'auxilio_creche': ['auxílio-creche', 'auxílio creche', 'berçário'],
    'funcef': ['funcef', 'previdência complementar', 'fundo de pensão'],
    'teletrabalho': ['teletrabalho', 'trabalho remoto', 'home office'],
}

topic_counts = Counter()
process_topics = {}

for p in cef_procs:
    txt = clean_html(p.get('txtConteudoDecisao', '') or '').lower()
    if len(txt) < 50:
        continue
    num = p.get('numFormatado', 'N/A')
    found = []
    for topic, terms in TOPICS.items():
        for t in terms:
            if t.lower() in txt:
                found.append(topic)
                topic_counts[topic] += 1
                break
    process_topics[num] = list(set(found))

print("\n=== TEMAS JURIDICOS NOS JULGAMENTOS CEF ===")
for topic, count in topic_counts.most_common():
    pct = round(count / max(len([p for p in cef_procs if len(clean_html(p.get('txtConteudoDecisao', '') or '')) > 50]), 1) * 100, 1)
    print(f"  {topic}: {count} ocorrências ({pct}%)")

# Turmas CEF deep analysis
with open('scraping_dissidio_coletivo_greve/turmas_records_cache.json', 'r', encoding='utf-8') as f:
    turmas = json.load(f)

cef_turmas = []
for num, rec in turmas.items():
    txt = ((rec.get('ementa') or '') + ' ' + (rec.get('inteiroTeorHtml') or '')).lower()
    if 'caixa' in txt or 'cef' in txt:
        cef_turmas.append(rec)

print(f"\n=== CEF nas Turmas: {len(cef_turmas)} acórdãos ===")

# CEF Turmas by Turma
turma_dist = Counter()
turma_relator = Counter()
turma_desfecho = Counter()
turma_tema = Counter()

for rec in cef_turmas:
    org = rec.get('orgaoJudicante', {}).get('descricao', 'N/A')
    turma_dist[org] += 1
    turma_relator[rec.get('nomRelator', 'N/A')] += 1
    
    txt = clean_html((rec.get('inteiroTeorHtml') or '') + ' ' + (rec.get('ementa') or '') + ' ' + (rec.get('dispositivo') or '')).lower()
    
    if any(k in txt for k in ['dias parados', 'desconto', 'oj 10', 'suspensão do contrato']):
        turma_tema['Desconto de Dias Parados'] += 1
    elif any(k in txt for k in ['reintegração', 'estabilidade', 'nulidade da dispensa']):
        turma_tema['Estabilidade / Reintegração'] += 1
    elif any(k in txt for k in ['ação de cumprimento', 'sentença normativa']):
        turma_tema['Cumprimento Sentença Normativa'] += 1
    else:
        turma_tema['Outros'] += 1
    
    disp = (rec.get('dispositivo') or '').lower()
    if 'negar provimento' in disp or 'não conhecer' in disp or 'desprovido' in disp:
        turma_desfecho['Recurso Não Provido / Mantido'] += 1
    elif 'dar provimento' in disp or 'provido' in disp:
        turma_desfecho['Recurso Provido'] += 1
    else:
        turma_desfecho['Outro / Parcial'] += 1

print("\nTurmas com mais casos CEF:")
for t, c in turma_dist.most_common():
    print(f"  {t}: {c}")

print("\nTop relatores CEF nas Turmas:")
for r, c in turma_relator.most_common(10):
    print(f"  {r}: {c}")

print("\nTemas CEF nas Turmas:")
for t, c in turma_tema.most_common():
    print(f"  {t}: {c}")

print("\nDesfechos CEF nas Turmas:")
for d, c in turma_desfecho.most_common():
    print(f"  {d}: {c}")
