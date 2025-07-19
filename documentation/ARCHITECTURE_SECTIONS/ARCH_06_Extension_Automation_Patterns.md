# Extension and Automation Patterns - Templates, Scripts, and Workflow Automation

## Introduction

MAO implements comprehensive extension and automation patterns that enable developers to extend the system seamlessly while maintaining quality, consistency, and reliability. These patterns provide template-based development, automated validation, and workflow automation capabilities that support the LOCAL-only architecture.

## Template-Based Development Patterns

### Tool Template Architecture

The system provides standardized templates for creating new tools with consistent patterns:

```python
# templates/tools/tool.py - Standardized Tool Template
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
import asyncio

class ToolTemplate:
    """Standardized template for creating MAO tools with integrated services"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.cache_manager = CacheManager()
        self.logger = self.setup_logger()
        self.tool_metadata = {
            "name": self.__class__.__name__,
            "version": "1.0.0",
            "capabilities": [],
            "dependencies": []
        }
        
    @handle_errors
    async def initialize(self):
        """Initialize tool with configuration and dependencies"""
        try:
            # Initialize cache manager
            await self.cache_manager.initialize()
            
            # Validate configuration
            validation_result = await self.validate_configuration()
            if not validation_result["valid"]:
                raise ValueError(f"Configuration validation failed: {validation_result['errors']}")
                
            # Setup tool-specific dependencies
            await self.setup_tool_dependencies()
            
            self.logger.info(f"Tool {self.tool_metadata['name']} initialized successfully")
            
            return {
                "status": "initialized",
                "tool_name": self.tool_metadata["name"],
                "config": self.config
            }
            
        except Exception as e:
            self.logger.error(f"Tool initialization failed: {e}")
            raise
            
    @handle_errors  
    async def execute(self, input_data: str, parameters: dict = None):
        """Execute tool with standardized error handling and caching"""
        parameters = parameters or {}
        
        # Input validation
        validation_result = await self.validate_input(input_data, parameters)
        if not validation_result["valid"]:
            return {
                "status": "error",
                "errors": validation_result["errors"],
                "warnings": validation_result["warnings"]
            }
            
        # Check cache for existing results
        cache_key = self.generate_cache_key(input_data, parameters)
        cached_result = await self.cache_manager.get(cache_key, "tool_results")
        
        if cached_result:
            return {
                "status": "success",
                "result": cached_result,
                "cached": True,
                "cost": {"tokens": 0, "time_ms": 0}
            }
            
        # Cost estimation before execution
        estimated_cost = self.estimate_cost(input_data, parameters)
        
        try:
            # Execute tool-specific logic
            start_time = asyncio.get_event_loop().time()
            result = await self.perform_tool_operation(input_data, parameters)
            execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
            
            # Cache successful results
            if result.get("success", True):
                await self.cache_manager.set(cache_key, result, "tool_results", ttl=3600)
                
            # Update cost with actual execution time
            actual_cost = estimated_cost.copy()
            actual_cost["time_ms"] = execution_time
            
            return {
                "status": "success",
                "result": result,
                "cached": False,
                "cost": actual_cost,
                "execution_metadata": {
                    "tool_name": self.tool_metadata["name"],
                    "execution_time_ms": execution_time
                }
            }
            
        except Exception as e:
            self.logger.error(f"Tool execution failed: {e}")
            return {
                "status": "error",
                "message": str(e),
                "cost": estimated_cost,
                "error_type": type(e).__name__
            }
            
    def estimate_cost(self, input_data: str, parameters: dict = None):
        """Estimate resource cost for budget planning"""
        base_cost = {
            "tokens": len(input_data.split()) * 1.2,
            "time_ms": 1000,
            "memory_mb": 10,
            "complexity": "medium",
            "api_calls": 0
        }
        
        # Adjust based on parameters
        if parameters:
            complexity_modifiers = {
                "detailed_analysis": 2.0,
                "high_quality": 1.5,
                "batch_processing": lambda count: count * 0.8
            }
            
            for param, value in parameters.items():
                if param in complexity_modifiers:
                    modifier = complexity_modifiers[param]
                    if callable(modifier):
                        base_cost["tokens"] *= modifier(value)
                    else:
                        base_cost["tokens"] *= modifier
                        base_cost["time_ms"] *= modifier
                        
        return base_cost
        
    async def perform_tool_operation(self, input_data: str, parameters: dict):
        """Tool-specific operation implementation (to be overridden)"""
        raise NotImplementedError("Tool-specific logic must be implemented in subclass")
        
    async def validate_input(self, input_data: str, parameters: dict = None):
        """Validate input data and parameters"""
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Basic input validation
        if not input_data or not input_data.strip():
            validation["valid"] = False
            validation["errors"].append("Input data cannot be empty")
            
        if len(input_data) > 50000:  # 50KB limit
            validation["valid"] = False
            validation["errors"].append("Input data exceeds maximum size limit")
            
        # Parameter validation
        if parameters and not isinstance(parameters, dict):
            validation["valid"] = False
            validation["errors"].append("Parameters must be a dictionary")
            
        return validation
        
    async def cleanup(self):
        """Cleanup resources and connections"""
        try:
            if hasattr(self.cache_manager, 'cleanup'):
                await self.cache_manager.cleanup()
                
            self.logger.info(f"Tool {self.tool_metadata['name']} cleanup completed")
            
        except Exception as e:
            self.logger.warning(f"Cleanup warning: {e}")
```

