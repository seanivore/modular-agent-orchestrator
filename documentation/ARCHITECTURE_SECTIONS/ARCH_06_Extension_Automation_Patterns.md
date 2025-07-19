# Extension and Automation Patterns - Templates, Scripts, and Workflow Automation

## Introduction

MAO implements comprehensive extension and automation patterns that enable developers to extend the system seamlessly while maintaining quality, consistency, and reliability. These patterns provide template-based development, automated validation, and workflow automation capabilities that support the LOCAL-only architecture.

## Template-Based Development Patterns

### Tool Template Architecture

The system provides standardized templates for creating new tools with consistent patterns:

```python
# templates/tools/tool.py - VERIFIED: Actual Template Implementation
from typing import Dict, Any, Optional
import asyncio
import json
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors


def estimate_cost(input_data: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    """
    Estimate execution cost for tool usage
    
    Args:
        input_data: Input data to process
        options: Optional processing options
        
    Returns:
        Dict with cost estimates (tokens, time, resources)
    """
    options = options or {}
    
    # Basic cost estimation template
    # Modify these calculations based on your tool's actual resource usage
    input_length = len(input_data)
    
    # Estimate based on input size
    estimated_tokens = input_length * 0.75  # Rough token estimate
    estimated_time = max(0.1, input_length / 1000)  # Rough time estimate in seconds
    estimated_memory = input_length * 2  # Rough memory estimate in bytes
    
    # Apply option-based multipliers
    if options.get('detailed_processing', False):
        estimated_tokens *= 2
        estimated_time *= 1.5
        
    if options.get('high_quality', False):
        estimated_tokens *= 1.3
        estimated_time *= 1.2
    
    return {
        'estimated_tokens': round(estimated_tokens, 2),
        'estimated_time_seconds': round(estimated_time, 2),
        'estimated_memory_bytes': estimated_memory,
        'complexity_score': min(10, input_length / 100)  # 1-10 scale
    }


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
        
        # MAO integrations
        self.cache = CacheManager()
        
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
            print(f"ERROR: Failed to initialize {self.name}: {e}")
            return False
            
    @handle_errors(operation_name="tool_execute", return_dict=True)
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
        
        # Estimate execution cost
        cost_estimate = estimate_cost(input_data, options)
        
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
            print(f"ERROR: Failed to cleanup {self.name}: {e}")
            return False
```

### Configuration Template Generation

The system provides actual template files for configuration generation. These template files exist in the `/templates/` directory:

**VERIFIED: Actual Template Files Available**

```json
// templates/tools/tool.json - REAL Template File
{
    "name": "tool_name",
    "version": "1.0.0",
    "description": "Template tool for MAO system",
    "type": "utility",
    "dependencies": [],
    "capabilities": [
        "example_capability"
    ],
    "ui_integration": {
        "button_snippet_function": "create_button_snippet",
        "terminal_ui_function": "create_terminal_ui"
    },
    "configuration": {
        "timeout": 30,
        "retries": 3
    },
    "output": {
        "format": "structured",
        "fields": ["result", "metadata"]
    }
}
```

**Configuration Templates Available:**
- `templates/tools/tool.json` - Tool configuration template
- `templates/models/model.json` - Model configuration template  
- `templates/providers/provider.json` - Provider configuration template
- `templates/cli_commands/cli_command.json` - CLI command template
- `templates/settings/setting_name_app_settings.json` - Settings template
- `templates/users/user_username.json` - User configuration template
- `templates/workflows/` - Workflow configuration templates

**TO BE IMPLEMENTED: Dynamic Template Generator**

The following ConfigurationTemplateGenerator class would need to be implemented to provide programmatic template generation:

```python
# TO BE IMPLEMENTED: Dynamic template generation
class ConfigurationTemplateGenerator:
    """Programmatic configuration template generator - NOT YET IMPLEMENTED"""
    
    def __init__(self):
        self.template_registry = {
            "tool": self.generate_tool_config_template,
            "model": self.generate_model_config_template,
            "provider": self.generate_provider_config_template,
            "cli_command": self.generate_cli_command_template
        }
        
    # Implementation would go here - currently uses static template files
```

## Automated Quality Validation

### Comprehensive Quality Validation System

The MAO validator ensures system-wide quality and architectural compliance:

