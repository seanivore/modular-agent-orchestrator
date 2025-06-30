#!/usr/bin/env python3
"""
Tool Template - MAO Tool Implementation Template
Copy this file to create new tools for the MAO system
"""

from typing import Dict, Any, Optional
import asyncio
import json
from pathlib import Path


class ToolTemplate:
    """
    Template class for MAO tools
    
    This serves as a template for creating new tools in the MAO system.
    Copy this file and modify the methods to implement your tool's functionality.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the tool with configuration
        
        Args:
            config: Tool configuration dictionary
        """
        self.config = config or {}
        self.name = self.config.get('name', 'tool_template')
        self.version = self.config.get('version', '1.0.0')
        self.timeout = self.config.get('timeout', 30)
        self.retries = self.config.get('retries', 3)
        
        # Tool state
        self.is_initialized = False
        self.last_result = None
        
    async def initialize(self) -> bool:
        """
        Initialize the tool (async setup if needed)
        
        Returns:
            bool: True if initialization successful
        """
        try:
            # Add any async initialization logic here
            # Examples: connect to APIs, load models, setup resources
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize {self.name}: {e}")
            return False
            
    async def execute(self, input_data: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main tool execution method
        
        Args:
            input_data: Primary input for the tool
            options: Optional parameters and configuration
            
        Returns:
            Dict containing execution results
        """
        if not self.is_initialized:
            await self.initialize()
            
        options = options or {}
        
        try:
            # Main tool logic goes here
            # This is where you implement your tool's core functionality
            
            # Example implementation:
            result = await self._process_input(input_data, options)
            
            # Store result for potential reuse
            self.last_result = result
            
            return {
                'success': True,
                'data': result,
                'message': f'{self.name} executed successfully',
                'metadata': {
                    'tool_name': self.name,
                    'version': self.version,
                    'execution_time': 'calculated_time_here'
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'{self.name} execution failed: {str(e)}',
                'error': str(e),
                'metadata': {
                    'tool_name': self.name,
                    'version': self.version
                }
            }
            
    async def _process_input(self, input_data: str, options: Dict[str, Any]) -> Any:
        """
        Internal method to process the input data
        
        Modify this method to implement your tool's specific logic
        
        Args:
            input_data: The input to process
            options: Processing options
            
        Returns:
            Processed result
        """
        # TEMPLATE: Replace this with your tool's actual logic
        
        # Example processing:
        processed_data = {
            'original_input': input_data,
            'processed_at': 'timestamp_here',
            'options_used': options,
            'result': f'Processed: {input_data}'
        }
        
        # Simulate some async work
        await asyncio.sleep(0.1)
        
        return processed_data
        
    async def validate_input(self, input_data: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate input before processing
        
        Args:
            input_data: Input to validate
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
        # Examples:
        
        if not input_data:
            validation_result['valid'] = False
            validation_result['errors'].append('Input data cannot be empty')
            
        if len(input_data) > 10000:  # Example limit
            validation_result['warnings'].append('Input data is very large')
            
        # Validate options
        if options:
            required_option_keys = []  # Define required options
            for key in required_option_keys:
                if key not in options:
                    validation_result['valid'] = False
                    validation_result['errors'].append(f'Required option missing: {key}')
                    
        return validation_result
        
    async def cleanup(self) -> bool:
        """
        Cleanup resources when tool is no longer needed
        
        Returns:
            bool: True if cleanup successful
        """
        try:
            # Add cleanup logic here
            # Examples: close connections, free resources, save state
            
            self.is_initialized = False
            return True
            
        except Exception as e:
            print(f"❌ Failed to cleanup {self.name}: {e}")
            return False
            
    def get_help(self) -> Dict[str, Any]:
        """
        Get help information for this tool
        
        Returns:
            Help information dictionary
        """
        return {
            'name': self.name,
            'version': self.version,
            'description': 'Template tool for MAO system',
            'usage': {
                'input': 'String input to process',
                'options': {
                    'option1': 'Description of option1',
                    'option2': 'Description of option2'
                }
            },
            'examples': [
                {
                    'description': 'Basic usage',
                    'input': 'example input',
                    'options': {},
                    'expected_output': 'Processed result'
                }
            ],
            'parameters': self.config.get('parameters', {}),
            'output_format': self.config.get('output', {})
        }
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get current tool status
        
        Returns:
            Status information
        """
        return {
            'name': self.name,
            'version': self.version,
            'initialized': self.is_initialized,
            'last_execution': 'timestamp_if_available',
            'configuration': self.config
        }


# Factory function for tool creation
def create_tool(config: Optional[Dict[str, Any]] = None) -> ToolTemplate:
    """
    Factory function to create tool instance
    
    Args:
        config: Tool configuration
        
    Returns:
        Tool instance
    """
    return ToolTemplate(config)


# Main execution for testing
async def main():
    """Test the tool template"""
    
    # Load config
    config_path = Path(__file__).parent / 'tool.json'
    config = {}
    
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            
    # Create and test tool
    tool = create_tool(config)
    
    # Test initialization
    print(f"🔧 Testing {tool.name}")
    initialized = await tool.initialize()
    print(f"✅ Initialized: {initialized}")
    
    # Test validation
    validation = await tool.validate_input("test input")
    print(f"🔍 Validation: {validation}")
    
    # Test execution
    result = await tool.execute("test input", {"test_option": True})
    print(f"🚀 Execution result: {result}")
    
    # Test help
    help_info = tool.get_help()
    print(f"❓ Help: {help_info}")
    
    # Test cleanup
    cleaned = await tool.cleanup()
    print(f"🧹 Cleanup: {cleaned}")


if __name__ == "__main__":
    asyncio.run(main())