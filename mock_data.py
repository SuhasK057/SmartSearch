"""
mock_data.py  —  Presentation Demo Mode data for NewsSphere / SmartSearch.

get_mock_data(domain) returns a list of article/job dicts whose keys
exactly match what the Jinja2 index.html template expects:

    title        (str)   card headline / job title
    source       (str)   publisher or company name
    image        (str)   absolute URL to a high-quality Unsplash image
    snippet      (str)   short description shown below the title
    link         (str)   "Read More / Apply" destination URL
    long_desc    (str)   expanded paragraph shown after "Read More"
    is_job       (bool)  True  → show requirements list + "Apply" CTA
    requirements (list)  only present when is_job is True
    company_class(str)   optional CSS class for branded border/glow
"""


# ---------------------------------------------------------------------------
# Helper: shared image pool keyed by topic
# ---------------------------------------------------------------------------
_IMAGES = {
    "ai":         "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=700&q=75",
    "finance":    "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=700&q=75",
    "work":       "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=700&q=75",
    "study":      "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=700&q=75",
    "campus":     "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=700&q=75",
    "code":       "https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&w=700&q=75",
    "google":     "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?auto=format&fit=crop&w=700&q=75",
    "amazon":     "https://images.unsplash.com/photo-1523474253046-8cd2748b5fd2?auto=format&fit=crop&w=700&q=75",
    "microsoft":  "https://images.unsplash.com/photo-1496200186974-4293800e2c20?auto=format&fit=crop&w=700&q=75",
    "meta":       "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&w=700&q=75",
    "space":      "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=700&q=75",
    "sports":     "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=700&q=75",
    "cricket":    "https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=700&q=75",
    "farm":       "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=700&q=75",
    "politics":   "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=700&q=75",
    "research":   "https://images.unsplash.com/photo-1532094349884-543559c5f3e3?auto=format&fit=crop&w=700&q=75",
    "esports":    "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=700&q=75",
    "freelance":  "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=700&q=75",
    "stock":      "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=700&q=75",
    "chip":       "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=700&q=75",
    "internship": "https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?auto=format&fit=crop&w=700&q=75",
    "apple":      "https://images.unsplash.com/photo-1510519138197-06b8628cbf4c?auto=format&fit=crop&w=700&q=75",
    "fusion":     "https://images.unsplash.com/photo-1507668077129-56e32842fceb?auto=format&fit=crop&w=700&q=75",
    "ev":         "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=700&q=75",
    "climate":    "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=700&q=75",
}


# ---------------------------------------------------------------------------
# Domain-specific mock data functions
# ---------------------------------------------------------------------------

def _jobs():
    return [
        {
            "title":         "Frontend Engineer — Google",
            "source":        "Google",
            "image":         _IMAGES["google"],
            "snippet":       "Location: Mountain View, CA  ·  Full-time  ·  $130k – $180k",
            "link":          "https://careers.google.com/",
            "long_desc":     (
                "Join Google's Chrome & Web Platform team to build the next generation "
                "of web experiences. You'll contribute to open-source projects, "
                "collaborate with world-class engineers, and shape products used by "
                "billions of people every day."
            ),
            "is_job":        True,
            "requirements":  ["React / Vue / Angular", "TypeScript", "3+ years experience", "Strong DSA fundamentals"],
            "company_class": "google-job",
        },
        {
            "title":         "Software Development Engineer II — Amazon",
            "source":        "Amazon",
            "image":         _IMAGES["amazon"],
            "snippet":       "Location: Seattle, WA  ·  Full-time  ·  $140k – $190k",
            "link":          "https://amazon.jobs/",
            "long_desc":     (
                "Amazon is hiring SDEs to architect and scale highly available "
                "distributed systems that power Prime, Alexa, and AWS. You will own "
                "features end-to-end and mentor junior engineers across the team."
            ),
            "is_job":        True,
            "requirements":  ["Java / C++ / Python", "System Design", "AWS services", "Leadership principles"],
            "company_class": "amazon-job",
        },
        {
            "title":         "Full Stack Developer — Microsoft",
            "source":        "Microsoft",
            "image":         _IMAGES["microsoft"],
            "snippet":       "Location: Redmond, WA  ·  Full-time  ·  $135k – $175k",
            "link":          "https://careers.microsoft.com/",
            "long_desc":     (
                "Help build the future of Azure DevOps and GitHub by contributing to "
                "core full-stack services. The role involves React frontends, "
                "C# / .NET backends, and cloud-native microservices on Azure."
            ),
            "is_job":        True,
            "requirements":  ["C# / .NET", "React", "Azure", "SQL / CosmosDB"],
            "company_class": "microsoft-job",
        },
        {
            "title":         "AI Research Engineer — Meta",
            "source":        "Meta",
            "image":         _IMAGES["meta"],
            "snippet":       "Location: Menlo Park, CA  ·  Full-time  ·  $150k – $220k",
            "link":          "https://www.metacareers.com/",
            "long_desc":     (
                "Work on cutting-edge generative AI and large language model research "
                "at Meta FAIR. You will co-author papers, train trillion-parameter "
                "models, and collaborate directly with the teams behind LLaMA and "
                "CodeLlama."
            ),
            "is_job":        True,
            "requirements":  ["PyTorch / JAX", "ML / Deep Learning", "Python", "Publications preferred"],
            "company_class": "meta-job",
        },
        {
            "title":         "Backend Engineer — Zomato",
            "source":        "Zomato",
            "image":         _IMAGES["code"],
            "snippet":       "Location: Gurugram, India  ·  Full-time  ·  ₹20 – 35 LPA",
            "link":          "https://www.zomato.com/careers",
            "long_desc":     (
                "Build and scale the order-management microservices powering "
                "Zomato's 25 million+ daily orders. The stack includes Go, Kafka, "
                "Redis, and PostgreSQL, deployed on AWS EKS."
            ),
            "is_job":        True,
            "requirements":  ["Go / Java", "Kafka / RabbitMQ", "PostgreSQL", "Kubernetes"],
            "company_class": "",
        },
    ]


