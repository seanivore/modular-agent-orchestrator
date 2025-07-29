import { spawn, ChildProcess } from 'child_process';
import path from 'path';

interface PythonMessage {
  type: 'command' | 'response' | 'error' | 'status';
  data: any;
  id?: string;
}

interface PythonResponse {
  success: boolean;
  data: any;
  error?: string;
}

export class PythonBridge {
  private pythonProcess: ChildProcess | null = null;
  private messageQueue: Map<string, (response: PythonResponse) => void> = new Map();
  private messageId = 0;

  constructor() {
    this.initializePythonProcess();
  }

  private initializePythonProcess() {
    // Path to the Python backend from terminal-ui directory
    const pythonPath = path.resolve(__dirname, '../../../mao_v4.py');
    
    try {
      this.pythonProcess = spawn('python3', [pythonPath, '--ui-mode'], {
        stdio: ['pipe', 'pipe', 'pipe'],
        cwd: path.resolve(__dirname, '../../..')
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

  private handlePythonResponse(data: string) {
    try {
      const lines = data.trim().split('\n');
      lines.forEach(line => {
        if (line.trim()) {
          const message: PythonMessage = JSON.parse(line);
          if (message.id && this.messageQueue.has(message.id)) {
            const callback = this.messageQueue.get(message.id)!;
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

  public async sendCommand(command: string, args: any = {}): Promise<PythonResponse> {
    if (!this.pythonProcess) {
      return { success: false, error: 'Python process not available' };
    }

    return new Promise((resolve) => {
      const id = (++this.messageId).toString();
      this.messageQueue.set(id, resolve);

      const message: PythonMessage = {
        type: 'command',
        id,
        data: { command, args }
      };

      this.pythonProcess!.stdin?.write(JSON.stringify(message) + '\n');

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
  public async executeSlashCommand(command: string): Promise<PythonResponse> {
    return this.sendCommand('slash_command', { command });
  }

  public async processGoal(goal: string): Promise<PythonResponse> {
    return this.sendCommand('goal', { goal });
  }

  public async getConfig(): Promise<PythonResponse> {
    return this.sendCommand('config', {});
  }

  public async getHelp(): Promise<PythonResponse> {
    return this.sendCommand('help', {});
  }

  public async getStats(): Promise<PythonResponse> {
    return this.sendCommand('stats', {});
  }

  public async chat(message: string): Promise<PythonResponse> {
    return this.sendCommand('chat', { message });
  }

  public disconnect() {
    if (this.pythonProcess) {
      this.pythonProcess.kill();
      this.pythonProcess = null;
    }
  }
}