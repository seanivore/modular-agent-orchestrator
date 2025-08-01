// CLASSIC TERMINAL - Interactive JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize terminal effects
    initTerminalEffects();
    initInteractiveElements();
    initKeyboardShortcuts();
});

function initTerminalEffects() {
    // Add typing effect to boot sequence
    const bootLines = document.querySelectorAll('.boot-line');
    bootLines.forEach((line, index) => {
        line.style.animationDelay = `${index * 0.8}s`;
    });

    // Add scanlines effect
    createScanlines();
    
    // Add terminal flicker effect
    addFlickerEffect();
}

function createScanlines() {
    const container = document.querySelector('.terminal-container');
    const scanlines = document.createElement('div');
    scanlines.className = 'scanlines';
    scanlines.innerHTML = Array(50).fill('<div class="scanline"></div>').join('');
    container.appendChild(scanlines);
    
    // Add CSS for scanlines
    const style = document.createElement('style');
    style.textContent = `
        .scanlines {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 998;
        }
        
        .scanline {
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 0, 0.03), transparent);
            margin-bottom: 10px;
            animation: scanline-move 3s linear infinite;
        }
        
        @keyframes scanline-move {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
    `;
    document.head.appendChild(style);
}

function addFlickerEffect() {
    const content = document.querySelector('.terminal-content');
    
    setInterval(() => {
        if (Math.random() > 0.98) { // 2% chance every interval
            content.style.opacity = '0.8';
            setTimeout(() => {
                content.style.opacity = '1';
            }, 50);
        }
    }, 100);
}

function initInteractiveElements() {
    // Add click handlers to navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', handleNavClick);
        link.addEventListener('mouseenter', playTypingSound);
    });
    
    // Add interactive command prompts
    const prompts = document.querySelectorAll('.command-prompt');
    prompts.forEach(prompt => {
        prompt.addEventListener('click', simulateCommand);
    });
    
    // Add hover effects to feature items
    const featureItems = document.querySelectorAll('.feature-item');
    featureItems.forEach(item => {
        item.addEventListener('mouseenter', highlightFeature);
        item.addEventListener('mouseleave', unhighlightFeature);
    });
}

function handleNavClick(event) {
    event.preventDefault();
    const link = event.target;
    const filename = link.textContent;
    
    // Simulate terminal output for clicked documentation
    simulateDocumentationView(filename);
}

function simulateDocumentationView(filename) {
    const output = document.createElement('div');
    output.className = 'simulated-output';
    output.innerHTML = `
        <div class="command-prompt">
            <span class="prompt">$ cat ${filename}</span>
        </div>
        <div class="output">
            <p>Loading ${filename}...</p>
            <p style="color: var(--accent-color);">Documentation content would appear here</p>
            <p style="color: var(--neutral-color);">Press ESC to return to main view</p>
        </div>
    `;
    
    document.querySelector('.content-area').appendChild(output);
    
    // Add escape key handler
    const escHandler = (e) => {
        if (e.key === 'Escape') {
            output.remove();
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
}

function simulateCommand(event) {
    const prompt = event.target.closest('.command-prompt');
    const command = prompt.querySelector('.prompt').textContent.replace('$ ', '');
    
    // Add visual feedback
    prompt.style.background = 'rgba(0, 255, 0, 0.1)';
    setTimeout(() => {
        prompt.style.background = 'transparent';
    }, 200);
    
    // Log command to console with terminal styling
    console.log(`%c$ ${command}`, 'color: #00ff00; font-family: monospace; font-weight: bold;');
}

function highlightFeature(event) {
    const item = event.target;
    const desc = item.querySelector('.file-desc');
    
    if (desc) {
        desc.style.color = 'var(--primary-color)';
        desc.style.transition = 'color 0.3s ease';
    }
}

function unhighlightFeature(event) {
    const item = event.target;
    const desc = item.querySelector('.file-desc');
    
    if (desc) {
        desc.style.color = 'var(--neutral-color)';
    }
}

function playTypingSound() {
    // Create a subtle audio feedback (optional - can be disabled)
    if (window.AudioContext || window.webkitAudioContext) {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.setValueAtTime(1000, audioContext.currentTime);
        gainNode.gain.setValueAtTime(0.01, audioContext.currentTime);
        
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.02);
    }
}

function initKeyboardShortcuts() {
    document.addEventListener('keydown', (event) => {
        // Ctrl+C - simulate terminal interrupt
        if (event.ctrlKey && event.key === 'c') {
            event.preventDefault();
            showTerminalInterrupt();
        }
        
        // Ctrl+L - simulate clear screen
        if (event.ctrlKey && event.key === 'l') {
            event.preventDefault();
            simulateClearScreen();
        }
        
        // Arrow keys - navigate through features
        if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
            navigateFeatures(event.key === 'ArrowDown');
        }
    });
}

