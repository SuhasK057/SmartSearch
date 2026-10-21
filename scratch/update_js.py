import os

js_path = r"C:\Users\Suhas\Documents\mini project\mini project final\SmartSearch\static\js\script.js"

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Add theme initialization at the very top
theme_init = """// ===================== THEME TOGGLE =====================
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    document.body.classList.add('light-theme');
}

document.addEventListener("DOMContentLoaded", () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = themeToggleBtn ? themeToggleBtn.querySelector('i') : null;

    if (themeIcon) {
        if (document.body.classList.contains('light-theme')) {
            themeIcon.classList.replace('fa-moon', 'fa-sun');
        } else {
            themeIcon.classList.replace('fa-sun', 'fa-moon');
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            document.body.classList.toggle('light-theme');
            const isLight = document.body.classList.contains('light-theme');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
            
            if (isLight) {
                themeIcon.classList.replace('fa-moon', 'fa-sun');
            } else {
                themeIcon.classList.replace('fa-sun', 'fa-moon');
            }
        });
    }

    // ===================== CARD EXPANSION =====================
    const readMoreBtns = document.querySelectorAll('.read-more-btn');
    readMoreBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const extraContent = this.nextElementSibling;
            const card = this.closest('.card');
            
            if (extraContent.style.display === 'none') {
                extraContent.style.display = 'block';
                this.textContent = 'Read Less';
                card.classList.add('expanded');
            } else {
                extraContent.style.display = 'none';
                this.textContent = 'Read More';
                card.classList.remove('expanded');
            }
        });
    });
});

"""

# Replace Like logic
old_like = """// ===================== LIKE BUTTON =====================

const likeButtons = document.querySelectorAll(".like");

// Fetch liked links on page load if there are like buttons
if (likeButtons.length > 0) {
    fetch('/liked_links')
        .then(r => r.json())
        .then(data => {
            const likedLinks = new Set(data.links || []);
            likeButtons.forEach(button => {
                const link = button.dataset.link || '';
                if (likedLinks.has(link)) {
                    button.innerHTML = '<i class="fa-solid fa-heart"></i> Liked';
                    button.style.color = "red";
                }
            });
        })
        .catch(err => console.error(err));
}

likeButtons.forEach(button => {
    button.addEventListener("click", function () {
        const link = button.dataset.link || '';
        if (!link) return;

        const isLiked = button.innerHTML.includes("fa-solid");

        if (isLiked) {
            button.innerHTML = '<i class="fa-regular fa-heart"></i> Like';
            button.style.color = "white";
            fetch('/unlike', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ link: link })
            });
        } else {
            button.innerHTML = '<i class="fa-solid fa-heart"></i> Liked';
            button.style.color = "red";
            fetch('/like', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ link: link })
            });
        }
    });
});"""

new_like = """// ===================== LIKE BUTTON =====================

const likeButtons = document.querySelectorAll(".like");

// Use localStorage to remember liked articles
let localLikes = JSON.parse(localStorage.getItem('likedArticles')) || [];
const likedLinks = new Set(localLikes);

likeButtons.forEach(button => {
    const link = button.dataset.link || '';
    if (likedLinks.has(link)) {
        button.innerHTML = '<i class="fa-solid fa-heart"></i> Liked';
        button.style.color = "red";
    }

    button.addEventListener("click", function () {
        if (!link) return;

        const isLiked = button.innerHTML.includes("fa-solid");

        if (isLiked) {
            // Unlike
            button.innerHTML = '<i class="fa-regular fa-heart"></i> Like';
            button.style.color = document.body.classList.contains('light-theme') ? "black" : "white";
            likedLinks.delete(link);
            fetch('/unlike', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ link: link })
            }).catch(()=>{});
        } else {
            // Like
            button.innerHTML = '<i class="fa-solid fa-heart"></i> Liked';
            button.style.color = "red";
            likedLinks.add(link);
            fetch('/like', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ link: link })
            }).catch(()=>{});
        }
        localStorage.setItem('likedArticles', JSON.stringify(Array.from(likedLinks)));
    });
});"""

js_content = js_content.replace(old_like, new_like)
js_content = theme_init + js_content

# Loading spinner code update for searchForm
old_search = """// ===================== SEARCH =====================
const searchForm = document.getElementById("searchForm");
if (searchForm) {
    searchForm.addEventListener("submit", function () {
        const searchInput = searchForm.querySelector("input[type='text']");
        if (searchInput) {
            searchInput.placeholder = "Searching...";
            searchInput.readOnly = true;
            searchInput.style.opacity = "0.7";
        }
    });
}"""

new_search = """// ===================== SEARCH =====================
const searchForm = document.getElementById("searchForm");
if (searchForm) {
    searchForm.addEventListener("submit", function () {
        const searchInput = searchForm.querySelector("input[type='text']");
        const submitBtn = searchForm.querySelector("button[type='submit']");
        if (searchInput) {
            searchInput.placeholder = "Searching...";
            searchInput.readOnly = true;
            searchInput.style.opacity = "0.7";
        }
        if (submitBtn) {
            submitBtn.innerHTML = '<div class="loading-spinner"></div>';
        }
    });
}"""
js_content = js_content.replace(old_search, new_search)

# fix button style in save as well to respect light theme
js_content = js_content.replace('button.style.color = "white";', 'button.style.color = document.body.classList.contains("light-theme") ? "var(--text-primary)" : "white";')

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("JS updated")
