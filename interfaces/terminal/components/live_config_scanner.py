#!/usr/bin/env python3
"""
MAO Live Config Scanner
Real-time config discovery and monitoring for the terminal interface
Ensures the application always shows current available configurations
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ..visual_language import MAO_COLORS, MAOVisualProtocol


class ConfigChangeHandler(FileSystemEventHandler):
    """File system event handler for config changes"""
    
    def __init__(self, scanner: 'LiveConfigScanner'):
        self.scanner = scanner
        
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            self.scanner.handle_config_change(event.src_path, 'modified')
            
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            self.scanner.handle_config_change(event.src_path, 'created')
            
    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            self.scanner.handle_config_change(event.src_path, 'deleted')


class LiveConfigScanner:
    """
    Real-time config discovery and monitoring system
    Provides live updates to the terminal interface when configs change
    """
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.visual_protocol = MAOVisualProtocol()
        
        # Config caches
        self.tools_cache = {}
        self.models_cache = {}
        self.providers_cache = {}
        self.cli_commands_cache = {}
        
        # Timestamps
        self.last_scan = {}
        self.scan_interval = 5.0  # seconds
        
        # File watcher
        self.observer = None
        self.event_handler = ConfigChangeHandler(self)
        
        # Change callbacks
        self.change_callbacks = []
        
        # Watch directories
        self.watch_directories = {
            'tools': self.config_dir / 'tools',
            'models': self.config_dir / 'models',
            'providers': self.config_dir / 'providers',
            'cli': self.config_dir / 'cli'
        }
        
        # Initialize
        self.scan_all_configs()
        
    def start_watching(self):
        """Start file system watching for config changes"""
        if self.observer:
            return
            
        self.observer = Observer()
        
        for watch_dir in self.watch_directories.values():
            if watch_dir.exists():
                self.observer.schedule(self.event_handler, str(watch_dir), recursive=True)
                
        self.observer.start()
        print(f"🔍 Started watching config directories for changes")
        
    def stop_watching(self):
        """Stop file system watching"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            print("⏹️ Stopped watching config directories")
            
    def add_change_callback(self, callback: Callable[[str, str, Dict], None]):
        """Add callback function to be called when configs change"""
        self.change_callbacks.append(callback)
        
    def handle_config_change(self, file_path: str, change_type: str):
        """Handle a config file change event"""
        config_type = self.determine_config_type(file_path)
        if not config_type:
            return
            
        print(f"📝 Config {change_type}: {file_path}")
        
        # Re-scan affected config type
        self.scan_config_type(config_type)
        
        # Notify callbacks
        config_data = self.get_config_data(file_path) if change_type != 'deleted' else None
        for callback in self.change_callbacks:
            try:
                callback(config_type, change_type, config_data)
            except Exception as e:
                print(f"❌ Error in change callback: {e}")
                
    def determine_config_type(self, file_path: str) -> Optional[str]:
        """Determine what type of config this file represents"""
        path = Path(file_path)
        
        for config_type, watch_dir in self.watch_directories.items():
            try:
                path.relative_to(watch_dir)
                return config_type
            except ValueError:
                continue
                
        return None
        
    def get_config_data(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Load config data from file"""
        try:
            with open(file_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
            
    def scan_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """Scan all config directories for current configurations"""
        all_configs = {}
        
        for config_type in self.watch_directories.keys():
            configs = self.scan_config_type(config_type)
            all_configs[config_type] = configs
            
        return all_configs
        
    def scan_config_type(self, config_type: str) -> Dict[str, Any]:
        """Scan a specific config type directory"""
        config_dir = self.watch_directories.get(config_type)
        if not config_dir or not config_dir.exists():
            return {}
            
        configs = {}
        
        for item in config_dir.iterdir():
            if item.is_dir():
                config_name = item.name
                json_file = item / f"{config_name}.json"
                
                if json_file.exists():
                    config_data = self.get_config_data(json_file)
                    if config_data:
                        # Add metadata
                        config_data['_meta'] = {
                            'name': config_name,
                            'path': str(json_file),
                            'last_modified': json_file.stat().st_mtime,
                            'complete': self.check_config_completeness(item, config_type)
                        }
                        configs[config_name] = config_data
                        
        # Update cache
        if config_type == 'tools':
            self.tools_cache = configs
        elif config_type == 'models':
            self.models_cache = configs
        elif config_type == 'providers':
            self.providers_cache = configs
        elif config_type == 'cli':
            self.cli_commands_cache = configs
            
        self.last_scan[config_type] = datetime.now()
        return configs
        
    def check_config_completeness(self, config_dir: Path, config_type: str) -> Dict[str, Any]:
        """Check if config directory has all required files"""
        required_files = {
            'tools': ['tool.py', 'tool.json', 'ui_tool.py', 'button_snippet.py'],
            'models': ['model.json'],
            'providers': ['provider.json'],
            'cli': ['command.py', 'command.json', 'ui_command.py']
        }
        
        files_needed = required_files.get(config_type, [])
        completeness = {
            'complete': True,
            'missing_files': [],
            'present_files': [],
            'completion_percentage': 0
        }
        
        for file_name in files_needed:
            file_path = config_dir / file_name
            if file_path.exists():
                completeness['present_files'].append(file_name)
            else:
                completeness['missing_files'].append(file_name)
                completeness['complete'] = False
                
        if files_needed:
            completeness['completion_percentage'] = (
                len(completeness['present_files']) / len(files_needed) * 100
            )
            
        return completeness
        
    def get_available_tools(self, refresh: bool = False) -> Dict[str, Any]:
        """Get available tools configurations"""
        if refresh or not self.tools_cache:
            self.scan_config_type('tools')
        return self.tools_cache.copy()
        
    def get_available_models(self, refresh: bool = False) -> Dict[str, Any]:
        """Get available model configurations"""
        if refresh or not self.models_cache:
            self.scan_config_type('models')
        return self.models_cache.copy()
        
    def get_available_providers(self, refresh: bool = False) -> Dict[str, Any]:
        """Get available provider configurations"""
        if refresh or not self.providers_cache:
            self.scan_config_type('providers')
        return self.providers_cache.copy()
        
    def get_available_cli_commands(self, refresh: bool = False) -> Dict[str, Any]:
        """Get available CLI command configurations"""
        if refresh or not self.cli_commands_cache:
            self.scan_config_type('cli')
        return self.cli_commands_cache.copy()
        
    def get_config_summary(self) -> Dict[str, Any]:
        """Get summary of all available configurations"""
        return {
            'tools': {
                'count': len(self.tools_cache),
                'complete': sum(1 for t in self.tools_cache.values() if t['_meta']['complete']['complete']),
                'last_scan': self.last_scan.get('tools')
            },
            'models': {
                'count': len(self.models_cache),
                'complete': sum(1 for m in self.models_cache.values() if m['_meta']['complete']['complete']),
                'last_scan': self.last_scan.get('models')
            },
            'providers': {
                'count': len(self.providers_cache),
                'complete': sum(1 for p in self.providers_cache.values() if p['_meta']['complete']['complete']),
                'last_scan': self.last_scan.get('providers')
            },
            'cli': {
                'count': len(self.cli_commands_cache),
                'complete': sum(1 for c in self.cli_commands_cache.values() if c['_meta']['complete']['complete']),
                'last_scan': self.last_scan.get('cli')
            }
        }
        
    def format_config_list(self, config_type: str) -> str:
        """Format config list for display in terminal"""
        configs = getattr(self, f"{config_type}_cache", {})
        
        if not configs:
            return self.visual_protocol.format_message(
                'assistant', f"No {config_type} configurations found. Add configs to configs/{config_type}/"
            )
            
        lines = [
            f"[{MAO_COLORS['pink']}]Available {config_type.title()}[/]",
            ""
        ]
        
        for name, config in sorted(configs.items()):
            meta = config.get('_meta', {})
            complete = meta.get('complete', {})
            
            # Status indicator
            if complete.get('complete', False):
                status_symbol = '●'
                status_color = MAO_COLORS['light_blue']
            else:
                status_symbol = '○'
                status_color = MAO_COLORS['yellow']
                
            # Format line
            description = config.get('description', config.get('help', 'No description'))
            completion_pct = complete.get('completion_percentage', 0)
            
            line = f"[{status_color}]{status_symbol}[/]   [{MAO_COLORS['light_blue']}]{name}[/] - {description}"
            
            if not complete.get('complete', False):
                line += f" [{MAO_COLORS['gray']}]({completion_pct:.0f}% complete)[/]"
                
            lines.append(line)
            
            # Show missing files if incomplete
            missing = complete.get('missing_files', [])
            if missing:
                missing_text = f"[{MAO_COLORS['light_brown']}]    └ Missing: {', '.join(missing)}[/]"
                lines.append(missing_text)
                
        return '\n'.join(lines)
        
    def get_incomplete_configs(self) -> Dict[str, List[str]]:
        """Get list of incomplete configurations"""
        incomplete = {}
        
        for config_type in ['tools', 'models', 'providers', 'cli']:
            configs = getattr(self, f"{config_type}_cache", {})
            incomplete_names = []
            
            for name, config in configs.items():
                meta = config.get('_meta', {})
                if not meta.get('complete', {}).get('complete', False):
                    incomplete_names.append(name)
                    
            if incomplete_names:
                incomplete[config_type] = incomplete_names
                
        return incomplete
        
    def validate_config_integrity(self) -> Dict[str, Any]:
        """Validate integrity of all configurations"""
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'config_count': 0,
            'complete_count': 0
        }
        
        for config_type in ['tools', 'models', 'providers', 'cli']:
            configs = getattr(self, f"{config_type}_cache", {})
            
            for name, config in configs.items():
                validation_results['config_count'] += 1
                
                # Check completeness
                meta = config.get('_meta', {})
                complete = meta.get('complete', {})
                
                if complete.get('complete', False):
                    validation_results['complete_count'] += 1
                else:
                    missing = complete.get('missing_files', [])
                    validation_results['warnings'].append(
                        f"{config_type}/{name}: Missing files: {', '.join(missing)}"
                    )
                    
                # Check required fields
                required_fields = self.get_required_fields(config_type)
                for field in required_fields:
                    if field not in config:
                        validation_results['errors'].append(
                            f"{config_type}/{name}: Missing required field '{field}'"
                        )
                        validation_results['valid'] = False
                        
        return validation_results
        
    def get_required_fields(self, config_type: str) -> List[str]:
        """Get required fields for config type"""
        required = {
            'tools': ['name', 'type', 'description'],
            'models': ['name', 'provider', 'model_id'],
            'providers': ['name', 'base_url', 'auth_type'],
            'cli': ['name', 'command', 'help', 'type']
        }
        return required.get(config_type, [])


class ConfigStatusDisplay:
    """Display component for showing config status in terminal"""
    
    def __init__(self, scanner: LiveConfigScanner):
        self.scanner = scanner
        self.visual_protocol = MAOVisualProtocol()
        
    def show_config_dashboard(self) -> str:
        """Show complete config dashboard"""
        summary = self.scanner.get_config_summary()
        incomplete = self.scanner.get_incomplete_configs()
        
        lines = [
            f"[{MAO_COLORS['pink']}]Configuration Dashboard[/]",
            ""
        ]
        
        # Summary by type
        for config_type, info in summary.items():
            complete_count = info['complete']
            total_count = info['count']
            completion_pct = (complete_count / total_count * 100) if total_count > 0 else 0
            
            if completion_pct == 100:
                status_color = MAO_COLORS['light_blue']
                status_symbol = '●'
            elif completion_pct >= 50:
                status_color = MAO_COLORS['yellow']
                status_symbol = '●'
            else:
                status_color = MAO_COLORS['gray']
                status_symbol = '○'
                
            line = f"[{status_color}]{status_symbol}[/]   [{MAO_COLORS['yellow']}]{config_type.title()}:[/] {complete_count}/{total_count} complete ({completion_pct:.0f}%)"
            lines.append(line)
            
        # Show incomplete configs
        if incomplete:
            lines.extend([
                "",
                f"[{MAO_COLORS['yellow']}]Incomplete Configurations:[/]"
            ])
            
            for config_type, names in incomplete.items():
                for name in names:
                    line = f"[{MAO_COLORS['light_brown']}]├──[/] [{MAO_COLORS['gray']}]{config_type}/{name}[/]"
                    lines.append(line)
                    
        lines.extend([
            "",
            f"[{MAO_COLORS['gray']}]Use /tools, /models, /providers, or /help to see details[/]"
        ])
        
        return '\n'.join(lines)


# Export key components
__all__ = [
    'LiveConfigScanner',
    'ConfigStatusDisplay',
    'ConfigChangeHandler'
]