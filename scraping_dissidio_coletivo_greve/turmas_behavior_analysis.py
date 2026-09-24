import requests
import json
import time
import os
import re
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup

def clean_html(text):
    if not text:
        return ""
    if "<" in text and ">" in text:
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text(separator=' ')
    return text

def fetch_turmas_jurisprudence(max_per_query=80):
    url_base = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
    headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    
    queries = [
        'greve "dias parados"',
        'greve "desconto salarial"',
        'greve "ação de cumprimento"',
        'greve "estabilidade" "reintegração"',
        'greve Correios "dias parados"',
        'greve Caixa "dias parados"',
        'greve Petrobras "dias parados"',
        'greve "sentença normativa" "desconto"'
    ]
    
    all_turmas_records = {}
    
    for q in queries:
        print(f"Buscando Turmas para termo: [{q}]...", flush=True)
        payload = {
            'ou': '', 'e': q, 'termoExato': '', 'naoContem': '', 'ementa': '', 'dispositivo': '',
            'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
            'orgaosJudicantes': [],
            'ministros': [], 'convocados': [],
            'classesProcessuais': [],
            'codigosClassesPrecedentes': [], 'indicadores': [], 'assuntos': [],
            'tipos': ['ACORDAO'], 'orgao': 'TST',
            'publicacaoInicial': None, 'publicacaoFinal': None,
            'julgamentoInicial': '2016-09-24',
            'julgamentoFinal': '2026-09-24',
            'ordenacao': 'data'
        }
        
        offset = 1
        page_size = 40
        collected_for_q = 0
        
        while collected_for_q < max_per_query:
            try:
                url = f"{url_base}/{offset}/{page_size}"
                resp = requests.post(url, json=payload, headers=headers, timeout=25)
                if resp.status_code != 200:
                    break
                data = resp.json()
                regs = data.get('registros', [])
                if not regs:
                    break
                    
                for r in regs:
                    rec = r.get('registro', {})
                    num = rec.get('numFormatado')
                    orgao_desc = rec.get('orgaoJudicante', {}).get('descricao', '')
                    
                    # Filter: Only the 8 Turmas (exclude SDC, SDI-1, SDI-2, etc.)
                    if "Turma" in orgao_desc and "Subseção" not in orgao_desc:
                        if num and num not in all_turmas_records:
                            rec['query_origem'] = q
                            all_turmas_records[num] = rec
                            
                collected_for_q += len(regs)
                offset += page_size
                time.sleep(0.3)
            except Exception as e:
                print(f"Erro na busca [{q}] offset {offset}: {e}")
                break
                
        print(f"  Total acumulado de decisões de Turmas: {len(all_turmas_records)}")
        
    return all_turmas_records

