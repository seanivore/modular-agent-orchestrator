// NEON TERMINAL - Cyberpunk interactive features with neon effects

document.addEventListener('DOMContentLoaded', function() {
    initializeNeonEffects();
    initializeCyberpunkTerminal();
    initializeInteractiveElements();
    initializeStatsAnimations();
    initializeParticleSystem();
});

// Initialize neon glow effects
function initializeNeonEffects() {
    const neonElements = document.querySelectorAll('.neon-panel, .neon-button, .neon-link');
    
    neonElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            element.style.boxShadow = '0 0 30px rgba(0, 255, 136, 0.5)';
        });
        
        element.addEventListener('mouseleave', () => {
            element.style.boxShadow = '';
        });
    });
    
    // Feature card special effects
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.addEventListener('mouseenter', () => {
            const colors = ['var(--primary)', 'var(--neon-blue)', 'var(--accent)', 'var(--neon-purple)'];
            const color = colors[index % colors.length];
            card.style.borderColor = color;
            card.style.boxShadow = `0 0 25px ${color}`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.borderColor = '';
            card.style.boxShadow = '';
        });
    });
}

// Cyberpunk terminal with advanced animations
function initializeCyberpunkTerminal() {
    const commands = [
        {
            cmd: 'orchestrate --workflow analysis --parallel --agents 3',
            output: [
                { text: '[INFO] Initializing cyberpunk orchestrator...', type: 'info' },
                { text: '[INFO] Loading workflow: analysis', type: 'info' },
                { text: '[WARN] Spawning 3 parallel agents...', type: 'warn' },
                { text: '[SUCCESS] Orchestration complete - 3 agents online', type: 'success' },
                { text: '[DATA] Processing 1,247 data points...', type: 'data' }
            ]
        },
        {
            cmd: 'memory query --context deep_analysis --verbose',
            output: [
                { text: '[INFO] Accessing memory subsystem...', type: 'info' },
                { text: '[DATA] Context: deep_analysis found', type: 'data' },
                { text: '[INFO] Retrieving 847 memory fragments...', type: 'info' },
                { text: '[SUCCESS] Memory context loaded successfully', type: 'success' }
            ]
        },
        {
            cmd: 'tools scan --category ai --parallel --neon-mode',
            output: [
                { text: '[INFO] Scanning tool repository...', type: 'info' },
                { text: '[DATA] Found 23 AI tools available', type: 'data' },
                { text: '[WARN] Neon mode activated - enhanced performance', type: 'warn' },
                { text: '[SUCCESS] All tools loaded and ready', type: 'success' }
            ]
        },
        {
            cmd: 'agents status --realtime --cyberpunk-display',
            output: [
                { text: '[INFO] Querying agent status...', type: 'info' },
                { text: '[DATA] Agent-001: ACTIVE (processing)', type: 'data' },
                { text: '[DATA] Agent-002: ACTIVE (analyzing)', type: 'data' },
                { text: '[DATA] Agent-003: ACTIVE (coordinating)', type: 'data' },
                { text: '[SUCCESS] All agents operational', type: 'success' }
            ]
        }
    ];
    
    let currentCommandIndex = 0;
    
    function executeCommand() {
        const commandElement = document.querySelector('.typing-command');
        const outputContainer = document.querySelector('.terminal-output');
        const cursor = document.querySelector('.cursor');
        
        if (!commandElement || !outputContainer) return;
        
        const command = commands[currentCommandIndex];
        
        // Clear previous content
        commandElement.textContent = '';
        outputContainer.innerHTML = '';
        
        // Type command with cyberpunk effect
        let charIndex = 0;
        const typeInterval = setInterval(() => {
            commandElement.textContent = command.cmd.substring(0, charIndex + 1);
            charIndex++;
            
            // Add glitch effect occasionally
            if (Math.random() < 0.1) {
                commandElement.style.textShadow = '0 0 10px var(--neon-pink)';
                setTimeout(() => {
                    commandElement.style.textShadow = '0 0 5px var(--primary)';
                }, 50);
            }
            
            if (charIndex >= command.cmd.length) {
                clearInterval(typeInterval);
                cursor.style.display = 'none';
                setTimeout(() => showCyberpunkOutput(command.output, outputContainer), 300);
            }
        }, 60);
    }
    
    function showCyberpunkOutput(output, container) {
        let lineIndex = 0;
        const outputInterval = setInterval(() => {
            const outputData = output[lineIndex];
            const line = document.createElement('div');
            line.className = `output-line ${outputData.type}`;
            line.textContent = outputData.text;
            
            // Add entrance animation
            line.style.opacity = '0';
            line.style.transform = 'translateX(-20px)';
            container.appendChild(line);
            
            setTimeout(() => {
                line.style.transition = 'all 0.3s ease';
                line.style.opacity = '1';
                line.style.transform = 'translateX(0)';
            }, 50);
            
            lineIndex++;
            
            if (lineIndex >= output.length) {
                clearInterval(outputInterval);
                setTimeout(() => {
                    document.querySelector('.cursor').style.display = 'inline-block';
                    currentCommandIndex = (currentCommandIndex + 1) % commands.length;
                    executeCommand();
                }, 4000);
            }
        }, 400);
    }
    
    // Start the terminal animation
    executeCommand();
}

