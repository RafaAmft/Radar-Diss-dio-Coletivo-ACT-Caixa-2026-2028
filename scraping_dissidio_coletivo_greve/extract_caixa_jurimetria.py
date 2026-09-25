import requests
import json
import re
import os
from bs4 import BeautifulSoup

def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_clean_document(reg):
    """
    Extrai a Ementa Oficial formatada ou o texto substantivo do Despacho/Decisão,
    removendo completamente o cabeçalho burocrático (PODER JUDICIÁRIO, SUSCITANTE, ADVOGADO, etc.)
    """
    ementa = (reg.get('ementa') or '').strip()
    disp = (reg.get('dispositivo') or '').strip()
    
    if ementa:
        doc_type = "Ementa do Acórdão"
        clean_em = clean_html(ementa)
        clean_text = f"📜 EMENTA OFICIAL:\n{clean_em}"
        if disp:
            clean_disp = clean_html(disp)
            clean_text += f"\n\n⚖️ DISPOSITIVO:\n{clean_disp}"
        return doc_type, clean_text
    
    # Caso seja Despacho ou Decisão Monocrática
    tipo_info = reg.get('tipo', {})
    tipo_nome = tipo_info.get('nome') if isinstance(tipo_info, dict) else 'Decisão Monocrática'
    doc_type = f"{tipo_nome} do Relator"
    
    raw_html = reg.get('txtConteudoDecisao') or reg.get('txtConteudoDecisaoHighlight') or ''
    soup = BeautifulSoup(raw_html, 'html.parser')
    for s in soup(['script', 'style']):
        s.extract()
    raw_text = soup.get_text(separator='\n')
    
    # Limpa linhas vazias
    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
    
    # Encontra onde o cabeçalho burocrático termina e onde começa o despacho de verdade
    start_idx = 0
    found_start = False
    for idx, l in enumerate(lines[:35]):
        # Padrões de início de despacho
        if re.match(r'^(d\s*e\s*s\s*p\s*a\s*c\s*h\s*o|d\s*e\s*c\s*i\s*s\s*[aã]\s*o|v\s*i\s*s\s*t\s*o\s*s)', l, re.IGNORECASE):
            start_idx = idx + 1
            found_start = True
            break
        elif re.match(r'^(trata-se|compulsando|ao\s+exame|em\s+aten[cç][aã]o|diante\s+d|vistos|defiro|indefiro)', l, re.IGNORECASE):
            start_idx = idx
            found_start = True
            break
            
    if found_start and start_idx < len(lines):
        body_lines = lines[start_idx:]
    else:
        # Se não achou marcador explícito, pula linhas com cara de cabeçalho
        body_lines = [l for l in lines if not re.match(r'^(poder|justi[cç]a|tribunal|processo|suscitant|suscitad|recorrent|recorrid|advogad|gvp|gp\/)', l, re.IGNORECASE)]
    
    # Junta parágrafos substantivos
    clean_body = "\n\n".join(body_lines[:20]) # até 20 parágrafos relevantes
    if not clean_body:
        clean_body = clean_html(raw_html)[:600]
        
    clean_text = f"📑 TEOR DO DESPACHO / DECISÃO:\n{clean_body}"
    return doc_type, clean_text

