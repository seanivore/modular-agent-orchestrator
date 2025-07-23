#!/usr/bin/env python3
"""
MAO Import Fixer Script
Automatically fixes common import issues found by the import auditor

This script can:
1. Replace sys.path.append + import patterns with clean dotted imports
2. Remove unused sys and os imports
3. Standardize common import patterns
4. Create backup files before changes
"""

# import os  # Removed - was only used for sys.path.append
import re
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any

class ImportFixer:
    def __init__(self, project_root: str = ".", backup: bool = True):
        self.project_root = Path(project_root)
        self.backup = backup
        self.fixes_applied = []
        
        # Known safe fixes (high confidence)
        self.safe_fixes = {
            # user_id_generator patterns
            (r"sys\.path\.append\(os\.path\.join\(os\.path\.dirname\(__file__\).*?user_id_generator.*?\)\)",
             r"from user_id_generator import (.*?)"):
                Path(r"from scripts.user_id_generator.user_id_generator import \\2"),
            
            # unique_id_generator patterns  
            (r"sys\.path\.append\(os\.path\.join\(os\.path\.dirname\(__file__\).*?unique_id_generator.*?\)\)",
             r"from unique_id_generator import (.*?)"):
                Path(r"from scripts.unique_id_generator.unique_id_generator import \\2"),
            
            # Orchestrator imports from scripts
            (r"sys\.path\.append\(str\(Path\(__file__\)\.parent\.parent\.parent\)\)",
             r"from orchestrator\.(.*?) import (.*?)"):
                Path(r"from orchestrator.\\1 import \\2")
        }
        
        # Files to skip (too risky or special cases)
        self.skip_files = [
            "versioning/v3 / ",  # Legacy versions
            "tests / typescript-",  # Non-Python
            "button_",  # Generated code snippets
        ]

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        file_str = str(file_path)
        for skip_pattern in self.skip_files:
            if skip_pattern in file_str:
                return True
        return False

    def backup_file(self, file_path: Path) -> None:
        """Create backup of file before modification"""
        if self.backup:
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            shutil.copy2(file_path, backup_path)

    def fix_sys_path_imports(self, file_path: Path, content: str) -> str:
        """Fix sys.path.append + import patterns"""
        lines = content.split(Path(r'\n'))
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Look for sys.path.append pattern
            if 'sys.path.append' in line and not self.should_skip_file(file_path):
                # Look for following import in next few lines
                import_line = None
                import_index = None
                
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip().startswith('from ') and 'import' in lines[j]:
                        import_line = lines[j].strip()
                        import_index = j
                        break
                
                # Apply safe fixes
                if import_line:
                    fixed = self.apply_safe_fix(line, import_line)
                    if fixed:
                        # Replace with clean import, skip sys.path.append line
                        fixed_lines.append(f"# {line.strip()}")  # Comment out old line
                        fixed_lines.append(fixed)
                        
                        # Skip the original import line
                        i = import_index + 1
                        
                        self.fixes_applied.append({
                            'file': str(file_path),
                            'old_pattern': f"{line.strip()} + {import_line}",
                            'new_pattern': fixed
                        })
                        continue
            
            fixed_lines.append(line)
            i += 1
        
        return Path(r'\n').join(fixed_lines)

    def apply_safe_fix(self, sys_path_line: str, import_line: str) -> str:
        """Apply a safe fix if pattern matches known good patterns"""
        # user_id_generator fix
        if 'user_id_generator' in sys_path_line and 'from user_id_generator import' in import_line:
            imports = import_line.split('import')[1].strip()
            return f"from scripts.user_id_generator.user_id_generator import {imports}"
        
        # unique_id_generator fix
        if 'unique_id_generator' in sys_path_line and 'from unique_id_generator import' in import_line:
            imports = import_line.split('import')[1].strip()
            return f"from scripts.unique_id_generator.unique_id_generator import {imports}"
        
        # Orchestrator imports from scripts
        if 'parent.parent.parent' in sys_path_line and 'from orchestrator.' in import_line:
            return import_line  # These are already clean
        
        return None

    def remove_unused_imports(self, file_path: Path, content: str) -> str:
        """Remove unused sys and os imports after sys.path.append removal"""
        lines = content.split(Path(r'\n'))
        fixed_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # Check for standalone sys or os imports
            if line_stripped in ['import sys', 'import os']:
                import_name = line_stripped.split()[1]
                
                # Check if this import is used elsewhere in the file
                used_elsewhere = any(f'{import_name}.' in other_line 
                                   for other_line in lines 
                                   if other_line.strip() != line_stripped)
                
                if not used_elsewhere:
                    fixed_lines.append(f"# {line_stripped}  # Removed - was only used for sys.path.append")
                    self.fixes_applied.append({
                        'file': str(file_path),
                        'old_pattern': line_stripped,
                        'new_pattern': 'REMOVED - unused after sys.path.append fix'
                    })
                    continue
            
            fixed_lines.append(line)
        
        return Path(r'\n').join(fixed_lines)

    def fix_file(self, file_path: Path) -> bool:
        """Fix a single file"""
        if self.should_skip_file(file_path):
            return False
        
        try:
            # Read original content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Apply fixes
            content = original_content
            content = self.fix_sys_path_imports(file_path, content)
            content = self.remove_unused_imports(file_path, content)
            
            # Only write if changes were made
            if content != original_content:
                # Create backup
                self.backup_file(file_path)
                
                # Write fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
            return False

    def run_fixer(self, audit_report_file: str = "import_audit_report.json") -> Dict[str, Any]:
        """Run automated fixes based on audit report"""
        print("🔧 Starting MAO Import Fixer...")
        
        # Load audit report if available
        if Path(audit_report_file).exists():
            with open(audit_report_file, 'r') as f:
                audit_data = json.load(f)
            
            sys_path_issues = audit_data.get('sys_path_issues', [])
            print(f"📊 Found {len(sys_path_issues)} sys.path.append issues to potentially fix")
        
        # Find all Python files to process
        python_files = []
        for py_file in self.project_root.rglob("*.py"):
            if not self.should_skip_file(py_file) and py_file.suffix == '.py':
                python_files.append(py_file)
        
        print(f"📁 Processing {len(python_files)} Python files...")
        
        fixed_count = 0
        for file_path in python_files:
            if self.fix_file(file_path):
                fixed_count += 1
                print(f"✅ Fixed: {file_path}")
        
        results = {
            'files_processed': len(python_files),
            'files_modified': fixed_count,
            'fixes_applied': len(self.fixes_applied),
            'individual_fixes': self.fixes_applied
        }
        
        print(f"\n📊 FIXER RESULTS:")
        print(f"  📁 Files processed: {results['files_processed']}")
        print(f"  ✅ Files modified: {results['files_modified']}")
        print(f"  🔧 Individual fixes: {results['fixes_applied']}")
        
        if self.backup:
            print(f"  💾 Backup files created with .backup extension")
        
        # Save results
        with open("import_fixes_applied.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        return results

def main():
    """Run the import fixer"""
    print("⚠️  MAO Import Fixer - This will modify your files!")
    print("📄 Make sure you have committed your changes first.")
    
    response = input("Continue? (y / N): ").strip().lower()
    if response != 'y':
        print("❌ Aborted")
        return
    
    fixer = ImportFixer(backup=True)
    results = fixer.run_fixer()
    
    print(f"\n✅ Import fixing complete!")
    print(f"📄 Results saved to: import_fixes_applied.json")
    print(f"🔄 Run the audit script again to see remaining issues")

if __name__ == "__main__":
    main() 