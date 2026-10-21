"""
app.py  —  SmartSearch / NewsSphere Flask application.

Routes:
    GET  /              → redirect to /login (or /domain if already logged in)
    GET  /login         → login page
    POST /login         → JSON auth endpoint
    GET  /register      → register page
    POST /register      → JSON register endpoint
    GET  /logout        → clear session → redirect to /login
    GET  /profile       → profile / onboarding page (login required)
    POST /profile       → save onboarding data (login required)
    POST /profile/update→ full profile update (login required, returns JSON)
    GET  /domain        → domain selection page (login required)
    GET  /index         → search feed (login required, profile-complete required)
    POST /save          → save a search result (login required, returns JSON)
    POST /unsave        → remove a saved result (login required, returns JSON)
    POST /like          → like an article (login required, returns JSON)
    POST /unlike        → unlike an article (login required, returns JSON)
    GET  /liked_links   → return user's liked links as JSON (login required)
    GET  /saved         → saved articles feed (login required)
"""

# ── Easter Egg ────────────────────────────────────────────────────────────────
try:
    import antigravity          # noqa: F401  🚀 anti-gravity mode engaged
except ImportError:
    pass                        # not installed in production — silent skip
# ─────────────────────────────────────────────────────────────────────────────

import os
import re
import time
import logging
from functools import wraps

from flask import (Flask, render_template, request,
                   redirect, url_for, session, jsonify, flash)

from models  import (init_db, create_user, verify_user,
                     get_user_by_id, update_profile,
                     complete_onboarding,
                     save_result, get_saved_results, is_result_saved)
from search  import google_search, job_search

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

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

# Environment variables take precedence over config placeholders
GOOGLE_API_KEY  = os.environ.get('GOOGLE_API_KEY') or GOOGLE_API_KEY
if GOOGLE_API_KEY == 'YOUR_GOOGLE_API_KEY_HERE':
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')

GOOGLE_CX       = os.environ.get('GOOGLE_CX') or GOOGLE_CX
if GOOGLE_CX == 'YOUR_SEARCH_ENGINE_ID_HERE':
    GOOGLE_CX = os.environ.get('GOOGLE_CX', '')

JSEARCH_API_KEY = os.environ.get('JSEARCH_API_KEY') or JSEARCH_API_KEY
if JSEARCH_API_KEY == 'YOUR_JSEARCH_API_KEY_HERE':
    JSEARCH_API_KEY = os.environ.get('JSEARCH_API_KEY', '')

JSEARCH_HOST    = os.environ.get('JSEARCH_HOST') or JSEARCH_HOST
SECRET_KEY      = os.environ.get('SECRET_KEY') or SECRET_KEY

# ---------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------
BASE_DIR       = os.path.abspath(os.path.dirname(__file__))
app            = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = SECRET_KEY

import datetime

# ---------------------------------------------------------------
# Custom In-Memory Rate Limiter (For /login)
# ---------------------------------------------------------------
login_attempts = {}

def check_rate_limit(ip):
    now = time.time()
    if ip not in login_attempts:
        login_attempts[ip] = []

    # Remove attempts older than 60 seconds
    login_attempts[ip] = [t for t in login_attempts[ip] if now - t < 60]

    if len(login_attempts[ip]) >= 5:
        return False
    return True

def record_attempt(ip):
    now = time.time()
    if ip not in login_attempts:
        login_attempts[ip] = []
    login_attempts[ip].append(now)

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
    'farmer':             'farmers',
    'sports_fan':         'sports',
    'politician':         'politics',
    'researcher':         'research',
}

DEFAULT_QUERIES = {
    'student':            'latest student education scholarships news India',
    'job_seeker':         'latest job openings hiring career news',
    'general_reader':     'top news headlines today',
    'investor':           'stock market updates finance news today',
    'engineer':           'engineering technology innovation news',
    'freelancer':         'freelancing remote work opportunities tips',
    'esports_fan':        'esports gaming tournaments results news',
    'internship_seeker':  f'internship opportunities for students India {datetime.datetime.now().year}',
    'farmer':             'latest farming agriculture news',
    'sports_fan':         'latest sports news updates',
    'politician':         'latest political news updates',
    'researcher':         'latest research papers and studies',
}

# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------

def _has_letters(s):
    """True if s contains at least one letter."""
    return bool(re.search(r'[a-zA-Z]', s))

