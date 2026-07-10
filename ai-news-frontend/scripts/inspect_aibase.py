import requests
from bs4 import BeautifulSoup

url = 'https://news.aibase.com/zh/news'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
resp = requests.get(url, headers=headers, timeout=20)
print('status', resp.status_code)
print('len', len(resp.text))

soup = BeautifulSoup(resp.text, 'html.parser')
# Find first few article links and print their structure
links = soup.select('a[href*="/zh/news/"]')
print('total links', len(links))
for i, a in enumerate(links[:5]):
    print(f'\n--- link {i} ---')
    print('href:', a.get('href'))
    print('text:', a.get_text(strip=True)[:200])
    print('html:', str(a)[:500])