### Configuration Template Generation

The system provides templates for configuration generation:

```python
# Configuration template generation patterns
class ConfigurationTemplateGenerator:
    def __init__(self):
        self.template_registry = {
            "tool": self.generate_tool_config_template,
            "model": self.generate_model_config_template,
            "provider": self.generate_provider_config_template,
            "cli_command": self.generate_cli_command_template,
            "user_setting": self.generate_user_setting_template
        }
        
    async def generate_tool_config_template(self, tool_name: str, capabilities: list = None):
        """Generate standardized tool configuration template"""
        capabilities = capabilities or []
        
        tool_config_template = {
            "name": tool_name,
            "version": "1.0.0",
            "description": f"{tool_name} tool for MAO system",
            "capabilities": capabilities,
            "dependencies": {
                "python_packages": [],
                "external_services": [],
                "api_keys": []
            },
            "configuration": {
                "default_timeout": 30000,
                "cache_enabled": True,
                "cache_ttl": 3600,
                "retry_attempts": 3,
                "batch_size": 10
            },
            "cost_model": {
                "base_tokens": 100,
                "complexity_multiplier": 1.0,
                "api_cost_per_request": 0.001
            },
            "ui_integration": {
                "button_generation": True,
                "progress_tracking": True,
                "result_formatting": "default"
            },
            "validation": {
                "input_size_limit": 50000,
                "required_parameters": [],
                "optional_parameters": []
            }
        }
        
        return tool_config_template
        
    async def generate_model_config_template(self, model_name: str, provider: str):
        """Generate model configuration template"""
        model_config_template = {
            "name": model_name,
            "provider": provider,
            "model_type": "language_model",
            "capabilities": [
                "text_generation",
                "conversation",
                "analysis"
            ],
            "parameters": {
                "max_tokens": 4096,
                "temperature": 0.7,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            },
            "cost_model": {
                "input_cost_per_token": 0.00001,
                "output_cost_per_token": 0.00003,
                "base_cost": 0.001
            },
            "limits": {
                "requests_per_minute": 60,
                "tokens_per_minute": 60000,
                "context_window": 128000
            },
            "compatibility": {
                "tools": ["all"],
                "workflows": ["standard", "advanced"],
                "features": ["streaming", "function_calling"]
            }
        }
        
        return model_config_template
        
    async def generate_cli_command_template(self, command_name: str, command_type: str = "utility"):
        """Generate CLI command configuration template"""
        cli_command_template = {
            "command": command_name,
            "terminal_flag": f"--{command_name}",
            "type": command_type,
            "interface_method": f"handle_{command_name}_command",
            "description": f"{command_name} command for MAO CLI",
            "category": self.determine_command_category(command_type),
            "parameters": {
                "required": [],
                "optional": []
            },
            "examples": [
                f"mao {command_name}",
                f"mao --{command_name}"
            ],
            "help_text": {
                "short": f"Execute {command_name} operation",
                "long": f"Detailed description of {command_name} command functionality and usage patterns."
            },
            "execution": {
                "timeout": 30000,
                "progress_tracking": True,
                "subprocess_safe": True
            }
        }
        
        return cli_command_template
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
# scripts/install_mao_command.sh - MAO installation automation

set -e  # Exit on any error

echo "🚀 Installing MAO (Modular Agent Orchestrator)..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Function to install Python dependencies
install_python_dependencies() {
    echo "📦 Installing Python dependencies..."
    
    # Check for Python
    if ! command_exists python3; then
        echo "❌ Python 3 is required but not installed."
        echo "Please install Python 3.8 or higher and try again."
        exit 1
    fi
    
    # Check for pip
    if ! command_exists pip3; then
        echo "❌ pip3 is required but not installed."
        echo "Please install pip and try again."
        exit 1
    fi
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        echo "✅ Python dependencies installed successfully"
    else
        echo "⚠️  requirements.txt not found, skipping Python dependencies"
    fi
}

# Function to install Node.js dependencies
install_nodejs_dependencies() {
    echo "📦 Installing Node.js dependencies..."
    
    # Check for Node.js
    if ! command_exists node; then
        echo "❌ Node.js is required but not installed."
        echo "Please install Node.js 16 or higher and try again."
        exit 1
    fi
    
    # Check for npm
    if ! command_exists npm; then
        echo "❌ npm is required but not installed."
        echo "Please install npm and try again."
        exit 1
    fi
    
    # Install Node.js dependencies
    if [ -f "package.json" ]; then
        npm install
        echo "✅ Node.js dependencies installed successfully"
    else
        echo "⚠️  package.json not found, skipping Node.js dependencies"
    fi
}

# Function to setup MAO command
setup_mao_command() {
    echo "🔧 Setting up MAO command..."
    
    local os_type=$(detect_os)
    local install_dir
    local mao_script_path="./scripts/mao.sh"
    
    # Determine installation directory based on OS
    case $os_type in
        "linux"|"macos")
            install_dir="/usr/local/bin"
            ;;
        "windows")
            install_dir="$HOME/bin"
            mkdir -p "$install_dir"
            ;;
        *)
            echo "⚠️  Unknown OS, using current directory"
            install_dir="."
            ;;
    esac
    
    # Check if MAO script exists
    if [ ! -f "$mao_script_path" ]; then
        echo "❌ MAO script not found at $mao_script_path"
        exit 1
    fi
    
    # Copy MAO script to installation directory
    if [ -w "$install_dir" ]; then
        cp "$mao_script_path" "$install_dir/mao"
        chmod +x "$install_dir/mao"
        echo "✅ MAO command installed to $install_dir/mao"
    else
        echo "❌ Permission denied: Cannot write to $install_dir"
        echo "Please run with sudo or choose a different installation directory"
        exit 1
    fi
    
    # Update PATH if necessary
    case $os_type in
        "linux"|"macos")
            if [[ ":$PATH:" != *":$install_dir:"* ]]; then
                echo "⚠️  $install_dir is not in your PATH"
                echo "Add this line to your shell profile (.bashrc, .zshrc, etc.):"
                echo "export PATH=\"$install_dir:\$PATH\""
            fi
            ;;
        "windows")
            echo "⚠️  Please add $install_dir to your PATH environment variable"
            ;;
    esac
}

# Function to validate installation
validate_installation() {
    echo "🔍 Validating MAO installation..."
    
    # Check if MAO command is available
    if command_exists mao; then
        echo "✅ MAO command is available"
        
        # Test MAO command
        if mao --version >/dev/null 2>&1; then
            echo "✅ MAO command working correctly"
        else
            echo "⚠️  MAO command found but not working properly"
        fi
    else
        echo "⚠️  MAO command not found in PATH"
        echo "You may need to restart your terminal or update your PATH"
    fi
    
    # Run MAO validator if available
    if [ -f "scripts/quality_validator/mao_validator.py" ]; then
        echo "🔍 Running quality validation..."
        python3 scripts/quality_validator/mao_validator.py
    fi
}

# Main installation process
main() {
    echo "🎯 Starting MAO installation process..."
    echo "Operating System: $(detect_os)"
    echo ""
    
    # Install dependencies
    install_python_dependencies
    echo ""
    
    install_nodejs_dependencies
    echo ""
    
    # Setup MAO command
    setup_mao_command
    echo ""
    
    # Validate installation
    validate_installation
    echo ""
    
    echo "🎉 MAO installation completed successfully!"
    echo ""
    echo "Quick Start:"
    echo "  mao help                 # Show available commands"
    echo "  mao goal \"your goal\"     # Create a new workflow"
    echo "  mao workflows            # List active workflows"
    echo ""
    echo "For more information, visit: https://github.com/your-org/mao"
}

# Run main function
main "$@"
```