def _has_digits(s):
    """True if s contains at least one digit."""
    return bool(re.search(r'\d', s))

# ---------------------------------------------------------------
# Login-required decorator
# ---------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.path in ['/like', '/unlike', '/save', '/unsave']:
                return jsonify({
                    'success': False,
                    'error': 'login_required',
                    'message': 'Please log in to like and save stories.',
                    'redirect': url_for('login')
                }), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ---------------------------------------------------------------
# Profile-complete guard
# Redirect to onboarding if user hasn't filled in occupation/age yet.
# ---------------------------------------------------------------
def profile_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_user_by_id(session.get('user_id'))
        if not user or not user.get('is_profile_complete'):
            flash('Please complete your profile to unlock your personalized news feed.',
                  'info')
            return redirect(url_for('profile'))
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

    from mock_data import get_landing_news
    from models import get_all_like_counts, get_all_save_counts

    category = request.args.get('category', 'all').strip().lower()
    query    = request.args.get('q', '').strip()

    # Always deliver a rich, curated news catalog so users can surf news immediately
    results = get_landing_news(category=category, query=query)
    all_like_counts = get_all_like_counts()
    all_save_counts = get_all_save_counts()

    for r in results:
        link = r.get('link', '')
        r.setdefault('long_desc', '')
        r.setdefault('is_job', False)
        r.setdefault('requirements', [])
        r.setdefault('company_class', '')
        r['is_liked'] = False
        r['is_saved'] = False
        r['like_count'] = all_like_counts.get(link, 0)
        r['save_count'] = all_save_counts.get(link, 0)

    return render_template(
        'landing.html',
        results=results,
        active_category=category,
        query=query
    )


# ---- Public News API (for dynamic search/filtering without page reload) ----
@app.route('/api/news', methods=['GET'])
def api_news():
    from mock_data import get_landing_news
    category = request.args.get('category', 'all').strip().lower()
    query    = request.args.get('q', '').strip()
    results  = get_landing_news(category=category, query=query)
    return jsonify({
        'success': True,
        'count': len(results),
        'results': results
    })


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
    ip = request.remote_addr
    if not check_rate_limit(ip):
        return jsonify({'success': False,
                        'message': 'Too many failed attempts. Please try again in 60 seconds.'}), 429

    data = request.get_json(silent=True)
    if not data:
        record_attempt(ip)
        return jsonify({'success': False, 'message': 'Invalid request.'}), 400

    email    = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        record_attempt(ip)
        return jsonify({'success': False, 'message': 'Email and password are required.'})

    if len(email) > 254 or len(password) > 256:
        record_attempt(ip)
        return jsonify({'success': False, 'message': 'Invalid length for email or password.'})

    user = verify_user(email, password)
    if user:
        if ip in login_attempts:
            del login_attempts[ip]
        session.clear()
        session['user_id'] = user['id']
        session['email']   = user['email']
        # Redirect to profile/onboarding if not yet complete
        if not user.get('is_profile_complete'):
            return jsonify({'success': True, 'redirect': url_for('profile')})
        return jsonify({'success': True, 'redirect': url_for('domain')})

    record_attempt(ip)
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

    email            = data.get('email', '').strip()
    password         = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    # ── Strict validation ──────────────────────────────────────
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required.'})

    if len(email) > 50:                          # ← 50-char email limit
        return jsonify({'success': False,
                        'message': 'Email must be 50 characters or fewer.'})

    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return jsonify({'success': False, 'message': 'Invalid email format.'})

    if len(password) < 8:
        return jsonify({'success': False,
                        'message': 'Password must be at least 8 characters.'})

    if len(password) > 256:
        return jsonify({'success': False,
                        'message': 'Password is too long (max 256 characters).'})

    if not _has_letters(password) or not _has_digits(password):   # ← alphanumeric
        return jsonify({'success': False,
                        'message': 'Password must contain both letters and numbers.'})

    if password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match.'})
    # ──────────────────────────────────────────────────────────

    user_id = create_user(email, password)
    if user_id:
        session.clear()
        session['user_id'] = user_id
        session['email']   = email.lower()
        return jsonify({'success': True, 'redirect': url_for('profile')})

    return jsonify({'success': False,
                    'message': 'An account with this email already exists.'})


