import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://jurisprudencia.tst.jus.br/', timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')
for tag in soup.find_all(['script', 'link']):
    src = tag.get('src') or tag.get('href')
    print(tag.name, src)

# Also check for inline scripts
for s in soup.find_all('script'):
    if s.string:
        print("Inline script:", s.string[:200])
