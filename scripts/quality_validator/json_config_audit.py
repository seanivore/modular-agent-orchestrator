#!/usr/bin/env python3
"""
MAO JSON Configuration Audit Script
Finds inconsistencies across all JSON config files in the modular architecture

This script analyzes:
1. Schema consistency across similar config types
2. Field naming inconsistencies (name vs id vs tool_id)
3. Date format variations 
4. Boolean format inconsistencies
5. Required field presence
6. Nested structure patterns
7. Value format standards
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from collections import defaultdict, Counter
from datetime import datetime

class JSONConfigAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "configs"
        self.issues = []
        self.schema_patterns = defaultdict(list)
        self.field_inconsistencies = defaultdict(set)
        self.date_formats = defaultdict(list)
        self.boolean_formats = defaultdict(list)
        
        # Expected schema patterns for different config types
        self.expected_schemas = {
            "tool": ["name", "description", "type", "enabled"],
            "model": ["name", "provider", "description", "parameters"],
            "provider": ["name", "type", "api_key_required", "base_url"],
            "user": ["username", "user_id", "created_at", "last_login"],
            "workflow": ["workflow_id", "name", "description", "phases"],
            "settings": ["default", "description", "type", "options"]
        }
        
        # Common field naming variations that should be standardized
        self.field_variations = {
            "identifier": ["id", "uid", "user_id", "tool_id", "workflow_id", "name"],
            "description": ["description", "desc", "summary", "info"],
            "timestamp": ["created_at", "createdAt", "created", "timestamp", "date"],
            "enabled": ["enabled", "active", "is_enabled", "is_active"],
            "required": ["required", "mandatory", "is_required"]
        }

    def find_all_json_files(self) -> List[Path]:
        """Find all JSON configuration files"""
        json_files = []
        
        # Look in configs directory and subdirectories
        for json_file in self.config_dir.rglob("*.json"):
            if not any(skip in str(json_file) for skip in ['.backup', 'node_modules', '__pycache__']):
                json_files.append(json_file)
        
        return json_files

    def detect_config_type(self, file_path: Path, content: Dict) -> str:
        """Detect what type of config file this is"""
        file_name = file_path.name.lower()
        file_parent = file_path.parent.name.lower()
        
        # Detect by filename patterns
        if 'tool_' in file_name or file_parent == 'tools':
            return 'tool'
        elif 'model' in file_name or file_parent == 'models':
            return 'model'
        elif 'provider' in file_name or file_parent == 'providers':
            return 'provider'
        elif 'user_' in file_name or file_parent == 'user':
            return 'user'
        elif 'workflow' in file_name or file_parent == 'workflows':
            return 'workflow'
        elif 'settings' in file_name or file_parent == 'settings':
            return 'settings'
        elif 'cli' in str(file_path):
            return 'cli_command'
        
        # Detect by content structure
        if isinstance(content, dict):
            keys = set(content.keys())
            if 'tool_id' in keys or 'function' in keys:
                return 'tool'
            elif 'model_name' in keys or 'provider' in keys:
                return 'model'
            elif 'api_key_required' in keys or 'base_url' in keys:
                return 'provider'
            elif 'username' in keys and 'user_id' in keys:
                return 'user'
            elif 'workflow_id' in keys or 'phases' in keys:
                return 'workflow'
            elif 'default' in keys and 'type' in keys:
                return 'settings'
        
        return 'unknown'

    def analyze_field_patterns(self, config_type: str, content: Dict, file_path: Path) -> None:
        """Analyze field naming patterns for consistency"""
        def extract_fields(obj, prefix=""):
            fields = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    fields.append(full_key)
                    if isinstance(value, (dict, list)):
                        fields.extend(extract_fields(value, full_key))
            elif isinstance(obj, list) and obj:
                if isinstance(obj[0], dict):
                    fields.extend(extract_fields(obj[0], prefix))
            return fields
        
        fields = extract_fields(content)
        self.schema_patterns[config_type].append({
            'file': str(file_path),
            'fields': fields,
            'field_count': len(fields)
        })

    def check_date_formats(self, content: Dict, file_path: Path) -> None:
        """Check for date format inconsistencies"""
        def find_dates(obj, path=""):
            dates = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if isinstance(value, str):
                        # Check if it looks like a date
                        if self.is_date_like(key, value):
                            dates.append({
                                'field': current_path,
                                'value': value,
                                'format': self.detect_date_format(value)
                            })
                    elif isinstance(value, (dict, list)):
                        dates.extend(find_dates(value, current_path))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    dates.extend(find_dates(item, f"{path}[{i}]"))
            return dates
        
        dates = find_dates(content)
        for date_info in dates:
            self.date_formats[date_info['format']].append({
                'file': str(file_path),
                'field': date_info['field'],
                'value': date_info['value']
            })

    def is_date_like(self, key: str, value: str) -> bool:
        """Check if a field looks like it contains a date"""
        date_keywords = ['date', 'time', 'created', 'updated', 'last_', 'at']
        key_lower = key.lower()
        
        # Check if key suggests it's a date
        if any(keyword in key_lower for keyword in date_keywords):
            return True
        
        # Check if value looks like a date
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # 2025-07-23
            r'\d{2}/\d{2}/\d{2,4}',  # 07/23/25 or 07/23/2025
            r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',  # ISO format
        ]
        
        return any(re.search(pattern, value) for pattern in date_patterns)

    def detect_date_format(self, value: str) -> str:
        """Detect the format of a date string"""
        if re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', value):
            return 'ISO_DATETIME'
        elif re.search(r'\d{4}-\d{2}-\d{2}', value):
            return 'ISO_DATE'
        elif re.search(r'\d{2}/\d{2}/\d{4}', value):
            return 'US_DATE'
        elif re.search(r'\d{2}/\d{2}/\d{2}', value):
            return 'SHORT_US_DATE'
        else:
            return 'UNKNOWN'

    def check_boolean_formats(self, content: Dict, file_path: Path) -> None:
        """Check for boolean format inconsistencies"""
        def find_booleans(obj, path=""):
            booleans = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if self.is_boolean_like(key, value):
                        booleans.append({
                            'field': current_path,
                            'value': value,
                            'type': type(value).__name__,
                            'format': self.detect_boolean_format(value)
                        })
                    elif isinstance(value, (dict, list)):
                        booleans.extend(find_booleans(value, current_path))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    booleans.extend(find_booleans(item, f"{path}[{i}]"))
            return booleans
        
        booleans = find_booleans(content)
        for bool_info in booleans:
            self.boolean_formats[bool_info['format']].append({
                'file': str(file_path),
                'field': bool_info['field'],
                'value': bool_info['value']
            })

    def is_boolean_like(self, key: str, value: Any) -> bool:
        """Check if a field looks like it should be a boolean"""
        boolean_keywords = ['enabled', 'active', 'required', 'mandatory', 'is_', 'has_', 'can_', 'should_']
        key_lower = key.lower()
        
        # Check key name
        if any(keyword in key_lower for keyword in boolean_keywords):
            return True
        
        # Check value
        if isinstance(value, bool):
            return True
        if isinstance(value, str) and value.lower() in ['true', 'false', 'yes', 'no', 'on', 'off']:
            return True
        if isinstance(value, int) and value in [0, 1]:
            return True
        
        return False

    def detect_boolean_format(self, value: Any) -> str:
        """Detect the format of a boolean value"""
        if isinstance(value, bool):
            return 'NATIVE_BOOL'
        elif isinstance(value, str):
            val_lower = value.lower()
            if val_lower in ['true', 'false']:
                return 'STRING_BOOL'
            elif val_lower in ['yes', 'no']:
                return 'YES_NO'
            elif val_lower in ['on', 'off']:
                return 'ON_OFF'
        elif isinstance(value, int) and value in [0, 1]:
            return 'INT_BOOL'
        
        return 'UNKNOWN'

    def find_schema_inconsistencies(self) -> Dict[str, List]:
        """Find inconsistencies in schema patterns"""
        inconsistencies = {}
        
        for config_type, patterns in self.schema_patterns.items():
            if len(patterns) < 2:
                continue
            
            # Analyze field consistency
            all_fields = set()
            field_frequency = Counter()
            
            for pattern in patterns:
                pattern_fields = set(pattern['fields'])
                all_fields.update(pattern_fields)
                field_frequency.update(pattern_fields)
            
            # Find fields that aren't in all files of this type
            total_files = len(patterns)
            inconsistent_fields = []
            
            for field, count in field_frequency.items():
                if count < total_files:
                    missing_from = []
                    for pattern in patterns:
                        if field not in pattern['fields']:
                            missing_from.append(pattern['file'])
                    
                    inconsistent_fields.append({
                        'field': field,
                        'present_in': count,
                        'total_files': total_files,
                        'missing_from': missing_from
                    })
            
            if inconsistent_fields:
                inconsistencies[config_type] = inconsistent_fields
        
        return inconsistencies

    def audit_single_file(self, file_path: Path) -> Optional[Dict]:
        """Audit a single JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            config_type = self.detect_config_type(file_path, content)
            
            # Analyze patterns
            self.analyze_field_patterns(config_type, content, file_path)
            self.check_date_formats(content, file_path)
            self.check_boolean_formats(content, file_path)
            
            return {
                'file': str(file_path),
                'config_type': config_type,
                'success': True
            }
            
        except Exception as e:
            error_info = {
                'file': str(file_path),
                'error': str(e),
                'success': False
            }
            self.issues.append(error_info)
            return error_info

    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Date format recommendations
        if len(self.date_formats) > 1:
            recommendations.append("🗓️ Standardize date formats - suggest using ISO format (YYYY-MM-DD) for consistency")
        
        # Boolean format recommendations
        if len(self.boolean_formats) > 1:
            recommendations.append("✅ Standardize boolean formats - suggest using native JSON booleans (true/false)")
        
        # Schema recommendations
        schema_issues = self.find_schema_inconsistencies()
        if schema_issues:
            recommendations.append("📋 Standardize schema structures across similar config types")
        
        recommendations.append("🔧 Create JSON schema templates for each config type")
        recommendations.append("🧪 Add JSON validation to prevent future inconsistencies")
        recommendations.append("📚 Document standard field naming conventions")
        
        return recommendations

    def run_audit(self) -> Dict[str, Any]:
        """Run complete JSON configuration audit"""
        print("🔍 Starting MAO JSON Configuration Audit...")
        
        json_files = self.find_all_json_files()
        print(f"📁 Found {len(json_files)} JSON config files to analyze")
        
        # Audit each file
        results = []
        for file_path in json_files:
            result = self.audit_single_file(file_path)
            if result:
                results.append(result)
        
        # Analyze patterns
        schema_inconsistencies = self.find_schema_inconsistencies()
        
        # Compile results
        audit_results = {
            'summary': {
                'total_files': len(json_files),
                'files_processed': len([r for r in results if r['success']]),
                'errors': len([r for r in results if not r['success']]),
                'config_types_found': len(self.schema_patterns),
                'date_formats_found': len(self.date_formats),
                'boolean_formats_found': len(self.boolean_formats),
                'schema_inconsistencies': len(schema_inconsistencies)
            },
            'config_types': dict(self.schema_patterns),
            'date_formats': dict(self.date_formats),
            'boolean_formats': dict(self.boolean_formats),
            'schema_inconsistencies': schema_inconsistencies,
            'errors': self.issues,
            'recommendations': self.generate_recommendations()
        }
        
        return audit_results

    def generate_report(self, output_file: str = "json_config_audit_report.json") -> None:
        """Generate detailed audit report"""
        results = self.run_audit()
        
        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 MAO JSON CONFIGURATION AUDIT RESULTS")
        print("="*60)
        
        summary = results['summary']
        print(f"📁 Total files: {summary['total_files']}")
        print(f"✅ Successfully processed: {summary['files_processed']}")
        print(f"❌ Errors: {summary['errors']}")
        print(f"📋 Config types found: {summary['config_types_found']}")
        print(f"🗓️ Date formats found: {summary['date_formats_found']}")
        print(f"✅ Boolean formats found: {summary['boolean_formats_found']}")
        print(f"⚠️ Schema inconsistencies: {summary['schema_inconsistencies']}")
        
        # Show date format inconsistencies
        if len(results['date_formats']) > 1:
            print(f"\n🗓️ DATE FORMAT INCONSISTENCIES:")
            for fmt, examples in results['date_formats'].items():
                print(f"  {fmt}: {len(examples)} files")
                for example in examples[:3]:
                    rel_path = str(Path(example['file']).relative_to(self.project_root))
                    print(f"    📄 {rel_path}: {example['field']} = {example['value']}")
        
        # Show boolean format inconsistencies
        if len(results['boolean_formats']) > 1:
            print(f"\n✅ BOOLEAN FORMAT INCONSISTENCIES:")
            for fmt, examples in results['boolean_formats'].items():
                print(f"  {fmt}: {len(examples)} files")
                for example in examples[:3]:
                    rel_path = str(Path(example['file']).relative_to(self.project_root))
                    print(f"    📄 {rel_path}: {example['field']} = {example['value']}")
        
        # Show schema inconsistencies
        if results['schema_inconsistencies']:
            print(f"\n📋 SCHEMA INCONSISTENCIES:")
            for config_type, issues in results['schema_inconsistencies'].items():
                print(f"  📦 {config_type.upper()} configs:")
                for issue in issues[:5]:
                    print(f"    ⚠️ '{issue['field']}' missing from {len(issue['missing_from'])} files")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"  {rec}")
        
        print(f"\n📄 Full report saved to: {output_file}")
        print("="*60)

def main():
    """Run the JSON configuration audit"""
    auditor = JSONConfigAuditor()
    auditor.generate_report()

if __name__ == "__main__":
    main() 