// GRADIENT TERMINAL - Modern interactive features with contemporary gradients

document.addEventListener('DOMContentLoaded', function() {
    initializeGradientEffects();
    initializeModernTerminal();
    initializeInteractiveElements();
    initializeScrollAnimations();
    initializeParallaxEffects();
});

// Initialize gradient interactive effects
function initializeGradientEffects() {
    // Dynamic gradient shifting on mouse movement
    const heroSection = document.querySelector('.hero-section');
    const gradientMesh = document.querySelector('.gradient-mesh');
    
    if (heroSection && gradientMesh) {
        heroSection.addEventListener('mousemove', (e) => {
            const rect = heroSection.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;
            const y = (e.clientY - rect.top) / rect.height;
            
            const gradientX1 = 20 + (x * 40);
            const gradientY1 = 80 - (y * 40);
            const gradientX2 = 80 - (x * 40);
            const gradientY2 = 20 + (y * 40);
            
            gradientMesh.style.background = `
                radial-gradient(circle at ${gradientX1}% ${gradientY1}%, rgba(0, 255, 136, 0.15) 0%, transparent 50%),
                radial-gradient(circle at ${gradientX2}% ${gradientY2}%, rgba(78, 205, 196, 0.15) 0%, transparent 50%),
                radial-gradient(circle at ${40 + x * 20}% ${40 + y * 20}%, rgba(255, 107, 107, 0.10) 0%, transparent 50%)
            `;
        });
    }
    
    // Feature card gradient interactions
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        const gradients = [
            'linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(78, 205, 196, 0.1) 100%)',
            'linear-gradient(135deg, rgba(78, 205, 196, 0.1) 0%, rgba(66, 165, 245, 0.1) 100%)',
            'linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 167, 38, 0.1) 100%)',
            'linear-gradient(135deg, rgba(117, 117, 117, 0.1) 0%, rgba(168, 168, 168, 0.1) 100%)'
        ];
        
        card.addEventListener('mouseenter', () => {
            card.style.background = gradients[index % gradients.length];
            card.style.borderColor = 'rgba(255, 255, 255, 0.3)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.background = '';
            card.style.borderColor = '';
        });
    });
}

