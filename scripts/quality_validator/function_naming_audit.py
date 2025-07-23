#!/usr/bin/env python3
"""
MAO Function Naming Audit Script
Finds inconsistencies in function/method naming across the codebase

This script analyzes:
1. Manager class method naming patterns
2. Similar functions with different names
3. Inconsistent parameter naming
4. Function naming conventions adherence
"""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Optional, Tuple
from collections import defaultdict, Counter

class FunctionNamingAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.function_patterns = defaultdict(list)
        self.method_patterns = defaultdict(list)
        self.parameter_patterns = defaultdict(list)
        self.inconsistencies = []
        
        # Common function families that should have consistent naming
        self.function_families = {
            "user_operations": ["get", "load", "fetch", "retrieve"],
            "data_storage": ["save", "store", "persist", "write"],
            "data_deletion": ["delete", "remove", "clear", "destroy"],
            "validation": ["validate", "check", "verify", "ensure"],
            "creation": ["create", "make", "generate", "build"],
            "update": ["update", "modify", "change", "edit"]
        }
        
        # Manager classes to focus on
        self.manager_classes = [
            "UsernameManager", "WorkflowManager", "SettingsManager", 
            "UserAnalyticsManager", "SystemAnalyticsManager", "CLIManager"
        ]

    def find_python_files(self) -> List[Path]:
        """Find all Python files, focusing on orchestrator and managers"""
        python_files = []
        
        # Priority directories
        priority_dirs = ["orchestrator", "configs/cli", "interfaces"]
        
        for priority_dir in priority_dirs:
            dir_path = self.project_root / priority_dir
            if dir_path.exists():
                for py_file in dir_path.rglob("*.py"):
                    if not any(skip in str(py_file) for skip in ['.backup', '__pycache__']):
                        python_files.append(py_file)
        
        return python_files

    def parse_file(self, file_path: Path) -> Optional[ast.Module]:
        """Parse a Python file into an AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return ast.parse(content, filename=str(file_path))
        except Exception as e:
            self.inconsistencies.append({
                'type': 'parse_error',
                'file': str(file_path),
                'error': str(e)
            })
            return None

    def extract_functions_and_methods(self, tree: ast.Module, file_path: Path) -> None:
        """Extract all function and method definitions from AST"""
        class FunctionVisitor(ast.NodeVisitor):
            def __init__(self, auditor, file_path):
                self.auditor = auditor
                self.file_path = file_path
                self.class_stack = []
            
            def visit_ClassDef(self, node):
                self.class_stack.append(node.name)
                self.generic_visit(node)
                self.class_stack.pop()
            
            def visit_FunctionDef(self, node):
                # Extract function info
                func_info = {
                    'name': node.name,
                    'file': str(self.file_path),
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'class': self.class_stack[-1] if self.class_stack else None,
                    'docstring': ast.get_docstring(node),
                    'is_method': bool(self.class_stack),
                    'is_private': node.name.startswith('_'),
                    'is_property': any(isinstance(d, ast.Name) and d.id == 'property' 
                                    for d in node.decorator_list) if node.decorator_list else False
                }
                
                # Categorize by type
                if func_info['is_method'] and self.class_stack:
                    class_name = self.class_stack[-1]
                    self.auditor.method_patterns[class_name].append(func_info)
                else:
                    self.auditor.function_patterns['standalone'].append(func_info)
                
                # Track parameter patterns
                for arg in func_info['args']:
                    self.auditor.parameter_patterns[arg].append({
                        'function': node.name,
                        'file': str(self.file_path),
                        'class': func_info['class']
                    })
                
                self.generic_visit(node)
        
        visitor = FunctionVisitor(self, file_path)
        visitor.visit(tree)

    def find_similar_functions(self) -> Dict[str, List]:
        """Find functions that might be doing similar things but have different names"""
        similar_functions = defaultdict(list)
        
        # Collect all functions across all classes
        all_functions = []
        
        # Add methods from all manager classes
        for class_name, methods in self.method_patterns.items():
            for method in methods:
                if not method['is_private'] and method['name'] not in ['__init__', '__str__', '__repr__']:
                    all_functions.append(method)
        
        # Add standalone functions
        for func in self.function_patterns.get('standalone', []):
            if not func['is_private']:
                all_functions.append(func)
        
        # Group by semantic similarity
        for family_name, verbs in self.function_families.items():
            family_functions = []
            for func in all_functions:
                func_name_lower = func['name'].lower()
                if any(verb in func_name_lower for verb in verbs):
                    family_functions.append(func)
            
            if len(family_functions) > 1:
                similar_functions[family_name] = family_functions
        
        return similar_functions

    def analyze_manager_consistency(self) -> Dict[str, Any]:
        """Analyze naming consistency across manager classes"""
        inconsistencies = {}
        
        # Focus on manager classes
        manager_methods = {}
        for class_name, methods in self.method_patterns.items():
            if any(manager in class_name for manager in self.manager_classes):
                manager_methods[class_name] = methods
        
        if len(manager_methods) < 2:
            return inconsistencies
        
        # Find common operation patterns
        operation_patterns = defaultdict(list)
        
        for class_name, methods in manager_methods.items():
            for method in methods:
                if not method['is_private']:
                    # Categorize method by apparent purpose
                    method_name = method['name'].lower()
                    
                    if any(verb in method_name for verb in ['get', 'load', 'fetch', 'retrieve']):
                        operation_patterns['retrieval'].append((class_name, method))
                    elif any(verb in method_name for verb in ['create', 'add', 'new']):
                        operation_patterns['creation'].append((class_name, method))
                    elif any(verb in method_name for verb in ['update', 'modify', 'change', 'set']):
                        operation_patterns['modification'].append((class_name, method))
                    elif any(verb in method_name for verb in ['delete', 'remove', 'clear']):
                        operation_patterns['deletion'].append((class_name, method))
                    elif any(verb in method_name for verb in ['list', 'find', 'search']):
                        operation_patterns['querying'].append((class_name, method))
        
        # Find inconsistencies within operation types
        for operation, methods in operation_patterns.items():
            if len(methods) > 1:
                # Group by apparent target (user, workflow, settings, etc.)
                target_groups = defaultdict(list)
                for class_name, method in methods:
                    method_name = method['name'].lower()
                    
                    if 'user' in method_name:
                        target_groups['user'].append((class_name, method))
                    elif 'workflow' in method_name:
                        target_groups['workflow'].append((class_name, method))
                    elif 'setting' in method_name:
                        target_groups['settings'].append((class_name, method))
                    else:
                        target_groups['general'].append((class_name, method))
                
                # Check for naming inconsistencies within each target group
                for target, target_methods in target_groups.items():
                    if len(target_methods) > 1:
                        method_names = [method['name'] for class_name, method in target_methods]
                        if len(set(method_names)) > 1:  # Different names for same operation
                            inconsistencies[f"{operation}_{target}"] = {
                                'operation': operation,
                                'target': target,
                                'methods': target_methods,
                                'issue': 'Different method names for similar operations'
                            }
        
        return inconsistencies

    def check_parameter_consistency(self) -> Dict[str, List]:
        """Check for parameter naming inconsistencies"""
        inconsistencies = {}
        
        # Common parameter variations that should be standardized
        param_variations = {
            'user_identifier': ['username', 'user_id', 'user_name', 'userid'],
            'workflow_identifier': ['workflow_id', 'workflow_name', 'wf_id'],
            'settings_name': ['setting_name', 'setting_id', 'setting_key'],
            'file_path': ['file_path', 'filepath', 'path', 'file_name'],
            'data_content': ['content', 'data', 'value', 'payload']
        }
        
        for concept, variations in param_variations.items():
            found_variations = []
            for param_name in variations:
                if param_name in self.parameter_patterns:
                    usages = self.parameter_patterns[param_name]
                    found_variations.append({
                        'param_name': param_name,
                        'usage_count': len(usages),
                        'functions': usages
                    })
            
            if len(found_variations) > 1:
                inconsistencies[concept] = found_variations
        
        return inconsistencies

    def generate_recommendations(self, similar_functions: Dict, manager_inconsistencies: Dict, 
                               param_inconsistencies: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if similar_functions:
            recommendations.append("🔧 Standardize function naming across similar operations")
            
        if manager_inconsistencies:
            recommendations.append("👥 Create consistent method naming conventions for Manager classes")
            
        if param_inconsistencies:
            recommendations.append("📝 Standardize parameter names across the codebase")
            
        recommendations.extend([
            "📚 Create and document function naming guidelines",
            "🏗️ Consider refactoring to use common base classes for managers",
            "🧪 Add linting rules to enforce naming conventions",
            "🔄 Review function families for consolidation opportunities"
        ])
        
        return recommendations

    def run_audit(self) -> Dict[str, Any]:
        """Run complete function naming audit"""
        print("🔍 Starting MAO Function Naming Audit...")
        
        python_files = self.find_python_files()
        print(f"📁 Found {len(python_files)} Python files to analyze")
        
        # Parse all files
        parsed_count = 0
        for file_path in python_files:
            tree = self.parse_file(file_path)
            if tree:
                self.extract_functions_and_methods(tree, file_path)
                parsed_count += 1
        
        # Analyze patterns
        similar_functions = self.find_similar_functions()
        manager_inconsistencies = self.analyze_manager_consistency()
        param_inconsistencies = self.check_parameter_consistency()
        
        # Compile results
        results = {
            'summary': {
                'files_analyzed': len(python_files),
                'files_parsed': parsed_count,
                'classes_found': len(self.method_patterns),
                'total_functions': sum(len(funcs) for funcs in self.function_patterns.values()),
                'total_methods': sum(len(methods) for methods in self.method_patterns.values()),
                'similar_function_groups': len(similar_functions),
                'manager_inconsistencies': len(manager_inconsistencies),
                'parameter_inconsistencies': len(param_inconsistencies)
            },
            'similar_functions': similar_functions,
            'manager_inconsistencies': manager_inconsistencies,
            'parameter_inconsistencies': param_inconsistencies,
            'errors': self.inconsistencies,
            'recommendations': self.generate_recommendations(similar_functions, manager_inconsistencies, param_inconsistencies)
        }
        
        return results

    def generate_report(self, output_file: str = "function_naming_audit_report.json") -> None:
        """Generate detailed audit report"""
        import json
        
        results = self.run_audit()
        
        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 MAO FUNCTION NAMING AUDIT RESULTS")
        print("="*60)
        
        summary = results['summary']
        print(f"📁 Files analyzed: {summary['files_analyzed']}")
        print(f"✅ Files parsed: {summary['files_parsed']}")
        print(f"🏛️ Classes found: {summary['classes_found']}")
        print(f"⚙️ Total functions: {summary['total_functions']}")
        print(f"🔧 Total methods: {summary['total_methods']}")
        print(f"👥 Similar function groups: {summary['similar_function_groups']}")
        print(f"⚠️ Manager inconsistencies: {summary['manager_inconsistencies']}")
        print(f"📝 Parameter inconsistencies: {summary['parameter_inconsistencies']}")
        
        # Show similar function groups
        if results['similar_functions']:
            print(f"\n👥 SIMILAR FUNCTION GROUPS:")
            for family, functions in list(results['similar_functions'].items())[:3]:
                print(f"  📦 {family.upper()}:")
                for func in functions[:5]:
                    class_info = f" ({func['class']})" if func['class'] else ""
                    print(f"    🔧 {func['name']}{class_info} - {Path(func['file']).name}")
        
        # Show manager inconsistencies
        if results['manager_inconsistencies']:
            print(f"\n⚠️ MANAGER INCONSISTENCIES:")
            for issue_key, issue in list(results['manager_inconsistencies'].items())[:3]:
                print(f"  📦 {issue['operation'].upper()} operations for {issue['target']}:")
                for class_name, method in issue['methods']:
                    print(f"    🔧 {class_name}.{method['name']}()")
        
        # Show parameter inconsistencies
        if results['parameter_inconsistencies']:
            print(f"\n📝 PARAMETER INCONSISTENCIES:")
            for concept, variations in list(results['parameter_inconsistencies'].items())[:3]:
                print(f"  📦 {concept.upper()}:")
                for var in variations:
                    print(f"    📝 '{var['param_name']}' used in {var['usage_count']} functions")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"  {rec}")
        
        print(f"\n📄 Full report saved to: {output_file}")
        print("="*60)

def main():
    """Run the function naming audit"""
    auditor = FunctionNamingAuditor()
    auditor.generate_report()

if __name__ == "__main__":
    main() 