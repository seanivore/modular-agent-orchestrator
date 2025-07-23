#!/usr/bin/env python3
"""
MAO File Path Fixer Script
Automatically fixes file path handling inconsistencies across the codebase

This script fixes:
1. Converts os.path usage to pathlib.Path
2. Replaces hardcoded path separators with Path operators
3. Fixes string concatenation path building
4. Standardizes file existence checking
5. Updates imports to use pathlib
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Optional, Tuple
from collections import defaultdict
import tempfile
import shutil

class FilePathFixer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.fixes_applied = defaultdict(list)
        self.backup_dir = Path("path_fixes_backup")
        
        # Conversion mappings
        self.os_path_to_pathlib = {
            'os.path.join': 'Path()  /  ',
            'os.path.exists': '.exists()',
            'os.path.dirname': '.parent',
            'os.path.basename': '.name',
            'os.path.abspath': '.resolve()',
            'os.path.relpath': '.relative_to()',
            'os.path.isfile': '.is_file()',
            'os.path.isdir': '.is_dir()',
            'os.path.splitext': '.stem and .suffix'
        }

    def create_backup(self, file_path: Path) -> Path:
        """Create backup of original file"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir()
        
        backup_path = self.backup_dir  /  f"{file_path.name}.backup"
        shutil.copy2(file_path, backup_path)
        return backup_path

    def find_python_files(self) -> List[Path]:
        """Find Python files to fix"""
        python_files = []
        
        # Focus on directories likely to have file operations
        priority_dirs = ["orchestrator", "configs / cli", "interfaces", "tools", "scripts"]
        
        for priority_dir in priority_dirs:
            dir_path = self.project_root  /  priority_dir
            if dir_path.exists():
                for py_file in dir_path.rglob("*.py"):
                    if not any(skip in str(py_file) for skip in ['.backup', '__pycache__', 'test_']):
                        python_files.append(py_file)
        
        return python_files

    def fix_imports(self, content: str) -> Tuple[str, List[str]]:
        """Add pathlib import and note os.path imports for potential removal"""
        lines = content.split(Path(r'\n'))
        fixes = []
        
        # Check if pathlib is already imported
        has_pathlib = any('from pathlib import' in line or 'import pathlib' in line for line in lines)
        has_os_path = any('import os' in line for line in lines)
        
        # Add pathlib import if needed
        if not has_pathlib:
            # Find the best place to add import (after existing imports)
            import_end = 0
            for i, line in enumerate(lines):
                if line.strip().startswith(('import ', 'from ')) and not line.strip().startswith('#'):
                    import_end = i + 1
            
            if import_end > 0:
                lines.insert(import_end, 'from pathlib import Path')
                fixes.append("Added pathlib.Path import")
            else:
                # Add at the beginning if no imports found
                lines.insert(0, 'from pathlib import Path')
                fixes.append("Added pathlib.Path import at top")
        
        return Path(r'\n').join(lines), fixes

    def fix_hardcoded_separators(self, content: str) -> Tuple[str, List[str]]:
        """Fix hardcoded path separators"""
        fixes = []
        
        # Replace common hardcoded separator patterns
        patterns = [
            # Simple concatenation patterns
            (r'([Path(r"\')][^Path(r"\')]*) / ([^Path(r"\')]*[Path(r"\')])', rPath(r'\1")  /  Path(r"\2')),  # "path / to" -> "path"  /  "to"
            (r'([Path(r"\')][^Path(r"\')]*\\[^Path(r"\')]*[Path(r"\')])', rPath(r'Path(r\1)')),  # Windows paths
        ]
        
        original_content = content
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                fixes.append(f"Fixed hardcoded path separators")
                content = new_content
        
        return content, fixes

    def fix_string_concatenation(self, content: str) -> Tuple[str, List[str]]:
        """Fix string concatenation used for path building"""
        fixes = []
        
        # Look for patterns like: variable + " / " + something
        patterns = [
            (rPath(r'(\w+)\s*\+\s*[")\'][" / Path(r"\\][")\Path(r']?\s*\+\s*(\w+)'), rPath(r'Path(\1) ") / Path(r" \2')),
            (r'([Path(r"\')][^Path(r"\')]*[Path(r"\')])\s*\+\s*[Path(r"\')][" / Path(r"\\][")\Path(r']?\s*\+\s*(\w+)'), rPath(r'Path(\1) ") / Path(r" \2')),
        ]
        
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                fixes.append("Fixed string concatenation path building")
                content = new_content
        
        return content, fixes

    def fix_os_path_calls(self, content: str) -> Tuple[str, List[str]]:
        """Convert os.path calls to pathlib equivalents"""
        fixes = []
        
        # Convert common os.path patterns
        conversions = [
            # Path(a) / b / c -> Path(a) / b  /  c
            (rPath(r'os\.path\.join\s*\(\s*([^)]+)\s*\)'), self._convert_os_path_join),
            
            # Path(path).exists() -> Path(path).exists()
            (rPath(r'os\.path\.exists\s*\(\s*([^)]+)\s*\)'), rPath(r'Path(\1).exists()')),
            
            # Path(path).parent -> Path(path).parent
            (rPath(r'os\.path\.dirname\s*\(\s*([^)]+)\s*\)'), rPath(r'Path(\1).parent')),
            
            # Path(path).name -> Path(path).name
            (rPath(r'os\.path\.basename\s*\(\s*([^)]+)\s*\)'), rPath(r'Path(\1).name')),
            
            # Path(path).resolve() -> Path(path).resolve()
            (rPath(r'os\.path\.abspath\s*\(\s*([^)]+)\s*\)'), rPath(r'Path(\1).resolve()')),
            
            # Path(path).is_file() -> Path(path).is_file()
            (rPath(r'os\.path\.isfile\s*\(\s*([^)]+)\s*\)'), rPath(r'Path(\1).is_file()')),
            
            # Path(path).is_dir() -> Path(path).is_dir()
            (rPath(r'os\.path\.isdir\s*\(\s*([^)]+)\s*\)'), rPath(r'Path(\1).is_dir()')),
        ]
        
        for pattern, replacement in conversions:
            if callable(replacement):
                new_content = re.sub(pattern, replacement, content)
            else:
                new_content = re.sub(pattern, replacement, content)
            
            if new_content != content:
                fixes.append(f"Converted os.path call to pathlib")
                content = new_content
        
        return content, fixes

    def _convert_os_path_join(self, match) -> str:
        """Convert os.path.join arguments to Path()  /  syntax"""
        args = match.group(1).split(',')
        args = [arg.strip() for arg in args]
        
        if len(args) == 1:
            return f"Path({args[0]})"
        else:
            first_arg = args[0]
            rest_args = '  /  '.join(args[1:])
            return f"Path({first_arg})  /  {rest_args}"

    def fix_file_operations(self, content: str) -> Tuple[str, List[str]]:
        """Fix file operation patterns"""
        fixes = []
        
        # Convert open() with manual path building to pathlib
        patterns = [
            # open(Path(path + " / " + file), ...) -> open(Path(path) / file, ...)
            (rPath(r'open\s*\(\s*([^)]+\+[^)]+),\s*([^)]+)\)'), rPath(r'open(Path(\1), \2)')),
        ]
        
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                fixes.append("Fixed file operation with pathlib")
                content = new_content
        
        return content, fixes

    def fix_file(self, file_path: Path) -> Dict[str, Any]:
        """Fix a single Python file"""
        try:
            # Read original content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            content = original_content
            all_fixes = []
            
            # Apply all fixes
            content, import_fixes = self.fix_imports(content)
            all_fixes.extend(import_fixes)
            
            content, separator_fixes = self.fix_hardcoded_separators(content)
            all_fixes.extend(separator_fixes)
            
            content, concat_fixes = self.fix_string_concatenation(content)
            all_fixes.extend(concat_fixes)
            
            content, os_path_fixes = self.fix_os_path_calls(content)
            all_fixes.extend(os_path_fixes)
            
            content, file_op_fixes = self.fix_file_operations(content)
            all_fixes.extend(file_op_fixes)
            
            # Only apply changes if fixes were made
            if content != original_content and all_fixes:
                # Create backup
                backup_path = self.create_backup(file_path)
                
                # Write fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return {
                    'file': str(file_path),
                    'fixes_applied': all_fixes,
                    'fix_count': len(all_fixes),
                    'backup_path': str(backup_path),
                    'status': 'fixed'
                }
            else:
                return {
                    'file': str(file_path),
                    'fixes_applied': [],
                    'fix_count': 0,
                    'status': 'no_changes_needed'
                }
                
        except Exception as e:
            return {
                'file': str(file_path),
                'fixes_applied': [],
                'fix_count': 0,
                'error': str(e),
                'status': 'error'
            }

    def run_fixes(self) -> Dict[str, Any]:
        """Run all path handling fixes"""
        print("🔧 Starting MAO File Path Fixes...")
        
        python_files = self.find_python_files()
        print(f"📁 Found {len(python_files)} Python files to analyze")
        
        results = []
        total_fixes = 0
        files_modified = 0
        
        for file_path in python_files:
            result = self.fix_file(file_path)
            results.append(result)
            
            if result['status'] == 'fixed':
                files_modified += 1
                total_fixes += result['fix_count']
                print(f"✅ Fixed {result['fix_count']} issues in {file_path.name}")
            elif result['status'] == 'error':
                print(f"❌ Error fixing {file_path.name}: {result['error']}")
        
        # Compile summary
        summary = {
            'files_analyzed': len(python_files),
            'files_modified': files_modified,
            'total_fixes_applied': total_fixes,
            'backup_directory': str(self.backup_dir),
            'fix_categories': {
                'import_fixes': sum(1 for r in results if any('import' in fix for fix in r.get('fixes_applied', []))),
                'separator_fixes': sum(1 for r in results if any('separator' in fix for fix in r.get('fixes_applied', []))),
                'concatenation_fixes': sum(1 for r in results if any('concatenation' in fix for fix in r.get('fixes_applied', []))),
                'os_path_fixes': sum(1 for r in results if any('os.path' in fix for fix in r.get('fixes_applied', []))),
            }
        }
        
        return {
            'summary': summary,
            'detailed_results': results
        }

    def generate_report(self, output_file: str = "file_path_fixes_report.json") -> None:
        """Generate detailed fix report"""
        import json
        
        results = self.run_fixes()
        
        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Print summary
        print(Path(r"\n") + "="*60)
        print("🔧 MAO FILE PATH FIXES RESULTS")
        print("="*60)
        
        summary = results['summary']
        print(f"📁 Files analyzed: {summary['files_analyzed']}")
        print(f"🔧 Files modified: {summary['files_modified']}")
        print(f"✅ Total fixes applied: {summary['total_fixes_applied']}")
        print(f"💾 Backup directory: {summary['backup_directory']}")
        
        # Show fix categories
        categories = summary['fix_categories']
        print(f"\n🔧 FIX BREAKDOWN:")
        print(f"  📦 Import fixes: {categories['import_fixes']}")
        print(f"  🛤️ Separator fixes: {categories['separator_fixes']}")
        print(f"  ➕ Concatenation fixes: {categories['concatenation_fixes']}")
        print(f"  🔄 os.path conversions: {categories['os_path_fixes']}")
        
        if summary['files_modified'] > 0:
            print(f"\n✅ SUCCESS! Fixed {summary[')total_fixes_applied']} path handling issues!"
            print(f"💡 Re-run the path audit to see improved scores")
        else:
            print(f"\n📋 No path handling issues found to fix")
        
        print(f"\n📄 Full report saved to: {output_file}")
        print("="*60)

def main():
    """Run the file path fixer"""
    fixer = FilePathFixer()
    fixer.generate_report()

if __name__ == "__main__":
    main() 