// Interactive elements with cyberpunk enhancements
function initializeInteractiveElements() {
    // Smooth scrolling with neon trail effect
    document.querySelectorAll('.neon-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            if (targetId.startsWith('#')) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    // Create neon trail effect
                    createNeonTrail(link);
                    targetElement.scrollIntoView({ 
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Enhanced button interactions
    document.querySelectorAll('.neon-button').forEach(button => {
        button.addEventListener('click', (e) => {
            // Cyberpunk click effect
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const explosion = document.createElement('div');
            explosion.style.cssText = `
                position: absolute;
                left: ${x}px;
                top: ${y}px;
                width: 4px;
                height: 4px;
                background: var(--primary);
                border-radius: 50%;
                transform: translate(-50%, -50%);
                animation: neon-explosion 0.6s ease-out forwards;
                pointer-events: none;
                box-shadow: 0 0 20px var(--primary);
            `;
            
            button.style.position = 'relative';
            button.appendChild(explosion);
            
            // Create multiple particles
            for (let i = 0; i < 8; i++) {
                setTimeout(() => {
                    createNeonParticle(button, x, y);
                }, i * 50);
            }
            
            setTimeout(() => explosion.remove(), 600);
        });
    });
    
    // Add explosion animation
    if (!document.querySelector('#neon-explosion')) {
        const style = document.createElement('style');
        style.id = 'neon-explosion';
        style.textContent = `
            @keyframes neon-explosion {
                0% {
                    transform: translate(-50%, -50%) scale(1);
                    opacity: 1;
                }
                100% {
                    transform: translate(-50%, -50%) scale(20);
                    opacity: 0;
                }
            }
            
            @keyframes neon-particle {
                0% {
                    transform: translate(-50%, -50%) scale(1);
                    opacity: 1;
                }
                100% {
                    transform: translate(-50%, -50%) translate(var(--dx), var(--dy)) scale(0);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Create neon particle effect
function createNeonParticle(container, centerX, centerY) {
    const particle = document.createElement('div');
    const angle = Math.random() * Math.PI * 2;
    const distance = 50 + Math.random() * 100;
    const dx = Math.cos(angle) * distance;
    const dy = Math.sin(angle) * distance;
    
    particle.style.cssText = `
        position: absolute;
        left: ${centerX}px;
        top: ${centerY}px;
        width: 2px;
        height: 2px;
        background: var(--primary);
        border-radius: 50%;
        --dx: ${dx}px;
        --dy: ${dy}px;
        animation: neon-particle 0.8s ease-out forwards;
        pointer-events: none;
        box-shadow: 0 0 10px var(--primary);
    `;
    
    container.appendChild(particle);
    setTimeout(() => particle.remove(), 800);
}

// Create neon trail effect
function createNeonTrail(element) {
    const trail = document.createElement('div');
    trail.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
        opacity: 0.7;
        animation: neon-trail 0.8s ease-out forwards;
        pointer-events: none;
        border-radius: 6px;
    `;
    
    element.style.position = 'relative';
    element.appendChild(trail);
    
    setTimeout(() => trail.remove(), 800);
    
    // Add trail animation
    if (!document.querySelector('#neon-trail')) {
        const style = document.createElement('style');
        style.id = 'neon-trail';
        style.textContent = `
            @keyframes neon-trail {
                0% { transform: translateX(-100%); }
                50% { transform: translateX(0%); }
                100% { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
}

// Animated statistics
function initializeStatsAnimations() {
    const statValues = document.querySelectorAll('.stat-value');
    const statFills = document.querySelectorAll('.stat-fill');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Animate stat values
                const statValue = entry.target.querySelector('.stat-value');
                if (statValue) {
                    const text = statValue.textContent;
                    if (text.includes('%')) {
                        const value = parseFloat(text);
                        animateValue(statValue, 0, value, 2000, '%');
                    } else if (text.includes('ms')) {
                        const value = parseInt(text);
                        animateValue(statValue, 0, value, 1500, 'ms', '< ');
                    } else if (text.includes('+')) {
                        const value = parseInt(text);
                        animateValue(statValue, 0, value, 2500, '+');
                    }
                }
                
                // Animate progress bars
                const statFill = entry.target.querySelector('.stat-fill');
                if (statFill) {
                    const width = statFill.style.width;
                    statFill.style.width = '0%';
                    setTimeout(() => {
                        statFill.style.transition = 'width 2s ease-out';
                        statFill.style.width = width;
                    }, 100);
                }
            }
        });
    }, { threshold: 0.5 });
    
    document.querySelectorAll('.stat-item').forEach(item => {
        observer.observe(item);
    });
}

// Animate number values
function animateValue(element, start, end, duration, suffix = '', prefix = '') {
    const range = end - start;
    const startTime = performance.now();
    
    function updateValue(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = start + (range * easeOut);
        
        if (suffix === '%') {
            element.textContent = current.toFixed(1) + suffix;
        } else if (suffix === 'ms') {
            element.textContent = prefix + Math.round(current) + suffix;
        } else if (suffix === '+') {
            element.textContent = Math.round(current).toLocaleString() + suffix;
        } else {
            element.textContent = prefix + Math.round(current) + suffix;
        }
        
        if (progress < 1) {
            requestAnimationFrame(updateValue);
        }
    }
    
    requestAnimationFrame(updateValue);
}

// Particle system for background
function initializeParticleSystem() {
    const particleContainer = document.createElement('div');
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    `;
    document.body.appendChild(particleContainer);
    
    function createFloatingParticle() {
        const particle = document.createElement('div');
        const size = Math.random() * 3 + 1;
        const x = Math.random() * window.innerWidth;
        const duration = Math.random() * 20000 + 10000;
        
        particle.style.cssText = `
            position: absolute;
            left: ${x}px;
            top: 100vh;
            width: ${size}px;
            height: ${size}px;
            background: var(--primary);
            border-radius: 50%;
            opacity: 0.3;
            animation: float-up ${duration}ms linear forwards;
            box-shadow: 0 0 ${size * 2}px var(--primary);
        `;
        
        particleContainer.appendChild(particle);
        
        setTimeout(() => {
            if (particle.parentNode) {
                particle.remove();
            }
        }, duration);
    }
    
    // Add floating animation
    if (!document.querySelector('#float-animation')) {
        const style = document.createElement('style');
        style.id = 'float-animation';
        style.textContent = `
            @keyframes float-up {
                0% {
                    transform: translateY(0) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 0.3;
                }
                90% {
                    opacity: 0.3;
                }
                100% {
                    transform: translateY(-100vh) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Create particles periodically
    setInterval(createFloatingParticle, 2000);
    
    // Create initial particles
    for (let i = 0; i < 5; i++) {
        setTimeout(createFloatingParticle, i * 400);
    }
}

// ASCII cat variations with cyberpunk theme
function initializeCyberpunkCat() {
    const asciiCat = document.querySelector('.neon-cat');
    if (!asciiCat) return;
    
    const catVariations = [
        '~(=^‥^)',
        '~(=^‥^)ノ',
        '~(=^‥^)/',
        '~(=^‥^)~',
        '~(=^‥^)⚡',
        '~(=^‥^)✨'
    ];
    
    let currentCat = 0;
    
    setInterval(() => {
        asciiCat.style.transform = 'scale(1.2)';
        asciiCat.style.textShadow = '0 0 20px var(--neon-pink)';
        
        setTimeout(() => {
            currentCat = (currentCat + 1) % catVariations.length;
            asciiCat.textContent = catVariations[currentCat];
            asciiCat.style.transform = 'scale(1)';
            asciiCat.style.textShadow = '0 0 10px var(--primary), 0 0 20px var(--primary)';
        }, 200);
    }, 3000);
}

// Initialize cyberpunk cat
document.addEventListener('DOMContentLoaded', initializeCyberpunkCat);