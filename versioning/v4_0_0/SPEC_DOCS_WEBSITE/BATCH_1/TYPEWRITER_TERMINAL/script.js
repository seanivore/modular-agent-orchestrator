// Typewriter Terminal Interactive Effects
class TypewriterTerminal {
    constructor() {
        this.init();
        this.setupTypingAnimation();
        this.setupInteractiveKeys();
        this.setupPaperEffects();
        this.setupDate();
        this.setupSoundEffects();
    }

    init() {
        console.log('Initializing Typewriter Terminal Interface...');
        this.typingLines = document.querySelectorAll('.typing-line');
        this.typewriterKeys = document.querySelectorAll('.typewriter-key');
        this.returnLever = document.querySelector('.return-lever');
        this.dateStamp = document.querySelector('.typed-date');
        
        this.currentLineIndex = 0;
        this.isTyping = false;
        this.typewriterSounds = [];
    }

    setupDate() {
        const now = new Date();
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        this.dateStamp.textContent = now.toLocaleDateString('en-US', options);
    }

    setupTypingAnimation() {
        // Start typing animation after a delay
        setTimeout(() => {
            this.typeNextLine();
        }, 1000);
    }

    typeNextLine() {
        if (this.currentLineIndex >= this.typingLines.length) {
            return;
        }

        const currentLine = this.typingLines[this.currentLineIndex];
        const text = currentLine.getAttribute('data-text');
        const delay = parseInt(currentLine.getAttribute('data-delay')) || 0;
        
        // Add delay if specified
        setTimeout(() => {
            this.typeText(currentLine, text, () => {
                currentLine.classList.add('typed');
                this.currentLineIndex++;
                
                // Continue to next line after a brief pause
                setTimeout(() => {
                    this.typeNextLine();
                }, 500);
            });
        }, delay);
    }

    typeText(element, text, callback) {
        this.isTyping = true;
        element.textContent = '';
        let charIndex = 0;

        const typeChar = () => {
            if (charIndex < text.length) {
                element.textContent += text[charIndex];
                charIndex++;
                
                // Simulate typewriter key press
                this.simulateKeyPress(text[charIndex - 1]);
                
                // Variable typing speed for realism
                const speed = this.getTypingSpeed();
                setTimeout(typeChar, speed);
            } else {
                this.isTyping = false;
                if (callback) callback();
            }
        };

        typeChar();
    }

    getTypingSpeed() {
        // Simulate human typing with variable speeds
        const baseSpeed = 80;
        const variation = Math.random() * 60 - 30; // -30 to +30ms variation
        return Math.max(30, baseSpeed + variation);
    }

    simulateKeyPress(char) {
        // Find corresponding key and animate it
        const key = Array.from(this.typewriterKeys).find(k => 
            k.getAttribute('data-key') === char.toUpperCase()
        );
        
        if (key) {
            key.style.transform = 'translateY(3px)';
            key.style.boxShadow = 'inset 0 2px 4px rgba(0, 0, 0, 0.3)';
            
            setTimeout(() => {
                key.style.transform = '';
                key.style.boxShadow = '';
            }, 100);
        }

        // Play typewriter sound
        this.playTypewriterSound();
        
        // Add paper shake effect
        this.addPaperShake();
    }

