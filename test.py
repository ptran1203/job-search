from bs4 import BeautifulSoup

text = None

with open('savee.html', 'r', encoding='utf-8') as f:
    f.read()

soup = BeautifulSoup(text, 'html.parser')

a = soup.find_all('div', ['read-more-content'])

print(a)
