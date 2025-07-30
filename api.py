import psycopg2

def upsert(key, val):
    conn = psycopg2.connect("dbname=tracey user=tracey")

    cur = conn.cursor()

    cur.execute("INSERT INTO cachetest (key, value) VALUES (%s, %s)",
                 (key, val))

    conn.commit()

    cur.close()
    conn.close()
    print('### finished upserting to db')
    return 0


def fetch(key):
    conn = psycopg2.connect("dbname=tracey user=tracey")

    cur = conn.cursor()

    cur.execute("SELECT value FROM cachetest WHERE key=%s", (key,))
    res = cur.fetchone()[0]
    print('res', res)

    conn.commit()
    
    cur.close()
    conn.close()
    print('### finished fetching from db')
    return res