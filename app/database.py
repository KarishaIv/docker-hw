import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS urls (code TEXT PRIMARY KEY, url TEXT)")
    conn.commit()
    conn.close()

def insert_url(code, url):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO urls (code, url) VALUES (?, ?)", (code, url))
    conn.commit()
    conn.close()

def get_url_by_code(code):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT url FROM urls WHERE code = ?", (code,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
