from app import get_db_connection

conn = get_db_connection()
conn.execute('INSERT INTO news (title, content) VALUES (?, ?)', ("Berita 1", "Ini adalah konten berita 1."))
conn.execute('INSERT INTO news (title, content) VALUES (?, ?)', ("Berita 2", "Ini adalah konten berita 2."))
conn.commit()
conn.close()
