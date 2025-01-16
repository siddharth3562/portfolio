from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Create SQLite database and contacts table (if it doesn't exist)
def init_db():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        return render_template('index.html', error='All fields are required')

    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)''', (name, email, message))
    conn.commit()
    conn.close()

    return render_template('index.html', success='Contact submitted successfully')

if __name__ == '__main__':
    init_db()  # Create the database and table if they don't exist
    app.run(debug=True)
