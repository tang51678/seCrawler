import sqlite3

def create_table():
    conn = sqlite3.connect('urls.sqlite3')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