```python
# scripts/quality_validator/mao_validator.py
class MAOQualityValidator:
    """Comprehensive quality control system for MAO ecosystem"""
    
    def __init__(self):
        self.validation_results = {
            "tool_structure": {"passed": 0, "failed": 0, "issues": []},
            "cost_functions": {"passed": 0, "failed": 0, "issues": []},
            "cache_patterns": {"passed": 0, "failed": 0, "issues": []},
            "import_paths": {"passed": 0, "failed": 0, "issues": []},
            "json_schemas": {"passed": 0, "failed": 0, "issues": []},
            "error_handling": {"passed": 0, "failed": 0, "issues": []}
        }
        
    async def validate_full_system(self, project_root: Path):
        """Comprehensive system validation with detailed reporting"""
        print("🔍 Starting MAO Quality Validation...")
        
        # Validation categories
        validation_tasks = [
            ("Tool Structure Validation", self.validate_tool_structure),
            ("Cost Function Validation", self.validate_cost_functions),
            ("Cache Pattern Validation", self.validate_cache_patterns),
            ("Import Path Validation", self.validate_import_paths),
            ("JSON Schema Validation", self.validate_json_schemas),
            ("Error Handling Validation", self.validate_error_handling)
        ]
        
        overall_success = True
        
        for task_name, validation_func in validation_tasks:
            print(f"\n📋 {task_name}...")
            
            try:
                task_result = await validation_func(project_root)
                
                if task_result["success"]:
                    print(f"  ✅ {task_name}: PASSED ({task_result['passed']} items)")
                else:
                    print(f"  ❌ {task_name}: FAILED ({task_result['failed']} issues)")
                    overall_success = False
                    
                # Display issues if any
                for issue in task_result.get("issues", []):
                    print(f"    ⚠️  {issue}")
                    
            except Exception as e:
                print(f"  💥 {task_name}: VALIDATION ERROR - {e}")
                overall_success = False
                
        # Generate summary report
        await self.generate_validation_report(overall_success)
        
        return {
            "overall_success": overall_success,
            "validation_results": self.validation_results,
            "summary": await self.generate_validation_summary()
        }
        
    async def validate_tool_structure(self, project_root: Path):
        """Validate 4-file tool architecture pattern"""
        tools_dir = project_root / "tools"
        validation_result = {"success": True, "passed": 0, "failed": 0, "issues": []}
        
        if not tools_dir.exists():
            validation_result["success"] = False
            validation_result["issues"].append("Tools directory not found")
            return validation_result
            
        for tool_dir in tools_dir.iterdir():
            if tool_dir.is_dir() and not tool_dir.name.startswith('.'):
                tool_validation = await self.validate_individual_tool_structure(tool_dir)
                
                if tool_validation["valid"]:
                    validation_result["passed"] += 1
                else:
                    validation_result["failed"] += 1
                    validation_result["success"] = False
                    validation_result["issues"].extend([
                        f"{tool_dir.name}: {issue}" for issue in tool_validation["issues"]
                    ])
                    
        self.validation_results["tool_structure"] = validation_result
        return validation_result
        
    async def validate_individual_tool_structure(self, tool_dir: Path):
        """Validate individual tool follows 4-file pattern"""
        required_files = ["logic.py", "tool.json"]
        optional_patterns = ["button_*.py", "ui_*.py"]
        
        validation = {"valid": True, "issues": []}
        
        # Check required files
        for required_file in required_files:
            file_path = tool_dir / required_file
            if not file_path.exists():
                validation["valid"] = False
                validation["issues"].append(f"Missing required file: {required_file}")
                
        # Check optional pattern files
        for pattern in optional_patterns:
            matching_files = list(tool_dir.glob(pattern))
            if not matching_files:
                validation["issues"].append(f"Missing optional file pattern: {pattern}")
                
        # Validate logic.py structure
        logic_file = tool_dir / "logic.py"
        if logic_file.exists():
            logic_validation = await self.validate_logic_file_structure(logic_file)
            if not logic_validation["valid"]:
                validation["valid"] = False
                validation["issues"].extend(logic_validation["issues"])
                
        return validation
        
    async def validate_cost_functions(self, project_root: Path):
        """Validate estimate_cost() function implementation"""
        validation_result = {"success": True, "passed": 0, "failed": 0, "issues": []}
        
        # Find all Python files in the project
        python_files = list(project_root.rglob("*.py"))
        
        for py_file in python_files:
            if await self.should_validate_cost_function(py_file):
                cost_validation = await self.validate_file_cost_function(py_file)
                
                if cost_validation["has_cost_function"]:
                    if cost_validation["valid_implementation"]:
                        validation_result["passed"] += 1
                    else:
                        validation_result["failed"] += 1
                        validation_result["success"] = False
                        validation_result["issues"].append(
                            f"{py_file.relative_to(project_root)}: {cost_validation['issue']}"
                        )
                        
        self.validation_results["cost_functions"] = validation_result
        return validation_result
        
    async def validate_file_cost_function(self, py_file: Path):
        """Validate cost function in specific file"""
        import ast
        
        validation = {
            "has_cost_function": False,
            "valid_implementation": False,
            "issue": None
        }
        
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "estimate_cost":
                    validation["has_cost_function"] = True
                    
                    # Check function signature
                    if len(node.args.args) > 0:
                        validation["valid_implementation"] = True
                    else:
                        validation["issue"] = "estimate_cost function has no parameters"
                        
                    # Check return statement
                    has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))
                    if not has_return:
                        validation["valid_implementation"] = False
                        validation["issue"] = "estimate_cost function missing return statement"
                        
                    break
                    
        except Exception as e:
            validation["issue"] = f"Failed to parse file: {e}"
            
        return validation
```

