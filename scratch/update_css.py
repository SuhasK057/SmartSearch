import os

css_path = r"C:\Users\Suhas\Documents\mini project\mini project final\SmartSearch\static\css\style.css"

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Add :root and .light-theme variables
root_vars = """
:root {
    --bg-main: #080b1f;
    --bg-nav: #10142f;
    --bg-card: #10142f;
    --text-primary: white;
    --text-secondary: #aeb2ca;
    --text-tertiary: #858aa9;
    --border-color: #292d55;
    --accent: #7357ff;
    --accent-hover: #9b7cff;
    --sidebar-bg-1: #111633;
    --sidebar-bg-2: #0e122b;
    --card-hover-border: #7357ff;
    --input-bg: #191e42;
}

body.light-theme {
    --bg-main: #f4f5f7;
    --bg-nav: #ffffff;
    --bg-card: #ffffff;
    --text-primary: #1a1a24;
    --text-secondary: #4a4d5e;
    --text-tertiary: #6b6f80;
    --border-color: #e2e4ec;
    --accent: #5a43cc;
    --accent-hover: #4533a1;
    --sidebar-bg-1: #ffffff;
    --sidebar-bg-2: #f9f9fb;
    --card-hover-border: #5a43cc;
    --input-bg: #f0f2f5;
}

.card.expanded {
    /* smooth height transition is typically handled by max-height on the content, but we can add some styling here */
}

/* Extra content inside card */
.extra-content {
    padding: 0 20px 20px;
    color: var(--text-secondary);
}

.read-more-btn {
    background: transparent;
    border: none;
    color: var(--accent);
    cursor: pointer;
    font-weight: bold;
    padding: 10px 20px;
    margin-top: -10px;
}
.read-more-btn:hover {
    color: var(--accent-hover);
    text-decoration: underline;
}

/* Company specific classes */
.google-job {
    border-top: 4px solid #4285F4;
}
.google-job:hover {
    box-shadow: 0 12px 35px rgba(66, 133, 244, 0.2);
}

.amazon-job {
    border-top: 4px solid #FF9900;
}
.amazon-job:hover {
    box-shadow: 0 12px 35px rgba(255, 153, 0, 0.2);
}

.microsoft-job {
    border-top: 4px solid #00A4EF;
}
.microsoft-job:hover {
    box-shadow: 0 12px 35px rgba(0, 164, 239, 0.2);
}

.meta-job, .facebook-job {
    border-top: 4px solid #0668E1;
}

/* Loading Spinner */
.loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border-left-color: var(--accent);
    animation: spin 1s linear infinite;
    display: inline-block;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

"""

# replace body
css = css.replace("body {\n    background: #080b1f;\n\n    color: white;\n}", 
"body {\n    background: var(--bg-main);\n    color: var(--text-primary);\n    transition: background-color 0.3s, color 0.3s;\n}")

# replace .navbar
css = css.replace("background: #10142f;", "background: var(--bg-nav);")
css = css.replace("border-bottom: 1px solid #292d55;", "border-bottom: 1px solid var(--border-color);")

# replace .card
css = css.replace(".card {\n    background: #10142f;\n\n    border: 1px solid #292d55;", 
".card {\n    background: var(--bg-card);\n    border: 1px solid var(--border-color);\n    transition: background-color 0.3s, color 0.3s, transform 0.3s, box-shadow 0.3s, border-color 0.3s;")

# text colors
css = css.replace("color: white;", "color: var(--text-primary);")
css = css.replace("color: #aeb2ca;", "color: var(--text-secondary);")
css = css.replace("color: #858aa9;", "color: var(--text-tertiary);")

# borders
css = css.replace("border: 1px solid #292d55;", "border: 1px solid var(--border-color);")

# .search-box input background
css = css.replace("background: #191e42;", "background: var(--input-bg);")

# Append new styles
new_css = root_vars + "\n" + css

with open(css_path, "w", encoding="utf-8") as f:
    f.write(new_css)

print("CSS updated")
