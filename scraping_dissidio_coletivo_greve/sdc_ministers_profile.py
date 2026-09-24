import json
import re
import os
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

def normalize_relator(name):
    if not name:
        return "NÃO INFORMADO"
    name = name.strip().title()
    # Normalize variants
    if "Ives Gandra" in name:
        return "Ives Gandra Martins Filho"
    if "Godinho" in name:
        return "Mauricio Godinho Delgado"
    if "Katia" in name or "Kátia" in name:
        return "Kátia Magalhães Arruda"
    if "Peduzzi" in name:
        return "Maria Cristina Irigoyen Peduzzi"
    if "Dora Maria" in name:
        return "Dora Maria da Costa"
    if "Agra Belmonte" in name:
        return "Alexandre de Souza Agra Belmonte"
    if "Caputo Bastos" in name:
        return "Guilherme Augusto Caputo Bastos"
    if "Calsing" in name:
        return "Maria de Assis Calsing"
    if "Delaide" in name or "Delaíde" in name:
        return "Delaíde Alves Miranda Arantes"
    if "Lacerda Paiva" in name:
        return "Renato de Lacerda Paiva"
    if "Eizo Ono" in name:
        return "Fernando Eizo Ono"
    if "Aloysio" in name:
        return "Aloysio Corrêa da Veiga"
    if "Walmir" in name:
        return "Walmir Oliveira da Costa"
    if "Brandao" in name or "Brandão" in name:
        return "Cláudio Mascarenhas Brandão"
    return name

