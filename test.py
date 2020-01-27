import os
import psycopg2

def get_connection():
    dsn = 'postgresql://hw17a124:@localhost:5432/ukemimasterdatabase'
    return psycopg2.connect(dsn)

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute('INSERT INTO endless VALUES (%s)', ('けいしt',20000,))
        cur.execute('SELECT * FROM endless')
        rows = cur.fetchall()
        print(rows)
    