def _student():
    return [
        {
            "title":   "PM Scholarship 2026: Apply Now for ₹75,000 Grant",
            "source":  "scholarships.gov.in",
            "image":   _IMAGES["campus"],
            "snippet": "Central sector scholarship for undergraduate students — last date 31 Oct 2026.",
            "link":    "https://scholarships.gov.in/",
            "long_desc": (
                "The Central Sector Scheme of Scholarships covers tuition and "
                "maintenance allowance for meritorious students from low-income "
                "families. Eligible candidates must have scored above 80% in "
                "Class 12 and belong to the top 20 percentile of their board."
            ),
            "is_job": False,
        },
        {
            "title":   "GeeksForGeeks launches Free DSA Mastery Course 2026",
            "source":  "geeksforgeeks.org",
            "image":   _IMAGES["code"],
            "snippet": "180-hour self-paced curriculum covering arrays, graphs, DP, and system design.",
            "link":    "https://www.geeksforgeeks.org/",
            "long_desc": (
                "GFG's new DSA Mastery path includes 500 curated problems, "
                "weekly live doubt sessions, and a certificate recognised by "
                "top product-based companies including Google, Amazon, and "
                "Flipkart placement drives."
            ),
            "is_job": False,
        },
        {
            "title":   "NPTEL July 2026 Courses: 1,000+ Free Certifications Open",
            "source":  "nptel.ac.in",
            "image":   _IMAGES["study"],
            "snippet": "IIT and IISc faculty deliver online certificate courses — enrol by 15 Nov.",
            "link":    "https://nptel.ac.in/",
            "long_desc": (
                "NPTEL's July semester offers 1,200+ courses across engineering, "
                "management, and humanities. Courses are free to audit; a proctored "
                "exam (₹1,000 fee) earns you an elite certificate co-branded by "
                "AICTE and the Ministry of Education."
            ),
            "is_job": False,
        },
        {
            "title":   "Internshala: 50,000 Internship Openings Added This Week",
            "source":  "internshala.com",
            "image":   _IMAGES["internship"],
            "snippet": "Work-from-home and on-site internships across tech, marketing, and design.",
            "link":    "https://internshala.com/",
            "long_desc": (
                "Internshala's weekly intake includes roles from startups and "
                "Fortune 500 companies, with stipends ranging from ₹5,000 to "
                "₹30,000 per month. Apply using your profile — no cover letter needed."
            ),
            "is_job": False,
        },
        {
            "title":   "LeetCode Weekly Contest 420 — Results & Solutions",
            "source":  "leetcode.com",
            "image":   _IMAGES["code"],
            "snippet": "Top performers share editorial walkthroughs for all 4 contest problems.",
            "link":    "https://leetcode.com/contest/",
            "long_desc": (
                "Contest 420 featured a segment-tree hard problem that stumped "
                "94% of participants. The official editorial by LeetCode staff "
                "breaks down an O(n log n) approach with clear diagrams — "
                "essential reading for upcoming campus placements."
            ),
            "is_job": False,
        },
    ]


def _general():
    return [
        {
            "title":   "The Future of AI: What to Expect in 2026",
            "source":  "TechCrunch",
            "image":   _IMAGES["ai"],
            "snippet": "Artificial intelligence continues to evolve at a breakneck pace across every industry.",
            "link":    "https://techcrunch.com/",
            "long_desc": (
                "Experts predict that by end of 2026, AI models will not only generate "
                "content but autonomously manage complex software ecosystems — "
                "improving development speed and reliability by up to 40%. "
                "Agentic workflows, multi-modal reasoning, and real-time collaboration "
                "are the three defining trends of the year."
            ),
            "is_job": False,
        },
        {
            "title":   "Global Markets Rally on Tech Earnings",
            "source":  "Bloomberg",
            "image":   _IMAGES["finance"],
            "snippet": "Stock markets hit record highs following stronger-than-expected Q3 tech earnings.",
            "link":    "https://bloomberg.com/",
            "long_desc": (
                "Investors showed renewed optimism as major technology firms posted "
                "record profits, driven by cloud computing and AI services. The S&P 500 "
                "crossed 6,200 points while the Nasdaq hit an all-time high of 22,400, "
                "with Nvidia and Microsoft leading the rally."
            ),
            "is_job": False,
        },
        {
            "title":   "New Study: 4-Day Work Week Boosts Productivity by 22%",
            "source":  "BBC News",
            "image":   _IMAGES["work"],
            "snippet": "Comprehensive trial across 1,000 companies shows gains in output and employee wellbeing.",
            "link":    "https://bbc.com/news",
            "long_desc": (
                "A landmark 12-month study by Oxford University tracked 61 companies "
                "that switched to a four-day week with no pay cut. Results showed a "
                "22% boost in productivity, 65% reduction in sick days, and a "
                "91% employee retention rate — challenging decades of 5-day orthodoxy."
            ),
            "is_job": False,
        },
        {
            "title":   "ISRO's Gaganyaan Mission: Crew Announced for 2026 Launch",
            "source":  "NDTV",
            "image":   _IMAGES["space"],
            "snippet": "India's first crewed spaceflight will carry three astronauts to a 400 km orbit.",
            "link":    "https://ndtv.com/",
            "long_desc": (
                "ISRO officially named the four-member Gaganyaan crew: Group Captains "
                "Prashanth Nair, Ajit Krishnan, Angad Pratap, and Wing Commander "
                "Shubhanshu Shukla. The seven-day mission will conduct microgravity "
                "experiments and mark India's entry into human spaceflight."
            ),
            "is_job": False,
        },
        {
            "title":   "Google DeepMind Releases AlphaCode 3 — Solves 90% of Competitive Problems",
            "source":  "reuters.com",
            "image":   _IMAGES["code"],
            "snippet": "The new model outperforms the median competitor on Codeforces, Div. 1 contests.",
            "link":    "https://reuters.com/",
            "long_desc": (
                "AlphaCode 3 achieves an estimated Elo of 1,980 on Codeforces, placing "
                "it in the top 2% of all registered competitive programmers globally. "
                "The model uses a chain-of-thought reasoning backbone combined with "
                "a novel self-debugging loop that fixes 78% of wrong submissions."
            ),
            "is_job": False,
        },
    ]


def _investor():
    return [
        {
            "title":   "Sensex Surges 1,200 Points — IT & Banking Stocks Lead",
            "source":  "moneycontrol.com",
            "image":   _IMAGES["stock"],
            "snippet": "BSE Sensex closes at 82,450 as FII inflows hit a 3-month high.",
            "link":    "https://www.moneycontrol.com/",
            "long_desc": (
                "Foreign institutional investors pumped ₹9,800 crore into Indian "
                "equities on Thursday, reversing four weeks of outflows. TCS, "
                "Infosys, HDFC Bank, and Reliance led the rally, contributing "
                "600+ points to the Sensex move."
            ),
            "is_job": False,
        },
        {
            "title":   "RBI Keeps Repo Rate Unchanged at 6.5% — What It Means for You",
            "source":  "economictimes.indiatimes.com",
            "image":   _IMAGES["finance"],
            "snippet": "MPC holds rates for the fifth consecutive meeting; stance remains 'withdrawal of accommodation'.",
            "link":    "https://economictimes.indiatimes.com/",
            "long_desc": (
                "The RBI's six-member Monetary Policy Committee voted 5-1 to keep "
                "the benchmark repo rate at 6.5%. Governor Shaktikanta Das cited "
                "moderating core inflation but flagged food price volatility as a "
                "near-term risk. EMIs on floating-rate loans remain unchanged."
            ),
            "is_job": False,
        },
        {
            "title":   "Gold Hits All-Time High of ₹78,500 per 10g",
            "source":  "nseindia.com",
            "image":   _IMAGES["stock"],
            "snippet": "Safe-haven demand driven by geopolitical tensions and dollar weakness.",
            "link":    "https://nseindia.com/",
            "long_desc": (
                "MCX Gold futures breached the ₹78,500 mark for the first time, "
                "extending a 14% year-to-date rally. Analysts at Kotak Securities "
                "set a 12-month target of ₹85,000 per 10g, citing sustained central-"
                "bank buying and a weakening US dollar index."
            ),
            "is_job": False,
        },
    ]


