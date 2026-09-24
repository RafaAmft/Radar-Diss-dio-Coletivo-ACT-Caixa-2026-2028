import json
import re
from bs4 import BeautifulSoup

with open('scraping_dissidio_coletivo_greve/all_entity_records.json', 'r', encoding='utf-8') as f:
    all_entity_data = json.load(f)

with open('scraping_dissidio_coletivo_greve/sdc_all_dc_dcg.json', 'r', encoding='utf-8') as f:
    sdc_dc_dcg = json.load(f)

cases = {}
def add_case(r):
    num = r.get('numFormatado') or r.get('numero')
    if not num:
        return
    cnj_match = re.search(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', str(num))
    if cnj_match:
        cnj = cnj_match.group(1)
    else:
        nu = r.get('numeracaoUnica')
        if isinstance(nu, dict) and nu.get('numero'):
            cnj = f"{nu['numero']:07d}-{nu['digito']:02d}.{nu['ano']}.{nu['orgao']}.{nu['tribunal']:02d}.{nu['vara']:04d}"
        else:
            return
    if cnj not in cases:
        cases[cnj] = []
    cases[cnj].append(r)

for ent, recs in all_entity_data.items():
    for r in recs:
        add_case(r)

for r in sdc_dc_dcg:
    add_case(r)

print(f"Total CNJ: {len(cases)}")

# Test on 20 cases with empty ementa
tested = 0
for cnj, rec_list in cases.items():
    for r in rec_list:
        txt = r.get('txtConteudoDecisao') or r.get('txtConteudoDecisaoHighlight') or r.get('inteiroTeorHtml') or ''
        clean_html = re.sub(r'<img[^>]*>', '', txt)
        soup = BeautifulSoup(clean_html[:5000], 'html.parser')
        text = soup.get_text()
        
        m_susc = re.search(r'SUSCITANTE\s*:\s*([^\n\r]+?)(?:SUSCITAD[AO]|REQUERID[AO]|\n|\r)', text, re.I)
        m_suscd = re.search(r'SUSCITAD[AO][S]?\s*:\s*([^\n\r]+?)(?:DESPACHO|AC[OÓ]RD[AÃ]O|RELAT[OÓ]RIO|\n|\r)', text, re.I)
        
        if m_susc and m_suscd:
            print(f"CNJ: {cnj} -> Suscitante: {m_susc.group(1).strip()[:60]} | Suscitado: {m_suscd.group(1).strip()[:60]}")
            tested += 1
            break
    if tested >= 15:
        break
