#!/usr/bin/env python3
"""
MAO GitHub Integration Webhook Handler
Handles GitHub webhooks to trigger automatic documentation updates
Integrates with Claude Code GitHub app for seamless PR creation
"""

import json
import hashlib
import hmac
from typing import Dict, Any, List, Optional
from pathlib import Path
from flask import Flask, request, jsonify
import subprocess
import os

from ..auto_docs.config_documenter import ConfigDocumenter


class GitHubWebhookHandler:
    """Handles GitHub webhook events for config documentation automation"""
    
    def __init__(self, repo_root: str = ".", webhook_secret: Optional[str] = None):
        self.repo_root = Path(repo_root)
        self.webhook_secret = webhook_secret or os.getenv('GITHUB_WEBHOOK_SECRET')
        self.config_documenter = ConfigDocumenter(repo_root)
        
        # Flask app for webhook endpoint
        self.app = Flask(__name__)
        self.setup_routes()
        
    def setup_routes(self):
        """Setup Flask routes for webhook handling"""
        
        @self.app.route('/webhook/github', methods=['POST'])
        def handle_webhook():
            """Main webhook handler endpoint"""
            
            # Verify webhook signature
            if not self.verify_signature(request):
                return jsonify({'error': 'Invalid signature'}), 401
                
            # Parse webhook payload
            payload = request.get_json()
            if not payload:
                return jsonify({'error': 'No JSON payload'}), 400
                
            # Handle the webhook event
            result = self.process_webhook_event(payload)
            return jsonify(result)
            
        @self.app.route('/webhook/status', methods=['GET'])
        def webhook_status():
            """Health check endpoint"""
            return jsonify({
                'status': 'active',
                'repo_root': str(self.repo_root),
                'config_documenter': 'ready'
            })
            
    def verify_signature(self, request) -> bool:
        """Verify GitHub webhook signature"""
        if not self.webhook_secret:
            # Skip verification if no secret configured (development mode)
            return True
            
        signature = request.headers.get('X-Hub-Signature-256')
        if not signature:
            return False
            
        # Compute expected signature
        body = request.get_data()
        expected_signature = 'sha256=' + hmac.new(
            self.webhook_secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
        
    def process_webhook_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process GitHub webhook event"""
        
        event_type = payload.get('action', 'unknown')
        
        # Handle push events (new commits)
        if 'commits' in payload:
            return self.handle_push_event(payload)
            
        # Handle pull request events
        elif 'pull_request' in payload:
            return self.handle_pr_event(payload)
            
        # Handle other events
        else:
            return {
                'status': 'ignored',
                'event_type': event_type,
                'message': 'Event type not handled'
            }
            
    def handle_push_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle git push events"""
        
        commits = payload.get('commits', [])
        if not commits:
            return {'status': 'no_commits', 'message': 'No commits in push event'}
            
        # Collect all changed files from commits
        changed_files = set()
        for commit in commits:
            changed_files.update(commit.get('added', []))
            changed_files.update(commit.get('modified', []))
            # Note: we might want to handle 'removed' files differently
            
        # Filter for config files
        config_files = [f for f in changed_files if f.startswith('configs/') and f.endswith('.json')]
        
        if not config_files:
            return {
                'status': 'no_config_changes',
                'message': 'No config files changed',
                'changed_files': list(changed_files)
            }
            
        # Process config changes
        return self.process_config_changes(config_files, payload)
        
    def handle_pr_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle pull request events"""
        
        action = payload.get('action')
        pr = payload.get('pull_request', {})
        
        # Handle PR opened/updated - check for Claude Code mentions
        if action in ['opened', 'synchronize']:
            body = pr.get('body', '')
            
            # Check if @claude is mentioned
            if '@claude' in body.lower():
                return self.handle_claude_mention(payload)
                
        return {
            'status': 'ignored',
            'action': action,
            'message': 'PR event not requiring action'
        }
        
    def handle_claude_mention(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle @claude mentions in PRs"""
        
        pr = payload.get('pull_request', {})
        pr_number = pr.get('number')
        
        # This could trigger Claude Code to:
        # 1. Review the PR
        # 2. Suggest improvements
        # 3. Auto-approve if it's a documentation update
        
        return {
            'status': 'claude_mentioned',
            'pr_number': pr_number,
            'message': 'Claude Code will be notified to review this PR'
        }
        
    def process_config_changes(self, config_files: List[str], payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process configuration file changes"""
        
        # Analyze config changes
        config_changes = self.config_documenter.scan_config_changes(config_files)
        
        if not config_changes:
            return {
                'status': 'no_actionable_changes',
                'config_files': config_files,
                'message': 'Config files changed but no documentation updates needed'
            }
            
        # Execute documentation workflow
        try:
            success = self.config_documenter.execute_github_workflow(config_changes)
            
            if success:
                return {
                    'status': 'documentation_updated',
                    'config_changes': len(config_changes),
                    'config_files': config_files,
                    'message': 'Documentation PR created successfully'
                }
            else:
                return {
                    'status': 'workflow_failed', 
                    'config_changes': len(config_changes),
                    'config_files': config_files,
                    'message': 'Failed to create documentation PR'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'config_files': config_files,
                'message': 'Error processing config changes'
            }
            
    def create_claude_code_integration(self) -> Dict[str, Any]:
        """Set up Claude Code GitHub integration"""
        
        integration_guide = {
            'steps': [
                {
                    'step': 1,
                    'title': 'Install Claude Code GitHub App',
                    'command': '/install-github-app',
                    'description': 'Run this command in Claude Code to install the GitHub app'
                },
                {
                    'step': 2,
                    'title': 'Configure Repository Access',
                    'description': 'Grant Claude Code access to your MAO repository'
                },
                {
                    'step': 3,
                    'title': 'Set Up Webhook',
                    'webhook_url': 'https://your-domain.com/webhook/github',
                    'events': ['push', 'pull_request'],
                    'description': 'Configure GitHub webhook to notify this handler'
                },
                {
                    'step': 4,
                    'title': 'Test Integration',
                    'test_command': 'Make a config change and commit to trigger automation',
                    'expected_result': 'Documentation PR should be created automatically'
                }
            ],
            'environment_variables': {
                'GITHUB_WEBHOOK_SECRET': 'Set this for webhook signature verification',
                'GITHUB_TOKEN': 'For GitHub API access (if needed)'
            },
            'workflow': {
                'config_change': 'Detected by webhook',
                'documentation_update': 'Auto-generated by ConfigDocumenter',
                'pr_creation': 'Auto-created with @claude mention',
                'claude_review': 'Claude Code reviews and suggests improvements',
                'merge': 'Manual approval and merge'
            }
        }
        
        return integration_guide
        
    def start_webhook_server(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """Start the webhook server"""
        print(f"🚀 Starting MAO GitHub webhook handler on {host}:{port}")
        print(f"📡 Webhook endpoint: http://{host}:{port}/webhook/github")
        print(f"💚 Status endpoint: http://{host}:{port}/webhook/status")
        
        self.app.run(host=host, port=port, debug=debug)


class GitHubCLIIntegration:
    """Integration with GitHub CLI for enhanced workflows"""
    
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        
    def create_documentation_pr(self, 
                               title: str,
                               body: str, 
                               branch: str,
                               reviewers: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create PR using GitHub CLI"""
        
        cmd = [
            'gh', 'pr', 'create',
            '--title', title,
            '--body', body,
            '--head', branch
        ]
        
        if reviewers:
            for reviewer in reviewers:
                cmd.extend(['--reviewer', reviewer])
                
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            pr_url = result.stdout.strip()
            
            return {
                'status': 'success',
                'pr_url': pr_url,
                'message': 'PR created successfully'
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'status': 'error',
                'error': e.stderr,
                'message': 'Failed to create PR'
            }
            
    def add_claude_comment(self, pr_number: int, message: str) -> Dict[str, Any]:
        """Add a comment mentioning @claude to a PR"""
        
        comment_body = f"@claude {message}"
        
        cmd = [
            'gh', 'pr', 'comment', str(pr_number),
            '--body', comment_body
        ]
        
        try:
            subprocess.run(cmd, cwd=self.repo_root, check=True)
            return {
                'status': 'success',
                'message': 'Claude mentioned in PR comment'
            }
        except subprocess.CalledProcessError as e:
            return {
                'status': 'error',
                'error': str(e),
                'message': 'Failed to add comment'
            }


def main():
    """Main function for testing webhook handler"""
    
    # Create webhook handler
    handler = GitHubWebhookHandler()
    
    # Show integration guide
    guide = handler.create_claude_code_integration()
    print("🔧 Claude Code GitHub Integration Guide:")
    print(json.dumps(guide, indent=2))
    
    # Start webhook server (for testing)
    if os.getenv('START_WEBHOOK_SERVER'):
        handler.start_webhook_server(debug=True)
    else:
        print("\n💡 To start webhook server: SET START_WEBHOOK_SERVER=1 and run again")


if __name__ == "__main__":
    main()