# ---------------------------------------------------------------
# Auth — Logout
# ---------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------------------------------------------------------
# Profile / Onboarding
# ---------------------------------------------------------------
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    user = get_user_by_id(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
    return render_template('profile.html', user=user)


@app.route('/profile', methods=['POST'])
@login_required
def profile_post():
    """
    Onboarding POST: save occupation + age and mark profile complete.
    Redirects to /domain on success so the user can pick their feed.
    """
    occupation = request.form.get('occupation', '').strip()
    age_raw    = request.form.get('age', '').strip()

    if not occupation:
        flash('Please enter your occupation.', 'error')
        return redirect(url_for('profile'))

    if not age_raw.isdigit() or not (1 <= int(age_raw) <= 120):
        flash('Please enter a valid age (1–120).', 'error')
        return redirect(url_for('profile'))

    complete_onboarding(session['user_id'], occupation, age_raw)
    flash('Profile saved! Welcome to NewsSphere.', 'success')
    return redirect(url_for('domain'))


@app.route('/profile/update', methods=['POST'])
@login_required
def profile_update():
    """Full profile update (JSON) — called from the detailed profile form."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request.'}), 400

    email = data.get('email', '').strip()

    # Server-side validation
    if not data.get('firstName', '').strip():
        return jsonify({'success': False, 'message': 'First name is required.'})
    if not email:
        return jsonify({'success': False, 'message': 'Email is required.'})
    if not data.get('phone', '').strip():
        return jsonify({'success': False, 'message': 'Phone number is required.'})
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return jsonify({'success': False, 'message': 'Invalid email format.'})

    import sqlite3
    try:
        update_profile(session['user_id'], data)
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Email already in use.'})

    session['email'] = email.lower()

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
            'occupation': user.get('occupation', ''),
            'location':   user.get('location', ''),
        }
    })


# ---------------------------------------------------------------
# Domain selection
# ---------------------------------------------------------------
@app.route('/domain')
@login_required
@profile_required
def domain():
    return render_template('domain.html')


# ---------------------------------------------------------------
# Search feed
# ---------------------------------------------------------------
@app.route('/index')
@login_required
@profile_required
def index():
    domain_param = request.args.get('domain', 'student')
    query        = request.args.get('q', '').strip()
    demo_mode    = request.args.get('demo', '').lower() == 'true'

    # Guard against unknown domain slugs
    if domain_param not in DOMAIN_KEY_MAP:
        domain_param = 'student'

    trusted_key = DOMAIN_KEY_MAP[domain_param]

    # Use domain-specific default query if user hasn't typed anything
    if not query:
        query = DEFAULT_QUERIES.get(domain_param, 'latest news')

    results   = []
    error_msg = None

    from mock_data import get_mock_data

    # ── Presentation Demo Mode ────────────────────────────────
    if demo_mode:
        results   = get_mock_data(domain_param)
        error_msg = None                          # never show error in demo
        return render_template('index.html',
                               results=results,
                               selected_domain=domain_param,
                               query=query,
                               error_msg=None)
    # ─────────────────────────────────────────────────────────

    try:
        if domain_param == 'job_seeker':
            # ── Always use JSearch for job listings ──────────
            if not JSEARCH_API_KEY or JSEARCH_API_KEY == 'YOUR_JSEARCH_API_KEY_HERE':
                results   = get_mock_data(domain_param)
                error_msg = None                  # silent demo failover
            else:
                raw_results = job_search(query, JSEARCH_API_KEY, JSEARCH_HOST)
                for job in raw_results:
                    results.append({
                        'title':        job.get('title', ''),
                        'link':         job.get('link', ''),
                        'snippet':      f"Location: {job.get('location', 'Remote')}",
                        'source':       job.get('company', ''),
                        'image':        '',
                        'long_desc':    '',
                        'is_job':       True,
                        'requirements': [],
                        'company_class':'',
                    })
                if not results:
                    results   = get_mock_data(domain_param)
                    error_msg = None              # silent demo failover
        else:
            # ── Google Custom Search for all other domains ───
            if not GOOGLE_API_KEY or GOOGLE_API_KEY == 'YOUR_GOOGLE_API_KEY_HERE':
                results   = get_mock_data(domain_param)
                error_msg = None                  # silent demo failover
            else:
                results = google_search(query, trusted_key, GOOGLE_API_KEY, GOOGLE_CX)
                if not results:
                    results   = get_mock_data(domain_param)
                    error_msg = None              # silent demo failover
                else:
                    # Patch live results to include extra keys for template
                    for r in results:
                        r.setdefault('long_desc',     '')
                        r.setdefault('is_job',        False)
                        r.setdefault('requirements',  [])
                        r.setdefault('company_class', '')

    except ValueError as e:
        results   = get_mock_data(domain_param)
        error_msg = None                          # silent demo failover
        logging.error(f'[index] ValueError: {e}')
    except Exception as e:
        results   = get_mock_data(domain_param)
        error_msg = None                          # silent demo failover
        logging.error(f'[index] Unexpected error: {e}')

    from models import get_all_like_counts, get_all_save_counts, get_liked_links, get_user_saved_links
    user_id = session.get('user_id')
    user_likes = set(get_liked_links(user_id)) if user_id else set()
    user_saves = set(get_user_saved_links(user_id)) if user_id else set()
    all_like_counts = get_all_like_counts()
    all_save_counts = get_all_save_counts()

    for r in results:
        link = r.get('link', '')
        r['is_liked']   = link in user_likes
        r['is_saved']   = link in user_saves
        r['like_count'] = all_like_counts.get(link, 0)
        r['save_count'] = all_save_counts.get(link, 0)

    return render_template(
        'index.html',
        results=results,
        selected_domain=domain_param,
        query=query,
        error_msg=error_msg,
    )


# ---------------------------------------------------------------
# Saved results feed
# ---------------------------------------------------------------
@app.route('/saved')
@login_required
@profile_required
def saved():
    user_id = session['user_id']
    results = get_saved_results(user_id)
    from models import get_all_like_counts, get_all_save_counts, get_liked_links
    user_likes = set(get_liked_links(user_id))
    all_like_counts = get_all_like_counts()
    all_save_counts = get_all_save_counts()
    for r in results:
        link = r.get('link', '')
        r['is_liked']   = link in user_likes
        r['is_saved']   = True
        r['like_count'] = all_like_counts.get(link, 0)
        r['save_count'] = all_save_counts.get(link, 1)
    return render_template('saved.html', results=results)


# ---------------------------------------------------------------
# Save / Unsave a result
# ---------------------------------------------------------------
@app.route('/save', methods=['POST'])
@login_required
def save():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False}), 400

    user_id = session['user_id']
    link    = data.get('link', '').strip()

    if not link:
        return jsonify({'success': False, 'message': 'Link is empty.'})

    from models import save_result, is_result_saved, get_save_count
    if not is_result_saved(user_id, link):
        save_result(
            user_id=user_id,
            title=data.get('title', ''),
            link=link,
            snippet=data.get('snippet', ''),
            source=data.get('source', ''),
        )
    cnt = get_save_count(link)
    return jsonify({'success': True, 'count': cnt})


@app.route('/unsave', methods=['POST'])
@login_required
def unsave():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False}), 400

    link = data.get('link', '').strip()
    cnt = 0
    if link:
        from models import remove_saved_result, get_save_count
        remove_saved_result(session['user_id'], link)
        cnt = get_save_count(link)
    return jsonify({'success': True, 'count': cnt})


# ---------------------------------------------------------------
# Like / Unlike
# ---------------------------------------------------------------
@app.route('/like', methods=['POST'])
@login_required
def like():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False}), 400
    link = data.get('link', '').strip()
    cnt = 0
    if link:
        from models import like_result, get_like_count
        like_result(session['user_id'], link)
        cnt = get_like_count(link)
    return jsonify({'success': True, 'count': cnt})


@app.route('/unlike', methods=['POST'])
@login_required
def unlike():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False}), 400
    link = data.get('link', '').strip()
    cnt = 0
    if link:
        from models import unlike_result, get_like_count
        unlike_result(session['user_id'], link)
        cnt = get_like_count(link)
    return jsonify({'success': True, 'count': cnt})


@app.route('/liked_links', methods=['GET'])
@login_required
def liked_links():
    from models import get_liked_links
    links = get_liked_links(session['user_id'])
    return jsonify({'links': links})


# ===============================================================
# Entry point
# ===============================================================
with app.app_context():
    init_db()          # create / migrate tables on first run

if __name__ == '__main__':
    app.run(debug=True)