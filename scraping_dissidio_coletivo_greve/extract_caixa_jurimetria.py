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

def parse_decision_record(reg):
    html_parts = [
        reg.get('ementa', ''),
        reg.get('dispositivo', ''),
        reg.get('txtConteudoDecisao', ''),
        reg.get('inteiroTeorHtml', ''),
        reg.get('txtConteudoDecisaoHighlight', ''),
        reg.get('txtEmentaHighlight', '')
    ]
    full_html = " ".join([h for h in html_parts if h])
    text = clean_html(full_html)
    
    num_formatado = reg.get('numFormatado', '')
    relator = (reg.get('nomRelator') or 'Não informado').title()
    data_pub = reg.get('dtaPublicacao', '')
    if 'T' in data_pub:
        data_pub = data_pub.split('T')[0]
    
    # CNJ
    cnj_match = re.search(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', num_formatado)
    cnj = cnj_match.group(1) if cnj_match else num_formatado
    
    # Classe
    classe = reg.get('codFase', '')
    if not classe:
        if num_formatado.startswith('DCG'): classe = 'DCG'
        elif num_formatado.startswith('DC'): classe = 'DC'
        elif num_formatado.startswith('ROT'): classe = 'ROT'
        elif num_formatado.startswith('RO'): classe = 'RO'
        elif num_formatado.startswith('Tut'): classe = 'TutCautAnt'
        elif num_formatado.startswith('PMPP'): classe = 'PMPP'
        else: classe = 'Dissídio Coletivo'
        
    # Check Polo Caixa
    polo_caixa = "Parte no Processo"
    if re.search(r'(suscitante|recorrente|autor|requerente)\s*:\s*[^;\n\r]*caixa\s+econ[oô]mica\s+federal', text[:3000], re.IGNORECASE):
        polo_caixa = "Suscitante / Recorrente (Autora)"
    elif re.search(r'(suscitad[oa]s?|recorrid[oa]s?|r[eé]u|requerid[oa])\s*:\s*[^;\n\r]*caixa\s+econ[oô]mica\s+federal', text[:3000], re.IGNORECASE):
        polo_caixa = "Suscitada / Recorrida (Ré)"
    elif re.search(r'recurso\s+ordin[aá]rio\s+da\s+caixa\s+econ[oô]mica\s+federal', text[:2000], re.IGNORECASE):
        polo_caixa = "Recorrente (Autora)"
    elif re.search(r'recurso\s+ordin[aá]rio\s+d[oe]\s+[^\.\n]+contra\s+(a\s+)?caixa', text[:2000], re.IGNORECASE):
        polo_caixa = "Recorrida (Ré)"

    # Identify Adversary Parties
    adversarios = []
    if re.search(r'contraf', text, re.IGNORECASE): adversarios.append('CONTRAF')
    if re.search(r'contec', text, re.IGNORECASE): adversarios.append('CONTEC')
    if re.search(r'fenae', text, re.IGNORECASE): adversarios.append('FENAE')
    sind_match = re.findall(r'sindicato\s+d[oe]s?\s+[a-zà-ú\s]{4,35}', text[:3000], re.IGNORECASE)
    for sm in sind_match[:2]:
        adversarios.append(sm.strip().title())
    if not adversarios:
        adversarios = ["Entidades Sindicais dos Bancários"]
    
    # Themes detection across full text
    temas = []
    if re.search(r'sa[uú]de\s+caixa|plano\s+de\s+sa[uú]de|assist[eê]ncia\s+m[eé]dica', text, re.IGNORECASE):
        temas.append('Saúde Caixa')
    if re.search(r'dias\s+parados|desconto.*sal[aá]ri|compensa[cç][aã]o\s+de\s+horas|greve', text, re.IGNORECASE):
        temas.append('Dias Parados & Greve')
    if re.search(r'plr|participa[cç][aã]o\s+nos\s+lucros|plr\s+social', text, re.IGNORECASE):
        temas.append('PLR & PLR Social')
    if re.search(r'7[aª]\s+e\s+8[aª]\s+hora|jornada|cargo\s+de\s+confian[cç]a|fun[cç][aã]o\s+gratificada|art\.?\s*224', text, re.IGNORECASE):
        temas.append('Jornada & 7ª/8ª Hora')
    if re.search(r'contingente|efetivo\s+m[ií]nimo|servi[cç]o\s+essencial|60%|70%|80%', text, re.IGNORECASE):
        temas.append('Contingenciamento Mínimo')
    if re.search(r'vale[\s-]?alimenta|vale[\s-]?refei|aux[ií]lio[\s-]?alimenta|cesta', text, re.IGNORECASE):
        temas.append('Auxílio Alimentação & Cesta')
    if re.search(r'reajuste|inpc|ipca|perda\s+inflacion[aá]ria|aumento\s+real', text, re.IGNORECASE):
        temas.append('Reajuste Salarial')
    if re.search(r'teletrabalho|home\s*office|trabalho\s+remoto|h[ií]brido', text, re.IGNORECASE):
        temas.append('Teletrabalho & Regime Híbrido')
    if re.search(r'piquete|interdito|turba[cç][aã]o|livre\s+acesso', text, re.IGNORECASE):
        temas.append('Piquetes & Acesso')
    if re.search(r'advogado|honor[aá]rio|advocef', text, re.IGNORECASE):
        temas.append('Advogados & Honorários da CEF')
    if re.search(r'comum\s+acordo|art\.?\s*114.*§\s*2', text, re.IGNORECASE):
        temas.append('Comum Acordo Constitucional')
    if not temas:
        temas = ['Cláusulas Gerais do ACT']

    # Outcome detection
    disp = clean_html(reg.get('dispositivo', '')).lower()
    desfecho = "Em Andamento / Despacho"
    if 'homolog' in disp or 'acordo' in disp:
        desfecho = "Acordo Homologado"
    elif 'negar-lhe provimento' in disp or 'negou-se provimento' in disp:
        desfecho = "Recurso Desprovido (Mantida Decisão Anterior)"
    elif 'dar-lhe provimento' in disp or 'deu-se provimento' in disp:
        desfecho = "Recurso Provido pelo TST"
    elif re.search(r'homolog[ao]|homologa[cç][aã]o|acordo\s+coletivo\s+homologado|autocomposi[cç][aã]o', text, re.IGNORECASE):
        desfecho = "Acordo Homologado"
    elif re.search(r'senten[cç]a\s+normativa|julgado\s+procedente|julgado\s+improcedente|fixa-se\s+a\s+cl[aá]usula', text, re.IGNORECASE):
        desfecho = "Sentença Normativa Fixada"
    elif re.search(r'defiro\s+parcialmente|defiro\s+o\s+pedido\s+liminar|concedo\s+a\s+tutela|medida\s+liminar', text, re.IGNORECASE):
        desfecho = "Liminar Deferida (Parcial ou Total)"
    elif re.search(r'indefiro\s+o\s+pedido|indefiro\s+a\s+liminar|denego', text, re.IGNORECASE):
        desfecho = "Liminar Indeferida"
    elif re.search(r'extin[cç][aã]o\s+do\s+processo|sem\s+resolu[cç][aã]o\s+de\s+m[eé]rito|falta\s+de\s+comum\s+acordo|perda\s+de\s+objeto', text, re.IGNORECASE):
        desfecho = "Extinto sem Resolução de Mérito"

    # Practical impact summary
    impacto = "Acompanhamento processual de direitos coletivos dos empregados da Caixa no TST."
    if "Acordo Homologado" in desfecho:
        impacto = "Conquista homologada: as cláusulas negociadas entre o banco e as entidades sindicais ganharam eficácia de título executivo judicial, com estabilidade garantida."
    elif "Liminar" in desfecho:
        impacto = "Medida cautelar de urgência: fixação de balizas operacionais (contingente e proteção de cláusulas) enquanto se aguarda o julgamento colegiado definitivo."
    elif "Sentença Normativa" in desfecho:
        impacto = "Decisão judicial impositiva da SDC: cláusulas criadas ou moduladas pelo Tribunal com força de lei para a categoria bancária da Caixa."
    elif "Recurso Provido" in desfecho:
        impacto = "Decisão reformada no TST: acolhimento da tese recursal com modificação do julgado regional para adequação à jurisprudência nacional."
    elif "Recurso Desprovido" in desfecho:
        impacto = "Decisão mantida: o TST rejeitou a reforma da decisão, prestigiando a jurisprudência consolidada da SDC."

    # Snippet from ementa or text
    ementa_limpa = clean_html(reg.get('ementa', ''))
    if ementa_limpa:
        snippet = ementa_limpa[:380] + "..." if len(ementa_limpa) > 380 else ementa_limpa
    else:
        snippet = text[:380] + "..." if len(text) > 380 else text

    return {
        "id": reg.get('id', ''),
        "cnj": cnj,
        "numFormatado": num_formatado,
        "classe": classe,
        "relator": relator,
        "dataPublicacao": data_pub,
        "poloCaixa": polo_caixa,
        "partesContrarias": ", ".join(list(dict.fromkeys(adversarios))[:2]),
        "desfecho": desfecho,
        "temas": temas,
        "resumoImpacto": impacto,
        "trechoDestaque": snippet,
        "linkPje": f"https://pje.tst.jus.br/consultaprocessual/detalhe-processo/{cnj.replace('-', '').replace('.', '')}"
    }

def main():
    print("Iniciando extração jurimétrica avançada de decisões da CAIXA no TST...")
    
    url_base = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
    headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    
    all_decisions = []
    seen_cnjs = set()
    
    # 1. FLAGSHIP: O PROCESSO ATUAL 2026/2028 (Decisão de 24/09/2026)
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
        "resumoImpacto": "O Min. Godinho rejeitou o pedido da Caixa de 80% e fixou contingente mínimo em 60% por agência (garantindo 40% do efetivo em greve legítima). Manteve a vigência de todas as cláusulas do ACT 2024/2026 (incluindo Saúde Caixa e vales), indeferiu a proibição de piquetes e derrubou o segredo de justiça dos autos. Prazo fatal de defesa: sábado (26/09) às 13h. Sessão de julgamento na SDC marcada para terça-feira (29/09) às 14h30.",
        "trechoDestaque": "Defiro parcialmente o pedido de liminar para determinar que sejam mantidos, em serviço, 60% dos empregados da Requerente e de suas subsidiárias... sob pena de multa diária de R$ 100.000,00. Indefiro o pleito inibitório voltado a compelir os Sindicatos Suscitados à abstenção de atos obstativos... Defiro a manutenção provisória das cláusulas normativas do ACT 2024/2026 até a decisão definitiva do presente dissídio coletivo...",
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
    
    # 2. FETCH FROM TST API FOR HISTORICAL CAIXA DECISIONS
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
        r = requests.post(f'{url_base}/1/100', json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json()
            regs = data.get('registros', [])
            print(f"Recebidos {len(regs)} registros da API do TST...")
            for item in regs:
                reg = item.get('registro', {})
                parsed = parse_decision_record(reg)
                cnj = parsed['cnj']
                if cnj not in seen_cnjs:
                    seen_cnjs.add(cnj)
                    parsed['is_flagship'] = False
                    all_decisions.append(parsed)
        else:
            print(f"API retornou status {r.status_code}")
    except Exception as e:
        print(f"Erro ao consultar API: {e}")

    # Also load from cached all_entity_records.json for completeness
    try:
        with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
            cached_data = json.load(f).get('Caixa Econômica Federal (CEF)', [])
            print(f"Verificando {len(cached_data)} registros no cache local...")
            for reg in cached_data:
                parsed = parse_decision_record(reg)
                cnj = parsed['cnj']
                if cnj not in seen_cnjs:
                    seen_cnjs.add(cnj)
                    parsed['is_flagship'] = False
                    all_decisions.append(parsed)
    except Exception as e:
        print(f"Erro ao carregar cache local: {e}")

    print(f"Total de decisões únicas da CAIXA consolidadas: {len(all_decisions)}")
    
    # Save JSON dataset in scraping directory and root directory
    out_json = 'scraping_dissidio_coletivo_greve/dados_decisoes_caixa.json'
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(all_decisions, f, ensure_ascii=False, indent=2)
    print(f"Arquivo gerado com sucesso: {out_json}")
    
    with open('dados_decisoes_caixa.json', 'w', encoding='utf-8') as f:
        json.dump(all_decisions, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
