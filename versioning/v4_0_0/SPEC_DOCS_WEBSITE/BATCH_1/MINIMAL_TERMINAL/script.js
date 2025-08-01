// MINIMAL TERMINAL - Clean interactive functionality

document.addEventListener('DOMContentLoaded', function() {
    initMinimalEffects();
    initInteractiveElements();
    initAccessibility();
    initPerformanceOptimizations();
});

function initMinimalEffects() {
    // Subtle entrance animations
    addEntranceAnimations();
    
    // Initialize cursor positioning
    initCursorTracking();
    
    // Add breathing animation to status indicator
    enhanceStatusIndicator();
}

function addEntranceAnimations() {
    const sections = document.querySelectorAll('section');
    
    // Create intersection observer for scroll-triggered animations
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
    
    sections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(section);
    });
}

function initCursorTracking() {
    const cursor = document.querySelector('.cursor-indicator');
    let isMouseMoving = false;
    let mouseTimeout;
    
    document.addEventListener('mousemove', (e) => {
        if (!isMouseMoving) {
            cursor.style.opacity = '0.3';
            isMouseMoving = true;
        }
        
        clearTimeout(mouseTimeout);
        mouseTimeout = setTimeout(() => {
            cursor.style.opacity = '0.7';
            isMouseMoving = false;
        }, 1000);
    });
}

function enhanceStatusIndicator() {
    const indicator = document.querySelector('.status-indicator');
    const statusText = document.querySelector('.status-text');
    
    // Simulate system status changes
    const statuses = [
        { text: 'system ready', color: 'var(--accent-color)' },
        { text: 'agents active', color: 'var(--primary-color)' },
        { text: 'memory synced', color: '#22c55e' }
    ];
    
    let currentStatus = 0;
    
    setInterval(() => {
        currentStatus = (currentStatus + 1) % statuses.length;
        const status = statuses[currentStatus];
        
        // Smooth transition
        statusText.style.opacity = '0';
        indicator.style.background = status.color;
        
        setTimeout(() => {
            statusText.textContent = status.text;
            statusText.style.opacity = '1';
        }, 300);
    }, 5000);
}

function initInteractiveElements() {
    // Feature card interactions
    initFeatureCards();
    
    // Documentation links
    initDocumentationLinks();
    
    // Command line interactions
    initCommandLines();
    
    // Code block interactions
    initCodeBlocks();
}

function initFeatureCards() {
    const cards = document.querySelectorAll('.feature-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-4px)';
            card.style.boxShadow = '0 8px 25px rgba(37, 99, 235, 0.15)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(-2px)';
            card.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.1)';
        });
        
        card.addEventListener('click', () => {
            simulateFeatureExploration(card);
        });
    });
}

function simulateFeatureExploration(card) {
    const featureName = card.querySelector('h3').textContent;
    const originalBorder = card.style.borderColor;
    
    // Visual feedback
    card.style.borderColor = 'var(--primary-color)';
    card.style.background = 'rgba(37, 99, 235, 0.05)';
    
    // Create temporary output
    const output = document.createElement('div');
    output.className = 'feature-exploration';
    output.innerHTML = `
        <div class="command-line" style="margin-top: 1rem;">
            <span class="prompt">→</span>
            <span class="command">explore "${featureName.toLowerCase()}"</span>
        </div>
        <div class="output-block">
            <p style="color: var(--secondary-color); font-size: 0.9rem;">
                Exploring ${featureName} capabilities...
            </p>
        </div>
    `;
    
    card.appendChild(output);
    
    // Remove after delay
    setTimeout(() => {
        output.remove();
        card.style.borderColor = originalBorder;
        card.style.background = 'var(--code-bg)';
    }, 2000);
}

