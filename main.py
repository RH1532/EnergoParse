from app.parser import parse_table
from app.database import save_to_database
from app.csv_writer import write_to_csv


def main():
    url = 'https://rosseti-lenenergo.ru/planned_work/'
    table_data = parse_table(url)
    save_to_database(table_data)
    write_to_csv(table_data, 'table_data.csv')

if __name__ == "__main__":
    main()