def _engineer():
    return [
        {
            "title":   "IEEE Releases 802.11bn: Wi-Fi 8 Standard Finalised",
            "source":  "ieee.org",
            "image":   _IMAGES["chip"],
            "snippet": "Next-gen Wi-Fi promises 100 Gbps theoretical throughput and sub-millisecond latency.",
            "link":    "https://ieee.org/",
            "long_desc": (
                "Wi-Fi 8 (802.11bn) introduces 320 MHz channels, 16-stream MIMO, "
                "and Multi-AP Coordination to virtually eliminate dead zones. The "
                "standard is expected in consumer devices by Q3 2027, with enterprise "
                "deployments starting as early as Q1 2027."
            ),
            "is_job": False,
        },
        {
            "title":   "NVIDIA Blackwell B200 GPU Benchmarks Leak — 3× Hopper Performance",
            "source":  "techcrunch.com",
            "image":   _IMAGES["chip"],
            "snippet": "Early benchmarks show unprecedented LLM inference throughput and energy efficiency.",
            "link":    "https://techcrunch.com/",
            "long_desc": (
                "Leaked benchmark sheets from a major hyperscaler show the B200 "
                "delivering 4.5 PetaFLOPs of FP8 throughput per card — roughly 3× "
                "the H100 — while consuming only 25% more power. Cloud vendors are "
                "expected to offer B200 instances by mid-2026."
            ),
            "is_job": False,
        },
        {
            "title":   "Quantum Computing Breakthrough: 1,000-Qubit Chip Achieves Error Correction",
            "source":  "arxiv.org",
            "image":   _IMAGES["research"],
            "snippet": "Google Quantum AI paper demonstrates logical qubit fidelity of 99.9% at scale.",
            "link":    "https://arxiv.org/",
            "long_desc": (
                "The preprint describes a 1,121-physical-qubit processor that "
                "encodes 49 logical qubits with below-threshold error rates. "
                "This is a landmark step toward fault-tolerant quantum computing "
                "that could break RSA-2048 encryption within a decade."
            ),
            "is_job": False,
        },
    ]


def _farmer():
    return [
        {
            "title":   "PM-KISAN 18th Installment Released: ₹2,000 Credited to 9 Crore Farmers",
            "source":  "pmkisan.gov.in",
            "image":   _IMAGES["farm"],
            "snippet": "Beneficiaries can check payment status at pmkisan.gov.in using Aadhaar number.",
            "link":    "https://pmkisan.gov.in/",
            "long_desc": (
                "The 18th installment of PM-KISAN was released on 5 October 2026, "
                "transferring ₹2,000 directly to 9.3 crore eligible farmer families. "
                "The scheme has now disbursed over ₹3.45 lakh crore since its "
                "inception in 2019, providing critical income support."
            ),
            "is_job": False,
        },
        {
            "title":   "Agmarknet: Onion Prices Drop 18% After Kharif Arrivals Surge",
            "source":  "agmarknet.gov.in",
            "image":   _IMAGES["farm"],
            "snippet": "Wholesale onion prices fall to ₹18/kg at Lasalgaon mandi as new crop arrives.",
            "link":    "https://agmarknet.gov.in/",
            "long_desc": (
                "The Lasalgaon Agricultural Produce Market Committee reported a "
                "bumper kharif onion crop arriving from Nashik district. Prices "
                "corrected sharply from ₹22/kg to ₹18/kg, providing relief to "
                "consumers but posing margin pressure for traders."
            ),
            "is_job": False,
        },
        {
            "title":   "Krishi Jagran: Drone Spraying Subsidy of ₹40,000 Now Available",
            "source":  "krishijagran.com",
            "image":   _IMAGES["farm"],
            "snippet": "SMAM scheme offers up to 50% subsidy on agricultural drones for small farmers.",
            "link":    "https://krishijagran.com/",
            "long_desc": (
                "Under the Sub-Mission on Agricultural Mechanization, small and "
                "marginal farmers can receive up to ₹40,000 (50% of cost) as subsidy "
                "for purchasing DGCA-approved agricultural drones. Applications are "
                "open through the local Krishi Vigyan Kendra."
            ),
            "is_job": False,
        },
    ]


def _sports():
    return [
        {
            "title":   "India Beat Australia by 6 Wickets in 2nd T20I — Series Level at 1-1",
            "source":  "espncricinfo.com",
            "image":   _IMAGES["cricket"],
            "snippet": "Suryakumar Yadav smashes 89* off 47 balls to chase down 183 with 5 balls to spare.",
            "link":    "https://www.espncricinfo.com/",
            "long_desc": (
                "India's chase of 183 was anchored by a blazing Suryakumar Yadav "
                "knock that included 8 sixes and 7 fours. Jasprit Bumrah earlier "
                "claimed 4/22 to restrict Australia. The series decider will be "
                "played in Hyderabad on 14 October."
            ),
            "is_job": False,
        },
        {
            "title":   "FIFA World Cup 2026 Draw: India in Group D with Brazil & Germany",
            "source":  "espn.com",
            "image":   _IMAGES["sports"],
            "snippet": "Historic first: India qualify for the FIFA World Cup — face daunting Group of Death.",
            "link":    "https://espn.com/",
            "long_desc": (
                "In a landmark moment for Indian football, the Blue Tigers were drawn "
                "into Group D alongside Brazil, Germany, and Morocco. Head coach "
                "Igor Stimac called it 'the greatest challenge and greatest honour' "
                "in Indian football history. Matches kick off 15 June 2026."
            ),
            "is_job": False,
        },
        {
            "title":   "Formula 1: Lando Norris Wins Singapore GP — Title Race Wide Open",
            "source":  "skysports.com",
            "image":   _IMAGES["sports"],
            "snippet": "McLaren's Norris cuts Verstappen's lead to 47 points with 6 races remaining.",
            "link":    "https://www.skysports.com/",
            "long_desc": (
                "Lando Norris converted pole into victory at the Marina Bay Street "
                "Circuit, benefiting from a late safety car that caught Max Verstappen "
                "on a two-stop strategy. The championship fight heads to Japan, "
                "Austin, Mexico City, and São Paulo — every point matters now."
            ),
            "is_job": False,
        },
    ]


def _politics():
    return [
        {
            "title":   "India Assumes G20 Presidency for Second Time in 2026",
            "source":  "reuters.com",
            "image":   _IMAGES["politics"],
            "snippet": "PM Modi chairs the inaugural session — climate finance and AI governance top agenda.",
            "link":    "https://reuters.com/",
            "long_desc": (
                "India's G20 presidency focuses on three pillars: climate-resilient "
                "infrastructure, AI regulation frameworks, and debt relief for "
                "developing nations. The summit will take place in New Delhi in "
                "November, with 43 world leaders expected to attend."
            ),
            "is_job": False,
        },
        {
            "title":   "US Presidential Election 2028: Early Polling Shows Tight Race",
            "source":  "apnews.com",
            "image":   _IMAGES["politics"],
            "snippet": "New AP-NORC poll shows approval ratings within the margin of error for both parties.",
            "link":    "https://apnews.com/",
            "long_desc": (
                "A national poll of 2,400 registered voters conducted 1-4 October "
                "shows the Democratic and Republican candidates tied at 46% each, "
                "with 8% undecided. Key battleground states — Pennsylvania, "
                "Georgia, and Arizona — will likely decide the outcome."
            ),
            "is_job": False,
        },
    ]


