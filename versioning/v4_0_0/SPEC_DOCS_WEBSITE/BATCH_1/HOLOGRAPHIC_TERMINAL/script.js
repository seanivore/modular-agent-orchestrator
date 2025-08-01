// Holographic Terminal Interactive Effects
class HolographicTerminal {
    constructor() {
        this.init();
        this.setupParallax();
        this.setupTypingAnimation();
        this.setupMouseEffects();
        this.setupResponsiveEffects();
    }

    init() {
        console.log('Initializing Holographic Terminal Interface...');
        this.container = document.querySelector('.holographic-container');
        this.layers = document.querySelectorAll('.depth-layer');
        this.particles = document.querySelector('.floating-particles');
        this.terminal = document.querySelector('.terminal-body');
        this.cursor = document.querySelector('.typing-cursor');
        
        // Add additional holographic elements
        this.createHolographicEffects();
    }

    setupParallax() {
        let mouseX = 0;
        let mouseY = 0;
        let targetX = 0;
        let targetY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX - window.innerWidth / 2) / window.innerWidth;
            mouseY = (e.clientY - window.innerHeight / 2) / window.innerHeight;
        });

        const updateParallax = () => {
            targetX += (mouseX - targetX) * 0.05;
            targetY += (mouseY - targetY) * 0.05;

            this.layers.forEach((layer, index) => {
                const depth = (index + 1) * 0.5;
                const rotateY = targetX * depth * 2;
                const rotateX = -targetY * depth * 2;
                const translateZ = index === 0 ? -200 : index === 1 ? -100 : index === 2 ? 0 : index === 3 ? 50 : 100;
                
                layer.style.transform = `
                    translateZ(${translateZ}px) 
                    rotateY(${rotateY}deg) 
                    rotateX(${rotateX}deg)
                `;
            });

            requestAnimationFrame(updateParallax);
        };

        updateParallax();
    }

    setupTypingAnimation() {
        const commands = [
            'mao --help',
            'mao agents list',
            'mao workflow create',
            'mao memory sync',
            'mao chat --model claude-sonnet-4',
            'mao tools install',
            'mao orchestrate --parallel'
        ];

        let commandIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let currentCommand = '';

        const typeCommand = () => {
            const fullCommand = commands[commandIndex];
            
            if (isDeleting) {
                currentCommand = fullCommand.substring(0, charIndex - 1);
                charIndex--;
            } else {
                currentCommand = fullCommand.substring(0, charIndex + 1);
                charIndex++;
            }

            // Update terminal display
            const terminalLine = document.querySelector('.terminal-line');
            if (terminalLine) {
                const commandSpan = terminalLine.querySelector('.typing-command');
                if (!commandSpan) {
                    const newCommandSpan = document.createElement('span');
                    newCommandSpan.className = 'typing-command';
                    newCommandSpan.style.color = 'var(--mao-primary)';
                    newCommandSpan.style.marginLeft = '0.5rem';
                    terminalLine.insertBefore(newCommandSpan, this.cursor);
                }
                terminalLine.querySelector('.typing-command').textContent = currentCommand;
            }

            let typeSpeed = isDeleting ? 50 : 100;

            if (!isDeleting && charIndex === fullCommand.length) {
                typeSpeed = 2000; // Pause at end
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                commandIndex = (commandIndex + 1) % commands.length;
                typeSpeed = 500;
            }

            setTimeout(typeCommand, typeSpeed);
        };

        // Start typing animation after a delay
        setTimeout(typeCommand, 1000);
    }

    setupMouseEffects() {
        // Add holographic mouse trail
        const trail = [];
        const maxTrailLength = 20;

        document.addEventListener('mousemove', (e) => {
            trail.push({ x: e.clientX, y: e.clientY, opacity: 1 });
            
            if (trail.length > maxTrailLength) {
                trail.shift();
            }

            this.updateMouseTrail(trail);
        });

        // Create trail elements
        for (let i = 0; i < maxTrailLength; i++) {
            const trailElement = document.createElement('div');
            trailElement.className = 'mouse-trail';
            trailElement.style.cssText = `
                position: fixed;
                width: 4px;
                height: 4px;
                background: var(--mao-primary);
                border-radius: 50%;
                pointer-events: none;
                z-index: 1000;
                box-shadow: 0 0 10px var(--holo-glow);
                opacity: 0;
                transition: opacity 0.1s ease;
            `;
            document.body.appendChild(trailElement);
        }
    }

    updateMouseTrail(trail) {
        const trailElements = document.querySelectorAll('.mouse-trail');
        
        trail.forEach((point, index) => {
            if (trailElements[index]) {
                const opacity = (1 - index / trail.length) * 0.7;
                trailElements[index].style.left = `${point.x}px`;
                trailElements[index].style.top = `${point.y}px`;
                trailElements[index].style.opacity = opacity;
            }
        });
    }

    createHolographicEffects() {
        // Add scanning lines effect
        const scanLine = document.createElement('div');
        scanLine.className = 'scan-line';
        scanLine.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, 
                transparent, 
                var(--mao-primary), 
                transparent);
            z-index: 1000;
            pointer-events: none;
            animation: scanMove 3s linear infinite;
        `;

        // Add scan line animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes scanMove {
                0% { top: -2px; opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { top: 100vh; opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(scanLine);

        // Add holographic noise
        this.createHolographicNoise();
    }

    createHolographicNoise() {
        const noise = document.createElement('div');
        noise.className = 'holographic-noise';
        noise.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><defs><filter id="noise"><feTurbulence baseFrequency="0.9"/></filter></defs><rect width="100%" height="100%" filter="url(%23noise)" opacity="0.03"/></svg>');
            z-index: 999;
            pointer-events: none;
            animation: noiseMove 0.5s linear infinite;
        `;

        const noiseStyle = document.createElement('style');
        noiseStyle.textContent = `
            @keyframes noiseMove {
                0% { transform: translate(0, 0); }
                100% { transform: translate(-10px, -10px); }
            }
        `;
        document.head.appendChild(noiseStyle);
        document.body.appendChild(noise);
    }

    setupResponsiveEffects() {
        // Adjust effects based on screen size
        const updateEffects = () => {
            const isMobile = window.innerWidth <= 768;
            const effects = document.querySelectorAll('.mouse-trail, .scan-line, .holographic-noise');
            
            effects.forEach(effect => {
                if (isMobile) {
                    effect.style.display = 'none';
                } else {
                    effect.style.display = 'block';
                }
            });
        };

        window.addEventListener('resize', updateEffects);
        updateEffects(); // Initial call
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new HolographicTerminal();
});

// Add smooth scrolling for any anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Performance optimization: Reduce effects on low-end devices
if (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4) {
    document.documentElement.style.setProperty('--animation-speed', '2s');
}