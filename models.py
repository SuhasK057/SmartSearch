import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

if os.environ.get('VERCEL'):
    # In Vercel serverless environment, filesystem is read-only except /tmp
    DB_PATH = '/tmp/smartsearch.db'
    bundled_db = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'smartsearch.db')
    if not os.path.exists(DB_PATH) and os.path.exists(bundled_db):
        import shutil
        try:
            shutil.copyfile(bundled_db, DB_PATH)
        except Exception as e:
            print(f"[models] Could not copy seed db to /tmp: {e}")
else:
    DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'smartsearch.db')


def get_db():
    """Open a database connection with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Create all tables if they don't exist yet.
    Safely adds new columns to existing tables using ALTER TABLE.
    Safe to call every time the app starts.
    """
    conn = get_db()
    try:
        c = conn.cursor()

        # Users table — holds auth credentials + full profile
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                email               TEXT    UNIQUE NOT NULL,
                password_hash       TEXT    NOT NULL,
                first_name          TEXT    DEFAULT '',
                last_name           TEXT    DEFAULT '',
                middle_name         TEXT    DEFAULT '',
                phone               TEXT    DEFAULT '',
                age                 TEXT    DEFAULT '',
                gender              TEXT    DEFAULT '',
                education           TEXT    DEFAULT '',
                profession          TEXT    DEFAULT '',
                location            TEXT    DEFAULT '',
                occupation          TEXT    DEFAULT '',
                is_profile_complete BOOLEAN DEFAULT 0,
                created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # --- Safe ALTER TABLE: add new columns to existing databases ---
        new_columns = [
            ("occupation",          "TEXT    DEFAULT ''"),
            ("is_profile_complete", "BOOLEAN DEFAULT 0"),
        ]
        for col_name, col_def in new_columns:
            try:
                c.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}")
            except sqlite3.OperationalError:
                # Column already exists — safe to ignore
                pass

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

        # Likes persistence table
        c.execute('''
            CREATE TABLE IF NOT EXISTS liked_results (
                user_id    INTEGER NOT NULL,
                link       TEXT NOT NULL,
                liked_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, link),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------

def create_user(email, password):
    """
    Insert a new user row.
    Returns the new user's id, or None if the email already exists.
    Passwords are stored as a bcrypt hash — never plain-text.
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
    Uses constant-time comparison via check_password_hash.
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
    try:
        row = conn.execute(
            'SELECT * FROM users WHERE email = ?', (email.lower().strip(),)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_user_by_id(user_id):
    conn = get_db()
    try:
        row = conn.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


# ---------------------------------------------------------------
# Profile update (full profile — existing /profile/update route)
# ---------------------------------------------------------------

def update_profile(user_id, data):
    """
    Update all profile fields for a user.
    `data` is the JSON dict sent from the frontend saveProfile() call.
    Raises sqlite3.IntegrityError if email already exists.
    """
    conn = get_db()
    try:
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
                   location    = ?,
                   occupation  = ?
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
                data.get('occupation', ''),
                user_id
            )
        )
        conn.commit()
    finally:
        conn.close()


def complete_onboarding(user_id, occupation, age):
    """
    Set occupation, age, and mark is_profile_complete = 1.
    Called from the onboarding POST /profile route.
    """
    conn = get_db()
    try:
        conn.execute(
            '''UPDATE users SET
                   occupation          = ?,
                   age                 = ?,
                   is_profile_complete = 1
               WHERE id = ?''',
            (occupation.strip(), str(age).strip(), user_id)
        )
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------
# Saved results
# ---------------------------------------------------------------

def save_result(user_id, title, link, snippet, source):
    conn = get_db()
    try:
        conn.execute(
            '''INSERT INTO saved_results (user_id, title, link, snippet, source)
               VALUES (?, ?, ?, ?, ?)''',
            (user_id, title, link, snippet, source)
        )
        conn.commit()
    finally:
        conn.close()

def remove_saved_result(user_id, link):
    conn = get_db()
    try:
        conn.execute(
            'DELETE FROM saved_results WHERE user_id = ? AND link = ?',
            (user_id, link)
        )
        conn.commit()
    finally:
        conn.close()

def is_result_saved(user_id, link):
    conn = get_db()
    try:
        row = conn.execute(
            'SELECT 1 FROM saved_results WHERE user_id = ? AND link = ?',
            (user_id, link)
        ).fetchone()
        return bool(row)
    finally:
        conn.close()

def get_saved_results(user_id):
    conn = get_db()
    try:
        results = conn.execute(
            'SELECT * FROM saved_results WHERE user_id = ? ORDER BY saved_at DESC',
            (user_id,)
        ).fetchall()
        return [dict(row) for row in results]
    finally:
        conn.close()

# ---------------------------------------------------------------
# Liked results
# ---------------------------------------------------------------

def like_result(user_id, link):
    conn = get_db()
    try:
        conn.execute(
            'INSERT OR IGNORE INTO liked_results (user_id, link) VALUES (?, ?)',
            (user_id, link)
        )
        conn.commit()
    finally:
        conn.close()

def unlike_result(user_id, link):
    conn = get_db()
    try:
        conn.execute(
            'DELETE FROM liked_results WHERE user_id = ? AND link = ?',
            (user_id, link)
        )
        conn.commit()
    finally:
        conn.close()

def get_liked_links(user_id):
    conn = get_db()
    try:
        results = conn.execute(
            'SELECT link FROM liked_results WHERE user_id = ?',
            (user_id,)
        ).fetchall()
        return [row['link'] for row in results]
    finally:
        conn.close()

def get_like_count(link):
    """Return total number of likes for a specific link."""
    conn = get_db()
    try:
        row = conn.execute(
            'SELECT COUNT(*) as cnt FROM liked_results WHERE link = ?',
            (link,)
        ).fetchone()
        return row['cnt'] if row else 0
    finally:
        conn.close()

def get_all_like_counts():
    """Return a mapping of link -> total like count."""
    conn = get_db()
    try:
        rows = conn.execute(
            'SELECT link, COUNT(*) as cnt FROM liked_results GROUP BY link'
        ).fetchall()
        return {row['link']: row['cnt'] for row in rows}
    finally:
        conn.close()

def get_save_count(link):
    """Return total number of saves for a specific link."""
    conn = get_db()
    try:
        row = conn.execute(
            'SELECT COUNT(*) as cnt FROM saved_results WHERE link = ?',
            (link,)
        ).fetchone()
        return row['cnt'] if row else 0
    finally:
        conn.close()

def get_all_save_counts():
    """Return a mapping of link -> total save count."""
    conn = get_db()
    try:
        rows = conn.execute(
            'SELECT link, COUNT(*) as cnt FROM saved_results GROUP BY link'
        ).fetchall()
        return {row['link']: row['cnt'] for row in rows}
    finally:
        conn.close()

def get_user_saved_links(user_id):
    """Return list of links saved by this user."""
    conn = get_db()
    try:
        rows = conn.execute(
            'SELECT link FROM saved_results WHERE user_id = ?',
            (user_id,)
        ).fetchall()
        return [row['link'] for row in rows]
    finally:
        conn.close()