def _researcher():
    return [
        {
            "title":   "Nature: New mRNA Vaccine Shows 94% Efficacy Against Dengue",
            "source":  "researchgate.net",
            "image":   _IMAGES["research"],
            "snippet": "Phase-III trial across 12,000 participants in India, Brazil, and Thailand.",
            "link":    "https://www.researchgate.net/",
            "long_desc": (
                "Researchers at the Serum Institute of India and Pfizer jointly "
                "published Phase-III results for an mRNA-based dengue vaccine. "
                "The vaccine achieved 94% efficacy against severe dengue and "
                "showed no serious adverse events, paving the way for WHO prequalification."
            ),
            "is_job": False,
        },
        {
            "title":   "arXiv: Transformer Architecture Achieves Human-Level Math Reasoning",
            "source":  "arxiv.org",
            "image":   _IMAGES["research"],
            "snippet": "Google DeepMind's model scores 90th percentile on IMO 2026 problems.",
            "link":    "https://arxiv.org/",
            "long_desc": (
                "AlphaProof 2, described in a 56-page preprint, combines a "
                "fine-tuned Gemini backbone with a Monte Carlo Tree Search over "
                "formal Lean 4 proofs. The system solved 5 of 6 problems at the "
                "2026 International Mathematical Olympiad, achieving gold-medal standard."
            ),
            "is_job": False,
        },
        {
            "title":   "Google Scholar: Most-Cited Papers of 2026 — AI Dominates Top 10",
            "source":  "scholar.google.com",
            "image":   _IMAGES["ai"],
            "snippet": "8 of the 10 most-cited papers of 2026 relate to large language models or AI safety.",
            "link":    "https://scholar.google.com/",
            "long_desc": (
                "The annual Google Scholar citation report reveals that AI research "
                "now accounts for 31% of all indexed papers — up from 18% in 2022. "
                "The top-cited paper, 'Constitutional AI' by Anthropic, has amassed "
                "over 14,000 citations in under 18 months."
            ),
            "is_job": False,
        },
    ]


def _esports():
    return [
        {
            "title":   "Team Liquid Wins Worlds 2026 — Beating T1 in a Historic 5-Game Final",
            "source":  "esportsinsider.com",
            "image":   _IMAGES["esports"],
            "snippet": "Liquid's BWIPO delivers an MVP performance to claim the Summoner's Cup in Seoul.",
            "link":    "https://esportsinsider.com/",
            "long_desc": (
                "In front of 40,000 fans at the KSPO Dome, Team Liquid defeated "
                "T1 3-2 in an electrifying Worlds final. BWIPO's Irelia in Game 5 "
                "was widely praised as one of the greatest competitive League of "
                "Legends performances ever witnessed."
            ),
            "is_job": False,
        },
        {
            "title":   "Navi Wins CS2 Major Copenhagen — s1mple Breaks Fragfest Record",
            "source":  "liquipedia.net",
            "image":   _IMAGES["esports"],
            "snippet": "s1mple records 42 kills in the Grand Final, the highest ever in a CS Major.",
            "link":    "https://liquipedia.net/counterstrike/",
            "long_desc": (
                "Natus Vincere swept FaZe Clan 2-0 at the CS2 Copenhagen Major, "
                "with s1mple posting a 1.48 HLTV rating over the entire tournament. "
                "The victory marks s1mple's first Major title since the Stockholm "
                "Major 2021, completing his career Grand Slam."
            ),
            "is_job": False,
        },
    ]


def _freelancer():
    return [
        {
            "title":   "Upwork Report: AI Prompt Engineering is the Fastest-Growing Freelance Skill",
            "source":  "upwork.com",
            "image":   _IMAGES["freelance"],
            "snippet": "Prompt engineers earn an average of $75/hr on Upwork — up 120% year-over-year.",
            "link":    "https://upwork.com/",
            "long_desc": (
                "Upwork's Q3 2026 Skills Index shows AI Prompt Engineering topping "
                "the fastest-growing skills list for the third consecutive quarter. "
                "Top earners combine domain expertise (legal, medical, finance) with "
                "prompt crafting to command $150+ per hour from enterprise clients."
            ),
            "is_job": False,
        },
        {
            "title":   "Fiverr Launches Fiverr Pro AI — Curated Marketplace for Top 1% Freelancers",
            "source":  "fiverr.com",
            "image":   _IMAGES["freelance"],
            "snippet": "Hand-vetted AI specialists in design, development, and content now on one platform.",
            "link":    "https://fiverr.com/",
            "long_desc": (
                "Fiverr Pro AI is an invite-only tier connecting enterprise clients "
                "with the platform's top-rated AI-fluent freelancers. Accepted "
                "sellers gain access to a dedicated account manager, priority search "
                "placement, and average project values of $2,500+."
            ),
            "is_job": False,
        },
    ]


def _internship():
    return [
        {
            "title":   "Google STEP Internship 2026 Applications Open — ₹3L Stipend",
            "source":  "internshala.com",
            "image":   _IMAGES["internship"],
            "snippet": "Student Training in Engineering Program for pre-final year CS undergrads.",
            "link":    "https://internshala.com/",
            "long_desc": (
                "Google's STEP (Student Training in Engineering Program) is a "
                "12-week paid internship for first and second-year computer science "
                "students. Interns work on real Google products under a dedicated "
                "mentor and are fast-tracked to full SWE interviews post-completion."
            ),
            "is_job": False,
        },
        {
            "title":   "Microsoft Engage 2026: 500 Internship Spots for Engineering Students",
            "source":  "unstop.com",
            "image":   _IMAGES["microsoft"],
            "snippet": "8-week program with ₹60,000/month stipend and full-time offer on successful completion.",
            "link":    "https://unstop.com/",
            "long_desc": (
                "Microsoft Engage is a 8-week immersive internship program for "
                "pre-final year engineering students. Participants build a full-stack "
                "feature inside a Microsoft product team, and top performers receive "
                "a full-time SDE offer at the end."
            ),
            "is_job": False,
        },
        {
            "title":   "Goldman Sachs Summer Analyst 2026: Finance & Tech Roles Now Open",
            "source":  "linkedin.com",
            "image":   _IMAGES["finance"],
            "snippet": "10-week program across engineering, risk, and investment banking divisions.",
            "link":    "https://www.linkedin.com/company/goldman-sachs/jobs/",
            "long_desc": (
                "Goldman Sachs is hiring Summer Analysts across its Engineering, "
                "Securities, and Investment Banking divisions. The program runs "
                "June–August 2026, offering $15,000/month compensation and a "
                "structured networking programme with senior leaders."
            ),
            "is_job": False,
        },
    ]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_DOMAIN_MAP = {
    "job_seeker":        _jobs,
    "student":           _student,
    "general_reader":    _general,
    "investor":          _investor,
    "engineer":          _engineer,
    "farmer":            _farmer,
    "sports_fan":        _sports,
    "politician":        _politics,
    "researcher":        _researcher,
    "esports_fan":       _esports,
    "freelancer":        _freelancer,
    "internship_seeker": _internship,
}


