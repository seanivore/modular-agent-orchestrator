#!/usr/bin/env python3
"""
MAO Import Audit Script - PRECISION VERSION
Analyzes import patterns and sys.path.append usage in ACTIVE codebase only

This precision version excludes:
- versioning/* files (old versions)
- test files with legacy patterns
- backup files

Focus on current active development for quality scoring.
"""

import os
import ast
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Any, Optional
import json

class PrecisionImportAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.sys_path_issues = []
        self.import_patterns = defaultdict(list)
        self.inconsistent_imports = defaultdict(lambda: defaultdict(list))
        self.other_issues = []
        
        # Files/directories to exclude from precision audit
        self.excluded_patterns = [
            'versioning/',           # All versioned files
            'v1/', 'v2/', 'v3/', 'v4/',  # Version directories
            '.backup',               # Backup files
            'node_modules/',         # JS dependencies
            '__pycache__/',          # Python cache
            'tests/typescript-terminal-playground/',  # External test code
            'sfa_v',                 # Versioned SFA files anywhere
        ]

    def should_exclude_file(self, file_path: Path) -> bool:
        """Check if file should be excluded from precision audit"""
        path_str = str(file_path)
        return any(pattern in path_str for pattern in self.excluded_patterns)

    def find_python_files(self) -> List[Path]:
        """Find all Python files, excluding versioned and backup files"""
        python_files = []
        
        for py_file in self.project_root.rglob("*.py"):
            if not self.should_exclude_file(py_file):
                python_files.append(py_file)
        
        return python_files

    def extract_imports_from_file(self, file_path: Path) -> Dict[str, Any]:
        """Extract import information from a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for structured import analysis
            tree = ast.parse(content)
            
            imports = {
                'regular_imports': [],      # import x
                'from_imports': [],         # from x import y
                'sys_path_appends': [],     # sys.path.append calls
                'import_lines': [],         # Raw import lines with numbers
            }
            
            # Extract imports using AST
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports['regular_imports'].append({
                            'module': alias.name,
                            'alias': alias.asname,
                            'line': node.lineno
                        })
                
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    names = [alias.name for alias in node.names]
                    imports['from_imports'].append({
                        'module': module,
                        'names': names,
                        'line': node.lineno
                    })
                
                # Check for sys.path.append calls
                elif isinstance(node, ast.Call):
                    if (isinstance(node.func, ast.Attribute) and
                        isinstance(node.func.value, ast.Attribute) and
                        isinstance(node.func.value.value, ast.Name) and
                        node.func.value.value.id == 'sys' and
                        node.func.value.attr == 'path' and
                        node.func.attr == 'append'):
                        
                        imports['sys_path_appends'].append({
                            'line': node.lineno,
                            'content': ast.get_source_segment(content, node) or 'sys.path.append(...)'
                        })
            
            # Also extract raw import lines for pattern analysis
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if (line.startswith('import ') or 
                    line.startswith('from ') or
                    'sys.path.append' in line):
                    imports['import_lines'].append({
                        'line_num': i,
                        'content': line
                    })
            
            return imports
            
        except Exception as e:
            return {'error': str(e)}

    def analyze_sys_path_usage(self, file_path: Path, imports: Dict) -> None:
        """Analyze sys.path.append usage patterns"""
        if 'sys_path_appends' in imports:
            for sys_path in imports['sys_path_appends']:
                # Look for corresponding imports that might need fixing
                related_imports = []
                for imp_line in imports['import_lines']:
                    if (imp_line['line_num'] > sys_path['line'] and 
                        imp_line['line_num'] < sys_path['line'] + 20):  # Within 20 lines
                        related_imports.append(imp_line['content'])
                
                self.sys_path_issues.append({
                    'file': str(file_path.relative_to(self.project_root)),
                    'line': sys_path['line'],
                    'content': sys_path['content'],
                    'related_imports': related_imports
                })

    def analyze_import_consistency(self, file_path: Path, imports: Dict) -> None:
        """Analyze import pattern consistency"""
        # Group by module for consistency analysis
        for from_import in imports.get('from_imports', []):
            module = from_import['module']
            names = ', '.join(sorted(from_import['names']))
            
            # Track import patterns
            key = f"{module} -> {names}"
            self.import_patterns[module].append({
                'pattern': key,
                'file': str(file_path.relative_to(self.project_root)),
                'names': from_import['names']
            })

    def find_import_inconsistencies(self) -> Dict[str, List]:
        """Find modules with inconsistent import patterns"""
        inconsistencies = {}
        
        for module, imports in self.import_patterns.items():
            if len(imports) < 2:  # Need at least 2 imports to check consistency
                continue
            
            # Group by import pattern
            pattern_groups = defaultdict(list)
            for imp in imports:
                pattern_groups[imp['pattern']].append(imp['file'])
            
            # If multiple patterns exist, it's inconsistent
            if len(pattern_groups) > 1:
                inconsistencies[module] = [
                    {
                        'pattern': pattern,
                        'files': files,
                        'count': len(files)
                    }
                    for pattern, files in pattern_groups.items()
                ]
        
        return inconsistencies

    def calculate_precision_score(self) -> float:
        """Calculate precision quality score focusing on active codebase"""
        total_files = len(self.find_python_files())
        if total_files == 0:
            return 100.0
        
        # Score components
        sys_path_penalty = min(50, len(self.sys_path_issues) * 5)  # Max 50 point penalty
        
        # Import consistency score
        inconsistency_count = sum(len(patterns) for patterns in self.find_import_inconsistencies().values())
        consistency_penalty = min(30, inconsistency_count * 2)  # Max 30 point penalty
        
        # Other issues penalty
        other_penalty = min(20, len(self.other_issues) * 3)  # Max 20 point penalty
        
        # Base score starts at 100, subtract penalties
        score = 100 - sys_path_penalty - consistency_penalty - other_penalty
        
        return max(0, score)

    def audit_file(self, file_path: Path) -> None:
        """Audit a single Python file"""
        imports = self.extract_imports_from_file(file_path)
        
        if 'error' in imports:
            self.other_issues.append({
                'file': str(file_path.relative_to(self.project_root)),
                'error': imports['error']
            })
            return
        
        # Analyze patterns
        self.analyze_sys_path_usage(file_path, imports)
        self.analyze_import_consistency(file_path, imports)

    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if self.sys_path_issues:
            recommendations.append("🔧 Replace remaining sys.path.append statements with clean dotted imports")
            recommendations.append("🧹 Remove unused 'import sys' statements after fixing sys.path.append")
        
        inconsistencies = self.find_import_inconsistencies()
        if inconsistencies:
            recommendations.append("📦 Standardize import patterns for commonly used modules")
            
        if len(self.sys_path_issues) == 0:
            recommendations.append("✨ EXCELLENT! No sys.path.append issues in active codebase!")
        
        if len(inconsistencies) <= 2:
            recommendations.append("👍 Import consistency is very good!")
        
        recommendations.append("🔄 Run tests after import changes to ensure functionality")
        
        return recommendations

    def run_audit(self) -> Dict[str, Any]:
        """Run complete precision import audit"""
        print("🎯 Starting MAO Import Precision Audit (Active Codebase Only)...")
        
        python_files = self.find_python_files()
        print(f"📁 Found {len(python_files)} active Python files to analyze")
        print(f"🚫 Excluding versioned and backup files for precision scoring")
        
        # Audit each file
        for file_path in python_files:
            self.audit_file(file_path)
        
        # Find inconsistencies
        inconsistencies = self.find_import_inconsistencies()
        
        # Calculate precision score
        precision_score = self.calculate_precision_score()
        
        # Compile results
        results = {
            'summary': {
                'total_files': len(python_files),
                'active_codebase_only': True,
                'sys_path_issues': len(self.sys_path_issues),
                'import_inconsistencies': len(inconsistencies),
                'other_issues': len(self.other_issues),
                'precision_score': precision_score
            },
            'sys_path_issues': self.sys_path_issues,
            'import_inconsistencies': inconsistencies,
            'other_issues': self.other_issues,
            'recommendations': self.generate_recommendations()
        }
        
        return results

    def generate_report(self, output_file: str = "import_precision_audit_report.json") -> None:
        """Generate precision audit report"""
        results = self.run_audit()
        
        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print("🎯 MAO IMPORT PRECISION AUDIT RESULTS")
        print("="*60)
        
        summary = results['summary']
        score = summary['precision_score']
        
        print(f"📊 Precision Score: {score:.1f}/100")
        print(f"📁 Active files analyzed: {summary['total_files']}")
        print(f"🚨 sys.path.append issues: {summary['sys_path_issues']}")
        print(f"⚠️ Import inconsistencies: {summary['import_inconsistencies']}")
        print(f"🔍 Other issues: {summary['other_issues']}")
        
        # Performance rating
        if score >= 90:
            print(f"\n🏆 LEXUS-LEVEL IMPORTS! Designer precision achieved!")
        elif score >= 80:
            print(f"\n✨ PREMIUM IMPORT QUALITY! Very strong patterns!")
        elif score >= 70:
            print(f"\n👍 GOOD IMPORT QUALITY! Room for fine-tuning!")
        else:
            print(f"\n🔧 IMPORT IMPROVEMENTS NEEDED!")
        
        # Show critical sys.path issues (active codebase only)
        if results['sys_path_issues']:
            print(f"\n🔧 ACTIVE CODEBASE SYS.PATH ISSUES:")
            for issue in results['sys_path_issues'][:10]:  # Top 10
                print(f"  📄 {issue['file']}:{issue['line']}")
                print(f"     {issue['content']}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"  {rec}")
        
        print(f"\n📄 Full report saved to: {output_file}")
        print("="*60)

def main():
    """Run the precision import audit"""
    auditor = PrecisionImportAuditor()
    auditor.generate_report()

if __name__ == "__main__":
    main() 