#!/usr/bin/env python3
"""
MAO v4 Quality Control Validator
Automated validation scripts to prevent regressions and ensure standardization
"""

import os
import sys
import json
import ast
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import re

@dataclass
class ValidationResult:
    """Results from a validation check"""
    validator: str
    passed: bool
    issues: List[str]
    warnings: List[str]
    checked_items: int
    
class Colors:
    """ANSI color codes for pretty output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


class MAOQualityValidator:
    """
    🎯 MAO v4 Quality Control Validator
    Comprehensive validation system to ensure standardization compliance
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.tools_dir = self.project_root / "tools"
        self.orchestrator_dir = self.project_root / "orchestrator"
        self.results: List[ValidationResult] = []
        
    def run_all_validations(self) -> bool:
        """Run all validation checks and return overall pass/fail"""
        print(f"{Colors.BOLD}{Colors.CYAN}🎯 MAO v4 Quality Control Validator{Colors.END}\n")
        print(f"{Colors.BLUE}Validating project at: {self.project_root.absolute()}{Colors.END}\n")
        
        # Run all validators
        validators = [
            ("Tool Structure", self.validate_tool_structure),
            ("Cost Functions", self.validate_cost_functions),
            ("Cache Patterns", self.validate_cache_patterns),
            ("Import Paths", self.validate_import_paths),
            ("JSON Schemas", self.validate_json_schemas),
            ("Error Handling", self.validate_error_handling)
        ]
        
        for name, validator in validators:
            print(f"{Colors.YELLOW}🔍 Running {name} Validator...{Colors.END}")
            try:
                result = validator()
                self.results.append(result)
                
                if result.passed:
                    print(f"{Colors.GREEN}✅ {name}: PASSED ({result.checked_items} items){Colors.END}")
                else:
                    print(f"{Colors.RED}❌ {name}: FAILED ({len(result.issues)} issues){Colors.END}")
                    
                if result.warnings:
                    print(f"{Colors.YELLOW}⚠️  {len(result.warnings)} warnings{Colors.END}")
                    
            except Exception as e:
                error_result = ValidationResult(
                    validator=name,
                    passed=False,
                    issues=[f"Validator crashed: {str(e)}"],
                    warnings=[],
                    checked_items=0
                )
                self.results.append(error_result)
                print(f"{Colors.RED}💥 {name}: CRASHED - {str(e)}{Colors.END}")
            
            print()
        
        # Print detailed results
        self.print_detailed_results()
        
        # Return overall pass/fail
        return all(result.passed for result in self.results)
    
    def validate_tool_structure(self) -> ValidationResult:
        """Validate 4-file pattern for each tool"""
        issues = []
        warnings = []
        checked_tools = 0
        
        if not self.tools_dir.exists():
            return ValidationResult(
                validator="Tool Structure",
                passed=False,
                issues=["Tools directory not found"],
                warnings=[],
                checked_items=0
            )
        
        # Check each tool directory
        for tool_dir in self.tools_dir.iterdir():
            if not tool_dir.is_dir() or tool_dir.name.startswith('.'):
                continue
                
            checked_tools += 1
            tool_name = tool_dir.name
            
            # Required files for each tool
            required_files = {
                "logic": tool_dir / f"{tool_name}.py",
                "button": tool_dir / f"button_{tool_name}.py",
                "ui": tool_dir / f"ui_{tool_name}.py",
                "config": tool_dir / f"tool_{tool_name}.json"
            }
            
            # Check if all required files exist
            missing_files = []
            for file_type, file_path in required_files.items():
                if not file_path.exists():
                    missing_files.append(file_type)
            
            if missing_files:
                issues.append(f"Tool '{tool_name}' missing files: {', '.join(missing_files)}")
                continue
            
            # Check for required functions in logic file
            logic_issues = self._check_logic_file_functions(required_files["logic"], tool_name)
            if logic_issues:
                issues.extend([f"Tool '{tool_name}': {issue}" for issue in logic_issues])
            
            # Check for required functions in button file  
            button_issues = self._check_button_file_functions(required_files["button"], tool_name)
            if button_issues:
                issues.extend([f"Tool '{tool_name}': {issue}" for issue in button_issues])
            
            # Check JSON config structure
            json_issues = self._check_json_config(required_files["config"], tool_name)
            if json_issues:
                warnings.extend([f"Tool '{tool_name}': {issue}" for issue in json_issues])
        
        return ValidationResult(
            validator="Tool Structure",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            checked_items=checked_tools
        )
    
    def validate_cost_functions(self) -> ValidationResult:
        """Ensure all tools have estimate_cost() function"""
        issues = []
        warnings = []
        checked_files = 0
        
        # Check all Python files in tools and orchestrator
        python_files = []
        
        # Tools directory
        if self.tools_dir.exists():
            for tool_dir in self.tools_dir.iterdir():
                if tool_dir.is_dir():
                    for py_file in tool_dir.glob("*.py"):
                        if not py_file.name.startswith("__"):
                            python_files.append(py_file)
        
        # Orchestrator directory  
        if self.orchestrator_dir.exists():
            for py_file in self.orchestrator_dir.glob("*.py"):
                if not py_file.name.startswith("__"):
                    python_files.append(py_file)
        
        for py_file in python_files:
            checked_files += 1
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse AST to find functions
                tree = ast.parse(content)
                
                # Look for estimate_cost function
                has_estimate_cost = False
                has_old_cost_functions = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if node.name == "estimate_cost":
                            has_estimate_cost = True
                        elif "_cost" in node.name and node.name != "estimate_cost":
                            has_old_cost_functions.append(node.name)
                
                # Check if main logic/orchestrator files have estimate_cost
                file_needs_cost = (
                    py_file.parent.name != "__pycache__" and
                    py_file.name not in ["__init__.py", "protocol.md"] and
                    "test" not in py_file.name.lower()
                )
                
                if file_needs_cost and not has_estimate_cost:
                    issues.append(f"Missing estimate_cost() function: {py_file.relative_to(self.project_root)}")
                
                if has_old_cost_functions:
                    warnings.append(f"Old cost functions found in {py_file.relative_to(self.project_root)}: {', '.join(has_old_cost_functions)}")
                    
            except Exception as e:
                warnings.append(f"Could not parse {py_file.relative_to(self.project_root)}: {str(e)}")
        
        return ValidationResult(
            validator="Cost Functions",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            checked_items=checked_files
        )
    
    def validate_cache_patterns(self) -> ValidationResult:
        """Verify CacheManager usage"""
        issues = []
        warnings = []
        checked_files = 0
        
        # Get all Python files
        python_files = []
        for directory in [self.tools_dir, self.orchestrator_dir]:
            if directory.exists():
                for py_file in directory.rglob("*.py"):
                    if not py_file.name.startswith("__") and "test" not in py_file.name.lower():
                        python_files.append(py_file)
        
        for py_file in python_files:
            checked_files += 1
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for CacheManager import
                has_cache_import = "CacheManager" in content
                has_cache_instance = "self.cache = CacheManager()" in content
                has_cache_usage = any(pattern in content for pattern in [
                    "get_cached_analysis",
                    "cache_content_analysis"
                ])
                
                # Main files should have cache integration
                is_main_file = (
                    py_file.name.endswith('.py') and
                    py_file.name not in ['__init__.py'] and
                    not py_file.name.startswith('ui_') and  # UI files don't need caching
                    'error_handling.py' not in py_file.name  # Error handling is foundational
                )
                
                if is_main_file:
                    if not has_cache_import:
                        issues.append(f"Missing CacheManager import: {py_file.relative_to(self.project_root)}")
                    elif not has_cache_instance:
                        issues.append(f"Missing cache instance: {py_file.relative_to(self.project_root)}")
                    elif not has_cache_usage:
                        warnings.append(f"CacheManager imported but not used: {py_file.relative_to(self.project_root)}")
                        
            except Exception as e:
                warnings.append(f"Could not parse {py_file.relative_to(self.project_root)}: {str(e)}")
        
        return ValidationResult(
            validator="Cache Patterns",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            checked_items=checked_files
        )
    
    def validate_import_paths(self) -> ValidationResult:
        """Check all import statements resolve correctly"""
        issues = []
        warnings = []
        checked_files = 0
        
        # Known problematic import patterns
        problematic_patterns = [
            "from orchestrator.files_api import",
            "from orchestrator.mcp_connector import", 
            "from .files_api import",
            "from .mcp_connector import",
            "import orchestrator.files_api",
            "import orchestrator.mcp_connector"
        ]
        
        # Get all Python files
        python_files = []
        for directory in [self.tools_dir, self.orchestrator_dir]:
            if directory.exists():
                for py_file in directory.rglob("*.py"):
                    if not py_file.name.startswith("__"):
                        python_files.append(py_file)
        
        for py_file in python_files:
            checked_files += 1
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                lines = content.split('\n')
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    
                    # Check for problematic import patterns
                    for pattern in problematic_patterns:
                        if pattern in line:
                            issues.append(f"Broken import in {py_file.relative_to(self.project_root)}:{line_num} - {line}")
                    
                    # Check for missing relative imports in orchestrator
                    if (py_file.parent.name == "orchestrator" and 
                        line.startswith("from orchestrator.") and
                        "files_api" not in line and "mcp_connector" not in line):
                        suggested = line.replace("from orchestrator.", "from .")
                        warnings.append(f"Should use relative import in {py_file.relative_to(self.project_root)}:{line_num} - suggest: {suggested}")
                        
            except Exception as e:
                warnings.append(f"Could not parse {py_file.relative_to(self.project_root)}: {str(e)}")
        
        return ValidationResult(
            validator="Import Paths",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            checked_items=checked_files
        )
    
    def validate_json_schemas(self) -> ValidationResult:
        """Validate JSON configuration schemas"""
        issues = []
        warnings = []
        checked_files = 0
        
        # Find all JSON config files
        json_files = []
        if self.tools_dir.exists():
            for tool_dir in self.tools_dir.iterdir():
                if tool_dir.is_dir():
                    for json_file in tool_dir.glob("tool_*.json"):
                        json_files.append(json_file)
        
        required_fields = ["name", "version", "description", "capabilities"]
        
        for json_file in json_files:
            checked_files += 1
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check required fields
                missing_fields = []
                for field in required_fields:
                    if field not in data:
                        missing_fields.append(field)
                
                if missing_fields:
                    issues.append(f"Missing fields in {json_file.relative_to(self.project_root)}: {', '.join(missing_fields)}")
                
                # Check for old field patterns
                if "id" in data and "name" not in data:
                    warnings.append(f"Should use 'name' instead of 'id' in {json_file.relative_to(self.project_root)}")
                
                if "tool_id" in data:
                    warnings.append(f"Should use 'name' instead of 'tool_id' in {json_file.relative_to(self.project_root)}")
                    
            except json.JSONDecodeError as e:
                issues.append(f"Invalid JSON in {json_file.relative_to(self.project_root)}: {str(e)}")
            except Exception as e:
                warnings.append(f"Could not read {json_file.relative_to(self.project_root)}: {str(e)}")
        
        return ValidationResult(
            validator="JSON Schemas",
            passed=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            checked_items=checked_files
        )
    
    def validate_error_handling(self) -> ValidationResult:
        """Check error handling patterns"""
        issues = []
        warnings = []
        checked_files = 0
        
        # Get all Python files
        python_files = []
        for directory in [self.tools_dir, self.orchestrator_dir]:
            if directory.exists():
                for py_file in directory.rglob("*.py"):
                    if (not py_file.name.startswith("__") and 
                        "error_handling.py" not in py_file.name and
                        "test" not in py_file.name.lower()):
                        python_files.append(py_file)
        
        for py_file in python_files:
            checked_files += 1
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for error handling imports
                has_error_import = "@handle_errors" in content or "handle_errors" in content
                has_error_decorator = "@handle_errors" in content
                
                # Check if it's a main logic file that should have error handling
                is_main_file = (
                    not py_file.name.startswith('ui_') and
                    py_file.name not in ['__init__.py'] and
                    'class ' in content  # Has classes, so likely needs error handling
                )
                
                if is_main_file and not has_error_import:
                    warnings.append(f"Consider adding error handling imports: {py_file.relative_to(self.project_root)}")
                elif has_error_import and not has_error_decorator:
                    warnings.append(f"Error handling imported but no decorators found: {py_file.relative_to(self.project_root)}")
                        
            except Exception as e:
                warnings.append(f"Could not parse {py_file.relative_to(self.project_root)}: {str(e)}")
        
        return ValidationResult(
            validator="Error Handling",
            passed=len(issues) == 0,  # Only warnings for error handling
            issues=issues,
            warnings=warnings,
            checked_items=checked_files
        )
    
    def print_detailed_results(self):
        """Print detailed validation results"""
        print(f"\n{Colors.BOLD}{Colors.WHITE}📊 DETAILED VALIDATION RESULTS{Colors.END}")
        print("=" * 60)
        
        total_issues = sum(len(r.issues) for r in self.results)
        total_warnings = sum(len(r.warnings) for r in self.results)
        passed_validators = sum(1 for r in self.results if r.passed)
        
        # Summary
        print(f"\n{Colors.BOLD}Summary:{Colors.END}")
        print(f"  Validators: {passed_validators}/{len(self.results)} passed")
        print(f"  Issues: {total_issues}")
        print(f"  Warnings: {total_warnings}")
        
        # Overall status
        if total_issues == 0:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 ALL VALIDATIONS PASSED!{Colors.END}")
            print(f"{Colors.GREEN}MAO v4 meets all quality standards!{Colors.END}")
        else:
            print(f"\n{Colors.BOLD}{Colors.RED}❌ VALIDATION FAILED{Colors.END}")
            print(f"{Colors.RED}Please fix {total_issues} issues before proceeding{Colors.END}")
        
        # Detailed breakdown
        for result in self.results:
            if result.issues or result.warnings:
                print(f"\n{Colors.BOLD}{result.validator}:{Colors.END}")
                
                for issue in result.issues:
                    print(f"  {Colors.RED}❌ {issue}{Colors.END}")
                
                for warning in result.warnings:
                    print(f"  {Colors.YELLOW}⚠️  {warning}{Colors.END}")
    
    # Helper methods
    def _check_logic_file_functions(self, file_path: Path, tool_name: str) -> List[str]:
        """Check required functions in logic file"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_functions = ["estimate_cost"]
            
            for func_name in required_functions:
                if f"def {func_name}(" not in content:
                    issues.append(f"Missing {func_name}() function in logic file")
            
            # Check for CacheManager
            if "CacheManager" not in content:
                issues.append("Missing CacheManager import in logic file")
                
        except Exception as e:
            issues.append(f"Could not read logic file: {str(e)}")
        
        return issues
    
    def _check_button_file_functions(self, file_path: Path, tool_name: str) -> List[str]:
        """Check required functions in button file"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "def create_button_snippet(" not in content:
                issues.append("Missing create_button_snippet() function in button file")
                
        except Exception as e:
            issues.append(f"Could not read button file: {str(e)}")
        
        return issues
    
    def _check_json_config(self, file_path: Path, tool_name: str) -> List[str]:
        """Check JSON config structure"""
        warnings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check for standardized field names
            if "id" in data and data["id"] != tool_name:
                warnings.append("Consider using 'name' field instead of 'id'")
                
        except Exception as e:
            warnings.append(f"Could not read JSON config: {str(e)}")
        
        return warnings


def main():
    """Run the MAO Quality Validator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MAO v4 Quality Control Validator")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    validator = MAOQualityValidator(args.project_root)
    success = validator.run_all_validations()
    
    if success:
        print(f"\n{Colors.BOLD}{Colors.GREEN}✅ Quality validation PASSED! MAO v4 is ready for production!{Colors.END}")
        sys.exit(0)
    else:
        print(f"\n{Colors.BOLD}{Colors.RED}❌ Quality validation FAILED! Please fix issues before proceeding.{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    main()