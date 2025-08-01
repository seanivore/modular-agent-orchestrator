// PIXEL TERMINAL - Interactive pixel-style effects

document.addEventListener('DOMContentLoaded', function() {
    initPixelEffects();
    initTypewriterEffects();
    initInteractiveElements();
    initBootSequence();
});

function initPixelEffects() {
    // Add pixel grid overlay effect
    const container = document.querySelector('.pixel-container');
    
    // Create floating pixels effect
    setInterval(() => {
        createFloatingPixel();
    }, 2000);
    
    // Add screen flicker effect
    setInterval(() => {
        flickerScreen();
    }, 8000 + Math.random() * 10000);
}

function createFloatingPixel() {
    const pixel = document.createElement('div');
    pixel.style.cssText = `
        position: fixed;
        width: 2px;
        height: 2px;
        background: var(--primary-color);
        z-index: 500;
        pointer-events: none;
        box-shadow: 0 0 4px var(--primary-color);
        left: ${Math.random() * window.innerWidth}px;
        top: ${window.innerHeight + 10}px;
        animation: floatUp 3s linear forwards;
    `;
    
    document.body.appendChild(pixel);
    
    setTimeout(() => {
        pixel.remove();
    }, 3000);
}

function flickerScreen() {
    const overlay = document.querySelector('.crt-overlay');
    overlay.style.opacity = '0.8';
    setTimeout(() => {
        overlay.style.opacity = '0.2';
    }, 100);
    setTimeout(() => {
        overlay.style.opacity = '0.4';
    }, 150);
    setTimeout(() => {
        overlay.style.opacity = '0.2';
    }, 200);
}

function initTypewriterEffects() {
    const command = document.querySelector('.demo-command');
    if (command && command.classList.contains('typing')) {
        // Start output animation after command is typed
        setTimeout(() => {
            animateOutput();
        }, 2000);
    }
}

function animateOutput() {
    const outputLines = document.querySelectorAll('.output-line');
    outputLines.forEach((line, index) => {
        setTimeout(() => {
            line.style.opacity = '0';
            line.style.animation = 'fadeInTypewriter 0.5s ease-out forwards';
            line.style.animationDelay = `${index * 0.3}s`;
        }, index * 300);
    });
}

function initInteractiveElements() {
    // Feature blocks hover effects
    const featureBlocks = document.querySelectorAll('.feature-block');
    featureBlocks.forEach(block => {
        block.addEventListener('mouseenter', () => {
            createPixelBurst(block);
        });
    });
    
    // Navigation buttons with pixel effects
    const navButtons = document.querySelectorAll('.nav-button');
    navButtons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            createButtonGlow(button);
        });
        
        button.addEventListener('click', (e) => {
            createClickEffect(e);
        });
    });
    
    // Terminal controls
    const controls = document.querySelectorAll('.btn');
    controls.forEach(btn => {
        btn.addEventListener('click', () => {
            createTerminalEffect(btn);
        });
    });
}

function createPixelBurst(element) {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    for (let i = 0; i < 8; i++) {
        const pixel = document.createElement('div');
        const angle = (i / 8) * Math.PI * 2;
        const distance = 50;
        
        pixel.style.cssText = `
            position: fixed;
            width: 3px;
            height: 3px;
            background: var(--accent-color);
            z-index: 1001;
            pointer-events: none;
            left: ${centerX}px;
            top: ${centerY}px;
            box-shadow: 0 0 6px var(--accent-color);
        `;
        
        document.body.appendChild(pixel);
        
        // Animate pixel burst
        pixel.animate([
            { transform: 'translate(0, 0)', opacity: 1 },
            { 
                transform: `translate(${Math.cos(angle) * distance}px, ${Math.sin(angle) * distance}px)`, 
                opacity: 0 
            }
        ], {
            duration: 800,
            easing: 'ease-out'
        }).onfinish = () => pixel.remove();
    }
}

function createButtonGlow(button) {
    button.style.boxShadow = `
        0 0 10px var(--primary-color),
        inset 0 0 10px rgba(0, 255, 65, 0.1)
    `;
    
    setTimeout(() => {
        button.style.boxShadow = '';
    }, 300);
}

function createClickEffect(e) {
    const ripple = document.createElement('div');
    const rect = e.target.getBoundingClientRect();
    
    ripple.style.cssText = `
        position: fixed;
        width: 4px;
        height: 4px;
        background: var(--accent-color);
        border-radius: 50%;
        z-index: 1002;
        pointer-events: none;
        left: ${e.clientX - 2}px;
        top: ${e.clientY - 2}px;
        box-shadow: 0 0 10px var(--accent-color);
        animation: pixelRipple 0.6s ease-out forwards;
    `;
    
    document.body.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
}

function createTerminalEffect(btn) {
    const effect = document.createElement('div');
    effect.textContent = btn.textContent;
    effect.style.cssText = `
        position: fixed;
        color: var(--primary-color);
        font-family: 'Press Start 2P', monospace;
        font-size: 8px;
        z-index: 1003;
        pointer-events: none;
        left: ${btn.getBoundingClientRect().left}px;
        top: ${btn.getBoundingClientRect().top - 20}px;
        animation: terminalPop 1s ease-out forwards;
    `;
    
    document.body.appendChild(effect);
    setTimeout(() => effect.remove(), 1000);
}

function initBootSequence() {
    // Add random glitch effect to boot sequence
    const bootLines = document.querySelectorAll('.boot-line');
    bootLines.forEach((line, index) => {
        setTimeout(() => {
            if (Math.random() > 0.7) {
                addGlitchEffect(line);
            }
        }, (index + 1) * 1000);
    });
}

function addGlitchEffect(element) {
    const originalText = element.textContent;
    const glitchChars = '!@#$%^&*()_+-=[]{}|;:,.<>?';
    
    // Create glitch text
    let glitchText = '';
    for (let i = 0; i < originalText.length; i++) {
        if (Math.random() > 0.8) {
            glitchText += glitchChars[Math.floor(Math.random() * glitchChars.length)];
        } else {
            glitchText += originalText[i];
        }
    }
    
    element.textContent = glitchText;
    element.style.color = 'var(--accent-color)';
    
    setTimeout(() => {
        element.textContent = originalText;
        element.style.color = '';
    }, 100);
}

// CSS Animation keyframes added dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes floatUp {
        from { 
            transform: translateY(0); 
            opacity: 1; 
        }
        to { 
            transform: translateY(-${window.innerHeight + 50}px); 
            opacity: 0; 
        }
    }
    
    @keyframes fadeInTypewriter {
        from { 
            opacity: 0; 
            transform: translateX(-10px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }
    
    @keyframes pixelRipple {
        from { 
            transform: scale(1); 
            opacity: 1; 
        }
        to { 
            transform: scale(20); 
            opacity: 0; 
        }
    }
    
    @keyframes terminalPop {
        0% { 
            transform: translateY(0) scale(1); 
            opacity: 1; 
        }
        50% { 
            transform: translateY(-10px) scale(1.2); 
            opacity: 0.8; 
        }
        100% { 
            transform: translateY(-20px) scale(0.8); 
            opacity: 0; 
        }
    }
`;
document.head.appendChild(style);