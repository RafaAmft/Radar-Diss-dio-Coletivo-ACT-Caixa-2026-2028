import requests
import re
import json

def inspect_tst_js():
    url = "https://jurisprudencia.tst.jus.br/static/js/main.f0922844.js"
    res = requests.get(url, timeout=20)
    print("Downloaded JS, size:", len(res.text))
    matches = set(re.findall(r'["\'](/[a-zA-Z0-9_\-\./]+)["\']', res.text))
    api_candidates = [m for m in matches if any(k in m.lower() for k in ['rest', 'api', 'juris', 'pesquis', 'buscar', 'acordao', 'sdc', 'processo'])]
    print("Candidates:", api_candidates)

if __name__ == "__main__":
    inspect_tst_js()
