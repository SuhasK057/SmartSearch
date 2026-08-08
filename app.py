import requests
from config import GOOGLE_API_KEY, GOOGLE_CX_ID, RAPIDAPI_KEY, RAPIDAPI_HOST
 
 
# ---- Trusted Sites Dictionary ----
# Structure: user_type -> category -> list of domains
# This is the core "what counts as a trustworthy source" decision.
TRUSTED_SITES = {
    "student": {
        "tutorials": ["geeksforgeeks.org", "w3schools.com", "nptel.ac.in"],
        "research": ["scholar.google.com", "researchgate.net", "arxiv.org"],
        "coding_practice": ["leetcode.com", "codeforces.com", "hackerrank.com"],
        "internships": ["internshala.com", "unstop.com", "linkedin.com"],
    },
    "job_seeker": {
        "jobs": ["linkedin.com", "naukri.com", "indeed.com", "glassdoor.com"],
        "interview": ["interviewbit.com", "geeksforgeeks.org"],
    },
    "farmers": {
        "prices": ["agmarknet.gov.in", "pmkisan.gov.in"],
        "news": ["krishijagran.com"],
    },
    "sports": {
        "general": ["espn.com", "skysports.com"],
        "cricket": ["espncricinfo.com"],
    },
    "news": {
        "general": ["bbc.com", "reuters.com", "thehindu.com", "ndtv.com"],
        "business": ["economictimes.indiatimes.com"],
    },
    "stock_market": {
        "analysis": ["moneycontrol.com", "economictimes.indiatimes.com"],
        "data": ["nseindia.com"],
    },
    "engineering": {
        "journals": ["ieee.org", "arxiv.org"],
        "news": ["techcrunch.com"],
    },
    "freelancing": {
        "platforms": ["upwork.com", "fiverr.com", "freelancer.com"],
    },
    "esports": {
        "news": ["esportsinsider.com"],
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
 
 
def google_search(query, user_type):
    """
    Searches Google Custom Search, restricted to trusted sites
    for the given user_type.
 
    Returns a list of dicts: title, link, snippet, source
    """
    if user_type not in TRUSTED_SITES:
        raise ValueError(f"Unknown user_type: {user_type}")
 
    sites = TRUSTED_SITES[user_type]
    all_sites = [site for category in sites.values() for site in category]
    site_filter = " OR ".join([f"site:{s}" for s in all_sites])
    final_query = f"{query} ({site_filter})"
 
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CX_ID,
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
                'source': item.get('displayLink')
                'image': item.get('pagemap', {}).get('cse_image', [{}])[0].get('src')
            })
    else:
        # No 'items' usually means quota hit, bad query, or bad API key
        print(f"[google_search] No items in response: {response}")
 
    return results
 
 
def job_search(query):
    """
    Searches JSearch (RapidAPI) for job listings.
 
    Returns a list of dicts: title, company, link, location
    """
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
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
    else:
        print(f"[job_search] No data in response: {response}")
 
    return results
 
 
# ---- Standalone test — run this file directly to sanity-check your APIs ----
# python search_engine.py
if __name__ == '__main__':
    print("Testing google_search()...")
    results = google_search("python tutorials", "student")
    print(f"Got {len(results)} results")
    for r in results[:3]:
        print(r)
 
    print("\nTesting job_search()...")
    jobs = job_search("developer jobs in chicago")
    print(f"Got {len(jobs)} results")
    for j in jobs[:3]:
        print(j)