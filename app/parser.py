import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def parse_table(url, page):
    response = requests.get(f"{url}?PAGEN_1={page}")
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')
    data = []
    current_date = datetime.now().date()
    for row in rows[1:]:
        cols = row.find_all(['th', 'td'])
        cols = [col.text.strip() for col in cols]
        if len(cols) >= 7:
            start_date = datetime.strptime(cols[3], '%d-%m-%Y').date()  # Change here
            if current_date <= start_date <= current_date + timedelta(days=7):
                cols[3] = cols[3] + ' ' + cols[4]
                cols[5] = cols[5] + ' ' + cols[6]
                cols = cols[:3] + cols[3:7] + cols[7:]
                data.append(cols)
    return data
