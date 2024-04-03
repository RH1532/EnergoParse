import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import pandas as pd


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


def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def filter_by_current_week(data):
    current_date = datetime.now().date()
    filtered_data = []
    for row in data:
        start_date = datetime.strptime(row[3], '%d-%m-%Y %H:%M').date()
        if current_date <= start_date <= current_date + timedelta(days=7):
            filtered_data.append(row)
    return filtered_data


base_url = 'https://rosseti-lenenergo.ru/planned_work/?PAGEN_1='
csv_filename = 'table_data.csv'


all_data = []
page_num = 1
while True:
    url = base_url + str(page_num)
    table_data = parse_table(url)
    if not table_data:
        break
    all_data.extend(table_data)
    if datetime.strptime(table_data[0][3], '%d-%m-%Y %H:%M').date() < datetime.now().date():
        break
    page_num += 1

filtered_data = filter_by_current_week(all_data)


column_names = [
    'Регион РФ (область, край, город фед. значения, округ)',
    'Административный район / Населённый пункт',
    'Адрес',
    'Дата начала',
    'Время начала',
    'Дата окончания',
    'Время окончания',
    'Филиал',
    'РЭС',
    'Комментарий',
    'ФИАС'
]


df = pd.DataFrame(filtered_data, columns=column_names)
df.to_csv(csv_filename, index=False)
