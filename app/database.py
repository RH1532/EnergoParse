import psycopg2

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
            end_date TIMESTAMP,
            type_of_work VARCHAR,
            res VARCHAR,
            other VARCHAR
        )
    """)

    for row in data:
        cur.execute("""
            INSERT INTO planned_work (region, district, address, start_date, end_date, type_of_work, res, other)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (row[0], row[1], row[2], row[3], row[5], row[6], row[7], row[8]))

    conn.commit()
    cur.close()
    conn.close()