// Modern terminal with sophisticated animations
function initializeModernTerminal() {
    const commands = [
        {
            cmd: 'mao orchestrate --workflow data_analysis --parallel',
            output: [
                { text: '✓ Orchestrator initialized successfully', type: 'success', delay: 300 },
                { text: '▶ Loading workflow: data_analysis', type: 'info', delay: 600 },
                { text: '📊 Spawning 3 parallel analysis agents', type: 'data', delay: 900 },
                { text: '🔄 Processing 15,847 data points...', type: 'info', delay: 1200 },
                { text: '✅ Analysis complete - insights generated', type: 'success', delay: 1500 }
            ]
        },
        {
            cmd: 'mao memory query --context research --format json',
            output: [
                { text: '🧠 Accessing memory subsystem...', type: 'info', delay: 300 },
                { text: '📋 Context: research found (847 entries)', type: 'data', delay: 600 },
                { text: '🔍 Retrieving contextual memory fragments', type: 'info', delay: 900 },
                { text: '📄 Formatting output as JSON structure', type: 'info', delay: 1200 },
                { text: '✓ Memory context retrieved successfully', type: 'success', delay: 1500 }
            ]
        },
        {
            cmd: 'mao tools discover --category ai --auto-install',
            output: [
                { text: '🔍 Scanning tool repositories...', type: 'info', delay: 300 },
                { text: '📦 Found 23 AI tools available', type: 'data', delay: 600 },
                { text: '⬇️ Auto-installing 5 new tools...', type: 'info', delay: 900 },
                { text: '🔧 Configuring tool integrations', type: 'info', delay: 1200 },
                { text: '✅ All tools loaded and ready', type: 'success', delay: 1500 }
            ]
        },
        {
            cmd: 'mao agents spawn --type researcher --count 4 --monitor',
            output: [
                { text: '🚀 Initializing agent spawner...', type: 'info', delay: 300 },
                { text: '👥 Creating 4 researcher agents', type: 'data', delay: 600 },
                { text: '🎯 Agent-001: ACTIVE (literature review)', type: 'success', delay: 900 },
                { text: '🎯 Agent-002: ACTIVE (data mining)', type: 'success', delay: 1000 },
                { text: '🎯 Agent-003: ACTIVE (trend analysis)', type: 'success', delay: 1100 },
                { text: '🎯 Agent-004: ACTIVE (report generation)', type: 'success', delay: 1200 },
                { text: '📊 Real-time monitoring enabled', type: 'info', delay: 1500 }
            ]
        }
    ];
    
    let currentCommandIndex = 0;
    let isTyping = false;
    
    function executeModernCommand() {
        if (isTyping) return;
        
        const typedCommand = document.querySelector('.typed-command');
        const outputContainer = document.querySelector('.output-container');
        const cursor = document.querySelector('.typing-cursor');
        
        if (!typedCommand || !outputContainer) return;
        
        isTyping = true;
        const command = commands[currentCommandIndex];
        
        // Clear previous content with fade
        outputContainer.style.opacity = '0';
        setTimeout(() => {
            outputContainer.innerHTML = '';
            outputContainer.style.opacity = '1';
        }, 200);
        
        // Type command with realistic typing speed
        typedCommand.textContent = '';
        cursor.style.opacity = '1';
        
        let charIndex = 0;
        const typeInterval = setInterval(() => {
            typedCommand.textContent = command.cmd.substring(0, charIndex + 1);
            charIndex++;
            
            // Add occasional typing variations
            const baseSpeed = 80;
            const variation = Math.random() * 40 - 20;
            
            if (charIndex >= command.cmd.length) {
                clearInterval(typeInterval);
                cursor.style.opacity = '0';
                setTimeout(() => showModernOutput(command.output, outputContainer), 400);
            }
        }, baseSpeed);
    }
    
    function showModernOutput(output, container) {
        output.forEach((line, index) => {
            setTimeout(() => {
                const outputLine = document.createElement('div');
                outputLine.className = `output-line ${line.type}`;
                outputLine.textContent = line.text;
                
                // Add entrance animation
                outputLine.style.opacity = '0';
                outputLine.style.transform = 'translateX(-20px)';
                container.appendChild(outputLine);
                
                // Animate in with stagger
                setTimeout(() => {
                    outputLine.style.transition = 'all 0.4s ease';
                    outputLine.style.opacity = '1';
                    outputLine.style.transform = 'translateX(0)';
                }, 50);
                
                // If this is the last line, prepare for next command
                if (index === output.length - 1) {
                    setTimeout(() => {
                        isTyping = false;
                        currentCommandIndex = (currentCommandIndex + 1) % commands.length;
                        setTimeout(executeModernCommand, 3000);
                    }, 1000);
                }
            }, line.delay);
        });
    }
    
    // Start the terminal demo
    setTimeout(executeModernCommand, 1000);
}

