import psycopg2
from psycopg2 import Error

def db_upsert(key, val):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect("dbname=tracey user=tracey")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO cachetest (key, value)
            VALUES (%s, %s)
            ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
        """, (key, val))

        conn.commit()
        print('### Finished upserting to db')

    except Error as e:
        print("### Error during upsert:", e)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def db_fetch(key):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect("dbname=tracey user=tracey")
        cur = conn.cursor()
        cur.execute("SELECT value FROM cachetest WHERE key = %s", (key,))
        row = cur.fetchone()
        if row is None:
            print('### Key not found in database.')
            return None
        print('res', row[0])
        print('### Finished fetching from db')
        return row[0]
    except Error as e:
        print('### Error fetching record:', e)
        return None
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()