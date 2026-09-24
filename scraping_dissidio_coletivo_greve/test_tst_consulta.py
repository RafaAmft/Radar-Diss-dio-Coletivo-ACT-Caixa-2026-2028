import requests
import re
from bs4 import BeautifulSoup

url = 'https://consultaprocessual.tst.jus.br/consultaProcessual/consultaTstNumUnica.do'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
print('Status:', r.status_code)
soup = BeautifulSoup(r.text, 'html.parser')
for form in soup.find_all('form'):
    print('Form action:', form.get('action'))
    for inp in form.find_all(['input', 'select']):
        print('  ', inp.get('name'), inp.get('type'), inp.get('value'))
