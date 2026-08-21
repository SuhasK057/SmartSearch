import requests
import config

TRUSTED_SITES = {
    "student": {
        "tutorials": ["geeksforgeeks.org", "w3schools.com", "nptel.ac.in"],[cite: 1, 2]
        "research": ["scholar.google.com", "researchgate.net", "arxiv.org"],[cite: 1, 2]
        "coding_practice": ["leetcode.com", "codeforces.com", "hackerrank.com"],[cite: 1, 2]
        "internships": ["internshala.com", "unstop.com", "linkedin.com"],[cite: 1, 2]
    },
    "job_seeker": {
        "jobs": ["linkedin.com", "naukri.com", "indeed.com", "glassdoor.com"],[cite: 1, 2]
        "interview": ["interviewbit.com", "geeksforgeeks.org"],[cite: 1, 2]
    },
    "farmers": {
        "prices": ["agmarknet.gov.in", "pmkisan.gov.in"],[cite: 1, 2]
        "news": ["krishijagran.com"],[cite: 1, 2]
    },
    "sports": {
        "general": ["espn.com", "skysports.com"],[cite: 1, 2]
        "cricket": ["espncricinfo.com"],[cite: 1, 2]
    },
    "news": {
        "general": ["bbc.com", "reuters.com", "thehindu.com", "ndtv.com"],[cite: 1, 2]
        "business": ["economictimes.indiatimes.com"],[cite: 1, 2]
    },
    "stock_market": {
        "analysis": ["moneycontrol.com", "economictimes.indiatimes.com"],[cite: 1, 2]
        "data": ["nseindia.com"],[cite: 1, 2]
    },
    "engineering": {
        "journals": ["ieee.org", "arxiv.org"],[cite: 1, 2]
        "news": ["techcrunch.com"],[cite: 1, 2]
    },
    "freelancing": {
        "platforms": ["upwork.com", "fiverr.com", "freelancer.com"],[cite: 1, 2]
    },
    "esports": {
        "news": ["esportsinsider.com"],[cite: 1, 2]
        "stats": ["liquipedia.net"],[cite: 1, 2]
    },
    "politics": {
        "wire_services": ["reuters.com", "apnews.com", "ptinews.com"],[cite: 1, 2]
    },
    "research": {
        "papers": ["scholar.google.com", "researchgate.net", "arxiv.org"],[cite: 1, 2]
    },
    "internships": {
        "listings": ["internshala.com", "unstop.com"],[cite: 1, 2]
    },
}

def google_search(query, user_type):
    """Searches Google Custom Search, restricted to trusted sites for user_type."""[cite: 1]
    if user_type not in TRUSTED_SITES:
        user_type = "news"  # Default fallback if unknown type[cite: 1]

    sites = TRUSTED_SITES[user_type][cite: 1]
    all_sites = [site for category in sites.values() for site in category][cite: 1]
    site_filter = " OR ".join([f"site:{s}" for s in all_sites])[cite: 1]
    final_query = f"{query} ({site_filter})"[cite: 1]

    url = "https://www.googleapis.com/customsearch/v1"[cite: 1]
    params = {
        'key': config.GOOGLE_API_KEY,[cite: 1]
        'cx': config.GOOGLE_CX_ID,[cite: 1]
        'q': final_query,[cite: 1]
        'num': 10[cite: 1]
    }

    try:
        response = requests.get(url, params=params, timeout=10).json()[cite: 1]
    except requests.exceptions.RequestException as e:
        print(f"[google_search] Request failed: {e}")[cite: 1]
        return []

    results = []
    if 'items' in response:[cite: 1]
        for item in response['items']:[cite: 1]
            results.append({
                'title': item.get('title'),[cite: 1]
                'link': item.get('link'),[cite: 1]
                'snippet': item.get('snippet'),[cite: 1]
                'source': item.get('displayLink'),  # Added missing comma here[cite: 1]
                'image': item.get('pagemap', {}).get('cse_image', [{}])[0].get('src')[cite: 1]
            })
    return results

def job_search(query):
    """Searches JSearch (RapidAPI) for job listings."""[cite: 1]
    url = "https://jsearch.p.rapidapi.com/search"[cite: 1]
    headers = {
        "X-RapidAPI-Key": config.RAPIDAPI_KEY,[cite: 1]
        "X-RapidAPI-Host": config.RAPIDAPI_HOST[cite: 1]
    }
    params = {"query": query, "page": "1", "num_pages": "1"}[cite: 1]

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10).json()[cite: 1]
    except requests.exceptions.RequestException as e:
        print(f"[job_search] Request failed: {e}")[cite: 1]
        return []

    results = []
    if 'data' in response:[cite: 1]
        for job in response['data']:[cite: 1]
            results.append({
                'title': job.get('job_title'),[cite: 1]
                'company': job.get('employer_name'),[cite: 1]
                'link': job.get('job_apply_link'),[cite: 1]
                'location': job.get('job_city', 'Remote')[cite: 1]
            })
    return results