### Configuration Documentation Script

Automated configuration documentation generation:

```python
# scripts/config_documenter.py
class ConfigurationDocumenter:
    """Automated configuration documentation generator"""
    
    def __init__(self):
        self.config_types = {
            "models": "AI model configurations",
            "providers": "AI service provider configurations", 
            "tools": "Tool configurations and metadata",
            "settings": "Application settings and user preferences",
            "cli": "CLI command configurations"
        }
        
    async def generate_full_documentation(self, output_dir: Path):
        """Generate comprehensive configuration documentation"""
        print("📚 Generating MAO configuration documentation...")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate documentation for each configuration type
        for config_type, description in self.config_types.items():
            print(f"📄 Documenting {config_type} configurations...")
            
            try:
                doc_content = await self.document_configuration_type(config_type)
                
                doc_file = output_dir / f"{config_type}_configuration.md"
                with open(doc_file, 'w') as f:
                    f.write(doc_content)
                    
                print(f"✅ {config_type} documentation saved to {doc_file}")
                
            except Exception as e:
                print(f"❌ Failed to document {config_type}: {e}")
                
        # Generate master configuration index
        index_content = await self.generate_configuration_index()
        index_file = output_dir / "configuration_index.md"
        
        with open(index_file, 'w') as f:
            f.write(index_content)
            
        print(f"📑 Configuration index saved to {index_file}")
        print("🎉 Configuration documentation generation completed!")
        
    async def document_configuration_type(self, config_type: str):
        """Document specific configuration type with examples"""
        config_dir = Path(f"configs/{config_type}")
        
        documentation = f"""# {config_type.title()} Configuration Documentation

## Overview

{self.config_types[config_type]}

## Configuration Files

"""
        
        if config_dir.exists():
            config_files = sorted(config_dir.glob("*.json"))
            
            for config_file in config_files:
                try:
                    with open(config_file, 'r') as f:
                        config_data = json.load(f)
                        
                    file_doc = await self.document_configuration_file(
                        config_file.name, 
                        config_data,
                        config_type
                    )
                    
                    documentation += file_doc + "\n\n"
                    
                except Exception as e:
                    documentation += f"### {config_file.name}\n\n❌ Error loading configuration: {e}\n\n"
        else:
            documentation += f"⚠️  Configuration directory `configs/{config_type}` not found.\n\n"
            
        # Add usage examples
        documentation += await self.generate_usage_examples(config_type)
        
        return documentation
        
    async def document_configuration_file(self, filename: str, config_data: dict, config_type: str):
        """Document individual configuration file"""
        doc = f"### {filename}\n\n"
        
        # Add description if available
        if "description" in config_data:
            doc += f"**Description:** {config_data['description']}\n\n"
            
        # Add key configuration elements
        if config_type == "models":
            doc += await self.document_model_config(config_data)
        elif config_type == "providers":
            doc += await self.document_provider_config(config_data)
        elif config_type == "tools":
            doc += await self.document_tool_config(config_data)
        elif config_type == "settings":
            doc += await self.document_settings_config(config_data)
        elif config_type == "cli":
            doc += await self.document_cli_config(config_data)
        else:
            doc += await self.document_generic_config(config_data)
            
        return doc
        
    async def document_model_config(self, config_data: dict):
        """Document model configuration specifics"""
        doc = "**Model Configuration:**\n\n"
        
        key_fields = ["name", "provider", "capabilities", "parameters", "cost_model"]
        
        for field in key_fields:
            if field in config_data:
                doc += f"- **{field.title()}:** `{config_data[field]}`\n"
                
        if "cost_model" in config_data:
            cost_model = config_data["cost_model"]
            doc += f"\n**Cost Information:**\n"
            doc += f"- Input cost: ${cost_model.get('input_cost_per_token', 'N/A')} per token\n"
            doc += f"- Output cost: ${cost_model.get('output_cost_per_token', 'N/A')} per token\n"
            
        return doc
```