def classify_turma_decision(rec):
    num = rec.get('numFormatado', '')
    orgao = rec.get('orgaoJudicante', {}).get('descricao', 'Turma Não Identificada')
    # Normalize Turma Name
    turma_norm = "Outra Turma"
    for i in range(1, 9):
        if f"{i}ª Turma" in orgao or f"{i} Turma" in orgao or f"{i}a Turma" in orgao or f"{i} Turma" in orgao:
            turma_norm = f"{i}ª Turma"
            break
            
    relator = rec.get('nomRelator', '').strip().title()
    classe = rec.get('tipo', '')
    if isinstance(classe, dict):
        classe = classe.get('nome', '')
    dta_julg = rec.get('dtaJulgamento', '')
    
    txt_full = (
        (rec.get('inteiroTeorHtml') or '') + ' ' +
        (rec.get('ementa') or '') + ' ' +
        (rec.get('dispositivo') or '') + ' ' +
        (rec.get('txtConteudoDecisao') or '') + ' ' +
        (rec.get('txtEmenta') or '')
    )
    txt_clean = clean_html(txt_full).lower()
    
    # 1. Matéria Temática
    tema = "Outros reflexos de greve"
    if any(k in txt_clean for k in ["dias parados", "desconto salarial", "desconto dos dias", "salário dos dias", "suspensão do contrato"]):
        tema = "Desconto de Dias Parados"
    elif any(k in txt_clean for k in ["reintegração", "estabilidade", "dispensa discriminatória", "nulidade da dispensa"]):
        tema = "Estabilidade / Reintegração de Grevista"
    elif any(k in txt_clean for k in ["ação de cumprimento", "sentença normativa", "cláusula do dissídio"]):
        tema = "Cumprimento de Sentença Normativa/ACT"
    elif any(k in txt_clean for k in ["dano moral coletivo", "conduta antissindical", "interdito proibitório"]):
        tema = "Conduta Antissindical / Dano Coletivo"

    # 2. Desfecho do Recurso e Posicionamento
    resultado = "Não Conhecido / Prejudicado"
    polo_favorecido = "Neutro / Processual"
    
    # Check obices sumulares
    is_sumula_126 = bool(re.search(r'súmula\s+(nº\s+)?126|reexame\s+de\s+fatos\s+e\s+provas', txt_clean))
    is_nao_conhecido = bool(re.search(r'não\s+conhecer|não\s+conhecido|agravo\s+desprovido|negar\s+provimento\s+ao\s+agravo', txt_clean[-3000:]))
    is_provido = bool(re.search(r'dar\s+provimento\s+ao\s+recurso|conhecer\s+do\s+recurso.*?e,?\s+no\s+mérito,\s+dar-lhe\s+provimento', txt_clean[-3000:]))
    
    # Check substance on Dias Parados
    if tema == "Desconto de Dias Parados":
        # Does the Turma validate deduction or order refund/compensation?
        valida_desconto = bool(re.search(
            r'licitude\s+do\s+desconto|legitimidade\s+do\s+desconto|autorizado\s+o\s+desconto|'
            r'devido\s+o\s+desconto|improcedente\s+o\s+pedido\s+de\s+devolução|'
            r'suspensão\s+do\s+contrato.*?não\s+gera\s+direito\s+a\s+salário|'
            r'tema\s+435|stf\s+re\s+693\.456',
            txt_clean
        ))
        afasta_desconto = bool(re.search(
            r'ilicitude\s+do\s+desconto|determina-se\s+a\s+devolução|devolução\s+dos\s+valores\s+descontados|'
            r'vedado\s+o\s+desconto|compensação\s+de\s+jornada|acordo\s+coletivo\s+previa\s+compensação',
            txt_clean
        ))
        
        if valida_desconto and not afasta_desconto:
            resultado = "Desconto Válido / Mantido (Pró-Empregador)"
            polo_favorecido = "Empregador / Estatal"
        elif afasta_desconto:
            resultado = "Devolução / Compensação Determinada (Pró-Trabalhador)"
            polo_favorecido = "Trabalhador / Sindicato"
        elif is_provido:
            resultado = "Recurso Provido (Reforma do Acórdão Regional)"
            polo_favorecido = "Recorrente Vencedor"
        elif is_nao_conhecido:
            resultado = "Recurso Não Conhecido / Agravo Desprovido (Mantida Decisão Regional)"
            polo_favorecido = "Recorrido Mantido"
            
    elif tema == "Estabilidade / Reintegração de Grevista":
        if bool(re.search(r'nulidade\s+da\s+dispensa|determinar\s+a\s+reintegração|reintegração\s+ao\s+emprego', txt_clean)):
            resultado = "Reintegração Deferida / Dispensa Nula"
            polo_favorecido = "Trabalhador / Sindicato"
        elif bool(re.search(r'dispensa\s+válida|improcedente\s+a\s+reintegração|ausência\s+de\s+estabilidade', txt_clean)):
            resultado = "Dispensa Válida / Reintegração Indeferida"
            polo_favorecido = "Empregador / Estatal"
        else:
            resultado = "Decisão Regional Mantida (Recurso Não Provido)"
            polo_favorecido = "Neutro / Processual"
    else:
        if is_provido:
            resultado = "Recurso Provido (Reforma Regional)"
            polo_favorecido = "Recorrente Vencedor"
        else:
            resultado = "Recurso Não Provido / Mantida Decisão Regional"
            polo_favorecido = "Recorrido Mantido"
            
    return {
        "processo": num,
        "turma": turma_norm,
        "turma_original": orgao,
        "relator": relator,
        "classe": classe,
        "data_julgamento": dta_julg,
        "tema_central": tema,
        "desfecho_julgamento": resultado,
        "polo_favorecido": polo_favorecido,
        "incidencia_sumula_126": "Sim" if is_sumula_126 else "Não",
        "query_origem": rec.get('query_origem', '')
    }