def parse_polo_and_parties(reg):
    """
    Analisa linha por linha o cabeçalho para não cruzar Suscitante com Suscitada.
    """
    raw_html = reg.get('txtConteudoDecisao') or reg.get('txtConteudoDecisaoHighlight') or reg.get('ementa') or ''
    soup = BeautifulSoup(raw_html, 'html.parser')
    for s in soup(['script', 'style']): s.extract()
    text = soup.get_text(separator='\n')
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    susc = ''
    resp = ''
    current_role = None
    
    for l in lines[:40]:
        if re.match(r'^(SUSCITANTE|RECORRENTE|AUTOR|REQUERENTE)\s*:', l, re.IGNORECASE):
            current_role = 'ativo'
            val = re.sub(r'^(SUSCITANTE|RECORRENTE|AUTOR|REQUERENTE)\s*:\s*', '', l, flags=re.IGNORECASE).strip()
            if val: susc = val
        elif re.match(r'^(SUSCITAD[OA]S?|RECORRID[OA]S?|R[EÉ]U|REQUERID[OA])\s*:', l, re.IGNORECASE):
            current_role = 'passivo'
            val = re.sub(r'^(SUSCITAD[OA]S?|RECORRID[OA]S?|R[EÉ]U|REQUERID[OA])\s*:\s*', '', l, flags=re.IGNORECASE).strip()
            if val: resp = val
        elif current_role == 'ativo' and not susc and not re.match(r'^(ADVOGAD|PROCURAD|OAB)', l, re.IGNORECASE):
            susc = l
        elif current_role == 'passivo' and not resp and not re.match(r'^(ADVOGAD|PROCURAD|OAB)', l, re.IGNORECASE):
            resp = l
            
    polo = "Parte no Processo"
    if 'caixa' in susc.lower() or 'cef' in susc.lower():
        polo = "Suscitante / Recorrente (Autora)"
        adversario = resp
    elif 'caixa' in resp.lower() or 'cef' in resp.lower():
        polo = "Suscitada / Recorrida (Ré)"
        adversario = susc
    else:
        # Análise textual de frases
        head = " ".join(lines[:25]).lower()
        if re.search(r'por\s+[^\.\n]+em\s+face\s+da\s+caixa', head) or re.search(r'contra\s+(a\s+)?caixa', head):
            polo = "Suscitada / Recorrida (Ré)"
            adversario = susc if susc else "Entidades Sindicais dos Bancários"
        elif re.search(r'pela\s+caixa\s+[^\.\n]+em\s+face\s+d', head) or re.search(r'recurso\s+ordin[aá]rio\s+da\s+caixa', head):
            polo = "Suscitante / Recorrente (Autora)"
            adversario = resp if resp else "Entidades Sindicais dos Bancários"
        else:
            adversario = susc if susc else (resp if resp else "Entidades Sindicais dos Bancários")
            
    if not adversario:
        adversario = "Entidades Sindicais dos Bancários"
        
    # Limpa adversário
    adversario = re.sub(r'\s+', ' ', adversario).strip()
    adversario = re.sub(r'^(ADVOGAD[OA]|Dra?\.|Dr\.)\s*', '', adversario, flags=re.IGNORECASE)
    
    return polo, adversario

