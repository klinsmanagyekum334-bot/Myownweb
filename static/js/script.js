// ============================================================
// MOBILE MENU TOGGLE
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger');
    const navRight = document.getElementById('navRight');

    if (hamburger && navRight) {
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('active');
            navRight.classList.toggle('active');
        });
    }

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        const navbar = document.querySelector('.navbar');
        if (navbar && !navbar.contains(e.target)) {
            if (navRight) navRight.classList.remove('active');
            if (hamburger) hamburger.classList.remove('active');
        }
    });

    // Close menu on resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            if (navRight) navRight.classList.remove('active');
            if (hamburger) hamburger.classList.remove('active');
        }
    });

    // ============================================================
    // FLASH MESSAGES
    // ============================================================
    document.querySelectorAll('.close-alert').forEach(btn => {
        btn.addEventListener('click', function() {
            const alert = this.parentElement;
            alert.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => alert.remove(), 300);
        });
    });

    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // ============================================================
    // EXPANDABLE SEARCH
    // ============================================================
    const navSearch = document.getElementById('navSearch');
    const searchToggle = document.getElementById('searchToggle');
    const searchInput = document.getElementById('searchInput');
    const searchOverlay = document.getElementById('searchResultsOverlay');
    const searchResultsList = document.getElementById('searchResultsList');
    const searchClose = document.getElementById('searchClose');

    if (searchToggle && navSearch) {
        searchToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            navSearch.classList.toggle('expanded');
            if (navSearch.classList.contains('expanded')) {
                searchInput.focus();
            }
        });
    }

    if (searchInput) {
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                const query = this.value.trim();
                if (query.length > 0) {
                    performSearch(query);
                }
            }
        });

        searchInput.addEventListener('input', function() {
            if (this.value.trim() === '' && searchOverlay) {
                searchOverlay.classList.remove('active');
            }
        });
    }

    if (searchClose) {
        searchClose.addEventListener('click', function() {
            searchOverlay.classList.remove('active');
        });
    }

    if (searchOverlay) {
        searchOverlay.addEventListener('click', function(e) {
            if (e.target === searchOverlay) {
                searchOverlay.classList.remove('active');
            }
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && searchOverlay) {
            searchOverlay.classList.remove('active');
            if (navSearch) navSearch.classList.remove('expanded');
        }
    });
});

// ============================================================
// SEARCH FUNCTION — Scans visible text on the page
// ============================================================
function performSearch(query) {
    const searchOverlay = document.getElementById('searchResultsOverlay');
    const searchResultsList = document.getElementById('searchResultsList');
    if (!searchOverlay || !searchResultsList) return;

    const queryLower = query.toLowerCase();
    const results = [];

    const mainContent = document.querySelector('main');
    if (!mainContent) return;

    const elements = mainContent.querySelectorAll('h1, h2, h3, h4, h5, p, li, span, div, a, img');
    const seen = new Set();

    elements.forEach(el => {
        if (seen.has(el)) return;
        seen.add(el);

        let text = '';
        if (el.tagName === 'IMG') {
            text = el.alt || '';
        } else {
            text = Array.from(el.childNodes)
                .filter(n => n.nodeType === 3)
                .map(n => n.textContent.trim())
                .join(' ')
                .trim();
        }

        if (text && text.toLowerCase().includes(queryLower)) {
            results.push(text);
        }
    });

    const uniqueResults = [...new Set(results)];

    searchResultsList.innerHTML = '';

    if (uniqueResults.length === 0) {
        searchResultsList.innerHTML = `<div class="search-no-results">❌ No results found for "<strong>${escapeHtml(query)}</strong>"</div>`;
    } else {
        uniqueResults.forEach(text => {
            const item = document.createElement('div');
            item.className = 'search-result-item';
            item.innerHTML = highlightMatch(text, query);
            searchResultsList.appendChild(item);
        });
    }

    searchOverlay.classList.add('active');
}

// Escape HTML to prevent injection
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Highlight the matching word
function highlightMatch(text, query) {
    const escapedText = escapeHtml(text);
    const escapedQuery = escapeHtml(query).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escapedQuery})`, 'gi');
    return escapedText.replace(regex, '<mark>$1</mark>');
}

// ============================================================
// SLIDE OUT ANIMATION
// ============================================================
const styleTag = document.createElement('style');
styleTag.textContent = `
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(styleTag);

// ============================================================
// SMOOTH SCROLL
// ============================================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