    setupInteractiveKeys() {
        this.typewriterKeys.forEach(key => {
            key.addEventListener('click', () => {
                this.handleKeyPress(key);
            });
        });

        // Return lever functionality
        if (this.returnLever) {
            this.returnLever.addEventListener('click', () => {
                this.handleCarriageReturn();
            });
        }

        // Keyboard event listeners
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardInput(e);
        });
    }

    handleKeyPress(key) {
        const char = key.getAttribute('data-key');
        
        // Animate key press
        key.style.transform = 'translateY(3px)';
        key.style.boxShadow = 'inset 0 2px 4px rgba(0, 0, 0, 0.3)';
        
        setTimeout(() => {
            key.style.transform = '';
            key.style.boxShadow = '';
        }, 150);

        // Play sound and effects
        this.playTypewriterSound();
        this.addPaperShake();
        
        // Add character to interactive area (if exists)
        this.addCharacterToOutput(char);
    }

    handleCarriageReturn() {
        this.returnLever.style.transform = 'rotate(-15deg)';
        
        setTimeout(() => {
            this.returnLever.style.transform = '';
        }, 300);

        // Play carriage return sound
        this.playCarriageReturnSound();
        
        // Add line break to output
        this.addLineBreakToOutput();
    }

    handleKeyboardInput(e) {
        // Don't interfere with typing animation
        if (this.isTyping) return;
        
        const char = e.key.toUpperCase();
        const key = Array.from(this.typewriterKeys).find(k => 
            k.getAttribute('data-key') === char
        );
        
        if (key) {
            this.handleKeyPress(key);
        } else if (e.key === 'Enter') {
            this.handleCarriageReturn();
        }
    }

    addCharacterToOutput(char) {
        // Create or update interactive output area
        let outputArea = document.querySelector('.interactive-output');
        if (!outputArea) {
            outputArea = document.createElement('div');
            outputArea.className = 'interactive-output';
            outputArea.style.cssText = `
                margin-top: 2rem;
                padding: 1rem;
                border: 2px dashed var(--mao-secondary);
                border-radius: 4px;
                background: rgba(44, 85, 48, 0.05);
                font-family: 'Courier Prime', monospace;
                min-height: 100px;
                white-space: pre-wrap;
            `;
            
            const contentBody = document.querySelector('.content-body');
            if (contentBody) {
                contentBody.appendChild(outputArea);
            }
        }
        
        outputArea.textContent += char;
    }

    addLineBreakToOutput() {
        const outputArea = document.querySelector('.interactive-output');
        if (outputArea) {
            outputArea.textContent += '\n';
        }
    }

    setupPaperEffects() {
        this.paperSheet = document.querySelector('.paper-sheet');
        this.shakeIntensity = 0;
    }

    addPaperShake() {
        if (!this.paperSheet) return;
        
        const shakeX = Math.random() * 0.5 - 0.25;
        const shakeY = Math.random() * 0.5 - 0.25;
        
        this.paperSheet.style.transform = `translate(${shakeX}px, ${shakeY}px)`;
        
        setTimeout(() => {
            this.paperSheet.style.transform = '';
        }, 50);
    }

    setupSoundEffects() {
        // Create audio context for sound effects (simplified)
        this.audioContext = null;
        
        // Initialize audio context on first user interaction
        document.addEventListener('click', () => {
            if (!this.audioContext) {
                try {
                    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                } catch (e) {
                    console.log('Audio context not supported');
                }
            }
        }, { once: true });
    }

    playTypewriterSound() {
        if (!this.audioContext) return;
        
        try {
            // Create a simple click sound
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800 + Math.random() * 200, this.audioContext.currentTime);
            oscillator.type = 'square';
            
            gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.1);
        } catch (e) {
            console.log('Sound generation failed');
        }
    }

    playCarriageReturnSound() {
        if (!this.audioContext) return;
        
        try {
            // Create a mechanical return sound
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(200, this.audioContext.currentTime);
            oscillator.frequency.linearRampToValueAtTime(100, this.audioContext.currentTime + 0.3);
            oscillator.type = 'sawtooth';
            
            gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.3);
        } catch (e) {
            console.log('Sound generation failed');
        }
    }

    // Additional paper aging effects
    setupPaperAging() {
        setInterval(() => {
            this.addPaperWear();
        }, 30000); // Add subtle wear every 30 seconds
    }

    addPaperWear() {
        const paperTexture = document.querySelector('.paper-texture');
        if (!paperTexture) return;
        
        // Add subtle random spots
        const spot = document.createElement('div');
        spot.style.cssText = `
            position: absolute;
            width: ${Math.random() * 3 + 1}px;
            height: ${Math.random() * 3 + 1}px;
            background: rgba(139, 69, 19, 0.03);
            border-radius: 50%;
            top: ${Math.random() * 100}%;
            left: ${Math.random() * 100}%;
            pointer-events: none;
        `;
        
        paperTexture.appendChild(spot);
        
        // Remove old spots to prevent accumulation
        const spots = paperTexture.querySelectorAll('div');
        if (spots.length > 50) {
            spots[0].remove();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TypewriterTerminal();
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

// Prevent text selection during typing animation
document.addEventListener('selectstart', (e) => {
    if (e.target.classList.contains('typing-line') && !e.target.classList.contains('typed')) {
        e.preventDefault();
    }
});

// Add vintage cursor for interactive elements
document.addEventListener('DOMContentLoaded', () => {
    const style = document.createElement('style');
    style.textContent = `
        .typewriter-key:hover,
        .return-lever:hover {
            cursor: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="none" stroke="black" stroke-width="2"/><circle cx="10" cy="10" r="2" fill="black"/></svg>') 10 10, pointer;
        }
    `;
    document.head.appendChild(style);
});