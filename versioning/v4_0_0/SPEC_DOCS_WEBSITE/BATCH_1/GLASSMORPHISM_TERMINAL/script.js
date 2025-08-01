// GLASSMORPHISM TERMINAL - Interactive features for modern glass terminal interface

document.addEventListener('DOMContentLoaded', function() {
    initializeGlassmorphismEffects();
    initializeTerminalAnimation();
    initializeInteractiveElements();
    initializeParallaxEffects();
});

// Initialize glassmorphism interactive effects
function initializeGlassmorphismEffects() {
    const glassPanels = document.querySelectorAll('.glass-panel');
    
    glassPanels.forEach(panel => {
        // Mouse move glass reflection effect
        panel.addEventListener('mousemove', (e) => {
            const rect = panel.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            panel.style.transform = `
                perspective(1000px) 
                rotateX(${rotateX}deg) 
                rotateY(${rotateY}deg)
                translateZ(10px)
            `;
            
            // Update glass reflection
            const glowIntensity = Math.min(
                Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2)) / 100,
                1
            );
            
            panel.style.boxShadow = `
                0 8px 32px rgba(0, 0, 0, 0.3),
                0 0 ${20 + glowIntensity * 20}px rgba(255, 255, 255, ${0.1 + glowIntensity * 0.1})
            `;
        });
        
        panel.addEventListener('mouseleave', () => {
            panel.style.transform = '';
            panel.style.boxShadow = '';
        });
    });
}

// Terminal typing animation
function initializeTerminalAnimation() {
    const commands = [
        'orchestrate --workflow analysis --parallel',
        'tools list --category search',
        'memory query --context workflow',
        'agents spawn --count 3 --type researcher'
    ];
    
    const outputs = [
        [
            '[INFO] Initializing modular orchestrator...',
            '[INFO] Loading workflow: analysis',
            '[INFO] Spawning 3 parallel agents...',
            '[SUCCESS] Orchestration complete'
        ],
        [
            '[INFO] Scanning tool directory...',
            '[INFO] Found 12 search tools',
            '[SUCCESS] Tools loaded successfully'
        ],
        [
            '[INFO] Querying memory system...',
            '[INFO] Context: workflow analysis',
            '[SUCCESS] Memory context retrieved'
        ],
        [
            '[INFO] Initializing agent spawner...',
            '[INFO] Creating researcher agents...',
            '[SUCCESS] 3 agents ready for deployment'
        ]
    ];
    
    let currentCommandIndex = 0;
    
    function typeCommand() {
        const commandElement = document.querySelector('.typing-animation');
        const outputContainer = document.querySelector('.terminal-output');
        
        if (!commandElement || !outputContainer) return;
        
        const command = commands[currentCommandIndex];
        const output = outputs[currentCommandIndex];
        
        // Clear previous content
        commandElement.textContent = '';
        outputContainer.innerHTML = '';
        
        // Type command
        let charIndex = 0;
        const typeInterval = setInterval(() => {
            commandElement.textContent = command.substring(0, charIndex + 1);
            charIndex++;
            
            if (charIndex >= command.length) {
                clearInterval(typeInterval);
                // Show output after command is typed
                setTimeout(() => showOutput(output, outputContainer), 500);
            }
        }, 50);
    }
    
    function showOutput(output, container) {
        let lineIndex = 0;
        const outputInterval = setInterval(() => {
            const line = document.createElement('div');
            line.className = 'output-line';
            line.textContent = output[lineIndex];
            
            // Add success class to success messages
            if (output[lineIndex].includes('[SUCCESS]')) {
                line.classList.add('success');
            }
            
            container.appendChild(line);
            lineIndex++;
            
            if (lineIndex >= output.length) {
                clearInterval(outputInterval);
                // Wait before next command
                setTimeout(() => {
                    currentCommandIndex = (currentCommandIndex + 1) % commands.length;
                    typeCommand();
                }, 3000);
            }
        }, 300);
    }
    
    // Start the animation
    typeCommand();
}

// Interactive elements
function initializeInteractiveElements() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            if (targetId.startsWith('#')) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ 
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Button interactions with glass effects
    document.querySelectorAll('.glass-button').forEach(button => {
        button.addEventListener('click', (e) => {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            
            button.style.position = 'relative';
            button.style.overflow = 'hidden';
            button.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Add ripple animation keyframes
    if (!document.querySelector('#ripple-animation')) {
        const style = document.createElement('style');
        style.id = 'ripple-animation';
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Parallax effects for terminal grid
function initializeParallaxEffects() {
    const terminalGrid = document.querySelector('.terminal-grid');
    
    if (!terminalGrid) return;
    
    let ticking = false;
    
    function updateParallax() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        
        terminalGrid.style.transform = `translate(${rate}px, ${rate}px)`;
        ticking = false;
    }
    
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    });
}

// Glass panel intersection observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all glass panels for scroll animations
document.addEventListener('DOMContentLoaded', () => {
    const glassPanels = document.querySelectorAll('.glass-panel');
    
    glassPanels.forEach(panel => {
        panel.style.opacity = '0';
        panel.style.transform = 'translateY(50px)';
        panel.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(panel);
    });
});

// ASCII cat animation
function initializeASCIICatAnimation() {
    const asciiCat = document.querySelector('.ascii-cat');
    if (!asciiCat) return;
    
    const catVariations = [
        '~(=^‥^)',
        '~(=^‥^)ノ',
        '~(=^‥^)/',
        '~(=^‥^)~'
    ];
    
    let currentCat = 0;
    
    setInterval(() => {
        currentCat = (currentCat + 1) % catVariations.length;
        asciiCat.textContent = catVariations[currentCat];
    }, 2000);
}

// Initialize cat animation
document.addEventListener('DOMContentLoaded', initializeASCIICatAnimation);