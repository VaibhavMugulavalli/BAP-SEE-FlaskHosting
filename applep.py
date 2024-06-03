from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages and session management

DATABASE = 'users.db'

app.config['SESSION_PERMANENT'] = False  # Ensure the session cookie expires when the browser closes

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print('Database initialized!')

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')  # This renders your existing index.html

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                            (username, password)).fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            session.permanent = False  # Ensure the session cookie expires when the browser closes
            flash('Login successful!', 'success')
            return render_template('index.html')  # Redirect to the home page after successful login
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already taken. Please choose another one.', 'danger')
        finally:
            conn.close()
            
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/assets/<path:filename>')
def custom_static(filename):
    return send_from_directory('assets', filename)


@app.after_request
def after_request(response):
    session.pop('username', None)
    return response

if __name__ == "__main__":
    init_db()
    app.run(debug=True)