def parse_decision_record(reg):
    doc_type, clean_content = extract_clean_document(reg)
    polo_caixa, parte_contraria = parse_polo_and_parties(reg)
    
    num_formatado = reg.get('numFormatado', '')
    relator = (reg.get('nomRelator') or 'Não informado').title()
    data_pub = reg.get('dtaPublicacao', '')
    if 'T' in data_pub:
        data_pub = data_pub.split('T')[0]
    
    cnj_match = re.search(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', num_formatado)
    cnj = cnj_match.group(1) if cnj_match else num_formatado
    
    classe = reg.get('codFase', '')
    if not classe:
        if num_formatado.startswith('DCG'): classe = 'DCG'
        elif num_formatado.startswith('DC'): classe = 'DC'
        elif num_formatado.startswith('ROT'): classe = 'ROT'
        elif num_formatado.startswith('RO'): classe = 'RO'
        elif num_formatado.startswith('Tut'): classe = 'TutCautAnt'
        elif num_formatado.startswith('PMPP'): classe = 'PMPP'
        else: classe = 'Dissídio Coletivo'
        
    full_text = clean_content.lower()
    
    # Temas detection
    temas = []
    if re.search(r'sa[uú]de\s+caixa|plano\s+de\s+sa[uú]de|assist[eê]ncia\s+m[eé]dica', full_text):
        temas.append('Saúde Caixa')
    if re.search(r'dias\s+parados|desconto.*sal[aá]ri|compensa[cç][aã]o\s+de\s+horas|greve', full_text):
        temas.append('Dias Parados & Greve')
    if re.search(r'plr|participa[cç][aã]o\s+nos\s+lucros|plr\s+social', full_text):
        temas.append('PLR & PLR Social')
    if re.search(r'7[aª]\s+e\s+8[aª]\s+hora|jornada|cargo\s+de\s+confian[cç]a|fun[cç][aã]o\s+gratificada|art\.?\s*224', full_text):
        temas.append('Jornada & 7ª/8ª Hora')
    if re.search(r'contingente|efetivo\s+m[ií]nimo|servi[cç]o\s+essencial|60%|70%|80%', full_text):
        temas.append('Contingenciamento Mínimo')
    if re.search(r'vale[\s-]?alimenta|vale[\s-]?refei|aux[ií]lio[\s-]?alimenta|cesta', full_text):
        temas.append('Auxílio Alimentação & Cesta')
    if re.search(r'reajuste|inpc|ipca|perda\s+inflacion[aá]ria|aumento\s+real', full_text):
        temas.append('Reajuste Salarial')
    if re.search(r'teletrabalho|home\s*office|trabalho\s+remoto|h[ií]brido', full_text):
        temas.append('Teletrabalho & Regime Híbrido')
    if re.search(r'piquete|interdito|turba[cç][aã]o|livre\s+acesso', full_text):
        temas.append('Piquetes & Acesso')
    if re.search(r'advogado|honor[aá]rio|advocef', full_text):
        temas.append('Advogados & Honorários da CEF')
    if re.search(r'comum\s+acordo|art\.?\s*114.*§\s*2', full_text):
        temas.append('Comum Acordo Constitucional')
    if not temas:
        temas = ['Cláusulas Gerais do ACT']

    # Desfecho
    disp = clean_html(reg.get('dispositivo', '')).lower()
    desfecho = "Em Andamento / Despacho"
    if 'homolog' in disp or 'acordo' in disp:
        desfecho = "Acordo Homologado"
    elif 'negar-lhe provimento' in disp or 'negou-se provimento' in disp:
        desfecho = "Recurso Desprovido (Mantida Decisão Anterior)"
    elif 'dar-lhe provimento' in disp or 'deu-se provimento' in disp:
        desfecho = "Recurso Provido pelo TST"
    elif re.search(r'homolog[ao]|homologa[cç][aã]o|acordo\s+coletivo\s+homologado|autocomposi[cç][aã]o', full_text):
        desfecho = "Acordo Homologado"
    elif re.search(r'senten[cç]a\s+normativa|julgado\s+procedente|julgado\s+improcedente|fixa-se\s+a\s+cl[aá]usula', full_text):
        desfecho = "Sentença Normativa Fixada"
    elif re.search(r'defiro\s+parcialmente|defiro\s+o\s+pedido\s+liminar|concedo\s+a\s+tutela|medida\s+liminar', full_text):
        desfecho = "Liminar Deferida (Parcial ou Total)"
    elif re.search(r'indefiro\s+o\s+pedido|indefiro\s+a\s+liminar|denego', full_text):
        desfecho = "Liminar Indeferida"
    elif re.search(r'extin[cç][aã]o\s+do\s+processo|sem\s+resolu[cç][aã]o\s+de\s+m[eé]rito|falta\s+de\s+comum\s+acordo|perda\s+de\s+objeto', full_text):
        desfecho = "Extinto sem Resolução de Mérito"

    # Resumo do Impacto contextualizado
    if "Acordo Homologado" in desfecho:
        impacto = "Conquista homologada: as cláusulas negociadas entre a Caixa e os sindicatos ganharam força executiva judicial, resguardando direitos e benefícios acordados sem risco de anulação."
    elif "Liminar" in desfecho:
        impacto = "Medida cautelar de urgência: fixação de contingente de trabalho e garantia de vigência provisória de direitos até a decisão colegiada final."
    elif "Sentença Normativa" in desfecho:
        impacto = "Decisão judicial impositiva da SDC: fixação compulsória de cláusulas pelo TST com vigência legal para os empregados da Caixa."
    elif "Recurso Provido" in desfecho:
        impacto = "Reforma no TST: acolhimento da tese recursal pelo Tribunal Superior, adequando a decisão regional ao entendimento consolidado da corte."
    elif "Recurso Desprovido" in desfecho:
        impacto = "Decisão mantida no TST: a corte rejeitou o recurso, confirmando o julgado anterior favorável à jurisprudência pacífica da SDC."
    elif "dias parados" in full_text and "desconto" in full_text:
        impacto = "Discussão direta sobre a legalidade do desconto de salários de greve e a aplicação de compensação de jornada em favor dos empregados."
    elif "plr" in full_text:
        impacto = "Disputa coletiva envolvendo o pagamento e as regras de distribuição da PLR e PLR Social da Caixa."
    elif "saúde caixa" in full_text:
        impacto = "Acompanhamento de regras de custeio, coparticipação e sustentabilidade do plano de assistência médica Saúde Caixa."
    else:
        impacto = "Acompanhamento processual de direitos coletivos dos empregados da Caixa no TST."

    return {
        "id": reg.get('id', ''),
        "cnj": cnj,
        "numFormatado": num_formatado,
        "classe": classe,
        "relator": relator,
        "dataPublicacao": data_pub,
        "poloCaixa": polo_caixa,
        "partesContrarias": parte_contraria[:60],
        "desfecho": desfecho,
        "temas": temas,
        "docType": doc_type,
        "resumoImpacto": impacto,
        "conteudoLimpo": clean_content,
        "linkPje": f"https://pje.tst.jus.br/consultaprocessual/detalhe-processo/{cnj.replace('-', '').replace('.', '')}"
    }

def main():
    print("Iniciando extração jurimétrica aperfeiçoada com limpeza estrutural de ementas e despachos...")
    
    all_decisions = []
    seen_cnjs = set()
    
    # 1. FLAGSHIP 2026: O CASO VIVO DO DISSÍDIO DA CAIXA
    flagship_case = {
        "id": "dcg-caixa-2026-godinho",
        "cnj": "1000975-72.2026.5.00.0000",
        "numFormatado": "DCG - 1000975-72.2026.5.00.0000",
        "classe": "DCG",
        "relator": "Mauricio Godinho Delgado",
        "dataPublicacao": "2026-09-24",
        "poloCaixa": "Suscitante (Autora da Ação)",
        "partesContrarias": "CONTRAF e CONTEC",
        "desfecho": "Liminar Deferida Parcialmente (60% Contingente + ACT Mantido)",
        "temas": [
            "Contingenciamento Mínimo",
            "Saúde Caixa",
            "Dias Parados & Greve",
            "Piquetes & Acesso",
            "Ultratividade do ACT"
        ],
        "docType": "Decisão Liminar em Tutela Provisória de Urgência",
        "resumoImpacto": "O Min. Godinho rejeitou o pedido da Caixa de 80% e fixou contingente mínimo em 60% por agência (garantindo 40% do efetivo em greve legítima). Manteve a vigência de todas as cláusulas do ACT 2024/2026 (incluindo Saúde Caixa e vales), indeferiu a proibição de piquetes e derrubou o segredo de justiça dos autos. Prazo fatal de defesa: sábado (26/09) às 13h. Sessão de julgamento na SDC marcada para terça-feira (29/09) às 14h30.",
        "conteudoLimpo": "📑 DISPOSITIVO DA DECISÃO LIMINAR (Min. Mauricio Godinho Delgado):\n\n\"...Dessa forma, sem prejuízo do juízo definitivo na análise da questão debatida, defiro parcialmente o pedido de liminar para determinar que sejam mantidos, em serviço, 60% (sessenta por cento) dos empregados da Requerente e de suas subsidiárias, de forma remota ou presencial, referentemente a cada agência, a partir da divulgação e/ou intimação desta decisão e durante todo o período de paralisação, observada a obrigação mútua das Partes pelo cumprimento da Lei de Greve (art. 11, caput).\n\nEstabeleço multa diária de R$ 100.000,00 (cem mil reais) em caso de descumprimento da liminar ora deferida, a ser paga pela entidade sindical que descumprir a presente determinação.\n\nIndefiro o pleito inibitório voltado a compelir os Sindicatos Suscitados à abstenção de atos obstativos ao livre acesso de empregados, clientes e usuários às dependências da Empresa...\n\nDefiro a manutenção provisória das cláusulas normativas do ACT 2024/2026 até a decisão definitiva do presente dissídio coletivo, sem conferir caráter definitivo ou de ultratividade às condições de trabalho.\n\n...determino, de imediato, o levantamento do segredo de justiça da petição inicial e dos documentos que a acompanham. Ressalvam-se do levantamento de sigilo, devendo ser mantidos com acesso restrito, apenas às partes e ao MPT, os seguintes documentos: Justificativas das cláusulas propostas (Doc. 03) e Relatório Atuarial e Nota Técnica GESAD n. 10336/2026 (Doc. 04)...\"",
        "linkPje": "https://pje.tst.jus.br/pjekz/validacao/26092420574531700000207281146?instancia=3",
        "is_flagship": True,
        "detalhesLiminar": {
            "pedidoCaixaContingente": "80%",
            "deferidoGodinhoContingente": "60% (Presencial ou Remoto)",
            "multaDescumprimento": "R$ 100.000,00 por dia",
            "pedidoPiquetes": "Indeferido (Competência da Vara do Trabalho e ausência de abusos comprovados)",
            "segredoJustica": "Levantado (Público, salvo Doc. 03 Justificativas e Doc. 04 Relatório Atuarial GESAD 10336/2026)",
            "statusACTAnterior": "Prorrogado e Vigente integralmente até julgamento definitivo",
            "proximosPassos": "Defesa das Confederações até 26/09 (13h) • Julgamento na SDC em 29/09 às 14:30"
        }
    }
    all_decisions.append(flagship_case)
    seen_cnjs.add("1000975-72.2026.5.00.0000")
    
    # 2. Carrega do cache local completo com mais de 50 decisões reais da Caixa
    try:
        with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
            cached_data = json.load(f).get('Caixa Econômica Federal (CEF)', [])
            print(f"Processando {len(cached_data)} registros do cache local...")
            for reg in cached_data:
                parsed = parse_decision_record(reg)
                cnj = parsed['cnj']
                if cnj not in seen_cnjs:
                    seen_cnjs.add(cnj)
                    parsed['is_flagship'] = False
                    all_decisions.append(parsed)
    except Exception as e:
        print(f"Erro ao carregar cache local: {e}")

    # 3. Também consulta a API para registros recentes adicionais
    url_base = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
    headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    payload = {
        'ou': '',
        'e': '"Caixa Econômica Federal"',
        'termoExato': '',
        'naoContem': '',
        'ementa': '',
        'dispositivo': '',
        'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
        'orgaosJudicantes': [{'codigo': 47, 'sigla': 'SDC', 'descricao': 'Seção Especializada em Dissídios Coletivos'}],
        'ministros': [],
        'convocados': [],
        'classesProcessuais': [
            {'codFase': 'DCG'}, {'codFase': 'DC'}, {'codFase': 'RO'}, {'codFase': 'ROT'}, {'codFase': 'RODC'}
        ],
        'codigosClassesPrecedentes': [],
        'indicadores': [],
        'assuntos': [],
        'tipos': ['ACORDAO', 'DESPACHO'],
        'orgao': 'TST',
        'publicacaoInicial': None,
        'publicacaoFinal': None,
        'julgamentoInicial': '2016-01-01',
        'julgamentoFinal': '2026-09-25',
        'ordenacao': 'data'
    }
    try:
        r = requests.post(f'{url_base}/1/100', json=payload, headers=headers, timeout=25)
        if r.status_code == 200:
            regs = r.json().get('registros', [])
            print(f"Recebidos {len(regs)} da API para checagem cruzada...")
            for item in regs:
                reg = item.get('registro', {})
                parsed = parse_decision_record(reg)
                cnj = parsed['cnj']
                if cnj not in seen_cnjs:
                    seen_cnjs.add(cnj)
                    parsed['is_flagship'] = False
                    all_decisions.append(parsed)
    except Exception as e:
        print(f"Aviso API: {e}")

    print(f"Total final de decisões limpas e estruturadas: {len(all_decisions)}")
    
    with open('scraping_dissidio_coletivo_greve/dados_decisoes_caixa.json', 'w', encoding='utf-8') as f:
        json.dump(all_decisions, f, ensure_ascii=False, indent=2)
    with open('dados_decisoes_caixa.json', 'w', encoding='utf-8') as f:
        json.dump(all_decisions, f, ensure_ascii=False, indent=2)
    print("Arquivos JSON atualizados com sucesso!")

if __name__ == '__main__':
    main()
