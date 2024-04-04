from fastapi import FastAPI, HTTPException
from datetime import date
import psycopg2


app = FastAPI()


def connect_to_db():
    return psycopg2.connect(dbname='postgres',
                            user='postgres',
                            password='1534',
                            host='localhost',
                            port='5432')


def get_today_works():
    conn = connect_to_db()
    cur = conn.cursor()
    today = date.today()
    cur.execute('SELECT * FROM planned_work WHERE start_date <= %s AND end_date >= %s', (today, today))
    works = cur.fetchall()
    cur.close()
    conn.close()
    return works


def get_works_in_region(region: str):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM planned_work WHERE region = %s', (region,))
    works = cur.fetchall()
    cur.close()
    conn.close()
    return works


@app.get('/works/today')
def read_today_works():
    works = get_today_works()
    if not works:
        raise HTTPException(status_code=404, detail='No works scheduled for today')
    return {'works': works}


@app.get('/works/region')
def read_works_in_region(region: str):
    works = get_works_in_region(region)
    if not works:
        raise HTTPException(status_code=404, detail=f'No works found in region: {region}')
    return {'works': works}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
