#!/usr/bin/env python3
"""
MAO File Path Handling Audit Script
Finds inconsistencies in file path handling patterns across the codebase

This script analyzes:
1. Path object usage vs string concatenation
2. Absolute vs relative path patterns
3. Cross-platform compatibility issues
4. Path separator inconsistencies
5. File existence checking patterns
6. Path joining methods
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from collections import defaultdict, Counter

class FilePathAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.path_operations = defaultdict(list)
        self.string_path_operations = defaultdict(list)
        self.pathlib_operations = defaultdict(list)
        self.path_separators = defaultdict(list)
        self.file_checks = defaultdict(list)
        
        # Path-related methods and functions to track
        self.pathlib_methods = {
            'Path', 'PurePath', 'WindowsPath', 'PosixPath'
        }
        
        self.string_path_functions = {
            'os.path.join', 'os.path.exists', 'os.path.dirname', 
            'os.path.basename', 'os.path.abspath', 'os.path.relpath'
        }
        
        # Common path patterns to look for
        self.problematic_patterns = {
            'hardcoded_separators': r'["\'][^"\']*[/\\][^"\']*["\']',
            'concatenated_paths': r'\+.*["\'][^"\']*[/\\]',
            'format_paths': r'\.format\(.*[/\\]',
            'fstring_paths': r'f["\'][^"\']*\{.*\}[^"\']*[/\\]'
        }

    def find_python_files(self) -> List[Path]:
        """Find Python files to analyze for path handling"""
        python_files = []
        
        # Focus on directories likely to have file operations
        priority_dirs = ["orchestrator", "configs/cli", "interfaces", "tools", "scripts"]
        
        for priority_dir in priority_dirs:
            dir_path = self.project_root / priority_dir
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

    def analyze_path_handling(self, tree: ast.Module, file_path: Path) -> None:
        """Analyze path handling patterns in a file"""
        
        # Also analyze raw content for string patterns
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.analyze_string_patterns(content, file_path)
        except Exception:
            pass
        
        class PathHandlingVisitor(ast.NodeVisitor):
            def __init__(self, auditor, file_path):
                self.auditor = auditor
                self.file_path = file_path
                self.current_function = None
                self.class_stack = []
                self.imported_modules = set()
                self.imported_names = set()
            
            def visit_ClassDef(self, node):
                self.class_stack.append(node.name)
                self.generic_visit(node)
                self.class_stack.pop()
            
            def visit_FunctionDef(self, node):
                old_function = self.current_function
                self.current_function = node.name
                self.generic_visit(node)
                self.current_function = old_function
            
            def visit_Import(self, node):
                for alias in node.names:
                    self.imported_modules.add(alias.name)
                    if alias.asname:
                        self.imported_names.add(alias.asname)
                    else:
                        self.imported_names.add(alias.name)
            
            def visit_ImportFrom(self, node):
                if node.module:
                    for alias in node.names:
                        full_name = f"{node.module}.{alias.name}"
                        self.imported_modules.add(full_name)
                        if alias.asname:
                            self.imported_names.add(alias.asname)
                        else:
                            self.imported_names.add(alias.name)
            
            def visit_Call(self, node):
                # Analyze function calls related to path handling
                call_info = {
                    'file': str(self.file_path),
                    'line': node.lineno,
                    'function': self.current_function,
                    'class': self.class_stack[-1] if self.class_stack else None
                }
                
                # Check for pathlib usage
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.auditor.pathlib_methods:
                        self.auditor.pathlib_operations[node.func.id].append({
                            **call_info,
                            'method': node.func.id,
                            'args_count': len(node.args)
                        })
                
                # Check for os.path usage
                elif isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Attribute):
                        # os.path.method pattern
                        if (isinstance(node.func.value.value, ast.Name) and 
                            node.func.value.value.id == 'os' and 
                            node.func.value.attr == 'path'):
                            
                            method_name = f"os.path.{node.func.attr}"
                            self.auditor.string_path_operations[method_name].append({
                                **call_info,
                                'method': method_name,
                                'args_count': len(node.args)
                            })
                    
                    # Path object method calls
                    elif (isinstance(node.func.value, ast.Name) and 
                          any(path_type in str(node.func.value.id) for path_type in ['path', 'Path'])):
                        
                        method_name = f"Path.{node.func.attr}"
                        self.auditor.pathlib_operations[method_name].append({
                            **call_info,
                            'method': method_name,
                            'args_count': len(node.args)
                        })
                
                # Check for file existence checks
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['exists', 'is_file', 'is_dir']:
                        self.auditor.file_checks[node.func.attr].append({
                            **call_info,
                            'method': node.func.attr
                        })
                
                self.generic_visit(node)
            
            def visit_BinOp(self, node):
                # Check for string concatenation that might be building paths
                if isinstance(node.op, ast.Add):
                    # Look for patterns like string + "/" + string
                    left_str = self.is_string_literal(node.left)
                    right_str = self.is_string_literal(node.right)
                    
                    if (left_str and ('/' in left_str or '\\' in left_str)) or \
                       (right_str and ('/' in right_str or '\\' in right_str)):
                        
                        self.auditor.string_path_operations['concatenation'].append({
                            'file': str(self.file_path),
                            'line': node.lineno,
                            'function': self.current_function,
                            'class': self.class_stack[-1] if self.class_stack else None,
                            'method': 'string_concatenation'
                        })
                
                self.generic_visit(node)
            
            def is_string_literal(self, node):
                """Check if node is a string literal and return its value"""
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    return node.value
                return None
        
        visitor = PathHandlingVisitor(self, file_path)
        visitor.visit(tree)

    def analyze_string_patterns(self, content: str, file_path: Path) -> None:
        """Analyze string patterns that might indicate path handling issues"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Look for hardcoded path separators
            if re.search(r'["\'][^"\']*[/\\][^"\']*["\']', line):
                self.path_separators['hardcoded'].append({
                    'file': str(file_path),
                    'line': i,
                    'content': line.strip()
                })
            
            # Look for path concatenation
            if '+' in line and ('/' in line or '\\' in line):
                self.path_separators['concatenated'].append({
                    'file': str(file_path),
                    'line': i,
                    'content': line.strip()
                })

    def find_path_inconsistencies(self) -> Dict[str, Any]:
        """Find inconsistent path handling patterns"""
        inconsistencies = {}
        
        # Mixed pathlib and os.path usage
        pathlib_count = sum(len(ops) for ops in self.pathlib_operations.values())
        string_path_count = sum(len(ops) for ops in self.string_path_operations.values())
        
        if pathlib_count > 0 and string_path_count > 0:
            inconsistencies['mixed_path_apis'] = {
                'description': 'Mixed usage of pathlib and os.path',
                'pathlib_operations': pathlib_count,
                'string_path_operations': string_path_count,
                'recommendation': 'Standardize on pathlib.Path for consistency and cross-platform compatibility'
            }
        
        # Hardcoded path separators
        hardcoded_separators = len(self.path_separators.get('hardcoded', []))
        if hardcoded_separators > 0:
            inconsistencies['hardcoded_separators'] = {
                'description': 'Hardcoded path separators found',
                'count': hardcoded_separators,
                'recommendation': 'Use pathlib.Path or os.path.join for cross-platform compatibility'
            }
        
        # String concatenation for paths
        concatenated_paths = len(self.string_path_operations.get('concatenation', []))
        if concatenated_paths > 0:
            inconsistencies['string_concatenation'] = {
                'description': 'String concatenation used for path building',
                'count': concatenated_paths,
                'recommendation': 'Use pathlib.Path / operator or os.path.join'
            }
        
        # Multiple file existence check methods
        check_methods = list(self.file_checks.keys())
        if len(check_methods) > 2:
            inconsistencies['varied_existence_checks'] = {
                'description': 'Multiple different file existence check methods',
                'methods': {method: len(checks) for method, checks in self.file_checks.items()},
                'recommendation': 'Standardize on pathlib.Path.exists() or Path.is_file()/is_dir()'
            }
        
        return inconsistencies

    def calculate_path_score(self) -> float:
        """Calculate path handling consistency score (0-100)"""
        total_operations = (sum(len(ops) for ops in self.pathlib_operations.values()) + 
                          sum(len(ops) for ops in self.string_path_operations.values()))
        
        if total_operations == 0:
            return 50  # No path operations found
        
        # Base score
        base_score = 70
        
        inconsistencies = self.find_path_inconsistencies()
        penalty = len(inconsistencies) * 15  # 15 points off per inconsistency type
        
        # Bonus for using pathlib
        pathlib_count = sum(len(ops) for ops in self.pathlib_operations.values())
        if total_operations > 0:
            pathlib_ratio = pathlib_count / total_operations
            pathlib_bonus = pathlib_ratio * 25  # Strong preference for pathlib
        else:
            pathlib_bonus = 0
        
        # Penalty for problematic patterns
        problematic_count = (len(self.path_separators.get('hardcoded', [])) + 
                           len(self.string_path_operations.get('concatenation', [])))
        if total_operations > 0:
            problematic_ratio = problematic_count / total_operations
            problematic_penalty = problematic_ratio * 30
        else:
            problematic_penalty = 0
        
        final_score = base_score + pathlib_bonus - penalty - problematic_penalty
        return max(0, min(100, final_score))

    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        inconsistencies = self.find_path_inconsistencies()
        
        if 'mixed_path_apis' in inconsistencies:
            recommendations.append("🔧 Standardize on pathlib.Path for all file operations")
        
        if 'hardcoded_separators' in inconsistencies:
            recommendations.append("🛤️ Replace hardcoded path separators with pathlib.Path / operator")
        
        if 'string_concatenation' in inconsistencies:
            recommendations.append("➕ Replace string concatenation with proper path joining methods")
        
        if 'varied_existence_checks' in inconsistencies:
            recommendations.append("📋 Standardize file existence checking methods")
        
        # General recommendations
        total_operations = (sum(len(ops) for ops in self.pathlib_operations.values()) + 
                          sum(len(ops) for ops in self.string_path_operations.values()))
        
        if total_operations > 0:
            recommendations.extend([
                "🌍 Ensure cross-platform compatibility in path handling",
                "📁 Use relative paths where appropriate for portability",
                "🧪 Add path handling tests for different operating systems",
                "📚 Document path handling conventions and standards"
            ])
        
        return recommendations

    def run_audit(self) -> Dict[str, Any]:
        """Run complete file path handling audit"""
        print("🔍 Starting MAO File Path Handling Audit...")
        
        python_files = self.find_python_files()
        print(f"📁 Found {len(python_files)} Python files to analyze")
        
        # Analyze each file
        parsed_count = 0
        for file_path in python_files:
            tree = self.parse_file(file_path)
            if tree:
                self.analyze_path_handling(tree, file_path)
                parsed_count += 1
        
        # Calculate metrics
        inconsistencies = self.find_path_inconsistencies()
        score = self.calculate_path_score()
        
        # Compile results
        results = {
            'summary': {
                'files_analyzed': len(python_files),
                'files_parsed': parsed_count,
                'pathlib_operations': sum(len(ops) for ops in self.pathlib_operations.values()),
                'string_path_operations': sum(len(ops) for ops in self.string_path_operations.values()),
                'file_existence_checks': sum(len(checks) for checks in self.file_checks.values()),
                'hardcoded_separators': len(self.path_separators.get('hardcoded', [])),
                'inconsistency_types': len(inconsistencies),
                'path_handling_score': score
            },
            'pathlib_operations': dict(self.pathlib_operations),
            'string_path_operations': dict(self.string_path_operations),
            'file_checks': dict(self.file_checks),
            'path_separators': dict(self.path_separators),
            'inconsistencies': inconsistencies,
            'recommendations': self.generate_recommendations()
        }
        
        return results

    def generate_report(self, output_file: str = "file_path_audit_report.json") -> None:
        """Generate detailed audit report"""
        import json
        
        results = self.run_audit()
        
        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 MAO FILE PATH HANDLING AUDIT RESULTS")
        print("="*60)
        
        summary = results['summary']
        print(f"📁 Files analyzed: {summary['files_analyzed']}")
        print(f"✅ Files parsed: {summary['files_parsed']}")
        print(f"🐍 Pathlib operations: {summary['pathlib_operations']}")
        print(f"📝 String path operations: {summary['string_path_operations']}")
        print(f"🔍 File existence checks: {summary['file_existence_checks']}")
        print(f"🛤️ Hardcoded separators: {summary['hardcoded_separators']}")
        print(f"⚠️ Inconsistency types: {summary['inconsistency_types']}")
        print(f"📊 Path Handling Score: {summary['path_handling_score']:.1f}/100")
        
        # Show pathlib operations
        if results['pathlib_operations']:
            print(f"\n🐍 PATHLIB OPERATIONS:")
            for operation, usages in results['pathlib_operations'].items():
                print(f"  {operation}: {len(usages)} usages")
        
        # Show string path operations
        if results['string_path_operations']:
            print(f"\n📝 STRING PATH OPERATIONS:")
            for operation, usages in results['string_path_operations'].items():
                print(f"  {operation}: {len(usages)} usages")
        
        # Show inconsistencies
        if results['inconsistencies']:
            print(f"\n⚠️ INCONSISTENCIES:")
            for inconsistency_type, details in results['inconsistencies'].items():
                print(f"  📦 {inconsistency_type}: {details['description']}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"  {rec}")
        
        print(f"\n📄 Full report saved to: {output_file}")
        print("="*60)

def main():
    """Run the file path handling audit"""
    auditor = FilePathAuditor()
    auditor.generate_report()

if __name__ == "__main__":
    main() 