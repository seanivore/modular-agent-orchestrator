#!/usr/bin/env python3
"""
UI Tool Template - MAO UI Component Template
Copy this file to create new UI components for tools
"""

from typing import Dict, Any, Optional, List
import asyncio
import json
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors


def estimate_cost(render_data: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    """
    Estimate rendering cost for UI component
    
    Args:
        render_data: Data to render in UI
        options: Optional rendering options
        
    Returns:
        Dict with cost estimates (complexity, render_time, memory)
    """
    options = options or {}
    
    # Calculate complexity based on data structure
    data_size = len(str(render_data))
    nested_levels = _count_nested_levels(render_data)
    
    # Base estimates
    estimated_complexity = min(10, (data_size / 100) + nested_levels)
    estimated_render_time = max(0.05, data_size / 10000)  # seconds
    estimated_memory = data_size * 3  # bytes for DOM representation
    
    # Apply option-based multipliers
    if options.get('interactive', False):
        estimated_complexity *= 1.5
        estimated_render_time *= 1.3
        
    if options.get('real_time_updates', False):
        estimated_complexity *= 2
        estimated_render_time *= 0.8  # optimized for updates
    
    return {
        'estimated_complexity': round(estimated_complexity, 2),
        'estimated_render_time_seconds': round(estimated_render_time, 3),
        'estimated_memory_bytes': estimated_memory,
        'nested_levels': nested_levels
    }


def _count_nested_levels(data: Any, level: int = 0) -> int:
    """Count maximum nesting levels in data structure"""
    if isinstance(data, dict):
        if not data:
            return level
        return max(_count_nested_levels(v, level + 1) for v in data.values())
    elif isinstance(data, list):
        if not data:
            return level
        return max(_count_nested_levels(item, level + 1) for item in data)
    else:
        return level


class UIToolTemplate:
    """
    Template class for MAO UI components
    
    This serves as a template for creating new UI components in the MAO system.
    Copy this file and modify the methods to implement your UI component's functionality.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the UI component with configuration
        
        Args:
            config: UI component configuration dictionary
        """
        self.config = config or {}
        self.name = self.config.get('name', 'ui_tool_template')
        self.version = self.config.get('version', '1.0.0')
        self.component_type = self.config.get('component_type', 'generic')
        self.theme = self.config.get('theme', 'default')
        
        # MAO integrations
        self.cache = CacheManager()
        
        # UI component state
        self.is_initialized = False
        self.last_render = None
        self.render_cache = {}
        
    async def initialize(self) -> bool:
        """
        Initialize the UI component (async setup if needed)
        
        Returns:
            bool: True if initialization successful
        """
        try:
            # Add any async initialization logic here
            # Examples: load themes, setup event handlers, initialize frameworks
            
            # Load theme configuration
            await self._load_theme()
            
            # Initialize render cache
            self.render_cache = {}
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to initialize UI component {self.name}: {e}")
            return False
            
    @handle_errors(operation_name="ui_render", return_dict=True)
    async def render(self, data: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main UI rendering method
        
        Args:
            data: Data to render in the UI component
            options: Optional rendering parameters and configuration
            
        Returns:
            Dict containing rendering results
        """
        if not self.is_initialized:
            await self.initialize()
            
        options = options or {}
        
        # Estimate rendering cost
        cost_estimate = estimate_cost(data, options)
        
        # Check cache for similar renders
        cache_key = self._generate_cache_key(data, options)
        cached_result = await self.cache.get(cache_key)
        
        if cached_result and not options.get('force_refresh', False):
            return {
                'success': True,
                'html': cached_result['html'],
                'css': cached_result['css'],
                'js': cached_result['js'],
                'message': f'{self.name} rendered from cache',
                'cached': True,
                'metadata': {
                    'component_name': self.name,
                    'version': self.version,
                    'cost_estimate': cost_estimate
                }
            }
        
        try:
            # Main rendering logic goes here
            render_result = await self._render_component(data, options)
            
            # Store result for potential reuse
            self.last_render = render_result
            
            # Cache the result
            await self.cache.set(cache_key, {
                'html': render_result['html'],
                'css': render_result['css'], 
                'js': render_result['js']
            }, ttl=3600)  # 1 hour cache
            
            return {
                'success': True,
                'html': render_result['html'],
                'css': render_result['css'],
                'js': render_result['js'],
                'message': f'{self.name} rendered successfully',
                'cached': False,
                'metadata': {
                    'component_name': self.name,
                    'version': self.version,
                    'render_time': render_result.get('render_time', 0),
                    'cost_estimate': cost_estimate
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'html': '<div class="error">Render failed</div>',
                'css': '.error { color: red; }',
                'js': 'console.error("Render failed");',
                'message': f'{self.name} rendering failed: {str(e)}',
                'error': str(e),
                'metadata': {
                    'component_name': self.name,
                    'version': self.version
                }
            }
            
    async def _render_component(self, data: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal method to render the UI component
        
        Modify this method to implement your component's specific rendering logic
        
        Args:
            data: The data to render
            options: Rendering options
            
        Returns:
            Rendering result with HTML, CSS, and JS
        """
        import time
        start_time = time.time()
        
        # TEMPLATE: Replace this with your component's actual rendering logic
        
        # Example rendering:
        component_id = f"{self.name}_{hash(str(data)) % 10000}"
        
        # Generate HTML
        html = self._generate_html(data, component_id, options)
        
        # Generate CSS
        css = self._generate_css(component_id, options)
        
        # Generate JavaScript
        js = self._generate_js(component_id, options)
        
        # Simulate some rendering work
        await asyncio.sleep(0.05)
        
        render_time = time.time() - start_time
        
        return {
            'html': html,
            'css': css,
            'js': js,
            'component_id': component_id,
            'render_time': render_time,
            'data_processed': data
        }
        
    def _generate_html(self, data: Dict[str, Any], component_id: str, options: Dict[str, Any]) -> str:
        """Generate HTML for the component"""
        
        # Basic template HTML structure
        html = f'''
        <div id="{component_id}" class="mao-ui-component {self.component_type}-component">
            <div class="component-header">
                <h3>{self.name}</h3>
                <span class="version">v{self.version}</span>
            </div>
            <div class="component-content">
                <div class="data-display">
                    <pre>{json.dumps(data, indent=2)}</pre>
                </div>
            </div>
            <div class="component-footer">
                <span class="status">Ready</span>
            </div>
        </div>
        '''
        
        return html.strip()
        
    def _generate_css(self, component_id: str, options: Dict[str, Any]) -> str:
        """Generate CSS for the component"""
        
        theme_colors = self._get_theme_colors()
        
        css = f'''
        #{component_id} {{
            border: 1px solid {theme_colors['border']};
            border-radius: 8px;
            padding: 16px;
            margin: 8px;
            background: {theme_colors['background']};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui;
        }}
        
        #{component_id} .component-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid {theme_colors['border']};
        }}
        
        #{component_id} .component-header h3 {{
            margin: 0;
            color: {theme_colors['primary']};
        }}
        
        #{component_id} .version {{
            font-size: 0.8em;
            color: {theme_colors['secondary']};
        }}
        
        #{component_id} .component-content {{
            margin: 12px 0;
        }}
        
        #{component_id} .data-display pre {{
            background: {theme_colors['code_background']};
            padding: 12px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 0.9em;
        }}
        
        #{component_id} .component-footer {{
            text-align: right;
            font-size: 0.8em;
            color: {theme_colors['secondary']};
        }}
        '''
        
        return css.strip()
        
    def _generate_js(self, component_id: str, options: Dict[str, Any]) -> str:
        """Generate JavaScript for the component"""
        
        js = f'''
        (function() {{
            const component = document.getElementById('{component_id}');
            if (!component) return;
            
            // Add interactive functionality
            component.addEventListener('click', function(e) {{
                if (e.target.closest('.component-header')) {{
                    const content = component.querySelector('.component-content');
                    content.style.display = content.style.display === 'none' ? 'block' : 'none';
                }}
            }});
            
            // Add hover effects
            component.addEventListener('mouseenter', function() {{
                component.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
            }});
            
            component.addEventListener('mouseleave', function() {{
                component.style.boxShadow = 'none';
            }});
            
            // Initialize component
            console.log('UI Component {self.name} initialized:', '{component_id}');
        }})();
        '''
        
        return js.strip()
        
    def _get_theme_colors(self) -> Dict[str, str]:
        """Get theme colors based on current theme"""
        
        themes = {
            'default': {
                'primary': '#333333',
                'secondary': '#666666', 
                'background': '#ffffff',
                'border': '#e0e0e0',
                'code_background': '#f5f5f5'
            },
            'dark': {
                'primary': '#ffffff',
                'secondary': '#cccccc',
                'background': '#2d2d2d', 
                'border': '#444444',
                'code_background': '#1e1e1e'
            }
        }
        
        return themes.get(self.theme, themes['default'])
        
    async def _load_theme(self) -> None:
        """Load theme configuration"""
        # Add theme loading logic here
        pass
        
    def _generate_cache_key(self, data: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Generate cache key for render result"""
        import hashlib
        key_data = f"{self.name}_{self.version}_{str(data)}_{str(options)}"
        return hashlib.md5(key_data.encode()).hexdigest()
        
    async def validate_data(self, data: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate data before rendering
        
        Args:
            data: Data to validate
            options: Validation options
            
        Returns:
            Validation results
        """
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Add your validation logic here
        if not isinstance(data, dict):
            validation_result['valid'] = False
            validation_result['errors'].append('Data must be a dictionary')
            
        if not data:
            validation_result['warnings'].append('Data is empty')
            
        # Check data size
        data_size = len(str(data))
        if data_size > 50000:  # 50KB limit
            validation_result['warnings'].append('Data is very large, may impact performance')
            
        return validation_result
        
    async def cleanup(self) -> bool:
        """
        Cleanup resources when component is no longer needed
        
        Returns:
            bool: True if cleanup successful
        """
        try:
            # Clear render cache
            self.render_cache.clear()
            
            # Clear component cache entries
            # Note: In production, you might want to be more selective
            
            self.is_initialized = False
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to cleanup UI component {self.name}: {e}")
            return False
            
    def get_help(self) -> Dict[str, Any]:
        """
        Get help information for this UI component
        
        Returns:
            Help information dictionary
        """
        return {
            'name': self.name,
            'version': self.version,
            'component_type': self.component_type,
            'description': 'Template UI component for MAO system',
            'usage': {
                'data': 'Dictionary of data to render',
                'options': {
                    'theme': 'UI theme (default, dark)',
                    'interactive': 'Enable interactive features',
                    'force_refresh': 'Skip cache and force re-render'
                }
            },
            'examples': [
                {
                    'description': 'Basic rendering',
                    'data': {'message': 'Hello World', 'count': 42},
                    'options': {},
                    'expected_output': 'HTML component with data display'
                }
            ],
            'themes': ['default', 'dark'],
            'output_format': {
                'html': 'Component HTML string',
                'css': 'Component CSS string',
                'js': 'Component JavaScript string'
            }
        }
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get current component status
        
        Returns:
            Status information
        """
        return {
            'name': self.name,
            'version': self.version,
            'component_type': self.component_type,
            'theme': self.theme,
            'initialized': self.is_initialized,
            'last_render_time': getattr(self.last_render, 'render_time', None) if self.last_render else None,
            'cache_entries': len(self.render_cache),
            'configuration': self.config
        }


# Factory function for UI component creation
def create_ui_tool(config: Optional[Dict[str, Any]] = None) -> UIToolTemplate:
    """
    Factory function to create UI component instance
    
    Args:
        config: UI component configuration
        
    Returns:
        UI component instance
    """
    return UIToolTemplate(config)


# Main execution for testing
async def main():
    """Test the UI tool template"""
    
    # Load config
    config_path = Path(__file__).parent / 'tool.json'
    config = {}
    
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            
    # Create and test UI component
    ui_component = create_ui_tool(config)
    
    # Test initialization
    print(f"TESTING: {ui_component.name}")
    initialized = await ui_component.initialize()
    print(f"SUCCESS: Initialized: {initialized}")
    
    # Test validation
    test_data = {'message': 'Test render', 'items': [1, 2, 3]}
    validation = await ui_component.validate_data(test_data)
    print(f"VALIDATION: {validation}")
    
    # Test rendering
    result = await ui_component.render(test_data, {'theme': 'default'})
    print(f"RENDER: Success: {result['success']}")
    print(f"HTML Length: {len(result['html'])}")
    
    # Test help
    help_info = ui_component.get_help()
    print(f"HELP: Available themes: {help_info['themes']}")
    
    # Test cleanup
    cleaned = await ui_component.cleanup()
    print(f"CLEANUP: {cleaned}")


if __name__ == "__main__":
    asyncio.run(main())