## Script Automation Patterns

### Installation and Setup Scripts

The system provides automated installation and setup scripts:

```bash
#!/bin/bash
# scripts/mao_launch_setup/install_mao_command.sh - VERIFIED: Actual Installation Script
# Install script for the Mao terminal interface command

# Set paths
BIN_DIR="${HOME}/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Backup existing mao if it exists
if [ -f "${BIN_DIR}/mao" ]; then
    echo "Backing up existing mao to mao.backup..."
    cp "${BIN_DIR}/mao" "${BIN_DIR}/mao.backup"
fi

# Create the mao command in bin directory (NO .sh extension)
echo "🚀 Creating Mao command in ${BIN_DIR}..."
cat > "${BIN_DIR}/mao" << EOF
#!/bin/bash
# Mao Terminal Interface Command
# Generated by install_mao_command.sh

# Get the absolute path to the project directory
PROJECT_DIR="$PROJECT_DIR"
LAUNCHER_PATH="\$PROJECT_DIR/mao_v4.py"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Launch Mao with all arguments passed through
python3 "\$LAUNCHER_PATH" "\$@"
EOF

# Make the command executable
chmod +x "${BIN_DIR}/mao"

# Check if ~/bin is in PATH
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo "⚠️  ~/bin is not in your PATH"
    echo "💡 Add this to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
    echo "   export PATH=\"\$HOME/bin:\$PATH\""
    echo ""
fi

# Verify the command was created
if [ -f "${BIN_DIR}/mao" ]; then
    echo "✅ Mao command installed successfully!"
    echo ""
    echo "🎭 You can now use:"
    echo "   mao           # New user onboarding"
    echo "   mao mao       # Smart launch (git-inspired)"
    echo ""
    echo "🚀 Try running: mao mao"
    echo ""
    echo "📝 Note: Make sure ~/bin is in your PATH to use 'mao' directly"
else
    echo "❌ Failed to create Mao command"
    exit 1
fi
```

### Configuration Documentation Script

Automated configuration documentation generation:

```python
# scripts/auto_docs/config_documenter.py - VERIFIED: Actual Implementation

class ConfigDocumenter:
    """Automatically generate and update docs when configs change"""
    
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.configs_dir = self.repo_root / "configs"
        self.docs_dir = self.repo_root / "versioning-docs"
        self.templates_dir = self.repo_root / "templates"
        
        # Mao integrations
        self.cache = CacheManager() if CacheManager else None
        
        # Config type mappings
        self.config_types = {
            'tools': {
                'path': 'configs/tools/',
                'doc_file': 'versioning-docs/technical-documentation/TOOLS_REFERENCE.md',
                'template_dir': 'templates/tools/',
                'required_files': ['tool.py', 'tool.json', 'ui_tool.py', 'button_snippet.py']
            },
            'models': {
                'path': 'configs/models/',
                'doc_file': 'versioning-docs/technical-documentation/MODELS_REFERENCE.md',
                'template_dir': 'templates/models/',
                'required_files': ['model.json']
            },
            'providers': {
                'path': 'configs/providers/',
                'doc_file': 'versioning-docs/technical-documentation/PROVIDERS_REFERENCE.md',
                'template_dir': 'templates/providers/',
                'required_files': ['provider.json']
            },
            'cli': {
                'path': 'configs/cli/',
                'doc_file': 'versioning-docs/technical-documentation/CLI_COMMANDS_REFERENCE.md',
                'template_dir': 'templates/cli/',
                'required_files': ['command.py', 'command.json', 'ui_command.py']
            }
        }
        
    @handle_errors(operation_name="config_scan", return_dict=True)
    def scan_config_changes(self, changed_files: List[str]) -> List[Dict[str, Any]]:
        """Detect and analyze config file changes"""
        config_changes = []
        
        for file_path in changed_files:
            if not file_path.startswith('configs/'):
                continue
                
            # Determine config type
            config_type = self.determine_config_type(file_path)
            if not config_type:
                continue
                
            change_info = self.analyze_config_change(file_path, config_type)
            if change_info:
                config_changes.append(change_info)
                
        return config_changes
        
    def determine_config_type(self, file_path: str) -> Optional[str]:
        """Determine what type of config this file represents"""
        for config_type, config_info in self.config_types.items():
            if file_path.startswith(config_info['path']):
                return config_type
        return None
        
    def analyze_config_change(self, file_path: str, config_type: str) -> Optional[Dict[str, Any]]:
        """Analyze a specific config file change"""
        full_path = self.repo_root / file_path
        
        if not full_path.exists():
            return {
                'type': 'deletion',
                'config_type': config_type,
                'file_path': file_path,
                'name': self.extract_config_name(file_path)
            }
            
        try:
            if file_path.endswith('.json'):
                with open(full_path) as f:
                    config_data = json.load(f)
                    
                return {
                    'type': 'addition' if self.is_new_config(file_path) else 'modification',
                    'config_type': config_type,
                    'file_path': file_path,
                    'name': config_data.get('name', self.extract_config_name(file_path)),
                    'data': config_data,
                    'completeness': self.check_config_completeness(file_path, config_type)
                }
        except (json.JSONDecodeError, IOError):
            return None
```