def get_mock_data(domain: str) -> list:
    """
    Return a list of article/job dicts for the given domain slug.

    Falls back to general news if the domain is unknown.
    All returned dicts include every key expected by the Jinja2 template:
        title, source, image, snippet, link, long_desc, is_job,
        requirements (list, only when is_job=True), company_class (str).
    """
    factory = _DOMAIN_MAP.get(domain, _general)
    results = factory()

    # Guarantee every dict has the optional keys so templates never KeyError
    for item in results:
        item.setdefault("long_desc",     "")
        item.setdefault("is_job",        False)
        item.setdefault("requirements",  [])
        item.setdefault("company_class", "")
        item.setdefault("image",         "")

    return results


# ---------------------------------------------------------------------------
# Landing Page / Intro Page Curated News Catalog
# ---------------------------------------------------------------------------

def _all_landing_stories():
    return [
        # --- TECHNOLOGY ---
        {
            "id": "tech-1",
            "title": "The Future of AI: What to Expect in 2026",
            "source": "TechCrunch",
            "category": "technology",
            "category_label": "Technology & AI",
            "image": _IMAGES["ai"],
            "snippet": "Artificial intelligence continues to evolve at a breakneck pace across every industry, from autonomous agents to multimodal reasoning.",
            "link": "https://techcrunch.com/",
            "long_desc": (
                "Experts predict that by the end of 2026, AI models will not only generate content but "
                "autonomously orchestrate complex software ecosystems — improving development speed "
                "and reliability by up to 40%. Agentic workflows, multi-modal reasoning, and real-time "
                "collaboration are the three defining trends of the year. Enterprise adoption has quadrupled "
                "as verifiable safety frameworks mature."
            ),
            "published_at": "15 mins ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#ArtificialIntelligence", "#TechTrends", "#Innovation"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "tech-2",
            "title": "NVIDIA Blackwell B200 GPU Benchmarks Leak — 3× Hopper Performance",
            "source": "techcrunch.com",
            "category": "technology",
            "category_label": "Technology & AI",
            "image": _IMAGES["chip"],
            "snippet": "Early benchmarks show unprecedented LLM inference throughput and groundbreaking energy efficiency.",
            "link": "https://techcrunch.com/",
            "long_desc": (
                "Leaked benchmark sheets from a major hyperscaler show the B200 delivering 4.5 PetaFLOPs "
                "of FP8 throughput per card — roughly 3× the H100 — while consuming only 25% more power. "
                "Cloud vendors are rolling out B200 clusters to accelerate next-generation frontier training runs."
            ),
            "published_at": "45 mins ago",
            "read_time": "4 min read",
            "likes": 0,
            "tags": ["#NVIDIA", "#Hardware", "#Blackwell", "#Semiconductors"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "tech-3",
            "title": "Apple Unveils M4 Ultra Silicon Architecture with 32-Core Neural Engine",
            "source": "theverge.com",
            "category": "technology",
            "category_label": "Technology & AI",
            "image": _IMAGES["apple"],
            "snippet": "New silicon breakthrough enables 100-billion-parameter local model execution on creative workstations.",
            "link": "https://theverge.com/",
            "long_desc": (
                "Apple's silicon roadmap reached a new milestone with the formal announcement of the M4 Ultra. "
                "Built on TSMC's 3nm generation-two process, the processor features 32 unified neural cores "
                "delivering 120 trillion operations per second, targeting on-device multimodal generation and "
                "high-performance creative workflows."
            ),
            "published_at": "2 hours ago",
            "read_time": "4 min read",
            "likes": 0,
            "tags": ["#Apple", "#M4", "#Hardware", "#Silicon"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "tech-4",
            "title": "Google DeepMind Releases AlphaCode 3 — Solves 90% of Competitive Problems",
            "source": "reuters.com",
            "category": "technology",
            "category_label": "Technology & AI",
            "image": _IMAGES["code"],
            "snippet": "The new model outperforms the median competitor on Codeforces, Div. 1 contests with self-debugging.",
            "link": "https://reuters.com/",
            "long_desc": (
                "AlphaCode 3 achieves an estimated Elo of 1,980 on Codeforces, placing it in the top 2% of all "
                "registered competitive programmers globally. The model uses a chain-of-thought reasoning "
                "backbone combined with a novel self-debugging loop that fixes 78% of wrong submissions."
            ),
            "published_at": "3 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#DeepMind", "#Programming", "#AI"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "tech-5",
            "title": "IEEE Releases 802.11bn: Wi-Fi 8 Standard Finalised",
            "source": "ieee.org",
            "category": "technology",
            "category_label": "Technology & AI",
            "image": _IMAGES["chip"],
            "snippet": "Next-gen Wi-Fi promises 100 Gbps theoretical throughput and sub-millisecond latency for dense spaces.",
            "link": "https://ieee.org/",
            "long_desc": (
                "Wi-Fi 8 (802.11bn) introduces 320 MHz channels, 16-stream MIMO, and Multi-AP Coordination to "
                "virtually eliminate dead zones. The standard is expected in consumer devices by Q3 2027, with "
                "enterprise deployments starting as early as Q1 2027."
            ),
            "published_at": "4 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#Networking", "#WiFi8", "#Technology"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "tech-6",
            "title": "OpenAI Announces Developer Preview for Native Agent Workflows",
            "source": "wired.com",
            "category": "technology",
            "category_label": "Technology & AI",
            "image": _IMAGES["ai"],
            "snippet": "New developer tooling enables multi-agent swarms with built-in memory, sandboxing, and state management.",
            "link": "https://wired.com/",
            "long_desc": (
                "At a dedicated developer briefing, OpenAI introduced its first-party framework for building "
                "persistent autonomous agents. The toolkit natively handles asynchronous state synchronization, "
                "parallel tool execution, and automated safety sandboxing, radically lowering the barrier for "
                "building agentic enterprise workflows."
            ),
            "published_at": "6 hours ago",
            "read_time": "5 min read",
            "likes": 0,
            "tags": ["#OpenAI", "#Agents", "#ArtificialIntelligence"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },

        # --- BUSINESS & FINANCE ---
        {
            "id": "biz-1",
            "title": "Global Markets Rally on Strong Tech Earnings and Rate Optimism",
            "source": "Bloomberg",
            "category": "business",
            "category_label": "Business & Finance",
            "image": _IMAGES["finance"],
            "snippet": "Stock markets hit record highs following stronger-than-expected Q3 earnings and cooling inflation figures.",
            "link": "https://bloomberg.com/",
            "long_desc": (
                "Investors showed renewed optimism as major technology and industrial firms posted record profits, "
                "driven by enterprise software and infrastructure demand. The S&P 500 crossed 6,200 points while the "
                "Nasdaq hit an all-time high of 22,400, with institutional liquidity remaining robust."
            ),
            "published_at": "30 mins ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#StockMarket", "#Earnings", "#Economy", "#Finance"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "biz-2",
            "title": "Sensex Surges 1,200 Points — IT & Banking Stocks Lead Massive Rally",
            "source": "moneycontrol.com",
            "category": "business",
            "category_label": "Business & Finance",
            "image": _IMAGES["stock"],
            "snippet": "BSE Sensex closes near 83,000 as Foreign Institutional Investor inflows hit a 3-month high.",
            "link": "https://www.moneycontrol.com/",
            "long_desc": (
                "Foreign institutional investors pumped ₹9,800 crore into Indian equities on Thursday, reversing "
                "four weeks of outflows. TCS, Infosys, HDFC Bank, and Reliance led the rally, contributing 600+ "
                "points to the Sensex move as economic growth momentum remains resilient."
            ),
            "published_at": "1 hour ago",
            "read_time": "2 min read",
            "likes": 0,
            "tags": ["#Sensex", "#Nifty", "#IndianMarkets", "#Investing"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "biz-3",
            "title": "Gold Hits All-Time High of ₹78,500 per 10g Driven by Safe-Haven Inflows",
            "source": "nseindia.com",
            "category": "business",
            "category_label": "Business & Finance",
            "image": _IMAGES["stock"],
            "snippet": "Safe-haven demand driven by central bank purchases and currency diversification pushes bullion to records.",
            "link": "https://nseindia.com/",
            "long_desc": (
                "MCX Gold futures breached the ₹78,500 mark for the first time, extending a 14% year-to-date rally. "
                "Analysts at Kotak Securities set a 12-month target of ₹85,000 per 10g, citing sustained central-bank "
                "buying and a weakening US dollar index."
            ),
            "published_at": "3 hours ago",
            "read_time": "2 min read",
            "likes": 0,
            "tags": ["#Gold", "#Commodities", "#PreciousMetals"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "biz-4",
            "title": "RBI Keeps Repo Rate Unchanged at 6.5% — Stability in Lending Rates",
            "source": "economictimes.indiatimes.com",
            "category": "business",
            "category_label": "Business & Finance",
            "image": _IMAGES["finance"],
            "snippet": "Monetary Policy Committee maintains rate pause while watching food price volatility.",
            "link": "https://economictimes.indiatimes.com/",
            "long_desc": (
                "The RBI's six-member Monetary Policy Committee voted 5-1 to keep the benchmark repo rate at 6.5%. "
                "Governor Shaktikanta Das cited moderating core inflation but flagged food price volatility as a "
                "near-term risk. Home loan and automobile EMIs remain stable for borrowers."
            ),
            "published_at": "5 hours ago",
            "read_time": "4 min read",
            "likes": 0,
            "tags": ["#RBI", "#InterestRates", "#Economy", "#Banking"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "biz-5",
            "title": "Electric Vehicle Sales Surge 45% as Battery Pack Prices Drop Below $80/kWh",
            "source": "wsj.com",
            "category": "business",
            "category_label": "Business & Finance",
            "image": _IMAGES["ev"],
            "snippet": "Cost parity with combustion engine vehicles arrives earlier than anticipated across global markets.",
            "link": "https://wsj.com/",
            "long_desc": (
                "Global passenger electric vehicle registrations crossed 3.2 million units last quarter, boosted by "
                "plummeting lithium iron phosphate cell costs. Automakers are expanding affordable models across "
                "Asia, Europe, and Latin America, accelerating consumer adoption."
            ),
            "published_at": "7 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#ElectricVehicles", "#CleanEnergy", "#Automotive"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },

        # --- SCIENCE & SPACE ---
        {
            "id": "sci-1",
            "title": "ISRO's Gaganyaan Mission: Astronaut Crew Announced for Historic 2026 Orbit",
            "source": "NDTV",
            "category": "science",
            "category_label": "Science & Space",
            "image": _IMAGES["space"],
            "snippet": "India's first crewed spaceflight will carry designated astronauts to a 400 km low-Earth orbit.",
            "link": "https://ndtv.com/",
            "long_desc": (
                "ISRO officially named the four-member Gaganyaan crew: Group Captains Prashanth Nair, Ajit Krishnan, "
                "Angad Pratap, and Wing Commander Shubhanshu Shukla. The mission will conduct critical microgravity "
                "experiments and validate India's human-rated launch vehicle systems."
            ),
            "published_at": "25 mins ago",
            "read_time": "4 min read",
            "likes": 0,
            "tags": ["#ISRO", "#Gaganyaan", "#SpaceExploration", "#India"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "sci-2",
            "title": "Quantum Computing Milestone: 1,000-Qubit Chip Demonstrates Real-Time Error Correction",
            "source": "arxiv.org",
            "category": "science",
            "category_label": "Science & Space",
            "image": _IMAGES["research"],
            "snippet": "Google Quantum AI paper demonstrates logical qubit fidelity of 99.9% at multi-hundred scale.",
            "link": "https://arxiv.org/",
            "long_desc": (
                "The preprint describes a 1,121-physical-qubit processor that encodes 49 logical qubits with "
                "below-threshold error rates. This is a foundational step toward fault-tolerant quantum computing "
                "that can simulate complex molecular chemistry and optimization."
            ),
            "published_at": "2 hours ago",
            "read_time": "4 min read",
            "likes": 0,
            "tags": ["#QuantumComputing", "#Physics", "#DeepTech"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "sci-3",
            "title": "Nature: New mRNA Vaccine Shows 94% Efficacy Against Severe Dengue Strains",
            "source": "researchgate.net",
            "category": "science",
            "category_label": "Science & Space",
            "image": _IMAGES["research"],
            "snippet": "Phase-III international clinical trial across 12,000 participants produces breakthrough protective results.",
            "link": "https://www.researchgate.net/",
            "long_desc": (
                "Researchers at the Serum Institute of India and Pfizer jointly published Phase-III results for "
                "an mRNA-based quadrivalent dengue vaccine. The vaccine achieved 94% efficacy against severe dengue and "
                "showed zero serious adverse events, clearing the path for expedited WHO prequalification."
            ),
            "published_at": "4 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#Health", "#Vaccines", "#Medicine", "#Science"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "sci-4",
            "title": "James Webb Telescope Confirms Water Vapor and Atmosphere on Rocky Exoplanet",
            "source": "nasa.gov",
            "category": "science",
            "category_label": "Science & Space",
            "image": _IMAGES["space"],
            "snippet": "High-precision transmission spectroscopy of LHS 1140 b detects clear atmospheric signatures.",
            "link": "https://nasa.gov/",
            "long_desc": (
                "Astronomers utilizing transmission spectroscopy data from the James Webb Space Telescope announced "
                "the definitive detection of water vapor and carbon dioxide signatures on exoplanet LHS 1140 b, "
                "a temperate rocky world located 48 light-years away in the constellation Cetus."
            ),
            "published_at": "6 hours ago",
            "read_time": "4 min read",
            "likes": 0,
            "tags": ["#NASA", "#JWST", "#Astronomy", "#Exoplanets"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "sci-5",
            "title": "Magnetic Confinement Fusion Reactor Sustains Net Energy Gain for 20 Minutes",
            "source": "nature.com",
            "category": "science",
            "category_label": "Science & Space",
            "image": _IMAGES["fusion"],
            "snippet": "Superconducting tokamak creates stable 100-million-degree plasma with net 1.4x electrical gain.",
            "link": "https://nature.com/",
            "long_desc": (
                "The Western Magnetic Fusion facility maintained a continuous burning plasma state delivering "
                "35 MW equivalent thermal output from a 25 MW heating input over twenty unbroken minutes, "
                "confirming steady-state reactor physics for grid-scale fusion installations."
            ),
            "published_at": "8 hours ago",
            "read_time": "5 min read",
            "likes": 0,
            "tags": ["#FusionEnergy", "#CleanTech", "#Physics"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },

        # --- SPORTS ---
        {
            "id": "spt-1",
            "title": "India Beat Australia by 6 Wickets in 2nd T20I — Series Level at 1-1",
            "source": "espncricinfo.com",
            "category": "sports",
            "category_label": "Sports",
            "image": _IMAGES["cricket"],
            "snippet": "Suryakumar Yadav smashes a breathtaking 89* off 47 balls to chase down 183 with 5 balls to spare.",
            "link": "https://www.espncricinfo.com/",
            "long_desc": (
                "India's chase of 183 was anchored by a blazing Suryakumar Yadav knock that included 8 sixes and "
                "7 boundaries. Jasprit Bumrah earlier claimed 4/22 to restrict Australia. The thrilling series "
                "decider will be played in Hyderabad this Sunday."
            ),
            "published_at": "10 mins ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#Cricket", "#TeamIndia", "#T20", "#Sports"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "spt-2",
            "title": "FIFA World Cup 2026 Draw: India in Group D Alongside Brazil and Germany",
            "source": "espn.com",
            "category": "sports",
            "category_label": "Sports",
            "image": _IMAGES["sports"],
            "snippet": "Historic qualification for the FIFA World Cup brings daunting matchups against traditional football powerhouses.",
            "link": "https://espn.com/",
            "long_desc": (
                "In a landmark moment for Indian football, the Blue Tigers were drawn into Group D alongside Brazil, "
                "Germany, and Morocco. Head coach Igor Stimac described the matchup as 'the greatest challenge and "
                "highest honour' in the country's sporting history."
            ),
            "published_at": "1 hour ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#Football", "#WorldCup", "#FIFA2026", "#BlueTigers"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "spt-3",
            "title": "Formula 1: Lando Norris Wins Singapore GP — Drivers' Title Battle Tightens",
            "source": "skysports.com",
            "category": "sports",
            "category_label": "Sports",
            "image": _IMAGES["sports"],
            "snippet": "McLaren driver converts pole position into a commanding night race victory under Marina Bay lights.",
            "link": "https://www.skysports.com/",
            "long_desc": (
                "Lando Norris converted pole into victory at the Marina Bay Street Circuit, managing tire degradation "
                "superbly despite a late safety car restart. The championship fight now heads to Austin and Mexico "
                "with the gap narrowed to just 47 points."
            ),
            "published_at": "3 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#Formula1", "#F1", "#LandoNorris", "#Motorsport"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "spt-4",
            "title": "Team Liquid Wins Worlds 2026 — Defeating T1 in Historic 5-Game Grand Final",
            "source": "esportsinsider.com",
            "category": "sports",
            "category_label": "Sports",
            "image": _IMAGES["esports"],
            "snippet": "Liquid captures the Summoner's Cup in Seoul before 40,000 roaring fans in an all-time classic.",
            "link": "https://esportsinsider.com/",
            "long_desc": (
                "In front of 40,000 fans at the KSPO Dome, Team Liquid defeated T1 3-2 in an electrifying Worlds final. "
                "BWIPO's Irelia in Game 5 was widely praised as one of the greatest competitive League of Legends "
                "performances ever witnessed on the international stage."
            ),
            "published_at": "5 hours ago",
            "read_time": "4 min read",
            "likes": 0,
            "tags": ["#Esports", "#LeagueOfLegends", "#Worlds2026", "#Gaming"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "spt-5",
            "title": "Navi Wins CS2 Major Copenhagen — s1mple Sets All-Time Frag Record",
            "source": "liquipedia.net",
            "category": "sports",
            "category_label": "Sports",
            "image": _IMAGES["esports"],
            "snippet": "s1mple records 42 kills in the Grand Final to sweep FaZe Clan and claim another MVP crown.",
            "link": "https://liquipedia.net/counterstrike/",
            "long_desc": (
                "Natus Vincere swept FaZe Clan 2-0 at the CS2 Copenhagen Major, with s1mple posting a 1.48 HLTV rating "
                "over the entire tournament. The victory marks another milestone in the legendary player's storied "
                "esports journey."
            ),
            "published_at": "7 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#CS2", "#Esports", "#Navi", "#Gaming"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },

        # --- EDUCATION & CAREERS ---
        {
            "id": "edu-1",
            "title": "PM Scholarship 2026: Applications Open for ₹75,000 Annual Higher Education Grant",
            "source": "scholarships.gov.in",
            "category": "education",
            "category_label": "Education & Careers",
            "image": _IMAGES["campus"],
            "snippet": "Central sector scholarship scheme for undergraduate and professional students — deadline 31 Oct.",
            "link": "https://scholarships.gov.in/",
            "long_desc": (
                "The Central Sector Scheme of Scholarships covers tuition and maintenance allowance for meritorious "
                "students from low-income families. Eligible candidates must have scored above 80% in Class 12 and "
                "belong to the top 20 percentile of their respective state or central board."
            ),
            "published_at": "35 mins ago",
            "read_time": "2 min read",
            "likes": 0,
            "tags": ["#Scholarships", "#Students", "#Education", "#College"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "edu-2",
            "title": "GeeksForGeeks Launches Free DSA Mastery Curriculum for 2026 Campus Placements",
            "source": "geeksforgeeks.org",
            "category": "education",
            "category_label": "Education & Careers",
            "image": _IMAGES["code"],
            "snippet": "180-hour self-paced path covering dynamic programming, graphs, and scalable system design.",
            "link": "https://www.geeksforgeeks.org/",
            "long_desc": (
                "GFG's new DSA Mastery path includes 500 curated problems, weekly live doubt sessions, and a "
                "verified certificate recognised by top product-based hiring teams including Google, Amazon, "
                "Microsoft, and Flipkart campus recruitment drives."
            ),
            "published_at": "2 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#Coding", "#DSA", "#Placements", "#ComputerScience"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "edu-3",
            "title": "Google STEP Internship 2026 Applications Open — Mentorship & ₹3 Lakh Stipend",
            "source": "internshala.com",
            "category": "education",
            "category_label": "Education & Careers",
            "image": _IMAGES["internship"],
            "snippet": "Student Training in Engineering Program invites first and second-year undergraduate developers.",
            "link": "https://internshala.com/",
            "long_desc": (
                "Google's STEP (Student Training in Engineering Program) is a 12-week paid internship for "
                "early-year computer science students. Interns collaborate on production features under a senior mentor "
                "and are fast-tracked to full Software Engineer roles upon graduation."
            ),
            "published_at": "3 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#Internships", "#Google", "#Careers", "#TechJobs"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "edu-4",
            "title": "NPTEL July 2026 Semester: Over 1,200 Free Certification Courses by IIT Faculty",
            "source": "nptel.ac.in",
            "category": "education",
            "category_label": "Education & Careers",
            "image": _IMAGES["study"],
            "snippet": "IIT and IISc professors deliver free online certificate programs across engineering and management.",
            "link": "https://nptel.ac.in/",
            "long_desc": (
                "NPTEL's semester catalog features over 1,200 courses across AI, civil engineering, data science, "
                "and humanities. Courses are free to audit with proctored exams yielding AICTE-recognized credentials "
                "prized by both academic institutions and industry employers."
            ),
            "published_at": "5 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#NPTEL", "#IIT", "#OnlineLearning", "#Certifications"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "edu-5",
            "title": "Upwork Skills Report: AI Prompt Engineering & Workflow Automation Lead Freelance Earnings",
            "source": "upwork.com",
            "category": "education",
            "category_label": "Education & Careers",
            "image": _IMAGES["freelance"],
            "snippet": "Independent contractors specializing in custom AI automation earn average rates exceeding $85/hour.",
            "link": "https://upwork.com/",
            "long_desc": (
                "Upwork's Q3 Skills Index confirms AI prompt engineering and automated workflow development as the "
                "fastest-growing contract specializations. High-earning freelancers combine deep domain context with "
                "API automation to deliver high-ROI digital transformation solutions."
            ),
            "published_at": "7 hours ago",
            "read_time": "4 min read",
            "likes": 0,
            "tags": ["#Freelance", "#RemoteWork", "#GigEconomy"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },

        # --- WORLD & POLITICS ---
        {
            "id": "pol-1",
            "title": "India Assumes G20 Presidency for 2026 — Clean Energy and AI Safety Top Global Agenda",
            "source": "reuters.com",
            "category": "politics",
            "category_label": "World & Politics",
            "image": _IMAGES["politics"],
            "snippet": "Inaugural summit in New Delhi convenes leaders to address international digital infrastructure and climate finance.",
            "link": "https://reuters.com/",
            "long_desc": (
                "India's 2026 G20 presidency focuses on three actionable pillars: climate-resilient infrastructure funding, "
                "multilateral AI governance benchmarks, and sovereign debt restructuring for developing economies. "
                "Delegates from 43 member states and observer organizations are participating in working groups."
            ),
            "published_at": "1 hour ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#G20", "#WorldPolitics", "#Diplomacy", "#India"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "pol-2",
            "title": "Oxford University Study: 4-Day Work Week Boosts Productivity by 22% and Retains Talent",
            "source": "BBC News",
            "category": "politics",
            "category_label": "World & Politics",
            "image": _IMAGES["work"],
            "snippet": "Comprehensive trial tracking 1,000 corporate employers demonstrates clear gains in health and output.",
            "link": "https://bbc.com/news",
            "long_desc": (
                "A landmark 12-month study by Oxford researchers tracked 61 international firms that transitioned "
                "to a 32-hour workweek with no salary reductions. Findings showed a 22% gain in revenue per employee, "
                "a 65% drop in sick days, and a 91% employee retention rate."
            ),
            "published_at": "2 hours ago",
            "read_time": "4 min read",
            "likes": 0,
            "tags": ["#Workplace", "#Productivity", "#GlobalNews", "#Culture"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "pol-3",
            "title": "PM-KISAN 18th Installment Disbursed: ₹2,000 Direct Benefit Sent to 9.3 Crore Farmers",
            "source": "pmkisan.gov.in",
            "category": "politics",
            "category_label": "World & Politics",
            "image": _IMAGES["farm"],
            "snippet": "Direct benefit transfer credits reach agricultural households across states; status live on portal.",
            "link": "https://pmkisan.gov.in/",
            "long_desc": (
                "The 18th installment of the PM-KISAN program disbursed over ₹18,600 crore directly into verified "
                "bank accounts of eligible smallholder farmers. Total cumulative transfers under the welfare initiative "
                "have now surpassed ₹3.45 lakh crore."
            ),
            "published_at": "4 hours ago",
            "read_time": "2 min read",
            "likes": 0,
            "tags": ["#Agriculture", "#Farmers", "#GovtSchemes"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "pol-4",
            "title": "Global Renewable Energy Surpasses 40% of Total Worldwide Electricity Generation",
            "source": "theguardian.com",
            "category": "politics",
            "category_label": "World & Politics",
            "image": _IMAGES["climate"],
            "snippet": "Rapid wind and solar deployment marks historic milestone in international transition away from fossil fuels.",
            "link": "https://theguardian.com/",
            "long_desc": (
                "An International Energy Agency assessment confirms that solar photovoltaic and wind capacity additions "
                "surpassed all conventional fuel sources combined over the past four quarters, pushing clean power "
                "to 40.8% of global electrical grid output."
            ),
            "published_at": "6 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#Climate", "#RenewableEnergy", "#Sustainability"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
        {
            "id": "pol-5",
            "title": "US Presidential Polling: Tight Contest Emerges in Key Midwestern Swing States",
            "source": "apnews.com",
            "category": "politics",
            "category_label": "World & Politics",
            "image": _IMAGES["politics"],
            "snippet": "National and battleground surveys show voter preferences split within statistical margin of error.",
            "link": "https://apnews.com/",
            "long_desc": (
                "Voters in key electoral swing states including Pennsylvania, Wisconsin, and Michigan remain evenly divided "
                "according to recent bipartisan polling. Economic outlook, healthcare policy, and tech regulation remain "
                "top determinants for independent undecided voters."
            ),
            "published_at": "8 hours ago",
            "read_time": "3 min read",
            "likes": 0,
            "tags": ["#WorldNews", "#Elections", "#Politics"],
            "is_job": False,
            "company_class": "",
            "requirements": [],
        },
    ]


def get_landing_news(category: str = "all", query: str = "") -> list:
    """
    Return curated, high-quality news articles for the NewsSphere intro/landing page.

    Supports filtering by category slug ('technology', 'business', 'science',
    'sports', 'education', 'politics') or searching across titles, snippets,
    descriptions, and tags.
    """
    stories = _all_landing_stories()

    # Category filter
    if category and category.lower() != "all":
        cat_lower = category.lower().strip()
        stories = [s for s in stories if s.get("category", "").lower() == cat_lower]

    # Search query filter
    if query and query.strip():
        import re
        q_tokens = [t.lower() for t in query.strip().split() if t.strip()]
        filtered = []
        for s in stories:
            text_corpus = (
                f"{s.get('title', '')} {s.get('snippet', '')} {s.get('source', '')} "
                f"{s.get('long_desc', '')} {s.get('category_label', '')} "
                f"{' '.join(s.get('tags', []))}"
            ).lower()
            
            # Match tokens: if short token (<=3 chars), require word boundary
            matched = False
            for tok in q_tokens:
                if len(tok) <= 3:
                    if re.search(r'(?i)\b' + re.escape(tok) + r'\b', text_corpus):
                        matched = True
                        break
                else:
                    if tok in text_corpus:
                        matched = True
                        break
            if matched:
                filtered.append(s)
        stories = filtered

    return stories

