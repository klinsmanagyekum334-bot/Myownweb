// ===== MOBILE MENU TOGGLE =====
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navCenter = document.querySelector('.nav-center');
    const navRight = document.querySelector('.nav-right');
    
    // Toggle menu on hamburger click
    if (hamburger) {
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('active');
            
            if (navCenter) {
                navCenter.classList.toggle('active');
            }
            if (navRight) {
                navRight.classList.toggle('active');
            }
        });
    }
    
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        const navbar = document.querySelector('.navbar');
        if (navbar && !navbar.contains(e.target)) {
            if (navCenter) {
                navCenter.classList.remove('active');
            }
            if (navRight) {
                navRight.classList.remove('active');
            }
            if (hamburger) {
                hamburger.classList.remove('active');
            }
        }
    });
    
    // Close menu on window resize (if going back to desktop)
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            if (navCenter) {
                navCenter.classList.remove('active');
            }
            if (navRight) {
                navRight.classList.remove('active');
            }
            if (hamburger) {
                hamburger.classList.remove('active');
            }
        }
    });
    
    // ===== FLASH MESSAGES =====
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.parentElement;
            alert.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => {
                alert.remove();
            }, 300);
        });
    });
    
    // Auto-dismiss flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// ===== SLIDE OUT ANIMATION =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ===== SMOOTH SCROLL FOR ANCHOR LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== IMAGE LOADING FALLBACK =====
// If an image fails to load, show placeholder
document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', function() {
        this.style.display = 'none';
        const parent = this.parentElement;
        if (parent) {
            const placeholder = document.createElement('div');
            placeholder.className = 'image-placeholder-fallback';
            placeholder.textContent = '🖼️';
            placeholder.style.cssText = `
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100%;
                height: 100%;
                min-height: 100px;
                background: #f1f2f6;
                color: #b2bec3;
                font-size: 2rem;
            `;
            parent.appendChild(placeholder);
        }
    });
});

// ===== SCROLL TO TOP BUTTON (Optional) =====
// Uncomment if you want a scroll-to-top button
/*
const scrollBtn = document.createElement('button');
scrollBtn.innerHTML = '↑';
scrollBtn.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 10px 15px;
    background: #f7971e;
    color: #fff;
    border: none;
    border-radius: 50%;
    font-size: 1.5rem;
    cursor: pointer;
    display: none;
    z-index: 999;
    box-shadow: 0 4px 15px rgba(247, 151, 30, 0.3);
`;
document.body.appendChild(scrollBtn);

window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
        scrollBtn.style.display = 'block';
    } else {
        scrollBtn.style.display = 'none';
    }
});

scrollBtn.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});
*/
