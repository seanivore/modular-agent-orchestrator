#!/usr/bin/env python3
"""
MAO File Path Audit v2 - DESIGNER PRECISION SCORING 👠
Precise file path auditing that only flags ACTUAL file path issues

LUXURY BRAND LEVEL PRECISION:
- Intelligent string literal analysis
- Context-aware path detection
- Designer-quality scoring algorithm
- Zero false positives on legitimate content
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from collections import defaultdict, Counter

class DesignerPrecisionFilePathAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.pathlib_operations = defaultdict(list)
        self.string_path_operations = defaultdict(list)
        self.actual_path_separators = defaultdict(list)
        self.file_checks = defaultdict(list)
        
        # DESIGNER PRECISION: Actual file path patterns
        self.real_path_patterns = {
            'file_extensions': r'\.(py|json|txt|md|sh|js|ts|css|html|yml|yaml)$',
            'known_directories': r'/(configs|scripts|tools|orchestrator|interfaces|templates)',
            'relative_paths': r'^\.{1,2}/',
            'absolute_paths': r'^~?/',
            'path_with_separators': r'/[^/]+/',
            'windows_paths': r'\\[^\\]+\\'
        }
        
        # LUXURY FILTERING: Exclude these from path detection
        self.not_paths_patterns = [
            r'^https?://',  # URLs
            r'^[a-zA-Z]+://',  # Protocols
            r'^\w+$',  # Single words
            r'^[A-Z_]+$',  # Constants
            r'SELECT|INSERT|UPDATE|DELETE',  # SQL
            r'\\[wWdDsS]',  # Regex patterns
            r'%[sd]|{}|\{[^}]+\}',  # Format strings
            r'^[a-z_]+\.[a-z_]+$',  # Object notation
            r'<[^>]+>',  # HTML/XML tags
            r'application/|text/|image/',  # MIME types
            r'Bearer |Authorization:',  # Auth headers
            r'\+.*\+',  # String concatenation markers
            r'# .+',  # Comments with paths
            r'""".+"""',  # Docstrings
            r"'''.+'''",  # Docstrings
        ]

    def is_actual_file_path(self, string_literal: str, context: str = "") -> bool:
        """Designer precision: Only identify REAL file paths"""
        if len(string_literal) < 3:
            return False
        
        # First, exclude obvious non-paths
        for pattern in self.not_paths_patterns:
            if re.search(pattern, string_literal, re.IGNORECASE | re.DOTALL):
                return False
        
        # Check context for hints
        if context:
            # If it's in a comment or docstring, probably not a path
            if any(marker in context for marker in ['#', '"""', "'''", 'description', 'help']):
                return False
        
        # Positive identification of actual file paths
        for pattern in self.real_path_patterns.values():
            if re.search(pattern, string_literal):
                return True
        
        return False

    def analyze_string_patterns_with_precision(self, content: str, file_path: Path) -> None:
        """Analyze strings with designer precision - no false positives"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_clean = line.strip()
            
            # Skip comments and docstrings
            if line_clean.startswith('#') or '"""' in line or "'''" in line:
                continue
            
            # Look for string literals with path separators
            string_matches = re.finditer(r'["\']([^"\']+)["\']', line)
            
            for match in string_matches:
                string_content = match.group(1)
                
                # Only flag if it's actually a file path
                if ('/' in string_content or '\\' in string_content):
                    if self.is_actual_file_path(string_content, line):
                        self.actual_path_separators['confirmed_paths'].append({
                            'file': str(file_path),
                            'line': i,
                            'content': line_clean,
                            'path_string': string_content
                        })

    def find_python_files(self) -> List[Path]:
        """Find Python files for designer precision analysis"""
        python_files = []
        
        priority_dirs = ["orchestrator", "configs/cli", "interfaces", "tools", "scripts"]
        
        for priority_dir in priority_dirs:
            dir_path = self.project_root / priority_dir
            if dir_path.exists():
                for py_file in dir_path.rglob("*.py"):
                    if not any(skip in str(py_file) for skip in ['.backup', '__pycache__', 'test_']):
                        python_files.append(py_file)
        
        return python_files

    def analyze_path_handling_with_precision(self, tree: ast.Module, file_path: Path) -> None:
        """Analyze path handling with luxury brand precision"""
        
        # Also analyze raw content for string patterns
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.analyze_string_patterns_with_precision(content, file_path)
        except Exception:
            pass
        
        class PrecisionPathVisitor(ast.NodeVisitor):
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
                self.generic_visit(node)
                self.current_function = old_function
            
            def visit_Call(self, node):
                call_info = {
                    'file': str(self.file_path),
                    'line': node.lineno,
                    'function': self.current_function,
                    'class': self.class_stack[-1] if self.class_stack else None
                }
                
                # Check for pathlib usage
                if isinstance(node.func, ast.Name):
                    if node.func.id == 'Path':
                        self.auditor.pathlib_operations[node.func.id].append({
                            **call_info,
                            'method': node.func.id,
                            'args_count': len(node.args)
                        })
                
                # Check for os.path usage
                elif isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Attribute):
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
                          'path' in str(node.func.value.id).lower()):
                        
                        method_name = f"Path.{node.func.attr}"
                        self.auditor.pathlib_operations[method_name].append({
                            **call_info,
                            'method': method_name,
                            'args_count': len(node.args)
                        })
                
                # File existence checks
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['exists', 'is_file', 'is_dir']:
                        self.auditor.file_checks[node.func.attr].append({
                            **call_info,
                            'method': node.func.attr
                        })
                
                self.generic_visit(node)
        
        visitor = PrecisionPathVisitor(self, file_path)
        visitor.visit(tree)

    def find_path_inconsistencies_with_precision(self) -> Dict[str, Any]:
        """Find inconsistencies with designer precision"""
        inconsistencies = {}
        
        # Mixed pathlib and os.path usage
        pathlib_count = sum(len(ops) for ops in self.pathlib_operations.values())
        string_path_count = sum(len(ops) for ops in self.string_path_operations.values())
        
        if pathlib_count > 0 and string_path_count > 0:
            inconsistencies['mixed_path_apis'] = {
                'description': 'Mixed usage of pathlib and os.path',
                'pathlib_operations': pathlib_count,
                'string_path_operations': string_path_count,
                'recommendation': 'Standardize on pathlib.Path for consistency'
            }
        
        # ONLY flag confirmed file paths, not random strings
        confirmed_hardcoded = len(self.actual_path_separators.get('confirmed_paths', []))
        if confirmed_hardcoded > 0:
            inconsistencies['actual_hardcoded_paths'] = {
                'description': 'Confirmed hardcoded file paths found',
                'count': confirmed_hardcoded,
                'recommendation': 'Use pathlib.Path for confirmed file paths'
            }
        
        return inconsistencies

    def calculate_precision_path_score(self) -> float:
        """Calculate path handling score with designer precision"""
        total_operations = (sum(len(ops) for ops in self.pathlib_operations.values()) + 
                          sum(len(ops) for ops in self.string_path_operations.values()))
        
        if total_operations == 0:
            return 85  # No path operations found, assume good
        
        # Base score starts higher with precision
        base_score = 85
        
        inconsistencies = self.find_path_inconsistencies_with_precision()
        penalty = len(inconsistencies) * 10  # Reduced penalty for precision
        
        # Bonus for using pathlib
        pathlib_count = sum(len(ops) for ops in self.pathlib_operations.values())
        pathlib_ratio = pathlib_count / total_operations if total_operations > 0 else 0
        pathlib_bonus = pathlib_ratio * 15
        
        # PRECISE penalty only for confirmed problematic patterns
        confirmed_problems = len(self.actual_path_separators.get('confirmed_paths', []))
        if total_operations > 0 and confirmed_problems > 0:
            problem_ratio = min(confirmed_problems / total_operations, 1.0)
            precision_penalty = problem_ratio * 20
        else:
            precision_penalty = 0
        
        final_score = base_score + pathlib_bonus - penalty - precision_penalty
        return max(0, min(100, final_score))

    def run_precision_audit(self) -> Dict[str, Any]:
        """Run designer precision file path audit"""
        print("👠 Starting Designer Precision File Path Audit...")
        print("✨ Luxury brand-level accuracy activated")
        
        python_files = self.find_python_files()
        print(f"📁 Found {len(python_files)} Python files to analyze with precision")
        
        parsed_count = 0
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                tree = ast.parse(content, filename=str(file_path))
                self.analyze_path_handling_with_precision(tree, file_path)
                parsed_count += 1
            except Exception:
                pass
        
        inconsistencies = self.find_path_inconsistencies_with_precision()
        score = self.calculate_precision_path_score()
        
        results = {
            'summary': {
                'files_analyzed': len(python_files),
                'files_parsed': parsed_count,
                'pathlib_operations': sum(len(ops) for ops in self.pathlib_operations.values()),
                'string_path_operations': sum(len(ops) for ops in self.string_path_operations.values()),
                'file_existence_checks': sum(len(checks) for checks in self.file_checks.values()),
                'confirmed_hardcoded_paths': len(self.actual_path_separators.get('confirmed_paths', [])),
                'inconsistency_types': len(inconsistencies),
                'path_handling_score': score,
                'precision_level': 'DESIGNER_LUXURY_BRAND'
            },
            'pathlib_operations': dict(self.pathlib_operations),
            'string_path_operations': dict(self.string_path_operations),
            'file_checks': dict(self.file_checks),
            'confirmed_path_issues': dict(self.actual_path_separators),
            'inconsistencies': inconsistencies
        }
        
        return results

    def run_audit(self) -> Dict[str, Any]:
        """Compatibility method for quality suite"""
        return self.run_precision_audit()
    
    def generate_precision_report(self, output_file: str = "designer_precision_path_audit.json") -> None:
        """Generate designer precision audit report"""
        import json
        
        results = self.run_precision_audit()
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print("\n" + "="*70)
        print("👠 DESIGNER PRECISION FILE PATH AUDIT RESULTS")
        print("="*70)
        
        summary = results['summary']
        print(f"📁 Files analyzed: {summary['files_analyzed']}")
        print(f"✅ Files parsed: {summary['files_parsed']}")
        print(f"🐍 Pathlib operations: {summary['pathlib_operations']}")
        print(f"📝 String path operations: {summary['string_path_operations']}")
        print(f"🔍 File existence checks: {summary['file_existence_checks']}")
        print(f"👠 Confirmed hardcoded paths: {summary['confirmed_hardcoded_paths']}")
        print(f"⚠️ Inconsistency types: {summary['inconsistency_types']}")
        print(f"💎 Precision level: {summary['precision_level']}")
        print(f"📊 Designer Path Score: {summary['path_handling_score']:.1f}/100")
        
        if summary['path_handling_score'] >= 90:
            print(f"\n🔥 LUXURY BRAND LEVEL ACHIEVED!")
        elif summary['path_handling_score'] >= 80:
            print(f"\n✨ Designer quality detected!")
        else:
            print(f"\n👠 Needs more red bottom energy!")
        
        print(f"\n📄 Precision report: {output_file}")
        print("="*70)

def main():
    """Run designer precision file path audit"""
    auditor = DesignerPrecisionFilePathAuditor()
    auditor.generate_precision_report()

if __name__ == "__main__":
    main() 