## Workflow Automation Patterns

### Automated Business Process Integration

The system enables automated business process workflows:

```python
# Workflow automation example for business processes
class BusinessProcessAutomation:
    """Automated business process workflows using MAO"""
    
    def __init__(self):
        self.workflow_templates = {
            "content_marketing": self.content_marketing_workflow,
            "data_analysis": self.data_analysis_workflow,
            "project_planning": self.project_planning_workflow,
            "customer_service": self.customer_service_workflow
        }
        
    async def execute_automated_workflow(self, workflow_type: str, inputs: dict):
        """Execute automated business workflow"""
        if workflow_type not in self.workflow_templates:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
            
        workflow_func = self.workflow_templates[workflow_type]
        
        # Initialize workflow tracking
        workflow_id = f"{workflow_type}_{int(time.time())}"
        
        try:
            result = await workflow_func(workflow_id, inputs)
            
            return {
                "workflow_id": workflow_id,
                "workflow_type": workflow_type,
                "status": "completed",
                "result": result,
                "automation_level": "full"
            }
            
        except Exception as e:
            return {
                "workflow_id": workflow_id,
                "workflow_type": workflow_type,
                "status": "failed",
                "error": str(e),
                "automation_level": "partial"
            }
            
    async def content_marketing_workflow(self, workflow_id: str, inputs: dict):
        """Automated content marketing workflow"""
        topic = inputs.get("topic", "")
        target_audience = inputs.get("target_audience", "general")
        content_types = inputs.get("content_types", ["blog_post", "social_media"])
        
        workflow_steps = []
        
        # Step 1: Research and ideation
        research_result = await self.execute_tool_step(
            "web_search",
            f"research latest trends in {topic}",
            {"count": 10, "freshness": "week"}
        )
        workflow_steps.append(("research", research_result))
        
        # Step 2: Content generation for each type
        content_results = {}
        
        for content_type in content_types:
            if content_type == "blog_post":
                blog_result = await self.execute_tool_step(
                    "content_creation",
                    f"write comprehensive blog post about {topic} for {target_audience}",
                    {"style": "professional", "length": "detailed"}
                )
                content_results["blog_post"] = blog_result
                
            elif content_type == "social_media":
                social_result = await self.execute_tool_step(
                    "content_creation",
                    f"create social media posts about {topic} for {target_audience}",
                    {"platforms": ["twitter", "linkedin"], "count": 5}
                )
                content_results["social_media"] = social_result
                
        workflow_steps.append(("content_generation", content_results))
        
        # Step 3: Image generation
        image_result = await self.execute_tool_step(
            "dalle_image_generation",
            f"create professional image for {topic} content marketing",
            {"style": "professional", "size": "1024x1024"}
        )
        workflow_steps.append(("image_generation", image_result))
        
        # Step 4: SEO optimization
        seo_result = await self.execute_tool_step(
            "seo_optimizer",
            f"optimize content for {topic} SEO",
            {"target_keywords": [topic], "content": content_results}
        )
        workflow_steps.append(("seo_optimization", seo_result))
        
        return {
            "topic": topic,
            "target_audience": target_audience,
            "workflow_steps": workflow_steps,
            "deliverables": {
                "content": content_results,
                "images": image_result,
                "seo_recommendations": seo_result
            }
        }
```

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