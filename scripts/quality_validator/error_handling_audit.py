#!/usr/bin/env python3
"""
MAO Error Handling Audit Script
Finds inconsistencies in error handling patterns across the codebase

This script analyzes:
1. @handle_errors decorator usage vs manual try" / "catch
2. Error return patterns (dict vs exceptions vs None)
3. Logging consistency in error scenarios
4. Error type standardization (APIError, ValidationError, etc.)
5. Error propagation patterns
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from collections import defaultdict, Counter

class ErrorHandlingAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.error_patterns = defaultdict(list)
        self.decorator_usage = defaultdict(list)
        self.manual_handling = defaultdict(list)
        self.error_types = defaultdict(list)
        self.return_patterns = defaultdict(list)
        self.logging_patterns = defaultdict(list)
        
        # Expected error types from MAO
        self.mao_error_types = [
            "APIError", "ValidationError", "ResourceError", 
            "ConfigError", "CacheError", "AuthError"
        ]
        
        # Error handling decorators
        self.error_decorators = [
            "handle_errors", "retry_with_backoff", "timeout"
        ]

    def find_python_files(self) -> List[Path]:
        """Find Python files, focusing on core functionality"""
        python_files = []
        
        # Priority directories for error handling analysis
        priority_dirs = ["orchestrator", "configs" / "cli", "interfaces", "tools"]
        
        for priority_dir in priority_dirs:
            dir_path = self.project_root " / " priority_dir
            if dir_path.exists():
                for py_file in dir_path.rglob("*.py"):
                    if not any(skip in str(py_file) for skip in ['.backup', '__pycache__', 'test_']):
                        python_files.append(py_file)
        
        return python_files

    def parse_file(self, file_path: Path) -> Optional[ast.Module]:
        """Parse Python file into AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return ast.parse(content, filename=str(file_path))
        except Exception:
            return None

    def analyze_error_handling(self, tree: ast.Module, file_path: Path) -> None:
        """Analyze error handling patterns in a file"""
        
        class ErrorHandlingVisitor(ast.NodeVisitor):
            def __init__(self, auditor, file_path):
                self.auditor = auditor
                self.file_path = file_path
                self.current_function = None
                self.class_stack = []
            
            def visit_ClassDef(self, node):
                self.class_stack.append(node.name)
                self.generic_visit(node)
                self.class_stack.pop()
            
            def visit_FunctionDef(self, node):
                old_function = self.current_function
                self.current_function = node.name
                
                # Check for error handling decorators
                has_error_decorator = False
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name):
                        if decorator.id in self.auditor.error_decorators:
                            has_error_decorator = True
                            self.auditor.decorator_usage[decorator.id].append({
                                'file': str(self.file_path),
                                'function': node.name,
                                'class': self.class_stack[-1] if self.class_stack else None,
                                'line': node.lineno
                            })
                    elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                        if decorator.func.id in self.auditor.error_decorators:
                            has_error_decorator = True
                            self.auditor.decorator_usage[decorator.func.id].append({
                                'file': str(self.file_path),
                                'function': node.name,
                                'class': self.class_stack[-1] if self.class_stack else None,
                                'line': node.lineno,
                                'args': [ast.unparse(arg) for arg in decorator.args] if decorator.args else []
                            })
                
                # Analyze function body for manual error handling
                self.analyze_function_body(node, has_error_decorator)
                
                self.generic_visit(node)
                self.current_function = old_function
            
            def analyze_function_body(self, func_node, has_decorator):
                """Analyze function body for error handling patterns"""
                try_blocks = []
                error_raises = []
                return_patterns = []
                
                for node in ast.walk(func_node):
                    # Find try" / "except blocks
                    if isinstance(node, ast.Try):
                        try_blocks.append({
                            'line': node.lineno,
                            'handlers': len(node.handlers),
                            'exception_types': [
                                ast.unparse(handler.type) if handler.type else "Exception"
                                for handler in node.handlers
                            ],
                            'has_finally': bool(node.finalbody),
                            'has_else': bool(node.orelse)
                        })
                    
                    # Find raise statements
                    elif isinstance(node, ast.Raise):
                        if node.exc:
                            if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                                error_type = node.exc.func.id
                            elif isinstance(node.exc, ast.Name):
                                error_type = node.exc.id
                            else:
                                error_type = "Unknown"
                        else:
                            error_type = "Re-raise"
                        
                        error_raises.append({
                            'line': node.lineno,
                            'error_type': error_type
                        })
                    
                    # Find return statements in error contexts
                    elif isinstance(node, ast.Return) and node.value:
                        return_value = ast.unparse(node.value)
                        if any(pattern in return_value.lower() for pattern in ['error', 'false', 'none', 'success']):
                            return_patterns.append({
                                'line': node.lineno,
                                'pattern': return_value
                            })
                
                # Record patterns for this function
                function_info = {
                    'file': str(self.file_path),
                    'function': func_node.name,
                    'class': self.class_stack[-1] if self.class_stack else None,
                    'has_decorator': has_decorator,
                    'try_blocks': len(try_blocks),
                    'error_raises': len(error_raises),
                    'return_patterns': len(return_patterns),
                    'manual_handling': len(try_blocks) > 0 and not has_decorator
                }
                
                if try_blocks:
                    self.auditor.manual_handling['try_catch'].append(function_info)
                
                for error_raise in error_raises:
                    self.auditor.error_types[error_raise['error_type']].append({
                        **function_info,
                        'line': error_raise['line']
                    })
                
                for return_pattern in return_patterns:
                    self.auditor.return_patterns[return_pattern['pattern']].append({
                        **function_info,
                        'line': return_pattern['line']
                    })
        
        visitor = ErrorHandlingVisitor(self, file_path)
        visitor.visit(tree)

    def find_inconsistent_patterns(self) -> Dict[str, Any]:
        """Find inconsistent error handling patterns"""
        inconsistencies = {}
        
        # Functions with both decorators and manual handling
        mixed_functions = []
        for pattern_type, functions in self.manual_handling.items():
            for func in functions:
                if func['has_decorator'] and func['manual_handling']:
                    mixed_functions.append(func)
        
        if mixed_functions:
            inconsistencies['mixed_handling'] = {
                'description': 'Functions using both @handle_errors and manual try" / "catch',
                'functions': mixed_functions,
                'recommendation': 'Choose either decorator or manual handling consistently'
            }
        
        # Inconsistent error types
        custom_errors = [err_type for err_type in self.error_types.keys() 
                        if err_type not in ['Exception', 'ValueError', 'TypeError', 'KeyError', 'AttributeError']]
        
        mao_errors_used = [err for err in custom_errors if err in self.mao_error_types]
        non_mao_errors = [err for err in custom_errors if err not in self.mao_error_types and err != "Unknown"]
        
        if non_mao_errors:
            inconsistencies['non_standard_errors'] = {
                'description': 'Custom error types not following MAO standards',
                'error_types': non_mao_errors,
                'mao_standard_types': self.mao_error_types,
                'recommendation': 'Use standardized MAO error types'
            }
        
        # Inconsistent return patterns
        return_pattern_counts = Counter()
        for pattern, usages in self.return_patterns.items():
            return_pattern_counts[pattern] += len(usages)
        
        if len(return_pattern_counts) > 3:  # Too many different patterns
            inconsistencies['varied_return_patterns'] = {
                'description': 'Too many different error return patterns',
                'patterns': dict(return_pattern_counts.most_common(10)),
                'recommendation': 'Standardize error return format (suggest dict with success" / "error keys)'
            }
        
        return inconsistencies

    def calculate_error_handling_score(self) -> float:
        """Calculate error handling consistency score (0-100)"""
        total_functions = 0
        well_handled_functions = 0
        
        # Count functions with error handling
        decorator_functions = sum(len(funcs) for funcs in self.decorator_usage.values())
        manual_functions = sum(len(funcs) for funcs in self.manual_handling.values())
        
        # Get unique functions (avoid double counting)
        unique_functions = set()
        for funcs in self.decorator_usage.values():
            for func in funcs:
                unique_functions.add(f"{func['file']}:{func['function']}")
        
        for funcs in self.manual_handling.values():
            for func in funcs:
                unique_functions.add(f"{func['file']}:{func['function']}")
        
        total_functions = len(unique_functions)
        
        if total_functions == 0:
            return 50  # No error handling found
        
        # Score based on consistency
        inconsistencies = self.find_inconsistent_patterns()
        penalty = len(inconsistencies) * 15  # 15 points off per inconsistency type
        
        # Bonus for using MAO error types
        mao_error_usage = sum(1 for err_type in self.error_types.keys() if err_type in self.mao_error_types)
        total_error_usage = len(self.error_types)
        
        if total_error_usage > 0:
            mao_bonus = (mao_error_usage / total_error_usage) * 20
        else:
            mao_bonus = 0
        
        # Base score
        decorator_ratio = decorator_functions " / " total_functions if total_functions > 0 else 0
        base_score = 70 + (decorator_ratio * 30)  # Prefer decorators
        
        final_score = base_score + mao_bonus - penalty
        return max(0, min(100, final_score))

    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        inconsistencies = self.find_inconsistent_patterns()
        
        if 'mixed_handling' in inconsistencies:
            recommendations.append("🔧 Remove manual try" / "catch from functions already using @handle_errors decorator")
        
        if 'non_standard_errors' in inconsistencies:
            recommendations.append("📚 Standardize on MAO error types (APIError, ValidationError, etc.)")
        
        if 'varied_return_patterns' in inconsistencies:
            recommendations.append("🔄 Standardize error return patterns across functions")
        
        # General recommendations
        total_decorator_usage = sum(len(funcs) for funcs in self.decorator_usage.values())
        total_manual_usage = sum(len(funcs) for funcs in self.manual_handling.values())
        
        if total_manual_usage > total_decorator_usage:
            recommendations.append("🎯 Increase usage of @handle_errors decorator for consistency")
        
        recommendations.extend([
            "📋 Document error handling standards and patterns",
            "🧪 Add linting rules for error handling consistency",
            "🔍 Consider centralized error logging configuration"
        ])
        
        return recommendations

    def run_audit(self) -> Dict[str, Any]:
        """Run complete error handling audit"""
        print("🔍 Starting MAO Error Handling Audit...")
        
        python_files = self.find_python_files()
        print(f"📁 Found {len(python_files)} Python files to analyze")
        
        # Analyze each file
        parsed_count = 0
        for file_path in python_files:
            tree = self.parse_file(file_path)
            if tree:
                self.analyze_error_handling(tree, file_path)
                parsed_count += 1
        
        # Calculate metrics
        inconsistencies = self.find_inconsistent_patterns()
        score = self.calculate_error_handling_score()
        
        # Compile results
        results = {
            'summary': {
                'files_analyzed': len(python_files),
                'files_parsed': parsed_count,
                'functions_with_decorators': sum(len(funcs) for funcs in self.decorator_usage.values()),
                'functions_with_manual_handling': sum(len(funcs) for funcs in self.manual_handling.values()),
                'error_types_found': len(self.error_types),
                'return_patterns_found': len(self.return_patterns),
                'inconsistency_types': len(inconsistencies),
                'error_handling_score': score
            },
            'decorator_usage': dict(self.decorator_usage),
            'manual_handling': dict(self.manual_handling),
            'error_types': dict(self.error_types),
            'return_patterns': dict(self.return_patterns),
            'inconsistencies': inconsistencies,
            'recommendations': self.generate_recommendations()
        }
        
        return results

    def generate_report(self, output_file: str = "error_handling_audit_report.json") -> None:
        """Generate detailed audit report"""
        import json
        
        results = self.run_audit()
        
        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Print summary
        print(Path(r"\n") + "="*60)
        print("📊 MAO ERROR HANDLING AUDIT RESULTS")
        print("="*60)
        
        summary = results['summary']
        print(f"📁 Files analyzed: {summary['files_analyzed']}")
        print(f"✅ Files parsed: {summary['files_parsed']}")
        print(f"🎯 Functions with @handle_errors: {summary['functions_with_decorators']}")
        print(f"🔧 Functions with manual try" / "catch: {summary['functions_with_manual_handling']}")
        print(f"🚨 Error types found: {summary['error_types_found']}")
        print(f"📤 Return patterns found: {summary['return_patterns_found']}")
        print(f"⚠️ Inconsistency types: {summary['inconsistency_types']}")
        print(f"📊 Error Handling Score: {summary['error_handling_score']:.1f}" / "100")
        
        # Show decorator usage
        if results['decorator_usage']:
            print(fPath(r"\n🎯 DECORATOR USAGE:"))
            for decorator, usages in results['decorator_usage'].items():
                print(f"  @{decorator}: {len(usages)} functions")
        
        # Show error types
        if results['error_types']:
            print(fPath(r"\n🚨 ERROR TYPES:"))
            for error_type, usages in list(results['error_types'].items())[:5]:
                print(f"  {error_type}: {len(usages)} usages")
        
        # Show inconsistencies
        if results['inconsistencies']:
            print(fPath(r"\n⚠️ INCONSISTENCIES:"))
            for inconsistency_type, details in results['inconsistencies'].items():
                print(f"  📦 {inconsistency_type}: {details['description']}")
        
        print(fPath(r"\n💡 RECOMMENDATIONS:"))
        for rec in results['recommendations']:
            print(f"  {rec}")
        
        print(fPath(r"\n📄 Full report saved to: {output_file}"))
        print("="*60)

def main():
    """Run the error handling audit"""
    auditor = ErrorHandlingAuditor()
    auditor.generate_report()

if __name__ == "__main__":
    main() 