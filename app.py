from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Fungsi untuk mendapatkan koneksi database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row  # Memungkinkan penggunaan nama kolom sebagai dictionary
    return conn

@app.route('/')
def dashboard():
    conn = get_db_connection()
    news_items = conn.execute('SELECT * FROM news').fetchall()
    conn.close()
    return render_template('dashboard.html', news_items=news_items)

@app.route('/news/<int:news_id>', methods=['GET', 'POST'])
def news_detail(news_id):
    conn = get_db_connection()

    if request.method == 'POST':
        content = request.form.get('content')
        flag = request.form.get('rahasia_data')
        conn.execute('INSERT INTO comments (news_id, content) VALUES (?, ?)', (news_id, content))
        conn.commit()
        if flag:  # Jika ada data flag
            return redirect('/flag')  # Redirect ke halaman flag
        return redirect(f'/news/{news_id}')

    news_item = conn.execute('SELECT * FROM news WHERE id = ?', (news_id,)).fetchone()
    comments = conn.execute('SELECT * FROM comments WHERE news_id = ?', (news_id,)).fetchall()
    conn.close()

    if news_item is None:
        return 'Berita tidak ditemukan!', 404

    return render_template('comments.html', news_item=news_item, comments=comments)

@app.route('/flag', methods=['GET', 'POST'])
def flag():
    if request.method == 'POST':
        # Handle any flag-related submission here if necessary
        # For example, you could process data or save to a database
        flag_data = request.form.get('flag_data')
        # Process the flag_data as needed
        return redirect('/')

    # If it's a GET request, you can display the flag information
    return render_template('flag.html')  # Create a flag.html template for this

if __name__ == '__main__':
    app.run(host='172.16.100.56', port=5000, debug=True)
