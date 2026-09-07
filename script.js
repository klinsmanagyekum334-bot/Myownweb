// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navCenter = document.querySelector('.nav-center');
    const navRight = document.querySelector('.nav-right');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navCenter.classList.toggle('active');
            navRight.classList.toggle('active');
        });
    }
    
    // Flash message close
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

// Add slideOut animation dynamically
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