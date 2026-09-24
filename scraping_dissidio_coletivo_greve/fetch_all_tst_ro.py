import requests
import json
import time

url_base = 'https://jurisprudencia-backend.tst.jus.br/rest/pesquisa-textual'
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

payload = {
    'ou': '', 'e': '', 'termoExato': '', 'naoContem': '', 'ementa': '', 'dispositivo': '',
    'numeracaoUnica': {'numero': '', 'ano': '', 'digito': '', 'orgao': '5', 'tribunal': '', 'vara': ''},
    'orgaosJudicantes': [{'codigo': 47, 'sigla': 'SDC', 'descricao': 'Seção Especializada em Dissídios Coletivos'}],
    'ministros': [], 'convocados': [],
    'classesProcessuais': [
        {'codFase': 'RO', 'desFase': 'Recurso Ordinário'},
        {'codFase': 'ROT', 'desFase': 'Recurso Ordinário Trabalhista'}
    ],
    'codigosClassesPrecedentes': [], 'indicadores': [], 'assuntos': [],
    'tipos': ['ACORDAO', 'DESPACHO'], 'orgao': 'TST',
    'publicacaoInicial': None, 'publicacaoFinal': None,
    'julgamentoInicial': '2016-09-24',
    'julgamentoFinal': '2026-09-24',
    'ordenacao': 'data'
}

all_records = []
page_size = 50
current_offset = 1
total_expected = 1868

print("Iniciando coleta de todos os RO/ROT na SDC do TST (2016-2026)...", flush=True)

while True:
    url = f"{url_base}/{current_offset}/{page_size}"
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code != 200:
            print(f"Erro no offset {current_offset}: status {r.status_code}", flush=True)
            break
        data = r.json()
        total_expected = data.get('totalRegistros', total_expected)
        regs = data.get('registros', [])
        if not regs:
            print(f"Nenhum registro no offset {current_offset}. Fim.", flush=True)
            break
        for item in regs:
            all_records.append(item.get('registro', {}))
        print(f"Coletados {len(all_records)} / {total_expected} RO/ROT (offset={current_offset})...", flush=True)
        if len(all_records) >= total_expected:
            break
        current_offset += page_size
        time.sleep(0.4)
    except Exception as e:
        print(f"Exceção no offset {current_offset}: {e}", flush=True)
        time.sleep(2)
        continue

output_path = 'scraping_dissidio_coletivo_greve/sdc_all_ro_rot.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_records, f, ensure_ascii=False, indent=2)

print(f"Salvo com sucesso! Total de registros RO/ROT coletados: {len(all_records)} em {output_path}", flush=True)