// Enhanced interactive elements
function initializeInteractiveElements() {
    // Smooth scrolling with gradient trail
    document.querySelectorAll('.nav-item, .footer-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            if (targetId && targetId.startsWith('#')) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    // Create gradient trail effect
                    createGradientTrail(link);
                    targetElement.scrollIntoView({ 
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Enhanced button interactions
    document.querySelectorAll('.gradient-button').forEach(button => {
        button.addEventListener('click', (e) => {
            // Modern ripple effect with gradient
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('div');
            ripple.style.cssText = `
                position: absolute;
                left: ${x}px;
                top: ${y}px;
                width: 0;
                height: 0;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(255,255,255,0.6) 0%, rgba(255,255,255,0.1) 70%, transparent 100%);
                transform: translate(-50%, -50%);
                animation: modern-ripple 0.6s ease-out;
                pointer-events: none;
                z-index: 10;
            `;
            
            button.style.position = 'relative';
            button.style.overflow = 'hidden';
            button.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
        
        // Gradient button hover effects
        button.addEventListener('mouseenter', () => {
            if (button.classList.contains('primary')) {
                button.style.background = 'linear-gradient(135deg, #00ff88 0%, #4ecdc4 50%, #42a5f5 100%)';
            } else {
                button.style.background = 'linear-gradient(135deg, rgba(78, 205, 196, 0.2) 0%, rgba(66, 165, 245, 0.2) 100%)';
                button.style.borderColor = '#42a5f5';
            }
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.background = '';
            button.style.borderColor = '';
        });
    });
    
    // Add modern ripple animation
    if (!document.querySelector('#modern-ripple')) {
        const style = document.createElement('style');
        style.id = 'modern-ripple';
        style.textContent = `
            @keyframes modern-ripple {
                0% {
                    width: 0;
                    height: 0;
                    opacity: 1;
                }
                100% {
                    width: 300px;
                    height: 300px;
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Create gradient trail effect
function createGradientTrail(element) {
    const trail = document.createElement('div');
    trail.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.3), rgba(78, 205, 196, 0.3), transparent);
        opacity: 0;
        border-radius: inherit;
        animation: gradient-trail 0.8s ease-out forwards;
        pointer-events: none;
    `;
    
    element.style.position = 'relative';
    element.appendChild(trail);
    
    setTimeout(() => trail.remove(), 800);
    
    // Add trail animation
    if (!document.querySelector('#gradient-trail')) {
        const style = document.createElement('style');
        style.id = 'gradient-trail';
        style.textContent = `
            @keyframes gradient-trail {
                0% { 
                    transform: translateX(-100%); 
                    opacity: 0; 
                }
                50% { 
                    opacity: 1; 
                }
                100% { 
                    transform: translateX(100%); 
                    opacity: 0; 
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Advanced scroll animations
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const fadeInObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                
                // Staggered animation for feature cards
                if (entry.target.classList.contains('features-grid')) {
                    const cards = entry.target.querySelectorAll('.feature-card');
                    cards.forEach((card, index) => {
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, index * 150);
                    });
                }
                
                // Architecture layer animations
                if (entry.target.classList.contains('architecture-flow')) {
                    const layers = entry.target.querySelectorAll('.arch-layer');
                    layers.forEach((layer, index) => {
                        setTimeout(() => {
                            layer.style.opacity = '1';
                            layer.style.transform = 'translateY(0)';
                        }, index * 200);
                    });
                }
            }
        });
    }, observerOptions);
    
    // Observe elements for scroll animations
    const animatedElements = document.querySelectorAll('.feature-card, .arch-layer, .features-grid, .architecture-flow, .section-header');
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(50px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        fadeInObserver.observe(element);
    });
    
    // Progress indicator for sections
    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progress = document.createElement('div');
                progress.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    height: 3px;
                    background: linear-gradient(90deg, var(--primary), var(--accent));
                    z-index: 1000;
                    animation: progress-fill 2s ease-out forwards;
                `;
                
                document.body.appendChild(progress);
                setTimeout(() => progress.remove(), 2000);
                
                // Add progress animation
                if (!document.querySelector('#progress-fill')) {
                    const style = document.createElement('style');
                    style.id = 'progress-fill';
                    style.textContent = `
                        @keyframes progress-fill {
                            0% { width: 0%; }
                            100% { width: 100%; }
                        }
                    `;
                    document.head.appendChild(style);
                }
            }
        });
    }, { threshold: 0.5 });
    
    document.querySelectorAll('.features-section, .architecture-section, .terminal-demo-section').forEach(section => {
        progressObserver.observe(section);
    });
}

// Parallax effects for modern feel
function initializeParallaxEffects() {
    const gridPattern = document.querySelector('.grid-pattern');
    const gradientMesh = document.querySelector('.gradient-mesh');
    
    let ticking = false;
    
    function updateParallax() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.3;
        const meshRate = scrolled * -0.1;
        
        if (gridPattern) {
            gridPattern.style.transform = `translate(${rate}px, ${rate}px)`;
        }
        
        if (gradientMesh) {
            gradientMesh.style.transform = `translateY(${meshRate}px)`;
        }
        
        ticking = false;
    }
    
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    });
    
    // Mouse parallax for hero section
    const heroVisual = document.querySelector('.hero-visual');
    if (heroVisual) {
        heroVisual.addEventListener('mousemove', (e) => {
            const rect = heroVisual.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            
            const terminalWindow = heroVisual.querySelector('.terminal-window');
            if (terminalWindow) {
                terminalWindow.style.transform = `
                    perspective(1000px) 
                    rotateY(${x * 10}deg) 
                    rotateX(${-y * 10}deg)
                    translateZ(20px)
                `;
            }
        });
        
        heroVisual.addEventListener('mouseleave', () => {
            const terminalWindow = heroVisual.querySelector('.terminal-window');
            if (terminalWindow) {
                terminalWindow.style.transform = '';
            }
        });
    }
}

