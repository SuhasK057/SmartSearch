import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = 'smartsearch.db'


def get_db():
    """Open a database connection with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Create all tables if they don't exist yet.
    Safe to call every time the app starts.
    """
    conn = get_db()
    c = conn.cursor()

    # Users table — holds auth credentials + full profile
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            first_name    TEXT    DEFAULT '',
            last_name     TEXT    DEFAULT '',
            middle_name   TEXT    DEFAULT '',
            phone         TEXT    DEFAULT '',
            age           TEXT    DEFAULT '',
            gender        TEXT    DEFAULT '',
            education     TEXT    DEFAULT '',
            profession    TEXT    DEFAULT '',
            location      TEXT    DEFAULT '',
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Saved search results
    c.execute('''
        CREATE TABLE IF NOT EXISTS saved_results (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            title      TEXT,
            link       TEXT,
            snippet    TEXT,
            source     TEXT,
            saved_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()


# ---------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------

def create_user(email, password):
    """
    Insert a new user row.
    Returns the new user's id, or None if the email already exists.
    """
    conn = get_db()
    try:
        c = conn.cursor()
        c.execute(
            'INSERT INTO users (email, password_hash) VALUES (?, ?)',
            (email.lower().strip(), generate_password_hash(password))
        )
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        return None          # duplicate email
    finally:
        conn.close()


def verify_user(email, password):
    """
    Check email + password.
    Returns the user dict on success, None on failure.
    """
    user = get_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None


# ---------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------

def get_user_by_email(email):
    conn = get_db()
    row = conn.execute(
        'SELECT * FROM users WHERE email = ?', (email.lower().strip(),)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    conn = get_db()
    row = conn.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ---------------------------------------------------------------
# Profile update
# ---------------------------------------------------------------

def update_profile(user_id, data):
    """
    Update all profile fields for a user.
    `data` is the JSON dict sent from the frontend saveProfile() call.
    """
    conn = get_db()
    conn.execute(
        '''UPDATE users SET
               first_name  = ?,
               last_name   = ?,
               middle_name = ?,
               email       = ?,
               phone       = ?,
               age         = ?,
               gender      = ?,
               education   = ?,
               profession  = ?,
               location    = ?
           WHERE id = ?''',
        (
            data.get('firstName', ''),
            data.get('lastName', ''),
            data.get('middleName', ''),
            data.get('email', '').lower().strip(),
            data.get('phone', ''),
            data.get('age', ''),
            data.get('gender', ''),
            data.get('education', ''),
            data.get('profession', ''),
            data.get('location', ''),
            user_id
        )
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------
# Saved results
# ---------------------------------------------------------------

def save_result(user_id, title, link, snippet, source):
    conn = get_db()
    conn.execute(
        '''INSERT INTO saved_results (user_id, title, link, snippet, source)
           VALUES (?, ?, ?, ?, ?)''',
        (user_id, title, link, snippet, source)
    )
    conn.commit()
    conn.close()