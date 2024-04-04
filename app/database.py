import psycopg2
from datetime import datetime

def save_to_database(data):
    DB_NAME = 'postgres'
    DB_USER = 'postgres'
    DB_PASSWORD = '1534'
    DB_HOST = 'localhost'
    DB_PORT = '5432'

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS planned_work (
            region VARCHAR,
            district VARCHAR,
            address VARCHAR,
            start_date TIMESTAMP,
            start_time TIME,  -- Изменено на TIME
            end_date TIMESTAMP,
            end_time TIME,    -- Изменено на TIME
            type_of_work VARCHAR,
            res VARCHAR,
            other VARCHAR,
            fias VARCHAR
        )
    """)

    for row in data:
        start_datetime = datetime.strptime(row[3], '%d-%m-%Y %H:%M')
        end_datetime = datetime.strptime(row[5], '%d-%m-%Y %H:%M')

        cur.execute("""
            INSERT INTO planned_work (region, district, address, start_date, start_time, end_date, end_time, type_of_work, res, other, fias)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (row[0], row[1], row[2], start_datetime.date(), start_datetime.time(), end_datetime.date(), end_datetime.time(), row[6], row[7], row[8], row[9]))

    conn.commit()
    cur.close()
    conn.close()