function initDocumentationLinks() {
    const docLinks = document.querySelectorAll('.doc-link');
    
    docLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            simulateDocumentationAccess(link);
        });
        
        link.addEventListener('mouseenter', () => {
            const icon = link.querySelector('.doc-icon');
            icon.textContent = '■';
            icon.style.color = 'var(--accent-color)';
        });
        
        link.addEventListener('mouseleave', () => {
            const icon = link.querySelector('.doc-icon');
            icon.textContent = '□';
            icon.style.color = 'var(--primary-color)';
        });
    });
}

function simulateDocumentationAccess(link) {
    const title = link.querySelector('.doc-title').textContent;
    
    // Create modal-like overlay
    const overlay = document.createElement('div');
    overlay.className = 'doc-preview-overlay';
    overlay.innerHTML = `
        <div class="doc-preview-content">
            <div class="doc-preview-header">
                <span class="prompt">→</span>
                <span class="command">open "${title.toLowerCase().replace(/\s+/g, '-')}.md"</span>
                <button class="close-preview">×</button>
            </div>
            <div class="doc-preview-body">
                <h2>${title}</h2>
                <p>Documentation content would be loaded here...</p>
                <p style="color: var(--secondary-color); font-size: 0.9rem; margin-top: 2rem;">
                    Press ESC or click × to close preview
                </p>
            </div>
        </div>
    `;
    
    // Style the overlay
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(8px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    const content = overlay.querySelector('.doc-preview-content');
    content.style.cssText = `
        background: var(--bg-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 2rem;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
    `;
    
    const header = overlay.querySelector('.doc-preview-header');
    header.style.cssText = `
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    `;
    
    const closeBtn = overlay.querySelector('.close-preview');
    closeBtn.style.cssText = `
        margin-left: auto;
        background: none;
        border: none;
        font-size: 1.5rem;
        color: var(--secondary-color);
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 4px;
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(overlay);
    
    // Animate in
    requestAnimationFrame(() => {
        overlay.style.opacity = '1';
    });
    
    // Close handlers
    const closePreview = () => {
        overlay.style.opacity = '0';
        setTimeout(() => overlay.remove(), 300);
    };
    
    closeBtn.addEventListener('click', closePreview);
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closePreview();
    });
    
    document.addEventListener('keydown', function escHandler(e) {
        if (e.key === 'Escape') {
            closePreview();
            document.removeEventListener('keydown', escHandler);
        }
    });
}

function initCommandLines() {
    const commandLines = document.querySelectorAll('.command-line');
    
    commandLines.forEach(line => {
        line.addEventListener('click', () => {
            const command = line.querySelector('.command').textContent;
            
            // Visual feedback
            line.style.background = 'rgba(37, 99, 235, 0.1)';
            line.style.borderRadius = '4px';
            line.style.padding = '0.5rem';
            line.style.margin = '0 -0.5rem 1rem';
            
            setTimeout(() => {
                line.style.background = 'transparent';
                line.style.padding = '0';
                line.style.margin = '0 0 1rem';
            }, 500);
            
            // Log to console
            console.log(`%c→ ${command}`, 'color: #2563eb; font-family: monospace; font-weight: 500;');
        });
    });
}

function initCodeBlocks() {
    const codeContainer = document.querySelector('.code-container');
    if (!codeContainer) return;
    
    // Add copy functionality
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-code-btn';
    copyButton.textContent = 'Copy';
    copyButton.style.cssText = `
        position: absolute;
        top: 0.75rem;
        right: 1rem;
        background: none;
        border: 1px solid var(--border-color);
        color: var(--secondary-color);
        font-family: inherit;
        font-size: 0.8rem;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.3s ease;
    `;
    
    codeContainer.style.position = 'relative';
    codeContainer.appendChild(copyButton);
    
    copyButton.addEventListener('click', () => {
        const codeText = codeContainer.querySelector('.code-content').textContent;
        navigator.clipboard.writeText(codeText).then(() => {
            copyButton.textContent = 'Copied!';
            copyButton.style.color = 'var(--accent-color)';
            copyButton.style.borderColor = 'var(--accent-color)';
            
            setTimeout(() => {
                copyButton.textContent = 'Copy';
                copyButton.style.color = 'var(--secondary-color)';
                copyButton.style.borderColor = 'var(--border-color)';
            }, 2000);
        });
    });
    
    copyButton.addEventListener('mouseenter', () => {
        copyButton.style.background = 'var(--code-bg)';
        copyButton.style.borderColor = 'var(--primary-color)';
    });
    
    copyButton.addEventListener('mouseleave', () => {
        copyButton.style.background = 'none';
        copyButton.style.borderColor = 'var(--border-color)';
    });
}

function initAccessibility() {
    // Add keyboard navigation for interactive elements
    const interactiveElements = document.querySelectorAll('.feature-card, .doc-link');
    
    interactiveElements.forEach((element, index) => {
        element.setAttribute('tabindex', '0');
        element.setAttribute('role', 'button');
        
        element.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                element.click();
            }
        });
        
        element.addEventListener('focus', () => {
            element.style.outline = '2px solid var(--primary-color)';
            element.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', () => {
            element.style.outline = 'none';
        });
    });
    
    // Add aria labels
    document.querySelectorAll('.feature-card').forEach(card => {
        const title = card.querySelector('h3').textContent;
        card.setAttribute('aria-label', `Explore ${title} feature`);
    });
    
    document.querySelectorAll('.doc-link').forEach(link => {
        const title = link.querySelector('.doc-title').textContent;
        link.setAttribute('aria-label', `Open ${title} documentation`);
    });
}

function initPerformanceOptimizations() {
    // Lazy load non-critical animations
    let animationsLoaded = false;
    
    const loadAnimations = () => {
        if (animationsLoaded) return;
        animationsLoaded = true;
        
        // Add subtle particle effects (optional)
        if (window.innerWidth > 768) {
            createSubtleParticles();
        }
    };
    
    // Load animations on user interaction
    document.addEventListener('mousemove', loadAnimations, { once: true });
    document.addEventListener('scroll', loadAnimations, { once: true });
    
    // Debounced resize handler
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            // Recalculate layouts if needed
            console.log('Layout recalculated for new viewport size');
        }, 250);
    });
}

function createSubtleParticles() {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-container';
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    `;
    
    // Create subtle floating dots
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: 2px;
            height: 2px;
            background: var(--primary-color);
            border-radius: 50%;
            opacity: 0.1;
            animation: float-${i % 3} ${8 + Math.random() * 4}s linear infinite;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
        `;
        
        particleContainer.appendChild(particle);
    }
    
    // Add keyframes for floating animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float-0 {
            0%, 100% { transform: translateY(0px) translateX(0px); }
            33% { transform: translateY(-10px) translateX(5px); }
            66% { transform: translateY(5px) translateX(-3px); }
        }
        
        @keyframes float-1 {
            0%, 100% { transform: translateY(0px) translateX(0px); }
            50% { transform: translateY(-15px) translateX(-5px); }
        }
        
        @keyframes float-2 {
            0%, 100% { transform: translateY(0px) translateX(0px); }
            25% { transform: translateY(-5px) translateX(3px); }
            75% { transform: translateY(-8px) translateX(-2px); }
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(particleContainer);
}

// Initialize theme preference detection
function initThemePreference() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    
    prefersDark.addEventListener('change', (e) => {
        if (e.matches) {
            // User prefers dark mode - could adapt colors accordingly
            console.log('Dark mode preferred');
        } else {
            console.log('Light mode preferred');
        }
    });
}

initThemePreference();

// Performance monitoring
if (process.env.NODE_ENV === 'development') {
    const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
            console.log(`%c${entry.name}: ${entry.duration.toFixed(2)}ms`, 
                       'color: #2563eb; font-family: monospace;');
        });
    });
    
    observer.observe({ entryTypes: ['measure', 'navigation'] });
}