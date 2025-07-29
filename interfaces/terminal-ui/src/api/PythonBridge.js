import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export class PythonBridge {
    constructor() {
        this.pythonProcess = null;
        this.messageQueue = new Map();
        this.messageId = 0;
        this.initializePythonProcess();
    }

    initializePythonProcess() {
        // Path to the Python backend - go up from interfaces/terminal-ui/ to project root
        // Current file: interfaces/terminal-ui/src/api/PythonBridge.js
        // Target: mao_v4.py (in project root)
        const currentDir = path.dirname(__filename);
        const projectRoot = path.resolve(currentDir, '../../'); // up 2 levels: terminal-ui -> interfaces -> root
        const pythonPath = path.join(projectRoot, 'mao_v4.py');

        console.log('Looking for mao_v4.py at:', pythonPath);

        try {
            this.pythonProcess = spawn('python3', [pythonPath, '--ui-mode'], {
                stdio: ['pipe', 'pipe', 'pipe'],
                cwd: projectRoot
            });

            this.pythonProcess.stdout?.on('data', (data) => {
                this.handlePythonResponse(data.toString());
            });

            this.pythonProcess.stderr?.on('data', (data) => {
                console.error('Python Error:', data.toString());
            });

            this.pythonProcess.on('error', (error) => {
                console.error('Failed to start Python process:', error);
            });

            this.pythonProcess.on('exit', (code) => {
                console.log(`Python process exited with code ${code}`);
                this.pythonProcess = null;
            });

        } catch (error) {
            console.error('Error initializing Python process:', error);
        }
    }

    handlePythonResponse(data) {
        try {
            const lines = data.trim().split('\n');
            lines.forEach(line => {
                if (line.trim()) {
                    const message = JSON.parse(line);
                    if (message.id && this.messageQueue.has(message.id)) {
                        const callback = this.messageQueue.get(message.id);
                        this.messageQueue.delete(message.id);
                        callback({
                            success: message.type !== 'error',
                            data: message.data,
                            error: message.type === 'error' ? message.data : undefined
                        });
                    }
                }
            });
        } catch (error) {
            console.error('Error parsing Python response:', error);
        }
    }

    async sendCommand(command, args = {}) {
        if (!this.pythonProcess) {
            return { success: false, error: 'Python process not available' };
        }

        return new Promise((resolve) => {
            const id = (++this.messageId).toString();
            this.messageQueue.set(id, resolve);

            const message = {
                type: 'command',
                id,
                data: { command, args }
            };

            this.pythonProcess.stdin?.write(JSON.stringify(message) + '\n');

            // Timeout after 30 seconds
            setTimeout(() => {
                if (this.messageQueue.has(id)) {
                    this.messageQueue.delete(id);
                    resolve({ success: false, error: 'Command timeout' });
                }
            }, 30000);
        });
    }

    // Specific methods for common Mao commands
    async executeSlashCommand(command) {
        return this.sendCommand('slash_command', { command });
    }

    async processGoal(goal) {
        return this.sendCommand('goal', { goal });
    }

    async getConfig() {
        return this.sendCommand('config', {});
    }

    async getHelp() {
        return this.sendCommand('help', {});
    }

    async getStats() {
        return this.sendCommand('stats', {});
    }

    async chat(message) {
        return this.sendCommand('chat', { message });
    }

    disconnect() {
        if (this.pythonProcess) {
            this.pythonProcess.kill();
            this.pythonProcess = null;
        }
    }
}