## Workflow Automation Patterns

### Automated Business Process Integration

**TO BE IMPLEMENTED: Business Process Automation System**

The MAO system provides foundational components for workflow automation through its existing infrastructure:

**VERIFIED: Existing Workflow Foundation**
- Workflow management via `orchestrator/workflow_manager.py`
- Workflow state tracking via `orchestrator/workflow_state.py`
- Tool integration patterns for automated execution
- MCP connector for external service integration
- Configuration-driven workflow templates

**VERIFIED: Workflow Template Files Available**
```
templates/workflows/
├── README.md
├── example-workflow_handoff_config.json
├── example-workflow_phase_config.json
└── example-workflow_workflow_config.json
```

**TO BE IMPLEMENTED: Comprehensive Business Process Automation**

The following BusinessProcessAutomation class represents the intended automation capabilities:

```python
# TO BE IMPLEMENTED: Advanced workflow automation
class BusinessProcessAutomation:
    """Automated business process workflows using MAO - FUTURE IMPLEMENTATION"""
    
    def __init__(self):
        # Would integrate with existing MAO components:
        # - WorkflowManager from orchestrator/workflow_manager.py
        # - ToolManager from orchestrator/manager_tools.py
        # - CacheManager from orchestrator/cache/cache_system.py
        # - MCP Hub from orchestrator/mcp_hub.py
        
        self.workflow_templates = {
            "content_marketing": self.content_marketing_workflow,
            "data_analysis": self.data_analysis_workflow,
            "project_planning": self.project_planning_workflow
        }
        
    async def execute_automated_workflow(self, workflow_type: str, inputs: dict):
        """Execute automated business workflow - IMPLEMENTATION NEEDED"""
        # Implementation would use existing MAO workflow infrastructure
        # Combined with tool orchestration and state management
        pass
        
    async def content_marketing_workflow(self, workflow_id: str, inputs: dict):
        """Content marketing automation - IMPLEMENTATION NEEDED"""
        # Would orchestrate existing tools:
        # - web_search tool for research
        # - dalle_generate tool for images  
        # - content creation workflows
        # - file_operations for output management
        pass
```

**Current Implementation Status:**
- ✅ Core workflow management infrastructure exists
- ✅ Tool orchestration patterns established
- ✅ Configuration templates available
- ❌ High-level business process automation not implemented
- ❌ Content marketing workflow automation not implemented
- ❌ Multi-step automated workflows need development

## Integration Guidelines

### Adding New Templates

To add new templates to the system:

1. **Create Template File**
   ```python
   # templates/new_category/template.py
   class NewTemplate:
       def __init__(self):
           # Template initialization
           pass
   ```

2. **Add Template Registration**
   ```python
   template_registry["new_category"] = NewTemplate
   ```

3. **Update Documentation**
   - Add template documentation
   - Include usage examples
   - Document configuration options

### Automation Script Development

For new automation scripts:

1. **Follow Standard Structure**
   - Error handling and logging
   - Progress reporting
   - Configuration validation
   - Cleanup procedures

2. **Integration Patterns**
   - Use MAO service patterns
   - Include cost estimation
   - Implement caching where appropriate
   - Follow privacy guidelines

3. **Quality Validation**
   - Add validation rules to MAO validator
   - Include automated testing
   - Document validation criteria

## Conclusion

MAO's extension and automation patterns provide a comprehensive framework for system extension while maintaining quality and consistency. The template-based development ensures standardized patterns, while automated validation prevents regression and maintains architectural compliance.

The script automation patterns enable efficient deployment and configuration management, while workflow automation provides powerful business process integration capabilities. These patterns work together to create an extensible, maintainable, and reliable foundation for AI orchestration system development.

The quality validation system ensures that all extensions maintain professional standards, while the template system enables rapid development without sacrificing consistency or reliability. This creates a sustainable ecosystem for continuous system enhancement and extension.