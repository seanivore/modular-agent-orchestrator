import {spawn, ChildProcess} from 'child_process';
import path from 'path';
import {fileURLToPath} from 'url';

interface PythonMessage {
	id: string;
	type: 'ping' | 'slash_command' | 'goal' | 'chat' | 'config' | 'help' | 'stats';
	data?: any;
	timestamp: number;
}

interface PythonResponse {
	id: string;
	success: boolean;
	data?: any;
	error?: string;
	timestamp: number;
}

export class PythonBridge {
	private pythonProcess: ChildProcess | null = null;
	private messageQueue = new Map<string, {resolve: (value: any) => void; reject: (error: Error) => void}>();
	private messageId = 0;
	private isInitialized = false;

	constructor() {
		this.initializePythonProcess();
	}

	private initializePythonProcess(): void {
		try {
			// Get the project root directory (from interfaces/mao/source/api/ up to project root)
			const currentFileUrl = import.meta.url;
			const currentFilePath = fileURLToPath(currentFileUrl);
			const projectRoot = path.resolve(path.dirname(currentFilePath), '../../../..');
			const pythonScriptPath = path.join(projectRoot, 'mao_v4.py');

			console.log(`🚀 Starting Python backend at: ${pythonScriptPath}`);

			this.pythonProcess = spawn('python3', [pythonScriptPath, '--ui-mode'], {
				stdio: ['pipe', 'pipe', 'pipe'],
				cwd: projectRoot,
			});

			this.pythonProcess.stdout?.on('data', (data: Buffer) => {
				const lines = data.toString().split('\n').filter(line => line.trim());
				for (const line of lines) {
					try {
						const response: PythonResponse = JSON.parse(line);
						this.handlePythonResponse(response);
					} catch (error) {
						console.log(`Python stdout: ${line}`);
					}
				}
			});

			this.pythonProcess.stderr?.on('data', (data: Buffer) => {
				console.error(`Python Error: ${data.toString()}`);
			});

			this.pythonProcess.on('close', (code: number | null) => {
				console.log(`Python process exited with code ${code}`);
				this.pythonProcess = null;
				this.isInitialized = false;
			});

			this.pythonProcess.on('error', (error: Error) => {
				console.error(`Failed to start Python process: ${error.message}`);
				this.pythonProcess = null;
				this.isInitialized = false;
			});

			this.isInitialized = true;
		} catch (error) {
			console.error(`Error initializing Python bridge: ${error}`);
			this.isInitialized = false;
		}
	}

	private handlePythonResponse(response: PythonResponse): void {
		const pending = this.messageQueue.get(response.id);
		if (pending) {
			this.messageQueue.delete(response.id);
			if (response.success) {
				pending.resolve(response.data);
			} else {
				pending.reject(new Error(response.error || 'Unknown Python error'));
			}
		}
	}

	private async sendMessage(type: PythonMessage['type'], data?: any): Promise<any> {
		return new Promise((resolve, reject) => {
			if (!this.pythonProcess || !this.isInitialized) {
				reject(new Error('Python backend not connected'));
				return;
			}

			const messageId = `msg-${++this.messageId}`;
			const message: PythonMessage = {
				id: messageId,
				type,
				data,
				timestamp: Date.now(),
			};

			this.messageQueue.set(messageId, {resolve, reject});

			// Set timeout for message
			setTimeout(() => {
				if (this.messageQueue.has(messageId)) {
					this.messageQueue.delete(messageId);
					reject(new Error('Message timeout'));
				}
			}, 5000);

			try {
				this.pythonProcess.stdin?.write(JSON.stringify(message) + '\n');
			} catch (error) {
				this.messageQueue.delete(messageId);
				reject(new Error(`Failed to send message: ${error}`));
			}
		});
	}

	async ping(): Promise<boolean> {
		try {
			await this.sendMessage('ping');
			return true;
		} catch (error) {
			return false;
		}
	}

	async executeSlashCommand(command: string): Promise<string> {
		try {
			const response = await this.sendMessage('slash_command', {command});
			return response.output || response.message || 'Command executed';
		} catch (error) {
			throw new Error(`Slash command failed: ${error}`);
		}
	}

	async processGoal(goal: string): Promise<string> {
		try {
			const response = await this.sendMessage('goal', {goal});
			return response.workflow || response.message || 'Goal processed';
		} catch (error) {
			throw new Error(`Goal processing failed: ${error}`);
		}
	}

	async chat(message: string): Promise<string> {
		try {
			const response = await this.sendMessage('chat', {message});
			return response.response || response.message || 'Message received';
		} catch (error) {
			throw new Error(`Chat failed: ${error}`);
		}
	}

	async getConfig(): Promise<any> {
		try {
			const response = await this.sendMessage('config');
			return response.config || {};
		} catch (error) {
			throw new Error(`Config retrieval failed: ${error}`);
		}
	}

	async getStats(): Promise<any> {
		try {
			const response = await this.sendMessage('stats');
			return response.stats || {};
		} catch (error) {
			throw new Error(`Stats retrieval failed: ${error}`);
		}
	}

	destroy(): void {
		if (this.pythonProcess) {
			this.pythonProcess.kill();
			this.pythonProcess = null;
		}
		this.messageQueue.clear();
		this.isInitialized = false;
	}
}
