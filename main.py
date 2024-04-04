from datetime import datetime
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

if __name__ == "__main__":
    main()
