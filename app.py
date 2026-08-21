import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# 1. Import configurations directly from your config_template file
import config_template as config[cite: 2, 4]
from models import db, User, UserPreference, SavedJob

app = Flask(__name__)

# Load configurations from config_template
app.config['SECRET_KEY'] = config.SECRET_KEY[cite: 2, 4]
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/newssphere_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database & Login Manager
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


# --- Helper API Functions Using config_template Variables ---

def google_search(query, user_type):
    """
    Searches Google Custom Search using TRUSTED_SITES, GOOGLE_API_KEY, 
    and GOOGLE_CX defined in config_template.py.
    """
    if user_type not in config.TRUSTED_SITES:[cite: 2, 4]
        user_type = "news"  # Default fallback

    sites = config.TRUSTED_SITES[user_type][cite: 2, 4]
    all_sites = [site for category in sites.values() for site in category]
    site_filter = " OR ".join([f"site:{s}" for s in all_sites])
    final_query = f"{query} ({site_filter})"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': config.GOOGLE_API_KEY,[cite: 2, 4]
        'cx': config.GOOGLE_CX,[cite: 2, 4]
        'q': final_query,
        'num': 10
    }

    try:
        response = requests.get(url, params=params, timeout=10).json()
    except requests.exceptions.RequestException as e:
        print(f"[google_search] Request failed: {e}")
        return []

    results = []
    if 'items' in response:
        for item in response['items']:
            results.append({
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet'),
                'source': item.get('displayLink'),
                'image': item.get('pagemap', {}).get('cse_image', [{}])[0].get('src')
            })
    return results


def job_search(query):
    """
    Searches JSearch (RapidAPI) using JSEARCH_API_KEY 
    and JSEARCH_HOST defined in config_template.py.
    """
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": config.JSEARCH_API_KEY,[cite: 2, 4]
        "X-RapidAPI-Host": config.JSEARCH_HOST[cite: 2, 4]
    }
    params = {"query": query, "page": "1", "num_pages": "1"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10).json()
    except requests.exceptions.RequestException as e:
        print(f"[job_search] Request failed: {e}")
        return []

    results = []
    if 'data' in response:
        for job in response['data']:
            results.append({
                'title': job.get('job_title'),
                'company': job.get('employer_name'),
                'link': job.get('job_apply_link'),
                'location': job.get('job_city', 'Remote')
            })
    return results


# --- App Routes ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('select_user_type'))
        
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('select_user_type'))
            
        flash('Invalid login credentials.')
    return render_template('login.html')


@app.route('/select-user-type', methods=['GET', 'POST'])
@login_required
def select_user_type():
    if request.method == 'POST':
        selected_type = request.form.get('user_type')  # student, job_seeker, etc.
        current_user.user_type = selected_type
        db.session.commit()
        return redirect(url_for('select_genres'))
        
    return render_template('user_type.html')


@app.route('/select-genres', methods=['GET', 'POST'])
@login_required
def select_genres():
    if request.method == 'POST':
        genre = request.form.get('genre')
        pref = UserPreference.query.get(current_user.id)
        if not pref:
            pref = UserPreference(user_id=current_user.id, preferred_categories=genre)
            db.session.add(pref)
        else:
            pref.preferred_categories = genre
        db.session.commit()
        
        return redirect(url_for('feed', category=genre))
        
    return render_template('genres.html')


@app.route('/feed')
@login_required
def feed():
    category = request.args.get('category', 'general')
    user_type = current_user.user_type or "news"
    
    # Route logic: Route to job_search if category is 'jobs', otherwise use google_search
    if category.lower() == 'jobs':
        results = job_search(f"latest jobs for {user_type}")
        return render_template('feed.html', results=results, is_job=True, category=category)
    else:
        results = google_search(category, user_type)
        return render_template('feed.html', results=results, is_job=False, category=category)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)