// Advanced ASCII cat animations
function initializeAdvancedCat() {
    const asciiCats = document.querySelectorAll('.ascii-cat, .ascii-cat-footer');
    
    const catStates = [
        '~(=^‥^)',
        '~(=^‥^)ノ',
        '~(=^‥^)/',
        '~(=^‥^)~',
        '~(=^‥^)✨',
        '~(=^‥^)⭐'
    ];
    
    asciiCats.forEach(cat => {
        let currentState = 0;
        
        setInterval(() => {
            // Smooth transition effect
            cat.style.transform = 'scale(1.1) rotate(5deg)';
            cat.style.transition = 'transform 0.2s ease';
            
            setTimeout(() => {
                currentState = (currentState + 1) % catStates.length;
                cat.textContent = catStates[currentState];
                cat.style.transform = '';
            }, 100);
        }, 4000);
        
        // Click interaction
        cat.addEventListener('click', () => {
            cat.style.animation = 'cat-celebration 1s ease-in-out';
            setTimeout(() => {
                cat.style.animation = '';
            }, 1000);
        });
    });
    
    // Add celebration animation
    if (!document.querySelector('#cat-celebration')) {
        const style = document.createElement('style');
        style.id = 'cat-celebration';
        style.textContent = `
            @keyframes cat-celebration {
                0%, 100% { transform: scale(1) rotate(0deg); }
                25% { transform: scale(1.3) rotate(10deg); }
                50% { transform: scale(1.2) rotate(-10deg); }
                75% { transform: scale(1.3) rotate(10deg); }
            }
        `;
        document.head.appendChild(style);
    }
}

// Performance monitoring
function initializePerformanceMonitoring() {
    // Monitor frame rate
    let lastTime = performance.now();
    let frameCount = 0;
    
    function checkPerformance() {
        frameCount++;
        const currentTime = performance.now();
        
        if (currentTime - lastTime >= 1000) {
            const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
            
            // Adjust animations based on performance
            if (fps < 30) {
                document.body.classList.add('reduced-motion');
            } else {
                document.body.classList.remove('reduced-motion');
            }
            
            frameCount = 0;
            lastTime = currentTime;
        }
        
        requestAnimationFrame(checkPerformance);
    }
    
    requestAnimationFrame(checkPerformance);
    
    // Add reduced motion styles
    if (!document.querySelector('#reduced-motion')) {
        const style = document.createElement('style');
        style.id = 'reduced-motion';
        style.textContent = `
            .reduced-motion * {
                animation-duration: 0.1s !important;
                transition-duration: 0.1s !important;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize all advanced features
document.addEventListener('DOMContentLoaded', () => {
    initializeAdvancedCat();
    initializePerformanceMonitoring();
});