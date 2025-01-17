from flask import Flask, render_template, request, jsonify, flash
import sqlite3
from contextlib import closing

app = Flask(__name__)
# Add a secret key for flash messages
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key

# Database helper function
def get_db_connection():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create SQLite database and contacts table
def init_db():
    try:
        with get_db_connection() as conn:
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
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Validate form data
        if not all([name, email, message]):
            flash('All fields are required', 'error')
            return render_template('index.html')

        # Use context manager for database connection
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)',
                (name, email, message)
            )
            conn.commit()

        flash('Message sent successfully!', 'success')
        return render_template('index.html')

    except sqlite3.Error as e:
        flash(f'An error occurred while saving your message. Please try again.', 'error')
        print(f"Database error: {e}")
        return render_template('index.html')
    except Exception as e:
        flash('An unexpected error occurred. Please try again.', 'error')
        print(f"Unexpected error: {e}")
        return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)