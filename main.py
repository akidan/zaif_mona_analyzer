
#-*-coding:utf-8-*- 
import requests
import bs4

ask_url = 'https://zaif.jp/more_data/mona_jpy/asks.html'

response = requests.get(ask_url)
soup = bs4.BeautifulSoup(response.text, "html.parser")
data_list = list()
for idx, tr in enumerate(soup.find_all('tr')):
    if idx != 0:
        tds = tr.find_all('td')
        data_list.append({
            'mona_price':        float(tds[0].contents[0].strip()),
            'mona_amount':       float(tds[1].contents[0].strip()),
            'mona_price_all':    float(tds[2].contents[0].strip()),
            'mona_count_amount': float(tds[4].contents[0].strip()),
            'mona_count_all':    float(tds[5].contents[0].strip())
        })
for data_dict in data_list:
    print(data_dict['mona_price_all'])
