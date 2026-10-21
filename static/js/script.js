/* =============================================================================
   script.js  —  NewsSphere / SmartSearch
   Anti-flash IIFE runs immediately (before DOMContentLoaded) to apply the
   stored colour theme before the browser paints the first frame.
============================================================================= */

(function () {
    if (localStorage.getItem('theme') === 'light') {
        document.body.classList.add('light-theme');
    }
})();


document.addEventListener('DOMContentLoaded', function () {

    /* ─────────────────────────────────────────────────────────────────────
       THEME TOGGLE
    ───────────────────────────────────────────────────────────────────── */
    var themeToggleBtn = document.getElementById('theme-toggle');
    var themeIcon      = themeToggleBtn ? themeToggleBtn.querySelector('i') : null;

    function syncThemeIcon() {
        if (!themeIcon) return;
        var isLight = document.body.classList.contains('light-theme');
        themeIcon.classList.toggle('fa-sun',  isLight);
        themeIcon.classList.toggle('fa-moon', !isLight);
    }

    syncThemeIcon(); // set correct icon immediately on load

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function () {
            document.body.classList.toggle('light-theme');
            var isLight = document.body.classList.contains('light-theme');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
            syncThemeIcon();
        });
    }


    /* ─────────────────────────────────────────────────────────────────────
       CARD EXPANSION  (Read More / Read Less)
       Each .read-more-btn is immediately followed by .extra-content
    ───────────────────────────────────────────────────────────────────── */
    document.querySelectorAll('.read-more-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var card  = this.closest('.card');
            var extra = this.nextElementSibling; // .extra-content

            if (!extra || !card) return;

            var isOpen = extra.style.display === 'block';

            extra.style.display = isOpen ? 'none' : 'block';
            this.innerHTML = isOpen 
                ? 'Read More <i class="fa-solid fa-chevron-down" style="font-size:12px;margin-left:4px;"></i>' 
                : 'Read Less <i class="fa-solid fa-chevron-up" style="font-size:12px;margin-left:4px;"></i>';
            card.classList.toggle('expanded', !isOpen);
        });
    });


    /* ─────────────────────────────────────────────────────────────────────
       FORMATTERS & ANIMATION HELPERS (Likes & Saves)
       Rule: For 0 or 1, do NOT show the number (no "0" in user's face!).
       Only show the count badge if count is greater than 1!
    ───────────────────────────────────────────────────────────────────── */
    function _formatLikeHTML(isLiked, count) {
        var num = count > 1 ? '<span class="action-count">' + count + '</span>' : '';
        return isLiked
            ? '<i class="fa-solid fa-heart"></i> Liked' + (num ? ' ' + num : '')
            : '<i class="fa-regular fa-heart"></i> Like' + (num ? ' ' + num : '');
    }

    function _formatSaveHTML(isSaved, count) {
        var num = count > 1 ? '<span class="action-count">' + count + '</span>' : '';
        return isSaved
            ? '<i class="fa-solid fa-bookmark"></i> Saved' + (num ? ' ' + num : '')
            : '<i class="fa-regular fa-bookmark"></i> Save' + (num ? ' ' + num : '');
    }

    function _triggerAnim(button, animClass, pulseClass) {
        button.classList.remove(animClass, pulseClass);
        void button.offsetWidth; // force browser reflow to replay keyframe
        button.classList.add(animClass, pulseClass);
        setTimeout(function () {
            button.classList.remove(animClass, pulseClass);
        }, 550);
    }

    /* ─────────────────────────────────────────────────────────────────────
       PERSISTENT LIKES (Backend sync + instantaneous state & counts)
    ───────────────────────────────────────────────────────────────────── */
    var localLikes = [];
    try {
        localLikes = JSON.parse(localStorage.getItem('likedArticles') || '[]');
    } catch (e) {
        localLikes = [];
    }
    var likedSet = new Set(localLikes);

    document.querySelectorAll('.like').forEach(function (button) {
        var link = (button.dataset.link || '').trim();
        var initialLiked = button.dataset.liked === 'true';
        var initialCount = parseInt(button.dataset.count || '0', 10);

        _setLiked(button, initialLiked, initialCount);

        button.addEventListener('click', function () {
            if (!link) return;

            var isLiked = button.dataset.liked === 'true';
            var curCount = parseInt(button.dataset.count || '0', 10);

            _triggerAnim(button, 'btn-pop', 'btn-pulse');

            if (isLiked) {
                var nextCount = Math.max(0, curCount - 1);
                _setLiked(button, false, nextCount);
                likedSet.delete(link);
                _saveLikes();
                _post('/unlike', { link: link })
                    .then(function (res) {
                        if (res && typeof res.count !== 'undefined') {
                            _setLiked(button, false, res.count);
                        }
                    })
                    .catch(function (err) {
                        _setLiked(button, true, curCount);
                        likedSet.add(link);
                        _saveLikes();
                        if (err && (err.message.indexOf('401') !== -1 || (err.error === 'login_required'))) {
                            button.classList.add('btn-lock-shake');
                            alert('Please log in to like stories.');
                            window.location.href = '/login';
                        }
                    });
            } else {
                var nextCount = curCount + 1;
                _setLiked(button, true, nextCount);
                likedSet.add(link);
                _saveLikes();
                _post('/like', { link: link })
                    .then(function (res) {
                        if (res && typeof res.count !== 'undefined') {
                            _setLiked(button, true, res.count);
                        }
                    })
                    .catch(function (err) {
                        _setLiked(button, false, curCount);
                        likedSet.delete(link);
                        _saveLikes();
                        if (err && (err.message.indexOf('401') !== -1 || (err.error === 'login_required'))) {
                            button.classList.add('btn-lock-shake');
                            alert('Please log in to like stories.');
                            window.location.href = '/login';
                        }
                    });
            }
        });
    });

    function _setLiked(button, state, count) {
        button.dataset.liked = state ? 'true' : 'false';
        if (typeof count !== 'undefined') {
            button.dataset.count = count;
        }
        var curCount = parseInt(button.dataset.count || '0', 10);
        button.innerHTML = _formatLikeHTML(state, curCount);
        button.style.color = state ? '#ff5c8a' : '';
    }

    function _saveLikes() {
        localStorage.setItem('likedArticles', JSON.stringify(Array.from(likedSet)));
    }


    /* ─────────────────────────────────────────────────────────────────────
       SAVE / UNSAVE (Backend sync + instantaneous state & counts)
    ───────────────────────────────────────────────────────────────────── */
    document.querySelectorAll('.save').forEach(function (button) {
        var isPreSaved = button.dataset.saved === 'true' || Boolean(button.querySelector('.fa-solid.fa-bookmark'));
        var initialCount = parseInt(button.dataset.count || (isPreSaved ? '1' : '0'), 10);

        _setSaved(button, isPreSaved, initialCount);

        button.addEventListener('click', function () {
            var link = (button.dataset.link || '').trim();
            if (!link) return;

            var isSaved = button.dataset.saved === 'true';
            var curCount = parseInt(button.dataset.count || '0', 10);

            _triggerAnim(button, 'btn-pop', 'btn-pulse');

            if (isSaved) {
                var nextCount = Math.max(0, curCount - 1);
                _setSaved(button, false, nextCount);
                _post('/unsave', { link: link })
                    .then(function (res) {
                        if (res && typeof res.count !== 'undefined') {
                            _setSaved(button, false, res.count);
                        }
                    })
                    .catch(function (err) {
                        if (err && (err.message.indexOf('401') !== -1 || (err.error === 'login_required'))) {
                            button.classList.add('btn-lock-shake');
                            alert('Please log in to save stories.');
                            window.location.href = '/login';
                        } else {
                            _setSaved(button, true, curCount);
                        }
                    });
            } else {
                var nextCount = curCount + 1;
                _setSaved(button, true, nextCount);
                _post('/save', {
                    title:   button.dataset.title   || '',
                    link:    link,
                    snippet: button.dataset.snippet || '',
                    source:  button.dataset.source  || ''
                })
                .then(function (res) {
                    if (res && typeof res.count !== 'undefined') {
                        _setSaved(button, true, res.count);
                    }
                })
                .catch(function (err) {
                    if (err && (err.message.indexOf('401') !== -1 || (err.error === 'login_required'))) {
                        button.classList.add('btn-lock-shake');
                        alert('Please log in to save stories.');
                        window.location.href = '/login';
                    }
                    _setSaved(button, false, curCount);
                });
            }
        });
    });

    function _setSaved(button, state, count) {
        button.dataset.saved = state ? 'true' : 'false';
        if (typeof count !== 'undefined') {
            button.dataset.count = count;
        }
        var curCount = parseInt(button.dataset.count || '0', 10);
        button.innerHTML = _formatSaveHTML(state, curCount);
        button.style.color = state ? '#1877f2' : '';
    }


    /* ─────────────────────────────────────────────────────────────────────
       SEARCH FORM — LOADING STATE
    ───────────────────────────────────────────────────────────────────── */
    var searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function () {
            var searchInput = searchForm.querySelector("input[name='q']");
            var submitBtn   = searchForm.querySelector("button[type='submit']");

            if (searchInput) {
                searchInput.placeholder = 'Searching…';
                searchInput.readOnly    = true;
                searchInput.style.opacity = '0.65';
            }
            if (submitBtn) {
                submitBtn.innerHTML = '<div class="loading-spinner"></div>';
                submitBtn.disabled  = true;
            }
        });
    }


    /* ─────────────────────────────────────────────────────────────────────
       PROFILE DROPDOWN
       BUG-FIX: added guard so clicking inside the dropdown links (which
       bubble up) doesn't close the dropdown before the link navigates.
    ───────────────────────────────────────────────────────────────────── */
    var profileIcon     = document.querySelector('.profile-icon');
    var profileDropdown = document.querySelector('.profile-dropdown');

    if (profileIcon && profileDropdown) {
        profileIcon.addEventListener('click', function (e) {
            e.stopPropagation();
            profileDropdown.classList.toggle('show');
        });

        // Close when clicking outside the entire profile-menu zone
        document.addEventListener('click', function (e) {
            if (profileDropdown.classList.contains('show') &&
                !e.target.closest('.profile-menu')) {
                profileDropdown.classList.remove('show');
            }
        });
    }


    /* ─────────────────────────────────────────────────────────────────────
       NOTIFICATION BELL
       BUG-FIX: target the parent <i> via the .fa-bell class but guard
       against null so pages without a bell don't throw errors.
    ───────────────────────────────────────────────────────────────────── */
    var bell = document.querySelector('i.fa-bell');
    if (bell) {
        bell.addEventListener('click', function () {
            alert('No new notifications.');
        });
    }


    /* ─────────────────────────────────────────────────────────────────────
       SIDEBAR ACTIVE HIGHLIGHT
    ───────────────────────────────────────────────────────────────────── */
    document.querySelectorAll('.left-sidebar li').forEach(function (item) {
        item.addEventListener('click', function () {
            document.querySelectorAll('.left-sidebar li').forEach(function (i) {
                i.style.background = '';
                i.style.color      = '';
            });
            item.style.background = 'var(--btn-hover-bg)';
            item.style.color      = 'var(--accent)';
        });
    });


    /* ─────────────────────────────────────────────────────────────────────
       HELPER — fire-and-forget POST, returns a Promise of the JSON body
    ───────────────────────────────────────────────────────────────────── */
    function _post(url, payload) {
        return fetch(url, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(payload)
        })
        .then(function (r) {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json();
        })
        .catch(function (err) {
            console.warn('[SmartSearch] POST ' + url + ' failed:', err.message);
            throw err;
        });
    }

}); // end DOMContentLoaded
