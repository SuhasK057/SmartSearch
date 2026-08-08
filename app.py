from flask import Flask, render_template, request, redirect, session
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from config import TRUSTED_SITES, GOOGLE_API_KEY, GOOGLE_CX_ID, RAPIDAPI_KEY, RAPIDAPI_HOST, SECRET_KEY
from models import init_db

app = Flask(__name__)
app.secret_key = SECRET_KEY
init_db()

def get_db():
    return sqlite3.connect('smartsearch.db')

def google_search(query, user_type):
    sites = TRUSTED_SITES[user_type]
    all_sites = [site for category in sites.values() for site in category]
    site_filter = " OR ".join([f"site:{s}" for s in all_sites])
    final_query = f"{query} ({site_filter})"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {'key': GOOGLE_API_KEY, 'cx': GOOGLE_CX_ID, 'q': final_query, 'num': 10}
    response = requests.get(url, params=params).json()

    results = []
    if 'items' in response:
        for item in response['items']:
            results.append({
                'title': item['title'], 'link': item['link'],
                'snippet': item['snippet'], 'source': item['displayLink']
            })
    return results

def job_search(query):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": RAPIDAPI_HOST}
    params = {"query": query, "page": "1", "num_pages": "1"}
    response = requests.get(url, headers=headers, params=params).json()

    results = []
    if 'data' in response:
        for job in response['data']:
            results.append({
                'title': job.get('job_title'), 'company': job.get('employer_name'),
                'link': job.get('job_apply_link'), 'location': job.get('job_city', 'Remote')
            })
    return results

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    user_type = request.form.get('user_type')
    query = request.form.get('query')
    if user_type == 'job_seeker':
        results = job_search(query)
    else:
        results = google_search(query, user_type)
    return render_template('results.html', results=results, query=query)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password_hash = generate_password_hash(request.form['password'])
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already taken"
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db()
        user = conn.execute('SELECT id, password_hash FROM users WHERE username = ?',
                             (request.form['username'],)).fetchone()
        conn.close()
        if user and check_password_hash(user[1], request.form['password']):
            session['user_id'] = user[0]
            session['username'] = request.form['username']
            return redirect('/')
        return "Invalid login"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/save-job', methods=['POST'])
def save_job():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    conn.execute('INSERT INTO saved_jobs (user_id, title, company, link, location) VALUES (?, ?, ?, ?, ?)',
                 (session['user_id'], request.form['title'], request.form['company'],
                  request.form['link'], request.form['location']))
    conn.commit()
    conn.close()
    return redirect('/saved-jobs')

@app.route('/saved-jobs')
def saved_jobs():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    jobs = conn.execute('SELECT title, company, link, location FROM saved_jobs WHERE user_id = ?',
                         (session['user_id'],)).fetchall()
    conn.close()
    return render_template('saved_jobs.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)