from fastapi import FastAPI, HTTPException
from datetime import datetime, date
import psycopg2


app = FastAPI()


def get_today_works():
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='1534', host='localhost', port='5432')
    cur = conn.cursor()
    today = date.today()
    cur.execute('SELECT * FROM planned_work WHERE start_date <= %s AND end_date >= %s', (today, today))
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
