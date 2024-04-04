from datetime import datetime
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from app.parser import parse_table
from app.database import save_to_database
from app.csv_writer import write_to_csv

def main():
    url = 'https://rosseti-lenenergo.ru/planned_work/'
    page_num = 1
    table_data = []
    while True:
        data = parse_table(url, page_num)
        if not data:
            break
        table_data.extend(data)
        if datetime.strptime(data[0][3], '%d-%m-%Y %H:%M').date() < datetime.now().date():
            break
        page_num += 1

    save_to_database(table_data)
    write_to_csv(table_data, 'table_data.csv')

    conn = psycopg2.connect(dbname='postgres', user='postgres', password='1534', host='localhost', port='5432')
    query = "SELECT * FROM planned_work"
    df = pd.read_sql(query, conn)
    conn.close()

    plt.figure(figsize=(10, 6))
    sns.countplot(x='type_of_work', data=df)
    plt.title('Distribution of Types of Work')
    plt.xlabel('Type of Work')
    plt.ylabel('Count')
    plt.xticks(rotation=15)
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.countplot(x='region', data=df, order=df['region'].value_counts().index)
    plt.title('Number of Works by Region')
    plt.xlabel('Region')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.show()

if __name__ == "__main__":
    main()