function showTerminalInterrupt() {
    const cursor = document.querySelector('.terminal-cursor');
    const originalText = cursor.textContent;
    
    cursor.textContent = '^C';
    cursor.style.color = 'var(--error-color)';
    
    setTimeout(() => {
        cursor.textContent = originalText;
        cursor.style.color = 'var(--cursor-color)';
    }, 1000);
}

function simulateClearScreen() {
    const content = document.querySelector('.content-area');
    content.style.opacity = '0';
    content.style.transform = 'translateY(-20px)';
    
    setTimeout(() => {
        content.style.opacity = '1';
        content.style.transform = 'translateY(0)';
        content.style.transition = 'all 0.5s ease';
    }, 300);
}

let currentFeatureIndex = -1;

function navigateFeatures(down) {
    const features = document.querySelectorAll('.feature-item');
    
    // Remove previous highlight
    if (currentFeatureIndex >= 0) {
        features[currentFeatureIndex].style.background = 'transparent';
        features[currentFeatureIndex].style.borderLeft = '3px solid transparent';
    }
    
    // Update index
    if (down) {
        currentFeatureIndex = (currentFeatureIndex + 1) % features.length;
    } else {
        currentFeatureIndex = currentFeatureIndex <= 0 ? features.length - 1 : currentFeatureIndex - 1;
    }
    
    // Highlight current feature
    const currentFeature = features[currentFeatureIndex];
    currentFeature.style.background = 'rgba(0, 255, 0, 0.15)';
    currentFeature.style.borderLeft = '3px solid var(--accent-color)';
    currentFeature.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Add performance monitoring
let frameCount = 0;
let lastTime = performance.now();

function monitorPerformance() {
    frameCount++;
    const currentTime = performance.now();
    
    if (currentTime - lastTime >= 1000) {
        const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
        console.log(`%cTerminal FPS: ${fps}`, 'color: #00ff00; font-family: monospace;');
        
        frameCount = 0;
        lastTime = currentTime;
    }
    
    requestAnimationFrame(monitorPerformance);
}

// Start performance monitoring in development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    monitorPerformance();
}

// Add easter egg - Konami code
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];

document.addEventListener('keydown', (event) => {
    konamiCode.push(event.code);
    
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        activateEasterEgg();
        konamiCode = [];
    }
});

function activateEasterEgg() {
    const cat = document.querySelector('.ascii-cat');
    const originalText = cat.textContent;
    
    // Matrix effect
    cat.textContent = '~(=^0^)';
    cat.style.color = '#ff0000';
    cat.style.animation = 'none';
    cat.style.textShadow = '0 0 20px #ff0000';
    
    // Create matrix rain effect
    createMatrixEffect();
    
    setTimeout(() => {
        cat.textContent = originalText;
        cat.style.color = 'var(--accent-color)';
        cat.style.animation = 'glow 2s ease-in-out infinite alternate';
        cat.style.textShadow = '0 0 10px var(--accent-color)';
        removeMatrixEffect();
    }, 5000);
}

function createMatrixEffect() {
    const matrixContainer = document.createElement('div');
    matrixContainer.className = 'matrix-effect';
    matrixContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1001;
        background: rgba(0, 0, 0, 0.8);
    `;
    
    for (let i = 0; i < 50; i++) {
        const drop = document.createElement('div');
        drop.style.cssText = `
            position: absolute;
            top: -100px;
            left: ${Math.random() * 100}%;
            color: #00ff00;
            font-family: monospace;
            font-size: 14px;
            animation: matrix-fall 3s linear infinite;
            animation-delay: ${Math.random() * 3}s;
        `;
        drop.textContent = String.fromCharCode(33 + Math.random() * 94);
        matrixContainer.appendChild(drop);
    }
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes matrix-fall {
            to { transform: translateY(100vh); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(matrixContainer);
    window.matrixContainer = matrixContainer;
    window.matrixStyle = style;
}

function removeMatrixEffect() {
    if (window.matrixContainer) {
        window.matrixContainer.remove();
        window.matrixStyle.remove();
    }
}