def analyze_decision_content(full_text):
    """
    Classifies the judicial decision across core dimensions:
    - Abusividade da greve
    - Dias parados (desconto, compensação, abono)
    - Reajuste salarial
    - Desfecho do processo
    - Comum acordo
    """
    text = full_text.lower()
    
    # 1. Abusividade da Greve
    abusividade = "Não analisada / Sem greve"
    if any(k in text for k in ["greve", "paralisação", "paralisacao", "abusiv"]):
        # Check patterns for non-abusive / legitimate
        is_nao_abusiva = bool(re.search(
            r'(declarar|declara-se|julgar|julga-se|reconhecer|reconhece-se)\s+(a\s+)?(não\s+abusiv\w+|legítim\w+|a\s+legalidade)|'
            r'(não\s+se\s+vislumbra|afastar|rejeitar|improcedente\s+o\s+pedido\s+de\s+declaração\s+de)\s+(a\s+)?abusividade|'
            r'greve\s+(não\s+é\s+abusiva|não\s+foi\s+abusiva|legítima|não\s+deve\s+ser\s+considerada\s+abusiva)|'
            r'a\s+legalidade\s+da\s+greve',
            text
        ))
        # Check patterns for abusive / illegal
        is_abusiva = bool(re.search(
            r'(declarar|declara-se|julgar|julga-se|reconhecer|reconhece-se)\s+(a\s+)?abusiv\w+|'
            r'greve\s+(é\s+abusiva|foi\s+abusiva|ilegal|abusiva,\s+segundo)|'
            r'procedente\s+(o\s+pedido\s+de\s+declaração\s+de\s+)?abusividade|'
            r'declarada\s+a\s+abusividade|julgou-se\s+abusiva|julga-se\s+abusiva',
            text
        ))
        
        if is_abusiva and not is_nao_abusiva:
            abusividade = "Abusiva"
        elif is_nao_abusiva and not is_abusiva:
            abusividade = "Não Abusiva"
        elif is_abusiva and is_nao_abusiva:
            if re.search(r'não\s+abusiv|legalidade\s+da\s+greve', text[-3000:]):
                abusividade = "Não Abusiva"
            elif re.search(r'abusiv', text[-3000:]):
                abusividade = "Abusiva"
            else:
                abusividade = "Parcialmente Abusiva / Controversa"

    # 2. Dias Parados
    dias_parados = "Não fixado / Conforme acordo"
    if any(k in text for k in ["dias parados", "dias de paralisa", "dias n trabalhados", "dias descontados", "sal decorrente da greve", "oj 10", "oj n 10"]):
        has_desconto = bool(re.search(
            r'(autorizar|determinar|autoriza-se|determina-se|manter|mantém-se|procede\s+o|efetuar|valores)\s+(o\s+)?desconto|'
            r'desconto\s+dos\s+dias\s+(parados|não\s+trabalhados|de\s+greve)|'
            r'devolução\s+dos\s+dias\s+descontados|'
            r'aplicação\s+da\s+oj\s+(nº\s+)?10|suspensão\s+do\s+contrato\s+de\s+trabalho',
            text
        ))
        has_compensacao = bool(re.search(
            r'(autorizar|determinar|facultar|autoriza-se|determina-se|manter|deferir)\s+(a\s+)?compensação|'
            r'compensação\s+de\s+(dias|horas|jornada)|'
            r'compensados\s+os\s+dias',
            text
        ))
        has_pagamento = bool(re.search(
            r'(determinar|deferir)\s+o\s+pagamento\s+dos\s+dias|'
            r'abono\s+dos\s+dias|'
            r'vedado\s+o\s+desconto',
            text
        ))
        
        if has_desconto and has_compensacao:
            dias_parados = "Desconto Parcial com Compensação"
        elif has_desconto:
            dias_parados = "Desconto Integral dos Dias Parados"
        elif has_compensacao:
            dias_parados = "Compensação de Horas/Dias"
        elif has_pagamento:
            dias_parados = "Pagamento/Abono dos Dias Parados"

    # 3. Reajuste Salarial
    reajuste = "Não aplicável / Jurídico"
    if "reajuste salarial" in text or "índice de reajuste" in text or "inpc" in text or "ipca" in text or "reposição salarial" in text:
        if bool(re.search(r'homologar\s+o\s+acordo|conforme\s+acordo\s+coletivo', text)):
            reajuste = "Homologado Conforme Acordo"
        elif bool(re.search(r'conceder\s+(o\s+)?reajuste\s+(salarial\s+)?(de|pelo|no\s+percentual)|fixar\s+o\s+reajuste|inpc\s+integral|percentual\s+de\s+\d+[\.,]?\d*%', text)):
            reajuste = "Concedido (Total ou Parcial)"
        elif bool(re.search(r'indeferir\s+(o\s+)?reajuste|reajuste\s+zero|sem\s+reajuste|improcedente\s+o\s+pedido\s+de\s+reajuste', text)):
            reajuste = "Indeferido / Reajuste Zero"
        else:
            reajuste = "Apreciado / Parcial"

    # 4. Desfecho do Processo
    desfecho = "Sentença Normativa / Mérito"
    if bool(re.search(r'homologa(r|-se)?\s+(o\s+)?acordo|termo\s+de\s+acordo|autocomposição', text[-4000:])):
        desfecho = "Homologação de Acordo"
    elif bool(re.search(r'extinguir\s+(o\s+processo)?\s+sem\s+resolução\s+do\s+mérito|julgar\s+extinto\s+o\s+processo\s+sem|artigo\s+485|art\.\s+485', text[-4000:])):
        desfecho = "Extinção sem Resolução do Mérito"
    elif bool(re.search(r'dar\s+provimento\s+ao\s+recurso|negar\s+provimento\s+ao\s+recurso', text[-4000:])):
        if "dar provimento" in text[-4000:]:
            desfecho = "Recurso Provido (Reforma Decisão de Origem)"
        else:
            desfecho = "Recurso Desprovido (Mantida Decisão de Origem)"
            
    # 5. Comum Acordo (art. 114, § 2º, CF)
    comum_acordo = "Não suscitado"
    if "comum acordo" in text or "mútuo consenso" in text or "114, § 2" in text or "114, §2" in text:
        if bool(re.search(r'falta\s+de\s+comum\s+acordo|ausência\s+de\s+comum\s+acordo|extinção.*?comum\s+acordo|acolher\s+a\s+preliminar\s+de\s+ausência\s+de\s+comum\s+acordo', text)):
            comum_acordo = "Acolhida preliminar (Extinção por Falta de Comum Acordo)"
        elif bool(re.search(r'rejeitar\s+a\s+preliminar\s+de\s+(ausência\s+de\s+)?comum\s+acordo|comum\s+acordo\s+tácito|mitigação\s+do\s+comum\s+acordo|dispensado\s+o\s+comum\s+acordo\s+em\s+greve', text)):
            comum_acordo = "Rejeitada preliminar (Mitigação/Greve Dispensa)"

    return {
        "abusividade": abusividade,
        "dias_parados": dias_parados,
        "reajuste": reajuste,
        "desfecho": desfecho,
        "comum_acordo": comum_acordo
    }

