import requests
import re

text = requests.get('https://jurisprudencia.tst.jus.br/static/js/main.f0922844.js', timeout=20).text

# Look for fetch or axios
fetches = re.findall(r'fetch\([^\)]+\)', text)
print("Fetches found:", len(fetches), fetches[:5])

# Look for URL patterns or paths
urls = re.findall(r'https?://[^\s\'"`,;)]+', text)
print("URLs found:", len(urls), set(urls))

# Look for strings containing "/api" or "/rest" or "/jurisprudencia"
strings = re.findall(r'["\'](/[^"\']+)["\']', text)
print("Total string paths:", len(strings))
filtered = [s for s in set(strings) if any(x in s for x in ['api', 'rest', 'servico', 'search', 'consulta', 'backend', 'tst'])]
print("Filtered paths:", filtered)
