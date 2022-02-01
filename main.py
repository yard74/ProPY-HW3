import requests
import bs4
from datetime import datetime

HEADERS = {
    'Cookie': '_ym_d=1631991263; _ym_uid=1631991263365300293; _ga=GA1.2.1304317440.1631991264; fl=ru; hl=ru; __gads=ID=be89f2dc02b17df3:T=1631991264:S=ALNI_MZGloYlJDuOe8EfuBl48VEK_9fEsg; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; habr_web_home=ARTICLES_LIST_ALL; _gid=GA1.2.670080226.1643736255; _ym_isad=1',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'If-None-Match': 'W/"3a153-SvarEJ0DFm+KAL5GB1ufNK4guhY"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.27',
    'sec-ch-ua-mobile': '?0'
    }

KEYWORDS = {'дизайн', 'фото', 'web', 'python'}

NEW_KEYWORDS = set()
for keyword in KEYWORDS:
    NEW_KEYWORDS.add(keyword.capitalize())

response = requests.get('https://habr.com/ru/all/', headers=HEADERS)
response.raise_for_status()
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')
for article in articles:
    a_title = article.find('h2')
    a_hubs = article.find_all('a', class_="tm-article-snippet__hubs-item-link")
    a_hubs = set([hub.find('span').text for hub in a_hubs])
    if NEW_KEYWORDS & a_hubs:
        a_tag = a_title.find('a')
        href = a_tag['href']
        a_url = 'https://habr.com' + href
        a_time = article.find('span', class_="tm-article-snippet__datetime-published")
        date = a_time.find('time')['title']
        d_format = '%Y-%m-%d, %H:%M'
        f_date = datetime.strptime(date, d_format)
        a_date = f_date.strftime('%d %B %Y, %H:%M')
        print(f'{a_date} - {a_title.text} - {a_url}')