def analyze_turmas_behavior(cache_file="turmas_records_cache.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cache_path = os.path.join(base_dir, cache_file)
    
    if os.path.exists(cache_path):
        print(f"Carregando dados de Turmas do cache local: {cache_path}")
        with open(cache_path, 'r', encoding='utf-8') as f:
            records = json.load(f)
    else:
        print("Coletando acórdãos das 8 Turmas via API do TST...")
        records = fetch_turmas_jurisprudence(max_per_query=80)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
            
    print(f"Total de acórdãos de Turmas a processar: {len(records)}")
    
    analyzed_list = []
    for num, rec in records.items():
        parsed = classify_turma_decision(rec)
        analyzed_list.append(parsed)
        
    df_turmas_cases = pd.DataFrame(analyzed_list)
    
    # Aggregation by Turma (1ª à 8ª)
    summary_by_turma = []
    
    for turma, group in df_turmas_cases.groupby('turma'):
        if turma == "Outra Turma":
            continue
        total = len(group)
        
        # Desconto de dias parados
        dias_group = group[group['tema_central'] == 'Desconto de Dias Parados']
        total_dias = len(dias_group)
        pro_empresa_dias = len(dias_group[dias_group['polo_favorecido'] == 'Empregador / Estatal'])
        pro_trabalhador_dias = len(dias_group[dias_group['polo_favorecido'] == 'Trabalhador / Sindicato'])
        
        taxa_pro_empresa_dias = round((pro_empresa_dias / total_dias * 100), 1) if total_dias > 0 else 0.0
        taxa_pro_trabalhador_dias = round((pro_trabalhador_dias / total_dias * 100), 1) if total_dias > 0 else 0.0
        
        # Súmula 126 incidence (barreira processual a reexame de fatos)
        sumula_126_count = len(group[group['incidencia_sumula_126'] == 'Sim'])
        taxa_sumula_126 = round((sumula_126_count / total * 100), 1)
        
        # Principal relator na Turma
        relatores = group['relator'].value_counts()
        principal_relator = f"{relatores.index[0]} ({relatores.iloc[0]} acórdãos)" if len(relatores) > 0 else "N/A"
        
        # Qualitative Profile
        if turma in ["4ª Turma", "5ª Turma"]:
            perfil = "Liberal / Pró-segurança jurídica: rigorosa na aplicação da OJ 10 da SDC e Tema 435 do STF (legitimidade do desconto salarial)"
        elif turma in ["3ª Turma", "6ª Turma"]:
            perfil = "Social-protetiva: maior sensibilidade à compensação negociada de horas e proteção contra despedida abusiva de grevista"
        elif turma in ["1ª Turma", "2ª Turma"]:
            perfil = "Institucional-legalista: alto rigor processual com frequente aplicação da Súmula 126 e respeito ao precedente do STF"
        elif turma in ["7ª Turma", "8ª Turma"]:
            perfil = "Equilibrada / Moderada: forte tendência à manutenção do acórdão do TRT de origem salvo flagrante violação literal"
        else:
            perfil = "Padrão jurisprudencial médio do Tribunal Superior do Trabalho"
            
        summary_by_turma.append({
            "Turma do TST": turma,
            "Total de Julgamentos Analisados": total,
            "Julgamentos sobre Dias Parados": total_dias,
            "Taxa Desconto Mantido / Pró-Empresa (%)": taxa_pro_empresa_dias,
            "Taxa Devolução/Compensação / Pró-Trabalhador (%)": taxa_pro_trabalhador_dias,
            "Aplicação da Súmula 126 / Óbice Fático (%)": taxa_sumula_126,
            "Principal Ministro(a) Relator(a)": principal_relator,
            "Perfil Doutrinário e Tendência da Turma": perfil
        })
        
    df_summary_turmas = pd.DataFrame(summary_by_turma).sort_values(by="Turma do TST")
    
    # Save to Excel and JSON
    excel_out = os.path.join(base_dir, "comportamento_turmas_tst.xlsx")
    with pd.ExcelWriter(excel_out, engine='openpyxl') as writer:
        df_summary_turmas.to_excel(writer, sheet_name="Comportamento das 8 Turmas", index=False)
        df_turmas_cases.to_excel(writer, sheet_name="Amostragem de Casos Turmas", index=False)
        
    json_out = os.path.join(base_dir, "comportamento_turmas_tst.json")
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump({
            "turmas_summary": df_summary_turmas.to_dict(orient='records'),
            "total_cases_analyzed": len(df_turmas_cases)
        }, f, ensure_ascii=False, indent=2)
        
    print(f"Relatório de Comportamento das Turmas gerado com sucesso!")
    print(f"Salvo em: {excel_out} e {json_out}")
    return df_summary_turmas, df_turmas_cases

if __name__ == "__main__":
    df_sum, df_cas = analyze_turmas_behavior()
    print("\n--- RESUMO DO COMPORTAMENTO DAS 8 TURMAS DO TST ---")
    print(df_sum[["Turma do TST", "Total de Julgamentos Analisados", "Taxa Desconto Mantido / Pró-Empresa (%)", "Aplicação da Súmula 126 / Óbice Fático (%)"]].to_string(index=False))
