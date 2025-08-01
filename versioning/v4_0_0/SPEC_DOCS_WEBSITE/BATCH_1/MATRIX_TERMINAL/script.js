// Matrix Terminal Interactive Effects
class MatrixTerminal {
    constructor() {
        this.init();
        this.setupMatrixRain();
        this.setupTerminalEffects();
        this.setupInteractiveElements();
        this.setupProgressAnimations();
        this.setupRealTimeUpdates();
    }

    init() {
        console.log('Initializing Matrix Terminal Interface...');
        this.canvas = document.getElementById('matrix-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.timeElement = document.getElementById('matrix-time');
        this.agentCount = document.getElementById('agent-count');
        this.processCount = document.getElementById('process-count');
        this.uptime = document.getElementById('uptime');
        this.currentCommand = document.getElementById('current-command');
        
        this.startTime = Date.now();
        this.matrixChars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()';
        this.drops = [];
        this.commands = [
            'mao chat --model claude-sonnet-4',
            'mao agents orchestrate --parallel',
            'mao workflow create --chain research,analyze,report',
            'mao memory sync --session-context',
            'mao tools install --category analysis',
            'mao config set --reality-mode true',
            'mao status --verbose',
            'mao help --commands'
        ];
        this.commandIndex = 0;
        
        this.resizeCanvas();
        this.initializeDrops();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        
        // Recalculate drops when canvas is resized
        this.initializeDrops();
        
        window.addEventListener('resize', () => {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
            this.initializeDrops();
        });
    }

    initializeDrops() {
        this.drops = [];
        const columns = Math.floor(this.canvas.width / 20);
        
        for (let i = 0; i < columns; i++) {
            this.drops[i] = {
                y: Math.random() * this.canvas.height,
                speed: Math.random() * 3 + 1,
                chars: [],
                opacity: Math.random() * 0.5 + 0.3
            };
            
            // Initialize character trail for each drop
            for (let j = 0; j < 20; j++) {
                this.drops[i].chars[j] = {
                    char: this.matrixChars[Math.floor(Math.random() * this.matrixChars.length)],
                    changeTime: Math.random() * 100
                };
            }
        }
    }

    setupMatrixRain() {
        const animate = () => {
            // Semi-transparent black background for trailing effect
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            
            this.ctx.font = '15px monospace';
            
            for (let i = 0; i < this.drops.length; i++) {
                const drop = this.drops[i];
                const x = i * 20;
                
                // Draw character trail
                for (let j = 0; j < drop.chars.length; j++) {
                    const y = drop.y - (j * 20);
                    if (y > 0 && y < this.canvas.height) {
                        // Update character occasionally
                        drop.chars[j].changeTime--;
                        if (drop.chars[j].changeTime <= 0) {
                            drop.chars[j].char = this.matrixChars[Math.floor(Math.random() * this.matrixChars.length)];
                            drop.chars[j].changeTime = Math.random() * 100 + 50;
                        }
                        
                        // Color gradient - brightest at head, fading down
                        const alpha = j === 0 ? 1 : Math.max(0, 1 - (j / 10));
                        if (j === 0) {
                            this.ctx.fillStyle = '#ffffff'; // White head
                        } else if (j < 3) {
                            this.ctx.fillStyle = `rgba(0, 255, 65, ${alpha})`;
                        } else {
                            this.ctx.fillStyle = `rgba(0, 143, 17, ${alpha * drop.opacity})`;
                        }
                        
                        this.ctx.fillText(drop.chars[j].char, x, y);
                    }
                }
                
                // Move drop down
                drop.y += drop.speed;
                
                // Reset drop when it goes off screen
                if (drop.y > this.canvas.height + drop.chars.length * 20) {
                    drop.y = -drop.chars.length * 20;
                    drop.speed = Math.random() * 3 + 1;
                    drop.opacity = Math.random() * 0.5 + 0.3;
                }
            }
            
            requestAnimationFrame(animate);
        };
        
        animate();
    }

    setupTerminalEffects() {
        // Add glitch effects randomly
        setInterval(() => {
            this.addGlitchEffect();
        }, Math.random() * 5000 + 3000);
        
        // Add screen flash effect
        setInterval(() => {
            this.addScreenFlash();
        }, Math.random() * 10000 + 5000);
    }

    addGlitchEffect() {
        const glitchLayer = document.querySelector('.glitch-layer');
        glitchLayer.style.animation = 'none';
        
        setTimeout(() => {
            glitchLayer.style.animation = 'glitchShift 0.1s infinite';
        }, 10);
        
        // Add temporary color distortion
        const terminal = document.querySelector('.terminal-interface');
        terminal.style.filter = 'hue-rotate(10deg) saturate(1.2)';
        
        setTimeout(() => {
            terminal.style.filter = '';
        }, 200);
    }

    addScreenFlash() {
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 255, 65, 0.1);
            z-index: 15;
            pointer-events: none;
            animation: flashEffect 0.1s ease-out;
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes flashEffect {
                0% { opacity: 0; }
                50% { opacity: 1; }
                100% { opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(flash);
        
        setTimeout(() => {
            document.body.removeChild(flash);
        }, 100);
    }

    setupInteractiveElements() {
        // Command typing simulation
        this.startCommandTyping();
        
        // Add keyboard event listeners
        document.addEventListener('keydown', (e) => {
            this.handleKeyPress(e);
        });
        
        // Add mouse interaction effects
        document.addEventListener('mousemove', (e) => {
            this.handleMouseMove(e);
        });
        
        // Add click effects
        document.addEventListener('click', (e) => {
            this.addClickEffect(e);
        });
    }

    startCommandTyping() {
        let charIndex = 0;
        let currentCommandText = '';
        const currentCommand = this.commands[this.commandIndex];
        
        const typeChar = () => {
            if (charIndex < currentCommand.length) {
                currentCommandText += currentCommand[charIndex];
                this.currentCommand.textContent = currentCommandText;
                charIndex++;
                
                // Variable typing speed
                const speed = Math.random() * 100 + 50;
                setTimeout(typeChar, speed);
            } else {
                // Pause, then delete and start next command
                setTimeout(() => {
                    this.deleteCommand(currentCommandText, () => {
                        this.commandIndex = (this.commandIndex + 1) % this.commands.length;
                        charIndex = 0;
                        currentCommandText = '';
                        setTimeout(() => {
                            this.startCommandTyping();
                        }, 500);
                    });
                }, 2000);
            }
        };
        
        typeChar();
    }

    deleteCommand(text, callback) {
        let currentText = text;
        
        const deleteChar = () => {
            if (currentText.length > 0) {
                currentText = currentText.slice(0, -1);
                this.currentCommand.textContent = currentText;
                
                setTimeout(deleteChar, 30);
            } else {
                callback();
            }
        };
        
        deleteChar();
    }

    handleKeyPress(e) {
        // Add keystroke effect
        const terminal = document.querySelector('.terminal-interface');
        terminal.style.boxShadow = `
            0 0 30px var(--matrix-glow),
            inset 0 0 30px rgba(0, 255, 65, 0.2)
        `;
        
        setTimeout(() => {
            terminal.style.boxShadow = `
                0 0 20px var(--matrix-glow),
                inset 0 0 20px rgba(0, 255, 65, 0.1)
            `;
        }, 100);
        
        // Special effects for certain keys
        if (e.key === 'Enter') {
            this.addMatrixBurst();
        }
    }

    handleMouseMove(e) {
        // Create matrix particle trail
        if (Math.random() < 0.1) { // Only sometimes, to avoid performance issues
            this.createMatrixParticle(e.clientX, e.clientY);
        }
    }

    createMatrixParticle(x, y) {
        const particle = document.createElement('div');
        const char = this.matrixChars[Math.floor(Math.random() * this.matrixChars.length)];
        
        particle.textContent = char;
        particle.style.cssText = `
            position: fixed;
            left: ${x}px;
            top: ${y}px;
            color: var(--mao-primary);
            font-family: 'Courier New', monospace;
            font-size: 12px;
            pointer-events: none;
            z-index: 20;
            animation: particleFade 1s ease-out forwards;
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes particleFade {
                0% { opacity: 1; transform: translateY(0px); }
                100% { opacity: 0; transform: translateY(-20px); }
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(particle);
        
        setTimeout(() => {
            if (document.body.contains(particle)) {
                document.body.removeChild(particle);
            }
        }, 1000);
    }

    addClickEffect(e) {
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: fixed;
            left: ${e.clientX - 25}px;
            top: ${e.clientY - 25}px;
            width: 50px;
            height: 50px;
            border: 2px solid var(--mao-primary);
            border-radius: 50%;
            pointer-events: none;
            z-index: 25;
            animation: rippleEffect 0.6s ease-out forwards;
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes rippleEffect {
                0% { transform: scale(0); opacity: 1; }
                100% { transform: scale(2); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(ripple);
        
        setTimeout(() => {
            if (document.body.contains(ripple)) {
                document.body.removeChild(ripple);
            }
        }, 600);
    }

    addMatrixBurst() {
        for (let i = 0; i < 10; i++) {
            setTimeout(() => {
                const burst = document.createElement('div');
                const char = this.matrixChars[Math.floor(Math.random() * this.matrixChars.length)];
                
                burst.textContent = char;
                burst.style.cssText = `
                    position: fixed;
                    left: ${Math.random() * window.innerWidth}px;
                    top: ${Math.random() * window.innerHeight}px;
                    color: var(--mao-light-green);
                    font-family: 'Courier New', monospace;
                    font-size: 20px;
                    pointer-events: none;
                    z-index: 20;
                    text-shadow: 0 0 10px var(--matrix-glow);
                    animation: burstFade 2s ease-out forwards;
                `;
                
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes burstFade {
                        0% { opacity: 1; transform: scale(1); }
                        50% { opacity: 1; transform: scale(1.5); }
                        100% { opacity: 0; transform: scale(0.5); }
                    }
                `;
                document.head.appendChild(style);
                document.body.appendChild(burst);
                
                setTimeout(() => {
                    if (document.body.contains(burst)) {
                        document.body.removeChild(burst);
                    }
                }, 2000);
            }, i * 100);
        }
    }

    setupProgressAnimations() {
        // Animate progress bars with delays
        const progressFills = document.querySelectorAll('.progress-fill');
        progressFills.forEach((fill, index) => {
            const width = fill.getAttribute('data-width') || '100';
            fill.style.setProperty('--target-width', width + '%');
            
            // Start animation with delay based on install sequence
            setTimeout(() => {
                fill.style.animation = 'progressFill 1s ease-in-out forwards';
            }, (index + 1) * 1000);
        });
    }

    setupRealTimeUpdates() {
        // Update timestamp
        const updateTime = () => {
            const now = new Date();
            const timeString = now.toLocaleTimeString('en-US', { 
                hour12: false,
                timeZone: 'UTC'
            });
            if (this.timeElement) {
                this.timeElement.textContent = timeString + ' UTC';
            }
        };
        
        updateTime();
        setInterval(updateTime, 1000);
        
        // Update uptime
        const updateUptime = () => {
            const elapsed = Date.now() - this.startTime;
            const hours = Math.floor(elapsed / 3600000);
            const minutes = Math.floor((elapsed % 3600000) / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);
            
            const upTimeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            if (this.uptime) {
                this.uptime.textContent = upTimeString;
            }
        };
        
        updateUptime();
        setInterval(updateUptime, 1000);
        
        // Simulate changing agent and process counts
        const updateCounts = () => {
            if (this.agentCount) {
                const agents = Math.floor(Math.random() * 8) + 1;
                this.agentCount.textContent = agents;
            }
            
            if (this.processCount) {
                const processes = Math.floor(Math.random() * 50) + 10;
                this.processCount.textContent = processes;
            }
        };
        
        updateCounts();
        setInterval(updateCounts, 5000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MatrixTerminal();
});

