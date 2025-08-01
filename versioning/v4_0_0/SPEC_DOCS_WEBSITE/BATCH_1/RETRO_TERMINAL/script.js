// RETRO TERMINAL - Vintage computing interactive functionality

document.addEventListener('DOMContentLoaded', function() {
    initRetroEffects();
    initVintageInteractions();
    initKeyboardCommands();
    initCRTEffects();
});

function initRetroEffects() {
    // Boot sequence with authentic delays
    animateBootSequence();
    
    // CRT flicker effects
    addCRTFlicker();
    
    // Vintage typing sounds (visual feedback)
    enableTypingEffects();
    
    // Add screen burn-in effect
    createBurnInEffect();
}

function animateBootSequence() {
    const bootLines = document.querySelectorAll('.boot-line');
    let totalDelay = 0;
    
    bootLines.forEach((line, index) => {
        const text = line.textContent;
        line.textContent = '';
        line.style.opacity = '1';
        
        setTimeout(() => {
            typewriterEffect(line, text, 50 + Math.random() * 30);
        }, totalDelay);
        
        totalDelay += (text.length * 60) + 400; // Authentic typing speed
    });
    
    // Add completion beep effect
    setTimeout(() => {
        playSystemBeep();
        startTerminalSession();
    }, totalDelay + 1000);
}

function typewriterEffect(element, text, speed) {
    let i = 0;
    const timer = setInterval(() => {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            
            // Add typing sound effect (visual)
            if (Math.random() > 0.8) {
                element.style.textShadow = '0 0 15px var(--primary-color)';
                setTimeout(() => {
                    element.style.textShadow = '0 0 10px var(--primary-color)';
                }, 50);
            }
        } else {
            clearInterval(timer);
        }
    }, speed);
}

function addCRTFlicker() {
    const screen = document.querySelector('.crt-screen');
    
    // Random screen flicker
    setInterval(() => {
        if (Math.random() > 0.95) { // 5% chance every interval
            screen.style.filter = 'brightness(1.2) contrast(1.1)';
            setTimeout(() => {
                screen.style.filter = 'brightness(1) contrast(1)';
            }, 100 + Math.random() * 200);
        }
    }, 1000);
    
    // Subtle phosphor persistence effect
    setInterval(() => {
        if (Math.random() > 0.99) { // Very rare
            const content = document.querySelector('.screen-content');
            content.style.textShadow = '0 0 20px var(--primary-color)';
            setTimeout(() => {
                content.style.textShadow = '';
            }, 300);
        }
    }, 500);
}

function enableTypingEffects() {
    const commandPrompts = document.querySelectorAll('.command-prompt');
    
    commandPrompts.forEach(prompt => {
        prompt.addEventListener('click', () => {
            simulateCommandExecution(prompt);
        });
    });
}

function simulateCommandExecution(promptElement) {
    const commandText = promptElement.querySelector('.command-text');
    const originalText = commandText.textContent;
    
    // Visual feedback - simulate typing delay
    commandText.style.animation = 'command-flicker 0.1s steps(2) 10';
    promptElement.style.background = 'rgba(255, 176, 0, 0.2)';
    
    // Create execution indicator
    const execIndicator = document.createElement('span');
    execIndicator.textContent = ' [EXECUTING...]';
    execIndicator.style.color = 'var(--accent-color)';
    execIndicator.style.animation = 'retro-glow 0.5s ease-in-out infinite alternate';
    commandText.appendChild(execIndicator);
    
    setTimeout(() => {
        execIndicator.remove();
        promptElement.style.background = 'transparent';
        commandText.style.animation = '';
        
        // Log to console with retro styling
        console.log(`%c${originalText} - COMMAND EXECUTED`, 
                   'color: #ffb000; font-family: monospace; font-weight: bold; text-shadow: 0 0 10px #ffb000;');
    }, 1500 + Math.random() * 1000);
}

