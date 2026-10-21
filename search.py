"""
search.py  —  Google Custom Search + JSearch (RapidAPI) wrappers.

Extracted from the old app.py (which was not a Flask app).
Bugs fixed:
  - Missing comma on line 95 of the original (SyntaxError)
  - API keys are now passed in as arguments instead of module-level imports,
    so this module has zero side-effects on import.
"""

import requests


# ---------------------------------------------------------------
# Trusted site lists per user-type / domain
# ---------------------------------------------------------------

TRUSTED_SITES = {
    "student": {
        "tutorials":        ["geeksforgeeks.org", "w3schools.com", "nptel.ac.in"],
        "research":         ["scholar.google.com", "researchgate.net", "arxiv.org"],
        "coding_practice":  ["leetcode.com", "codeforces.com", "hackerrank.com"],
        "internships":      ["internshala.com", "unstop.com", "linkedin.com"],
    },
    "job_seeker": {
        "jobs":      ["linkedin.com", "naukri.com", "indeed.com", "glassdoor.com"],
        "interview": ["interviewbit.com", "geeksforgeeks.org"],
    },
    "farmers": {
        "prices": ["agmarknet.gov.in", "pmkisan.gov.in"],
        "news":   ["krishijagran.com"],
    },
    "sports": {
        "general": ["espn.com", "skysports.com"],
        "cricket": ["espncricinfo.com"],
    },
    "news": {
        "general":  ["bbc.com", "reuters.com", "thehindu.com", "ndtv.com"],
        "business": ["economictimes.indiatimes.com"],
    },
    "stock_market": {
        "analysis": ["moneycontrol.com", "economictimes.indiatimes.com"],
        "data":     ["nseindia.com"],
    },
    "engineering": {
        "journals": ["ieee.org", "arxiv.org"],
        "news":     ["techcrunch.com"],
    },
    "freelancing": {
        "platforms": ["upwork.com", "fiverr.com", "freelancer.com"],
    },
    "esports": {
        "news":  ["esportsinsider.com"],
        "stats": ["liquipedia.net"],
    },
    "politics": {
        "wire_services": ["reuters.com", "apnews.com", "ptinews.com"],
    },
    "research": {
        "papers": ["scholar.google.com", "researchgate.net", "arxiv.org"],
    },
    "internships": {
        "listings": ["internshala.com", "unstop.com"],
    },
}


# ---------------------------------------------------------------
# Google Custom Search
# ---------------------------------------------------------------

def google_search(query, user_type, api_key, cx_id, num=10):
    """
    Search Google Custom Search restricted to trusted sites for user_type.

    Args:
        query     : search string typed by the user
        user_type : key from TRUSTED_SITES (e.g. "student", "news")
        api_key   : Google API key
        cx_id     : Custom Search Engine ID
        num       : number of results (max 10 per Google's free tier)

    Returns:
        list of dicts: {title, link, snippet, source, image}
        Returns [] on any network / API error so the page still renders.

    Raises:
        ValueError if user_type is not in TRUSTED_SITES
    """
    if user_type not in TRUSTED_SITES:
        raise ValueError(f"Unknown user_type: '{user_type}'")

    # Build "site:x.com OR site:y.com …" filter
    all_sites   = [s for cat in TRUSTED_SITES[user_type].values() for s in cat]
    site_filter = " OR ".join(f"site:{s}" for s in all_sites)
    final_query = f"{query} ({site_filter})"

    params = {
        'key': api_key,
        'cx':  cx_id,
        'q':   final_query,
        'num': num,
    }

    try:
        resp = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params=params,
            timeout=10
        )
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"[google_search] Network error: {e}")
        return []

    results = []
    if 'items' in data:
        for item in data['items']:
            pagemap = item.get('pagemap', {})
            cse_image = pagemap.get('cse_image', [])
            image_url = cse_image[0].get('src', '') if cse_image else ''
            
            results.append({
                'title':   item.get('title', ''),
                'link':    item.get('link', ''),
                'snippet': item.get('snippet', ''),
                'source':  item.get('displayLink', ''),  # ← BUG FIX: comma was missing here
                'image':   image_url,
            })
    else:
        err_code = data.get('error', {}).get('code', 'unknown')
        err_msg  = data.get('error', {}).get('message', '')
        print(f"[google_search] No items returned. code={err_code} msg={err_msg}")

    return results


# ---------------------------------------------------------------
# JSearch (RapidAPI) — job listings
# ---------------------------------------------------------------

def job_search(query, api_key, host):
    """
    Search JSearch on RapidAPI for job listings.

    Returns:
        list of dicts: {title, company, link, location}
    """
    headers = {
        "X-RapidAPI-Key":  api_key,
        "X-RapidAPI-Host": host,
    }
    params = {"query": query, "page": "1", "num_pages": "1"}

    try:
        resp = requests.get(
            "https://jsearch.p.rapidapi.com/search",
            headers=headers,
            params=params,
            timeout=10
        )
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"[job_search] Network error: {e}")
        return []

    results = []
    if 'data' in data:
        for job in data['data']:
            results.append({
                'title':    job.get('job_title', ''),
                'company':  job.get('employer_name', ''),
                'link':     job.get('job_apply_link', ''),
                'location': job.get('job_city') or 'Remote',
            })
    else:
        print(f"[job_search] No data in response: {data}")

    return results