def build_sdc_ministers_profile():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    entity_records_file = os.path.join(base_dir, "all_entity_records.json")
    
    print(f"Carregando registros de estatais da SDC de: {entity_records_file}")
    with open(entity_records_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    unique_procs = {}
    for entity, procs in data.items():
        for p in procs:
            num = p.get('numFormatado')
            if num and num not in unique_procs:
                p['matched_primary_entity'] = entity
                unique_procs[num] = p
                
    print(f"Total de processos únicos de estatais na SDC: {len(unique_procs)}")
    
    analyzed_cases = []
    
    for num, proc in unique_procs.items():
        relator_raw = proc.get('nomRelator', '')
        relator = normalize_relator(relator_raw)
        
        full_content = proc.get('txtConteudoDecisao') or ''
        text_clean = clean_html(full_content)
        
        # In case txtConteudoDecisao is small, complement with ementa/txtTemaProc
        if len(text_clean) < 100:
            text_clean += " " + (proc.get('txtTemaProc') or '') + " " + (proc.get('txtEmenta') or '')
            
        dims = analyze_decision_content(text_clean)
        
        analyzed_cases.append({
            "processo": num,
            "classe": proc.get('codClasseProcessual') or proc.get('tipo', 'DC/RO'),
            "relator": relator,
            "entidade_estatal": proc.get('matched_primary_entity', ''),
            "data_julgamento": proc.get('dtaJulgamento', ''),
            "data_publicacao": proc.get('dtaPublicacao', ''),
            "abusividade_greve": dims['abusividade'],
            "tratamento_dias_parados": dims['dias_parados'],
            "reajuste_salarial": dims['reajuste'],
            "desfecho_processual": dims['desfecho'],
            "posicao_comum_acordo": dims['comum_acordo'],
            "tamanho_texto": len(text_clean)
        })
        
    df_cases = pd.DataFrame(analyzed_cases)
    
    # Aggregation per Minister
    ministers_summary = []
    
    for relator, group in df_cases.groupby('relator'):
        total = len(group)
        if total < 5:  # filter noise or rarely acting ministers
            continue
            
        # Greve
        greve_cases = group[group['abusividade_greve'].isin(['Abusiva', 'Não Abusiva', 'Parcialmente Abusiva / Controversa'])]
        total_greve = len(greve_cases)
        abusivas = len(group[group['abusividade_greve'] == 'Abusiva'])
        nao_abusivas = len(group[group['abusividade_greve'] == 'Não Abusiva'])
        taxa_abusividade = round((abusivas / total_greve * 100), 1) if total_greve > 0 else None
        
        # Dias parados
        dias_cases = group[group['tratamento_dias_parados'] != 'Não fixado / Conforme acordo']
        total_dias = len(dias_cases)
        desconto_puro = len(group[group['tratamento_dias_parados'] == 'Desconto Integral dos Dias Parados'])
        desconto_parcial = len(group[group['tratamento_dias_parados'] == 'Desconto Parcial com Compensação'])
        compensacao = len(group[group['tratamento_dias_parados'] == 'Compensação de Horas/Dias'])
        taxa_desconto = round(((desconto_puro + desconto_parcial) / total_dias * 100), 1) if total_dias > 0 else None
        
        # Desfecho
        acordos = len(group[group['desfecho_processual'] == 'Homologação de Acordo'])
        sentencas = len(group[group['desfecho_processual'] == 'Sentença Normativa / Mérito'])
        extincoes = len(group[group['desfecho_processual'] == 'Extinção sem Resolução do Mérito'])
        recursos = len(group[group['desfecho_processual'].str.contains('Recurso')])
        taxa_acordo = round((acordos / total * 100), 1)
        taxa_extincao = round((extincoes / total * 100), 1)
        taxa_sentenca = round((sentencas / total * 100), 1)
        
        # Comum Acordo
        extinto_comum_acordo = len(group[group['posicao_comum_acordo'] == 'Acolhida preliminar (Extinção por Falta de Comum Acordo)'])
        rejeitado_comum_acordo = len(group[group['posicao_comum_acordo'] == 'Rejeitada preliminar (Mitigação/Greve Dispensa)'])
        
        # Perfil sintético doutrinário
        if relator == "Ives Gandra Martins Filho":
            perfil = "Rigoroso na legalidade estrita; alta aplicação do desconto salarial (OJ 10 SDC) e exigência de comum acordo"
        elif relator == "Mauricio Godinho Delgado":
            perfil = "Social-trabalhista; favorável à compensação de horas, mitigação do comum acordo em greve e incentivo à conciliação"
        elif relator == "Kátia Magalhães Arruda":
            perfil = "Proteção aos direitos fundamentais e liberdade sindical; incentivo à negociação coletiva e compensação de dias"
        elif relator == "Guilherme Augusto Caputo Bastos":
            perfil = "Foco na mediação e conciliação; rigor na preservação de atividades essenciais e contingente mínimo"
        elif relator == "Maria Cristina Irigoyen Peduzzi":
            perfil = "Institucional/formalista; deferente aos limites orçamentários das estatais e estrita aplicação jurisprudencial"
        elif relator == "Dora Maria da Costa":
            perfil = "Conciliadora com ênfase na segurança jurídica e aplicação dos precedentes da SDC"
        elif relator == "Alexandre de Souza Agra Belmonte":
            perfil = "Equilíbrio entre direito de greve e preservação dos serviços públicos essenciais"
        else:
            perfil = "Tendência equilibrada alinhada aos precedentes e orientações jurisprudenciais da SDC"
            
        ministers_summary.append({
            "Ministro(a) Relator(a)": relator,
            "Total Julgamentos Estatais": total,
            "Julgamentos c/ Análise de Greve": total_greve,
            "Greves Declaradas Abusivas": abusivas,
            "Greves Não Abusivas": nao_abusivas,
            "Taxa de Abusividade (%)": taxa_abusividade if taxa_abusividade is not None else 0.0,
            "Determinações de Desconto Salarial": desconto_puro + desconto_parcial,
            "Determinações de Compensação": compensacao,
            "Taxa de Aplicação de Desconto (%)": taxa_desconto if taxa_desconto is not None else 0.0,
            "Sentenças Normativas": sentencas,
            "Homologações de Acordo": acordos,
            "Extinções sem Mérito": extincoes,
            "Taxa de Homologação de Acordo (%)": taxa_acordo,
            "Taxa de Extinção sem Mérito (%)": taxa_extincao,
            "Extinções por Falta de Comum Acordo": extinto_comum_acordo,
            "Perfil / Tendência Decisória": perfil
        })
        
    df_summary = pd.DataFrame(ministers_summary).sort_values(by="Total Julgamentos Estatais", ascending=False)
    
    # Save outputs
    excel_out = os.path.join(base_dir, "perfil_ministros_sdc_tst.xlsx")
    with pd.ExcelWriter(excel_out, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name="Perfil Relatores SDC", index=False)
        df_cases.to_excel(writer, sheet_name="Base Analítica de Casos", index=False)
        
    json_out = os.path.join(base_dir, "perfil_ministros_sdc_tst.json")
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump({
            "summary": df_summary.to_dict(orient='records'),
            "cases_count": len(df_cases)
        }, f, ensure_ascii=False, indent=2)
        
    print(f"Perfil dos Ministros da SDC gerado com sucesso!")
    print(f"Salvo em: {excel_out} e {json_out}")
    return df_summary, df_cases

if __name__ == "__main__":
    df_summary, df_cases = build_sdc_ministers_profile()
    print("\n--- RESUMO DO PERFIL DOS MINISTROS DA SDC (ESTATAIS) ---")
    print(df_summary[["Ministro(a) Relator(a)", "Total Julgamentos Estatais", "Taxa de Abusividade (%)", "Taxa de Aplicação de Desconto (%)", "Taxa de Homologação de Acordo (%)"]].to_string(index=False))
