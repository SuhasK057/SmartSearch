"""
app.py  —  SmartSearch / NewsSphere Flask application.

Routes:
    GET  /              → redirect to /login (or /domain if already logged in)
    GET  /login         → login page
    POST /login         → JSON auth endpoint
    GET  /register      → register page
    POST /register      → JSON register endpoint
    GET  /logout        → clear session → redirect to /login
    GET  /profile       → profile page (login required)
    POST /profile/update→ save profile data (login required, returns JSON)
    GET  /domain        → domain selection page (login required)
    GET  /index         → search feed (login required)
    POST /save          → save a search result (login required, returns JSON)
"""

import os
from functools import wraps

from flask import (Flask, render_template, request,
                   redirect, url_for, session, jsonify)

from models  import (init_db, create_user, verify_user,
                     get_user_by_id, update_profile, save_result)
from search  import google_search, job_search

# ---------------------------------------------------------------
# Config — load from config.py, fall back to environment variables
# ---------------------------------------------------------------
try:
    from config import GOOGLE_API_KEY, GOOGLE_CX, JSEARCH_API_KEY, JSEARCH_HOST, SECRET_KEY
except ImportError:
    GOOGLE_API_KEY  = os.environ.get('GOOGLE_API_KEY', '')
    GOOGLE_CX       = os.environ.get('GOOGLE_CX', '')
    JSEARCH_API_KEY = os.environ.get('JSEARCH_API_KEY', '')
    JSEARCH_HOST    = os.environ.get('JSEARCH_HOST', 'jsearch.p.rapidapi.com')
    SECRET_KEY      = os.environ.get('SECRET_KEY', 'dev-secret-fallback')

# ---------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------
app            = Flask(__name__)
app.secret_key = SECRET_KEY

# ---------------------------------------------------------------
# Domain mapping: frontend domain slug → TRUSTED_SITES key + default query
# ---------------------------------------------------------------
DOMAIN_KEY_MAP = {
    'student':            'student',
    'job_seeker':         'job_seeker',
    'general_reader':     'news',
    'investor':           'stock_market',
    'engineer':           'engineering',
    'freelancer':         'freelancing',
    'esports_fan':        'esports',
    'internship_seeker':  'internships',
}

DEFAULT_QUERIES = {
    'student':            'latest student education scholarships news India',
    'job_seeker':         'latest job openings hiring career news',
    'general_reader':     'top news headlines today',
    'investor':           'stock market updates finance news today',
    'engineer':           'engineering technology innovation news',
    'freelancer':         'freelancing remote work opportunities tips',
    'esports_fan':        'esports gaming tournaments results news',
    'internship_seeker':  'internship opportunities for students India 2025',
}

# ---------------------------------------------------------------
# Login-required decorator
# ---------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ===============================================================
# ROUTES
# ===============================================================

# ---- Root redirect ----
@app.route('/')
def root():
    if 'user_id' in session:
        return redirect(url_for('domain'))
    return redirect(url_for('login'))


# ---------------------------------------------------------------
# Auth — Login
# ---------------------------------------------------------------
@app.route('/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect(url_for('domain'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request.'}), 400

    email    = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required.'})

    user = verify_user(email, password)
    if user:
        session['user_id'] = user['id']
        session['email']   = user['email']
        return jsonify({'success': True, 'redirect': url_for('profile')})

    return jsonify({'success': False, 'message': 'Invalid email or password. Please try again.'})


# ---------------------------------------------------------------
# Auth — Register
# ---------------------------------------------------------------
@app.route('/register', methods=['GET'])
def register():
    if 'user_id' in session:
        return redirect(url_for('domain'))
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request.'}), 400

    email    = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required.'})

    user_id = create_user(email, password)
    if user_id:
        session['user_id'] = user_id
        session['email']   = email.lower()
        return jsonify({'success': True, 'redirect': url_for('profile')})

    return jsonify({'success': False, 'message': 'An account with this email already exists.'})


# ---------------------------------------------------------------
# Auth — Logout
# ---------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------------------------------------------------------
# Profile
# ---------------------------------------------------------------
@app.route('/profile')
@login_required
def profile():
    user = get_user_by_id(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
    return render_template('profile.html', user=user)


@app.route('/profile/update', methods=['POST'])
@login_required
def profile_update():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request.'}), 400

    # Server-side validation
    if not data.get('firstName', '').strip():
        return jsonify({'success': False, 'message': 'First name is required.'})
    if not data.get('email', '').strip():
        return jsonify({'success': False, 'message': 'Email is required.'})
    if not data.get('phone', '').strip():
        return jsonify({'success': False, 'message': 'Phone number is required.'})

    update_profile(session['user_id'], data)
    session['email'] = data.get('email', session.get('email', '')).lower()

    # Return the saved values so the frontend can update its display
    user = get_user_by_id(session['user_id'])
    return jsonify({
        'success': True,
        'user': {
            'firstName':  user.get('first_name', ''),
            'lastName':   user.get('last_name', ''),
            'middleName': user.get('middle_name', ''),
            'email':      user.get('email', ''),
            'phone':      user.get('phone', ''),
            'age':        user.get('age', ''),
            'gender':     user.get('gender', ''),
            'education':  user.get('education', ''),
            'profession': user.get('profession', ''),
            'location':   user.get('location', ''),
        }
    })


# ---------------------------------------------------------------
# Domain selection
# ---------------------------------------------------------------
@app.route('/domain')
@login_required
def domain():
    return render_template('domain.html')


# ---------------------------------------------------------------
# Search feed
# ---------------------------------------------------------------
@app.route('/index')
@login_required
def index():
    domain_param = request.args.get('domain', 'student')
    query        = request.args.get('q', '').strip()

    # Guard against unknown domain slugs
    if domain_param not in DOMAIN_KEY_MAP:
        domain_param = 'student'

    trusted_key = DOMAIN_KEY_MAP[domain_param]

    # Use domain-specific default query if user hasn't typed anything
    if not query:
        query = DEFAULT_QUERIES.get(domain_param, 'latest news')

    results   = []
    error_msg = None

    if not GOOGLE_API_KEY or GOOGLE_API_KEY == 'YOUR_GOOGLE_API_KEY_HERE':
        error_msg = (
            'Google API key is not configured. '
            'Please add your key to config.py.'
        )
    else:
        try:
            results = google_search(query, trusted_key, GOOGLE_API_KEY, GOOGLE_CX)
            if not results:
                error_msg = (
                    'No results found. Your Google Custom Search API daily quota '
                    'may be exhausted (100 free queries/day), or the query returned '
                    'no matches from the trusted sites.'
                )
        except ValueError as e:
            error_msg = str(e)
        except Exception as e:
            error_msg = 'Search is temporarily unavailable. Please try again later.'
            print(f'[index] Unexpected search error: {e}')

    return render_template(
        'index.html',
        results=results,
        selected_domain=domain_param,
        query=query,
        error_msg=error_msg,
    )


# ---------------------------------------------------------------
# Save a result
# ---------------------------------------------------------------
@app.route('/save', methods=['POST'])
@login_required
def save():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False}), 400

    save_result(
        user_id=session['user_id'],
        title=data.get('title', ''),
        link=data.get('link', ''),
        snippet=data.get('snippet', ''),
        source=data.get('source', ''),
    )
    return jsonify({'success': True})


# ===============================================================
# Entry point
# ===============================================================
if __name__ == '__main__':
    init_db()          # create tables on first run
    app.run(debug=True)