// Add context menu override for authentic terminal feel
document.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    
    // Show matrix-style context menu
    const contextMenu = document.createElement('div');
    contextMenu.style.cssText = `
        position: fixed;
        left: ${e.clientX}px;
        top: ${e.clientY}px;
        background: var(--terminal-bg);
        border: 1px solid var(--mao-primary);
        border-radius: 4px;
        padding: 0.5rem;
        z-index: 1000;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: var(--mao-primary);
        box-shadow: 0 0 10px var(--matrix-glow);
    `;
    
    contextMenu.innerHTML = `
        <div style="padding: 0.25rem 0.5rem; cursor: pointer;">Copy Matrix Code</div>
        <div style="padding: 0.25rem 0.5rem; cursor: pointer;">Paste Command</div>
        <div style="padding: 0.25rem 0.5rem; cursor: pointer;">Inspect Reality</div>
    `;
    
    document.body.appendChild(contextMenu);
    
    // Remove context menu on click elsewhere
    const removeMenu = () => {
        if (document.body.contains(contextMenu)) {
            document.body.removeChild(contextMenu);
        }
        document.removeEventListener('click', removeMenu);
    };
    
    setTimeout(() => {
        document.addEventListener('click', removeMenu);
    }, 100);
});

// Performance optimization for mobile devices
if (window.innerWidth <= 768) {
    // Reduce matrix rain density on mobile
    document.documentElement.style.setProperty('--animation-speed', '2s');
}