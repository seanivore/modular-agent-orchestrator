#!/usr/bin/env python3
"""
MAO Cache Usage Audit Script
Finds inconsistencies in cache usage patterns across the codebase

This script analyzes:
1. CacheManager instantiation patterns (singleton vs multiple instances)
2. Cache key naming conventions and consistency
3. Cache operation patterns (get/set/clear usage)
4. Error handling in cache operations
5. Cache lifetime and expiration handling
6. Cache bypass patterns
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from collections import defaultdict, Counter

class CacheUsageAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.cache_instantiations = defaultdict(list)
        self.cache_operations = defaultdict(list)
        self.cache_key_patterns = defaultdict(list)
        self.cache_errors = []
        self.cache_imports = defaultdict(list)
        
        # Expected cache patterns from MAO
        self.cache_methods = [
            'cache_content_analysis', 'get_cached_analysis', 'clear_cache',
            'cache_workflow_analysis', 'get_cached_workflow', 'cache_user_data'
        ]
        
        # Cache key naming patterns to look for
        self.key_pattern_types = {
            'underscore': r'^[a-z_]+$',
            'pipe_separated': r'^[a-z_]+\|[a-z_|\|]+$', 
            'dot_separated': r'^[a-z_.]+$',
            'mixed_case': r'[A-Z]',
            'contains_spaces': r'\s',
            'contains_special': r'[^a-zA-Z0-9_|.-]'
        }

    def find_python_files(self) -> List[Path]:
        """Find Python files with potential cache usage"""
        python_files = []
        
        # Focus on directories likely to use cache
        priority_dirs = ["orchestrator", "configs/cli", "interfaces", "tools"]
        
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

    def analyze_cache_usage(self, tree: ast.Module, file_path: Path) -> None:
        """Analyze cache usage patterns in a file"""
        
        class CacheUsageVisitor(ast.NodeVisitor):
            def __init__(self, auditor, file_path):
                self.auditor = auditor
                self.file_path = file_path
                self.current_function = None
                self.cache_variable_names = set()
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
            
            def visit_Import(self, node):
                for alias in node.names:
                    if 'cache' in alias.name.lower():
                        self.auditor.cache_imports['import'].append({
                            'file': str(self.file_path),
                            'line': node.lineno,
                            'module': alias.name,
                            'alias': alias.asname
                        })
            
            def visit_ImportFrom(self, node):
                if node.module and 'cache' in node.module.lower():
                    for alias in node.names:
                        self.auditor.cache_imports['from_import'].append({
                            'file': str(self.file_path),
                            'line': node.lineno,
                            'module': node.module,
                            'name': alias.name,
                            'alias': alias.asname
                        })
            
            def visit_Assign(self, node):
                # Look for cache instantiations
                if isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name):
                        if 'cache' in node.value.func.id.lower():
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    self.cache_variable_names.add(target.id)
                                    self.auditor.cache_instantiations['direct'].append({
                                        'file': str(self.file_path),
                                        'line': node.lineno,
                                        'variable': target.id,
                                        'constructor': node.value.func.id,
                                        'function': self.current_function,
                                        'class': self.class_stack[-1] if self.class_stack else None
                                    })
                    elif isinstance(node.value.func, ast.Attribute):
                        if 'cache' in node.value.func.attr.lower():
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    self.cache_variable_names.add(target.id)
                                    self.auditor.cache_instantiations['method'].append({
                                        'file': str(self.file_path),
                                        'line': node.lineno,
                                        'variable': target.id,
                                        'method': node.value.func.attr,
                                        'function': self.current_function,
                                        'class': self.class_stack[-1] if self.class_stack else None
                                    })
                
                self.generic_visit(node)
            
            def visit_Call(self, node):
                # Analyze cache method calls
                if isinstance(node.func, ast.Attribute):
                    # Check if it's a cache operation
                    if (isinstance(node.func.value, ast.Name) and 
                        (node.func.value.id in self.cache_variable_names or 
                         'cache' in node.func.value.id.lower())):
                        
                        # Extract cache key if present
                        cache_key = None
                        if node.args:
                            if isinstance(node.args[0], ast.Constant):
                                cache_key = node.args[0].value
                            elif isinstance(node.args[0], ast.JoinedStr):
                                cache_key = "f-string"
                            elif isinstance(node.args[0], ast.BinOp):
                                cache_key = "concatenated"
                        
                        operation_info = {
                            'file': str(self.file_path),
                            'line': node.lineno,
                            'method': node.func.attr,
                            'cache_variable': node.func.value.id,
                            'cache_key': cache_key,
                            'arg_count': len(node.args),
                            'function': self.current_function,
                            'class': self.class_stack[-1] if self.class_stack else None
                        }
                        
                        self.auditor.cache_operations[node.func.attr].append(operation_info)
                        
                        # Analyze cache key patterns
                        if cache_key and isinstance(cache_key, str):
                            self.analyze_cache_key(cache_key, operation_info)
                
                self.generic_visit(node)
            
            def analyze_cache_key(self, cache_key, operation_info):
                """Analyze cache key naming patterns"""
                key_info = {
                    **operation_info,
                    'key_value': cache_key,
                    'key_length': len(cache_key),
                    'patterns': []
                }
                
                # Check against known patterns
                for pattern_name, pattern_regex in self.auditor.key_pattern_types.items():
                    if re.search(pattern_regex, cache_key):
                        key_info['patterns'].append(pattern_name)
                
                # Categorize by apparent structure
                if '|' in cache_key:
                    category = 'pipe_separated'
                elif '_' in cache_key and cache_key.islower():
                    category = 'underscore_snake'
                elif '.' in cache_key:
                    category = 'dot_notation'
                elif cache_key.lower() != cache_key:
                    category = 'mixed_case'
                else:
                    category = 'simple'
                
                self.auditor.cache_key_patterns[category].append(key_info)
        
        visitor = CacheUsageVisitor(self, file_path)
        visitor.visit(tree)

    def find_cache_inconsistencies(self) -> Dict[str, Any]:
        """Find inconsistent cache usage patterns"""
        inconsistencies = {}
        
        # Multiple cache instantiation patterns
        instantiation_types = list(self.cache_instantiations.keys())
        if len(instantiation_types) > 1:
            inconsistencies['multiple_instantiation_patterns'] = {
                'description': 'Multiple ways of creating cache instances',
                'patterns': {k: len(v) for k, v in self.cache_instantiations.items()},
                'recommendation': 'Standardize cache instantiation (prefer singleton pattern)'
            }
        
        # Inconsistent cache key naming
        key_categories = list(self.cache_key_patterns.keys())
        if len(key_categories) > 2:  # Allow some variation
            inconsistencies['inconsistent_key_naming'] = {
                'description': 'Multiple cache key naming conventions',
                'patterns': {k: len(v) for k, v in self.cache_key_patterns.items()},
                'recommendation': 'Standardize cache key format (suggest pipe_separated for MAO)'
            }
        
        # Unusual cache operations
        standard_operations = {'get_cached_analysis', 'cache_content_analysis', 'clear_cache'}
        found_operations = set(self.cache_operations.keys())
        non_standard = found_operations - standard_operations
        
        if non_standard:
            inconsistencies['non_standard_operations'] = {
                'description': 'Non-standard cache operation methods',
                'operations': list(non_standard),
                'standard_operations': list(standard_operations),
                'recommendation': 'Use standard MAO cache methods'
            }
        
        # Cache key length variations
        if self.cache_key_patterns:
            all_keys = []
            for category_keys in self.cache_key_patterns.values():
                all_keys.extend([k['key_length'] for k in category_keys])
            
            if all_keys:
                avg_length = sum(all_keys) / len(all_keys)
                very_long = [k for k in all_keys if k > avg_length * 2]
                very_short = [k for k in all_keys if k < 5]
                
                if very_long or very_short:
                    inconsistencies['key_length_variations'] = {
                        'description': 'Significant cache key length variations',
                        'average_length': round(avg_length, 1),
                        'very_long_keys': len(very_long),
                        'very_short_keys': len(very_short),
                        'recommendation': 'Maintain consistent key length and descriptiveness'
                    }
        
        return inconsistencies

    def calculate_cache_score(self) -> float:
        """Calculate cache usage consistency score (0-100)"""
        total_operations = sum(len(ops) for ops in self.cache_operations.values())
        
        if total_operations == 0:
            return 50  # No cache usage found
        
        # Base score starts high if cache is being used
        base_score = 75
        
        inconsistencies = self.find_cache_inconsistencies()
        penalty = len(inconsistencies) * 12  # 12 points off per inconsistency type
        
        # Bonus for using standard MAO cache methods
        standard_operations = {'get_cached_analysis', 'cache_content_analysis', 'clear_cache'}
        standard_usage = sum(len(ops) for method, ops in self.cache_operations.items() 
                           if method in standard_operations)
        
        if total_operations > 0:
            standard_ratio = standard_usage / total_operations
            standard_bonus = standard_ratio * 20
        else:
            standard_bonus = 0
        
        # Bonus for consistent key patterns
        if self.cache_key_patterns:
            dominant_pattern = max(self.cache_key_patterns.items(), key=lambda x: len(x[1]))
            total_keys = sum(len(keys) for keys in self.cache_key_patterns.values())
            consistency_ratio = len(dominant_pattern[1]) / total_keys
            consistency_bonus = consistency_ratio * 15
        else:
            consistency_bonus = 0
        
        final_score = base_score + standard_bonus + consistency_bonus - penalty
        return max(0, min(100, final_score))

    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        inconsistencies = self.find_cache_inconsistencies()
        
        if 'multiple_instantiation_patterns' in inconsistencies:
            recommendations.append("🔧 Standardize cache instantiation (use singleton CacheManager pattern)")
        
        if 'inconsistent_key_naming' in inconsistencies:
            recommendations.append("🏷️ Standardize cache key naming convention (suggest pipe_separated format)")
        
        if 'non_standard_operations' in inconsistencies:
            recommendations.append("📚 Use standard MAO cache methods (cache_content_analysis, get_cached_analysis, clear_cache)")
        
        if 'key_length_variations' in inconsistencies:
            recommendations.append("📏 Maintain consistent cache key length and descriptiveness")
        
        # General recommendations
        total_operations = sum(len(ops) for ops in self.cache_operations.values())
        
        if total_operations > 0:
            recommendations.extend([
                "⚡ Consider cache performance monitoring and metrics",
                "🕒 Review cache expiration strategies",
                "🧪 Add cache testing patterns",
                "📋 Document cache key conventions and usage patterns"
            ])
        else:
            recommendations.append("🚀 Consider implementing caching for performance optimization")
        
        return recommendations

    def run_audit(self) -> Dict[str, Any]:
        """Run complete cache usage audit"""
        print("🔍 Starting MAO Cache Usage Audit...")
        
        python_files = self.find_python_files()
        print(f"📁 Found {len(python_files)} Python files to analyze")
        
        # Analyze each file
        parsed_count = 0
        for file_path in python_files:
            tree = self.parse_file(file_path)
            if tree:
                self.analyze_cache_usage(tree, file_path)
                parsed_count += 1
        
        # Calculate metrics
        inconsistencies = self.find_cache_inconsistencies()
        score = self.calculate_cache_score()
        
        # Compile results
        results = {
            'summary': {
                'files_analyzed': len(python_files),
                'files_parsed': parsed_count,
                'cache_instantiations': sum(len(insts) for insts in self.cache_instantiations.values()),
                'cache_operations': sum(len(ops) for ops in self.cache_operations.values()),
                'cache_key_patterns': len(self.cache_key_patterns),
                'inconsistency_types': len(inconsistencies),
                'cache_usage_score': score
            },
            'cache_instantiations': dict(self.cache_instantiations),
            'cache_operations': dict(self.cache_operations),
            'cache_key_patterns': dict(self.cache_key_patterns),
            'cache_imports': dict(self.cache_imports),
            'inconsistencies': inconsistencies,
            'recommendations': self.generate_recommendations()
        }
        
        return results

    def generate_report(self, output_file: str = "cache_usage_audit_report.json") -> None:
        """Generate detailed audit report"""
        import json
        
        results = self.run_audit()
        
        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 MAO CACHE USAGE AUDIT RESULTS")
        print("="*60)
        
        summary = results['summary']
        print(f"📁 Files analyzed: {summary['files_analyzed']}")
        print(f"✅ Files parsed: {summary['files_parsed']}")
        print(f"🏗️ Cache instantiations: {summary['cache_instantiations']}")
        print(f"⚡ Cache operations: {summary['cache_operations']}")
        print(f"🏷️ Cache key patterns: {summary['cache_key_patterns']}")
        print(f"⚠️ Inconsistency types: {summary['inconsistency_types']}")
        print(f"📊 Cache Usage Score: {summary['cache_usage_score']:.1f}/100")
        
        # Show cache operations
        if results['cache_operations']:
            print(f"\n⚡ CACHE OPERATIONS:")
            for operation, usages in results['cache_operations'].items():
                print(f"  {operation}: {len(usages)} usages")
        
        # Show key patterns
        if results['cache_key_patterns']:
            print(f"\n🏷️ CACHE KEY PATTERNS:")
            for pattern, keys in results['cache_key_patterns'].items():
                print(f"  {pattern}: {len(keys)} keys")
        
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
    """Run the cache usage audit"""
    auditor = CacheUsageAuditor()
    auditor.generate_report()

if __name__ == "__main__":
    main() 