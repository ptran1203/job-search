
import requests


url = 'https://www.topitworks.com/vi/viec-lam/skill/java'

r = requests.get(url)

with open('zsave.html', 'w', encoding='utf-8') as f:
    f.write(r.text)

