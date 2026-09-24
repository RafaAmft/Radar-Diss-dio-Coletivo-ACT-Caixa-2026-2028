import requests
import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

def clean_html(text):
    if not text:
        return ""
    if "<" in text and ">" in text:
        return BeautifulSoup(text, 'html.parser').get_text(separator=' ')
    return text

def monitor_caixa_dissidio():
    """
    Rastreia despachos, acórdãos e movimentações recentes de dissídios coletivos
    envolvendo a Caixa Econômica Federal no TST.
    """
    url_base = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
    headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

    queries = [
        'Caixa Econômica Federal dissídio',
        'Caputo Bastos Caixa',
        'Contraf Caixa dissídio',
        '1000422-59.2025'
    ]

    found_movements = []
    seen_ids = set()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando varredura diária no TST...", flush=True)

    for q in queries:
        payload = {
            'ou': '', 'e': q, 'termoExato': '', 'naoContem': '', 'ementa': '', 'dispositivo': '',
            'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
            'orgaosJudicantes': [],
            'ministros': [], 'convocados': [],
            'classesProcessuais': [],
            'codigosClassesPrecedentes': [], 'indicadores': [], 'assuntos': [],
            'tipos': ['DESPACHO', 'ACORDAO'], 'orgao': 'TST',
            'publicacaoInicial': None, 'publicacaoFinal': None,
            'julgamentoInicial': None, 'julgamentoFinal': None,
            'ordenacao': 'data'
        }

        try:
            r = requests.post(f"{url_base}/1/15", json=payload, headers=headers, timeout=25)
            if r.status_code == 200:
                data = r.json()
                for reg in data.get('registros', []):
                    rec = reg.get('registro', {})
                    num = rec.get('numFormatado') or rec.get('id')
                    txt = clean_html(rec.get('txtConteudoDecisao') or rec.get('ementa') or '')
                    
                    # Filtra apenas se for relevante para a Caixa e conflito coletivo
                    if num and num not in seen_ids and any(k in txt.lower() for k in ['caixa econômica', 'cef', 'contraf', 'dissídio', 'acordo coletivo']):
                        seen_ids.add(num)
                        found_movements.append({
                            'numero': num,
                            'tipo': rec.get('tipo', {}).get('nome') if isinstance(rec.get('tipo'), dict) else str(rec.get('tipo', '')),
                            'orgao': rec.get('orgaoJudicante', {}).get('descricao', ''),
                            'relator': rec.get('nomRelator', ''),
                            'data_publicacao': rec.get('dtaPublicacao', ''),
                            'data_julgamento': rec.get('dtaJulgamento', ''),
                            'resumo': txt[:350].strip() + '...' if len(txt) > 350 else txt
                        })
        except Exception as e:
            print(f"Erro na query [{q}]: {e}")

    # Salva histórico de monitoramento
    log_file = 'monitoramento_diario_caixa.json'
    historico = {
        'ultima_execucao': datetime.now().isoformat(),
        'total_registros_relevantes': len(found_movements),
        'registros': found_movements
    }

    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

    print(f"Varredura concluída. {len(found_movements)} movimentações/decisões catalogadas em {log_file}.")
    return historico

if __name__ == '__main__':
    monitor_caixa_dissidio()
