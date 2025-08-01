// Mao Watercolor Terminal - Interactive effects
document.addEventListener('DOMContentLoaded', function() {
    initWatercolorEffects();
    initInteractiveElements();
    initResponsiveAnimations();
});

function initWatercolorEffects() {
    // Create dynamic watercolor bleed effects
    const container = document.querySelector('.watercolor-container');
    
    // Add random watercolor spots on mouse movement
    container.addEventListener('mousemove', function(e) {
        if (Math.random() > 0.95) { // Only 5% chance to create effect
            createWatercolorSpot(e.clientX, e.clientY);
        }
    });
    
    // Animate existing bleed backgrounds
    const bleeds = document.querySelectorAll('.bleed-bg');
    bleeds.forEach((bleed, index) => {
        // Add slight movement on mouse proximity
        container.addEventListener('mousemove', function(e) {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const bleedRect = bleed.getBoundingClientRect();
            const bleedX = bleedRect.left - rect.left + bleedRect.width / 2;
            const bleedY = bleedRect.top - rect.top + bleedRect.height / 2;
            
            const distance = Math.sqrt(Math.pow(x - bleedX, 2) + Math.pow(y - bleedY, 2));
            const maxDistance = 300;
            
            if (distance < maxDistance) {
                const influence = (maxDistance - distance) / maxDistance;
                const moveX = (x - bleedX) * influence * 0.1;
                const moveY = (y - bleedY) * influence * 0.1;
                
                bleed.style.transform = `translate(${moveX}px, ${moveY}px) scale(${1 + influence * 0.2})`;
            } else {
                bleed.style.transform = 'translate(0, 0) scale(1)';
            }
        });
    });
}

function createWatercolorSpot(x, y) {
    const spot = document.createElement('div');
    const colors = [
        'rgba(45, 74, 62, 0.1)',
        'rgba(122, 155, 118, 0.15)',
        'rgba(200, 168, 130, 0.12)',
        'rgba(244, 231, 209, 0.2)'
    ];
    
    spot.style.position = 'fixed';
    spot.style.left = x + 'px';
    spot.style.top = y + 'px';
    spot.style.width = Math.random() * 100 + 50 + 'px';
    spot.style.height = Math.random() * 100 + 50 + 'px';
    spot.style.background = colors[Math.floor(Math.random() * colors.length)];
    spot.style.borderRadius = '50%';
    spot.style.filter = 'blur(' + (Math.random() * 30 + 20) + 'px)';
    spot.style.pointerEvents = 'none';
    spot.style.zIndex = '1';
    spot.style.transform = 'translate(-50%, -50%)';
    spot.style.animation = 'watercolor-fade 3s ease-out forwards';
    
    document.body.appendChild(spot);
    
    // Remove after animation
    setTimeout(() => {
        if (spot.parentNode) {
            spot.parentNode.removeChild(spot);
        }
    }, 3000);
}

function initInteractiveElements() {
    // Enhanced watercolor card hover effects
    const cards = document.querySelectorAll('.watercolor-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 15px 40px rgba(45, 74, 62, 0.15)';
            
            // Intensify watercolor background on hover
            const before = window.getComputedStyle(this, '::before');
            this.style.setProperty('--hover-opacity', '0.6');
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 8px 32px rgba(45, 74, 62, 0.1)';
            this.style.setProperty('--hover-opacity', '0.4');
        });
    });
    
    // Interactive typing animation
    const command = document.querySelector('.typing-animation');
    if (command) {
        const commands = [
            'mao --help',
            'mao init project',
            'mao chat "analyze data"',
            'mao orchestrate agents',
            'mao --version'
        ];
        let currentIndex = 0;
        
        setInterval(() => {
            currentIndex = (currentIndex + 1) % commands.length;
            command.textContent = commands[currentIndex];
        }, 3000);
    }
    
    // Cat logo interaction
    const catLogo = document.querySelector('.cat-logo');
    if (catLogo) {
        catLogo.addEventListener('click', function() {
            this.style.animation = 'cat-bounce 0.6s ease-in-out';
            setTimeout(() => {
                this.style.animation = '';
            }, 600);
        });
    }
}

function initResponsiveAnimations() {
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe cards for scroll animations
    const cards = document.querySelectorAll('.watercolor-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Responsive watercolor adjustments
    function adjustWatercolorForScreen() {
        const isMobile = window.innerWidth < 768;
        const bleeds = document.querySelectorAll('.bleed-bg');
        
        bleeds.forEach(bleed => {
            if (isMobile) {
                bleed.style.filter = 'blur(40px)';
                bleed.style.opacity = '0.4';
            } else {
                bleed.style.filter = 'blur(60px)';
                bleed.style.opacity = '0.6';
            }
        });
    }
    
    adjustWatercolorForScreen();
    window.addEventListener('resize', adjustWatercolorForScreen);
}

// CSS animations defined in JavaScript for dynamic injection
const dynamicStyles = `
    @keyframes watercolor-fade {
        0% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0);
        }
        50% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
        100% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(1.5);
        }
    }
    
    @keyframes cat-bounce {
        0%, 100% { transform: translateY(0); }
        25% { transform: translateY(-10px) rotate(-5deg); }
        50% { transform: translateY(-15px) rotate(0deg); }
        75% { transform: translateY(-5px) rotate(5deg); }
    }
    
    .watercolor-card:hover::before {
        opacity: var(--hover-opacity, 0.6) !important;
        animation-duration: 8s;
    }
`;

// Inject dynamic styles
const styleSheet = document.createElement('style');
styleSheet.textContent = dynamicStyles;
document.head.appendChild(styleSheet);

// Performance optimization for mobile
if ('ontouchstart' in window) {
    document.body.classList.add('touch-device');
    
    // Reduce animations on mobile for better performance
    const style = document.createElement('style');
    style.textContent = `
        .touch-device .bleed-bg {
            animation-duration: 12s !important;
        }
        .touch-device .watercolor-card::before {
            animation-duration: 20s !important;
        }
    `;
    document.head.appendChild(style);
}