function createBurnInEffect() {
    // Simulate old CRT burn-in patterns
    const burnInLayer = document.createElement('div');
    burnInLayer.className = 'burn-in-layer';
    burnInLayer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 15;
        background: radial-gradient(ellipse at 30% 40%, rgba(255, 176, 0, 0.02) 0%, transparent 50%),
                    radial-gradient(ellipse at 70% 60%, rgba(255, 136, 0, 0.015) 0%, transparent 40%);
        mix-blend-mode: screen;
        opacity: 0.6;
    `;
    
    document.querySelector('.crt-screen').appendChild(burnInLayer);
}

function initVintageInteractions() {
    // Directory listing interactions
    initDirectoryBrowser();
    
    // Menu system navigation
    initMenuSystem();
    
    // Status monitoring
    initStatusMonitoring();
    
    // Batch file execution
    initBatchFileRunner();
}

function initDirectoryBrowser() {
    const dirEntries = document.querySelectorAll('.dir-entry');
    
    dirEntries.forEach(entry => {
        entry.addEventListener('click', () => {
            const dirName = entry.querySelector('.dir-name').textContent;
            simulateDirectoryAccess(dirName, entry);
        });
        
        entry.addEventListener('mouseenter', () => {
            entry.style.background = 'rgba(255, 176, 0, 0.15)';
            entry.style.transform = 'translateX(5px)';
            playSystemTick();
        });
        
        entry.addEventListener('mouseleave', () => {
            entry.style.background = 'transparent';
            entry.style.transform = 'translateX(0)';
        });
    });
}

function simulateDirectoryAccess(dirName, entryElement) {
    // Create DOS-style access simulation
    const accessMsg = document.createElement('div');
    accessMsg.className = 'directory-access';
    accessMsg.innerHTML = `
        <div style="color: var(--accent-color); margin: 10px 0;">
            ACCESSING DIRECTORY: ${dirName}
        </div>
        <div style="color: var(--primary-color); font-size: 12px;">
            LOADING SYSTEM FILES...
            <div style="margin: 5px 0;">
                [████████████████████████████████] 100%
            </div>
            DIRECTORY CONTENTS AVAILABLE
        </div>
    `;
    
    accessMsg.style.cssText = `
        background: rgba(255, 176, 0, 0.1);
        border: 1px solid var(--secondary-color);
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
        animation: retro-glow 2s ease-in-out;
    `;
    
    entryElement.parentNode.insertBefore(accessMsg, entryElement.nextSibling);
    
    setTimeout(() => {
        accessMsg.remove();
    }, 3000);
}

function initMenuSystem() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            const docType = item.getAttribute('data-doc');
            simulateDocumentationLoad(docType, index + 1);
        });
        
        item.addEventListener('mouseenter', () => {
            item.style.background = 'rgba(255, 255, 0, 0.2)';
            playSystemTick();
        });
        
        item.addEventListener('mouseleave', () => {
            item.style.background = 'transparent';
        });
    });
}

function simulateDocumentationLoad(docType, menuNumber) {
    // Create retro loading screen
    const loadingScreen = document.createElement('div');
    loadingScreen.className = 'doc-loading-screen';
    loadingScreen.innerHTML = `
        <div class="loading-header">
            ╔══════════════════════════════════════════╗
            ║         LOADING DOCUMENTATION            ║
            ║              PLEASE WAIT...              ║
            ╚══════════════════════════════════════════╝
        </div>
        <div class="loading-content">
            <div class="loading-bar">
                READING FILE: ${docType.toUpperCase()}.DOC
                <div class="progress-indicator">
                    <span class="progress-bar">████████████████████████████████</span>
                </div>
                BYTES READ: <span class="byte-counter">0</span> / 65536
            </div>
        </div>
        <div class="loading-footer">
            <div style="margin-top: 20px; color: var(--neutral-color); font-size: 12px;">
                PRESS ESC TO CANCEL
            </div>
        </div>
    `;
    
    loadingScreen.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--screen-bg);
        border: 2px solid var(--primary-color);
        padding: 30px;
        z-index: 1000;
        color: var(--primary-color);
        font-family: var(--mono-font);
        text-align: center;
        box-shadow: 0 0 50px rgba(255, 176, 0, 0.3);
        min-width: 400px;
    `;
    
    document.body.appendChild(loadingScreen);
    
    // Animate byte counter
    const byteCounter = loadingScreen.querySelector('.byte-counter');
    let bytes = 0;
    const interval = setInterval(() => {
        bytes += Math.floor(Math.random() * 5000) + 1000;
        if (bytes >= 65536) {
            bytes = 65536;
            clearInterval(interval);
            
            setTimeout(() => {
                loadingScreen.remove();
                showDocumentationPreview(docType);
            }, 500);
        }
        byteCounter.textContent = bytes.toLocaleString();
    }, 100);
    
    // ESC key handler
    const escHandler = (e) => {
        if (e.key === 'Escape') {
            clearInterval(interval);
            loadingScreen.remove();
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
}

function showDocumentationPreview(docType) {
    const docContent = {
        'getting-started': 'INSTALLATION AND CONFIGURATION GUIDE\nSYSTEM REQUIREMENTS AND SETUP PROCEDURES',
        'agent-config': 'AI AGENT CONFIGURATION MANUAL\nNEURAL NETWORK PARAMETERS AND ROUTING',
        'tool-dev': 'MODULAR TOOL DEVELOPMENT KIT\nJSON CONFIGURATION AND API INTEGRATION',
        'workflows': 'WORKFLOW ORCHESTRATION PATTERNS\nAUTOMATION SEQUENCES AND TRIGGERS',
        'api-ref': 'COMPLETE TECHNICAL REFERENCE\nFUNCTION CALLS AND PARAMETER DEFINITIONS'
    };
    
    const preview = document.createElement('div');
    preview.className = 'doc-preview';
    preview.innerHTML = `
        <div class="doc-window">
            <div class="doc-title-bar">
                ${docType.toUpperCase()}.DOC - DOCUMENTATION VIEWER
                <button class="close-doc">×</button>
            </div>
            <div class="doc-content">
                <pre>${docContent[docType] || 'DOCUMENTATION CONTENT PLACEHOLDER'}</pre>
                <div style="margin-top: 20px; color: var(--neutral-color);">
                    [FULL DOCUMENTATION WOULD BE LOADED HERE]
                </div>
            </div>
        </div>
    `;
    
    preview.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1001;
    `;
    
    const docWindow = preview.querySelector('.doc-window');
    docWindow.style.cssText = `
        background: var(--screen-bg);
        border: 3px solid var(--primary-color);
        width: 80%;
        max-width: 700px;
        height: 70%;
        display: flex;
        flex-direction: column;
        box-shadow: 0 0 50px rgba(255, 176, 0, 0.4);
    `;
    
    const titleBar = preview.querySelector('.doc-title-bar');
    titleBar.style.cssText = `
        background: var(--secondary-color);
        color: var(--screen-bg);
        padding: 10px;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
    `;
    
    const docContentEl = preview.querySelector('.doc-content');
    docContentEl.style.cssText = `
        flex: 1;
        padding: 20px;
        color: var(--primary-color);
        overflow-y: auto;
        font-family: var(--mono-font);
    `;
    
    const closeBtn = preview.querySelector('.close-doc');
    closeBtn.style.cssText = `
        background: none;
        border: none;
        color: var(--screen-bg);
        font-size: 20px;
        cursor: pointer;
        padding: 5px 10px;
    `;
    
    document.body.appendChild(preview);
    
    closeBtn.addEventListener('click', () => preview.remove());
    preview.addEventListener('click', (e) => {
        if (e.target === preview) preview.remove();
    });
}

function initStatusMonitoring() {
    const statusRows = document.querySelectorAll('.status-row');
    
    // Simulate system monitoring
    setInterval(() => {
        statusRows.forEach(row => {
            if (Math.random() > 0.9) {
                row.style.color = 'var(--accent-color)';
                row.style.textShadow = '0 0 10px var(--accent-color)';
                
                setTimeout(() => {
                    row.style.color = 'var(--primary-color)';
                    row.style.textShadow = '';
                }, 500);
            }
        });
    }, 2000);
}

function initBatchFileRunner() {
    const batchFile = document.querySelector('.batch-file');
    if (!batchFile) return;
    
    batchFile.addEventListener('click', () => {
        simulateBatchExecution(batchFile);
    });
}

function simulateBatchExecution(batchElement) {
    const execWindow = document.createElement('div');
    execWindow.className = 'batch-execution';
    execWindow.innerHTML = `
        <div class="exec-header">
            EXECUTING INSTALL.BAT...
        </div>
        <div class="exec-output">
            <div class="exec-line">C:\\MAO>@ECHO OFF</div>
            <div class="exec-line">C:\\MAO>REM MAO INSTALLATION SCRIPT</div>
            <div class="exec-line">C:\\MAO>ECHO DOWNLOADING MAO v4.0...</div>
            <div class="exec-line output-line">DOWNLOADING MAO v4.0...</div>
            <div class="exec-line">C:\\MAO>CURL -SSL https://get.mao.dev | BASH</div>
            <div class="exec-line output-line">DOWNLOAD COMPLETE</div>
            <div class="exec-line output-line">INSTALLATION SUCCESSFUL!</div>
        </div>
    `;
    
    execWindow.style.cssText = `
        position: fixed;
        top: 20%;
        left: 20%;
        width: 60%;
        height: 60%;
        background: var(--screen-bg);
        border: 2px solid var(--primary-color);
        padding: 20px;
        z-index: 1000;
        color: var(--primary-color);
        font-family: var(--mono-font);
        overflow-y: auto;
        box-shadow: 0 0 30px rgba(255, 176, 0, 0.3);
    `;
    
    const header = execWindow.querySelector('.exec-header');
    header.style.cssText = `
        color: var(--accent-color);
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
        border-bottom: 1px solid var(--secondary-color);
        padding-bottom: 10px;
    `;
    
    document.body.appendChild(execWindow);
    
    // Animate execution lines
    const execLines = execWindow.querySelectorAll('.exec-line');
    execLines.forEach((line, index) => {
        line.style.opacity = '0';
        setTimeout(() => {
            line.style.opacity = '1';
            typewriterEffect(line, line.textContent, 30);
            line.textContent = '';
        }, index * 800);
    });
    
    // Auto-close after execution
    setTimeout(() => {
        execWindow.remove();
    }, (execLines.length * 800) + 3000);
}

function initKeyboardCommands() {
    // Classic DOS-style keyboard shortcuts
    document.addEventListener('keydown', (event) => {
        // F1 - Help system
        if (event.key === 'F1') {
            event.preventDefault();
            showHelpSystem();
        }
        
        // Ctrl+C - Break execution
        if (event.ctrlKey && event.key === 'c') {
            event.preventDefault();
            showBreakMessage();
        }
        
        // Alt+Tab simulation
        if (event.altKey && event.key === 'Tab') {
            event.preventDefault();
            simulateTaskSwitch();
        }
        
        // Number keys for menu selection
        if (event.key >= '1' && event.key <= '5') {
            const menuItem = document.querySelector(`[data-doc]:nth-child(${event.key})`);
            if (menuItem) {
                menuItem.click();
            }
        }
    });
}

function showHelpSystem() {
    const helpWindow = document.createElement('div');
    helpWindow.innerHTML = `
        <div class="help-content">
            <div class="help-header">
                ╔══════════════════════════════════════════╗
                ║              HELP SYSTEM v4.0           ║
                ╚══════════════════════════════════════════╝
            </div>
            <div class="help-body">
                KEYBOARD SHORTCUTS:
                ──────────────────
                F1          - SHOW THIS HELP
                CTRL+C      - BREAK EXECUTION
                ALT+TAB     - TASK SWITCHER
                1-5         - SELECT MENU ITEM
                ESC         - CLOSE WINDOWS
                
                MOUSE COMMANDS:
                ──────────────
                CLICK       - EXECUTE COMMAND
                HOVER       - HIGHLIGHT ITEM
                
                SYSTEM STATUS: ONLINE
                MEMORY USAGE:  45% OF 64K
                AGENTS:        4 ACTIVE
            </div>
            <div class="help-footer">
                PRESS ANY KEY TO CONTINUE...
            </div>
        </div>
    `;
    
    helpWindow.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--screen-bg);
        border: 2px solid var(--accent-color);
        padding: 20px;
        z-index: 1002;
        color: var(--primary-color);
        font-family: var(--mono-font);
        box-shadow: 0 0 40px rgba(255, 255, 0, 0.4);
        min-width: 500px;
    `;
    
    document.body.appendChild(helpWindow);
    
    const closeHelp = () => {
        helpWindow.remove();
        document.removeEventListener('keydown', closeHelp);
    };
    
    document.addEventListener('keydown', closeHelp);
}

function showBreakMessage() {
    const breakMsg = document.createElement('div');
    breakMsg.textContent = '^C - BREAK';
    breakMsg.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--screen-bg);
        color: var(--accent-color);
        padding: 10px 20px;
        border: 1px solid var(--accent-color);
        font-family: var(--mono-font);
        font-weight: bold;
        z-index: 1003;
        text-shadow: 0 0 10px var(--accent-color);
    `;
    
    document.body.appendChild(breakMsg);
    
    setTimeout(() => {
        breakMsg.remove();
    }, 2000);
}

function simulateTaskSwitch() {
    const taskSwitcher = document.createElement('div');
    taskSwitcher.innerHTML = `
        <div class="task-header">TASK SWITCHER</div>
        <div class="task-list">
            <div class="task-item active">MAO.EXE - AGENT ORCHESTRATOR</div>
            <div class="task-item">DOCS.EXE - DOCUMENTATION VIEWER</div>
            <div class="task-item">CONFIG.EXE - SYSTEM CONFIGURATION</div>
            <div class="task-item">MONITOR.EXE - SYSTEM MONITOR</div>
        </div>
    `;
    
    taskSwitcher.style.cssText = `
        position: fixed;
        top: 30%;
        left: 30%;
        width: 40%;
        background: var(--screen-bg);
        border: 2px solid var(--primary-color);
        padding: 15px;
        z-index: 1004;
        color: var(--primary-color);
        font-family: var(--mono-font);
        box-shadow: 0 0 30px rgba(255, 176, 0, 0.3);
    `;
    
    const activeTask = taskSwitcher.querySelector('.task-item.active');
    activeTask.style.cssText = `
        background: var(--primary-color);
        color: var(--screen-bg);
        padding: 5px;
        margin: 2px 0;
    `;
    
    document.body.appendChild(taskSwitcher);
    
    setTimeout(() => {
        taskSwitcher.remove();
    }, 2000);
}

function initCRTEffects() {
    // Add phosphor persistence effect
    addPhosphorPersistence();
    
    // Simulate electron beam refresh
    addBeamRefresh();
}

function addPhosphorPersistence() {
    const screen = document.querySelector('.screen-content');
    let persistenceTimeout;
    
    screen.addEventListener('scroll', () => {
        clearTimeout(persistenceTimeout);
        screen.style.filter = 'blur(0.5px) brightness(1.1)';
        
        persistenceTimeout = setTimeout(() => {
            screen.style.filter = 'none';
        }, 200);
    });
}

function addBeamRefresh() {
    // Simulate CRT refresh rate with subtle flicker
    setInterval(() => {
        const content = document.querySelector('.screen-content');
        content.style.opacity = '0.98';
        
        setTimeout(() => {
            content.style.opacity = '1';
        }, 16); // ~60Hz refresh rate
    }, 1000 / 60);
}

// Audio feedback functions (using Web Audio API for authentic sounds)
function playSystemBeep() {
    createTone(800, 200, 0.1); // Classic PC beep
}

function playSystemTick() {
    createTone(1200, 50, 0.05); // Subtle UI feedback
}

function createTone(frequency, duration, volume) {
    if (!window.AudioContext && !window.webkitAudioContext) return;
    
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
    oscillator.type = 'square'; // Retro square wave
    
    gainNode.gain.setValueAtTime(volume, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration / 1000);
    
    oscillator.start();
    oscillator.stop(audioContext.currentTime + duration / 1000);
}

function startTerminalSession() {
    // Initialize terminal after boot sequence
    const currentPrompt = document.querySelector('.current-prompt');
    currentPrompt.style.animation = 'retro-glow 2s ease-in-out infinite alternate';
    
    console.log('%cMAO v4.0 TERMINAL SESSION STARTED', 
               'color: #ffb000; font-family: monospace; font-weight: bold; font-size: 14px;');
}