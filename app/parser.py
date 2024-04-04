# parser.py
import requests
from bs4 import BeautifulSoup

def parse_table(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all(['th', 'td'])
        cols = [col.text.strip() for col in cols]
        if len(cols) >= 7:
            cols[3] = cols[3] + ' ' + cols[4]
            cols[5] = cols[5] + ' ' + cols[6]
            cols = cols[:3] + cols[3:7] + cols[7:]
            data.append(cols)
    return data
