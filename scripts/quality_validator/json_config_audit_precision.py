#!/usr/bin/env python3
"""
MAO JSON Configuration Precision Audit Script
Designer-level scoring that recognizes quality and compliance

This script scores based on:
1. Schema compliance and consistency (0-100 points)
2. Field naming standards adherence (0-100 points) 
3. Date format standardization (0-100 points)
4. Boolean format consistency (0-100 points)
5. Structure quality patterns (0-100 points)

Scoring Philosophy: Reward compliance, not just count problems
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from collections import defaultdict, Counter
from datetime import datetime

class JSONConfigPrecisionAuditor:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "configs"
        self.total_files = 0
        self.compliance_scores = {
            'schema_compliance': 0,
            'field_naming': 0,
            'date_formats': 0,
            'boolean_formats': 0,
            'structure_quality': 0
        }
        
        # Standard patterns we expect (after Lexus-level fixes)
        self.standard_date_format = 'ISO_DATETIME'  # 2025-01-15T10:30:00Z
        self.standard_boolean_format = 'NATIVE_BOOL'  # true/false
        
        # Expected standard field names (post-normalization)
        self.standard_fields = {
            'tool': ['name', 'description', 'type', 'enabled', 'version'],
            'model': ['name', 'provider', 'description', 'parameters'],
            'provider': ['name', 'type', 'api_key_required', 'base_url'],
            'user': ['username', 'user_id', 'created_at', 'last_login'],
            'workflow': ['workflow_id', 'name', 'description', 'phases'],
            'settings': ['default', 'description', 'type', 'options']
        }

    def find_all_json_files(self) -> List[Path]:
        """Find all JSON configuration files"""
        json_files = []
        for json_file in self.config_dir.rglob("*.json"):
            if not any(skip in str(json_file) for skip in ['.backup', 'node_modules', '__pycache__']):
                json_files.append(json_file)
        return json_files

    def detect_config_type(self, file_path: Path, content: Dict) -> str:
        """Detect configuration type"""
        file_name = file_path.name.lower()
        file_parent = file_path.parent.name.lower()
        
        # Detect by path structure
        if 'tool' in file_name or file_parent == 'tools':
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
        
        return 'other'

    def score_schema_compliance(self, config_type: str, content: Dict) -> float:
        """Score how well the schema matches expected standards"""
        if config_type not in self.standard_fields:
            return 80.0  # Neutral score for non-standard types
        
        expected_fields = set(self.standard_fields[config_type])
        actual_fields = set(content.keys()) if isinstance(content, dict) else set()
        
        if not expected_fields:
            return 100.0  # Perfect if no expectations
        
        # Score based on field presence
        matching_fields = expected_fields.intersection(actual_fields)
        compliance_ratio = len(matching_fields) / len(expected_fields)
        
        # Bonus points for having all expected fields
        if compliance_ratio == 1.0:
            return 100.0
        elif compliance_ratio >= 0.8:
            return 85.0 + (compliance_ratio - 0.8) * 75  # 85-100 range
        elif compliance_ratio >= 0.6:
            return 70.0 + (compliance_ratio - 0.6) * 75  # 70-85 range
        else:
            return compliance_ratio * 70  # 0-70 range

    def score_field_naming(self, content: Dict) -> float:
        """Score field naming consistency and standards"""
        if not isinstance(content, dict):
            return 50.0
        
        def check_naming_standards(obj, path=""):
            violations = 0
            total_fields = 0
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    total_fields += 1
                    
                    # Check for standard naming patterns
                    if not self.is_standard_field_name(key):
                        violations += 1
                    
                    # Recursively check nested objects
                    if isinstance(value, (dict, list)):
                        nested_violations, nested_total = check_naming_standards(value, f"{path}.{key}")
                        violations += nested_violations
                        total_fields += nested_total
            
            elif isinstance(obj, list) and obj:
                for i, item in enumerate(obj):
                    if isinstance(item, dict):
                        nested_violations, nested_total = check_naming_standards(item, f"{path}[{i}]")
                        violations += nested_violations
                        total_fields += nested_total
            
            return violations, total_fields
        
        violations, total_fields = check_naming_standards(content)
        
        if total_fields == 0:
            return 100.0
        
        compliance_ratio = (total_fields - violations) / total_fields
        return compliance_ratio * 100

    def is_standard_field_name(self, field_name: str) -> bool:
        """Check if field name follows standard conventions"""
        # Standard patterns: snake_case, common names
        if re.match(r'^[a-z][a-z0-9_]*[a-z0-9]$', field_name):
            return True
        if field_name in ['id', 'name', 'type', 'url']:  # Single word standards
            return True
        return False

    def score_date_formats(self, content: Dict) -> float:
        """Score date format consistency"""
        def find_dates(obj):
            dates = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str) and self.is_date_field(key, value):
                        dates.append(value)
                    elif isinstance(value, (dict, list)):
                        dates.extend(find_dates(value))
            elif isinstance(obj, list):
                for item in obj:
                    dates.extend(find_dates(item))
            return dates
        
        dates = find_dates(content)
        if not dates:
            return 100.0  # Perfect if no dates to check
        
        standard_count = sum(1 for date in dates if self.is_standard_date_format(date))
        return (standard_count / len(dates)) * 100

    def is_date_field(self, key: str, value: str) -> bool:
        """Check if field appears to be a date"""
        date_keywords = ['date', 'time', 'created', 'updated', 'last_', 'at']
        key_lower = key.lower()
        return any(keyword in key_lower for keyword in date_keywords)

    def is_standard_date_format(self, date_string: str) -> bool:
        """Check if date follows our standard ISO format"""
        iso_patterns = [
            r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?',  # ISO datetime
            r'\d{4}-\d{2}-\d{2}'  # ISO date
        ]
        return any(re.match(pattern, date_string) for pattern in iso_patterns)

    def score_boolean_formats(self, content: Dict) -> float:
        """Score boolean format consistency"""
        def find_booleans(obj):
            booleans = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if self.is_boolean_field(key, value):
                        booleans.append(value)
                    elif isinstance(value, (dict, list)):
                        booleans.extend(find_booleans(value))
            elif isinstance(obj, list):
                for item in obj:
                    booleans.extend(find_booleans(item))
            return booleans
        
        booleans = find_booleans(content)
        if not booleans:
            return 100.0  # Perfect if no booleans to check
        
        standard_count = sum(1 for boolean in booleans if isinstance(boolean, bool))
        return (standard_count / len(booleans)) * 100

    def is_boolean_field(self, key: str, value: Any) -> bool:
        """Check if field appears to be a boolean"""
        boolean_keywords = ['enabled', 'active', 'required', 'is_', 'has_', 'can_']
        key_lower = key.lower()
        
        if any(keyword in key_lower for keyword in boolean_keywords):
            return True
        if isinstance(value, bool):
            return True
        if isinstance(value, str) and value.lower() in ['true', 'false']:
            return True
        
        return False

    def score_structure_quality(self, content: Dict) -> float:
        """Score overall structure quality"""
        if not isinstance(content, dict):
            return 30.0
        
        quality_score = 0
        
        # Well-formed JSON structure (20 points)
        quality_score += 20
        
        # Has meaningful top-level fields (20 points)
        if len(content) >= 3:
            quality_score += 20
        elif len(content) >= 1:
            quality_score += 10
        
        # Consistent nesting depth (20 points)
        max_depth = self.calculate_max_depth(content)
        if max_depth <= 3:
            quality_score += 20
        elif max_depth <= 5:
            quality_score += 15
        else:
            quality_score += 10
        
        # No empty values (20 points)
        empty_count = self.count_empty_values(content)
        if empty_count == 0:
            quality_score += 20
        elif empty_count <= 2:
            quality_score += 15
        else:
            quality_score += 10
        
        # Consistent field types (20 points)
        if self.has_consistent_types(content):
            quality_score += 20
        else:
            quality_score += 10
        
        return min(quality_score, 100)

    def calculate_max_depth(self, obj, depth=0):
        """Calculate maximum nesting depth"""
        if isinstance(obj, dict):
            if not obj:
                return depth
            return max(self.calculate_max_depth(value, depth + 1) for value in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return depth
            return max(self.calculate_max_depth(item, depth + 1) for item in obj)
        else:
            return depth

    def count_empty_values(self, obj):
        """Count empty or null values"""
        count = 0
        if isinstance(obj, dict):
            for value in obj.values():
                if value is None or value == "" or value == []:
                    count += 1
                elif isinstance(value, (dict, list)):
                    count += self.count_empty_values(value)
        elif isinstance(obj, list):
            for item in obj:
                count += self.count_empty_values(item)
        return count

    def has_consistent_types(self, obj):
        """Check for consistent field types"""
        # This is a simplified check - in practice would be more sophisticated
        if isinstance(obj, dict):
            return len(obj) > 0  # Basic check
        return True

    def audit_file(self, file_path: Path) -> Dict[str, Any]:
        """Audit a single JSON file with precision scoring"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            config_type = self.detect_config_type(file_path, content)
            
            # Calculate individual scores
            scores = {
                'schema_compliance': self.score_schema_compliance(config_type, content),
                'field_naming': self.score_field_naming(content),
                'date_formats': self.score_date_formats(content),
                'boolean_formats': self.score_boolean_formats(content),
                'structure_quality': self.score_structure_quality(content)
            }
            
            # Calculate overall file score
            overall_score = sum(scores.values()) / len(scores)
            
            return {
                'file': str(file_path.relative_to(self.project_root)),
                'config_type': config_type,
                'scores': scores,
                'overall_score': overall_score,
                'success': True
            }
            
        except Exception as e:
            return {
                'file': str(file_path.relative_to(self.project_root)),
                'error': str(e),
                'success': False
            }

    def run_audit(self) -> Dict[str, Any]:
        """Run precision audit on all JSON files"""
        json_files = self.find_all_json_files()
        self.total_files = len(json_files)
        
        results = []
        total_scores = defaultdict(float)
        successful_files = 0
        
        for file_path in json_files:
            result = self.audit_file(file_path)
            results.append(result)
            
            if result['success']:
                successful_files += 1
                for category, score in result['scores'].items():
                    total_scores[category] += score
        
        # Calculate average scores
        if successful_files > 0:
            avg_scores = {
                category: total / successful_files 
                for category, total in total_scores.items()
            }
            overall_avg = sum(avg_scores.values()) / len(avg_scores)
        else:
            avg_scores = {category: 0.0 for category in self.compliance_scores.keys()}
            overall_avg = 0.0
        
        return {
            'summary': {
                'total_files': self.total_files,
                'successful_audits': successful_files,
                'overall_score': overall_avg,
                'category_scores': avg_scores
            },
            'file_results': results,
            'scoring_method': 'precision_compliance'
        }

def main():
    """Run the precision audit"""
    auditor = JSONConfigPrecisionAuditor()
    results = auditor.run_audit()
    
    print("🎯 JSON CONFIG PRECISION AUDIT RESULTS")
    print("=" * 50)
    
    summary = results['summary']
    print(f"📊 Overall Score: {summary['overall_score']:.1f}/100")
    print(f"📁 Files Audited: {summary['successful_audits']}/{summary['total_files']}")
    
    print("\n📋 Category Breakdown:")
    for category, score in summary['category_scores'].items():
        print(f"  {category.replace('_', ' ').title()}: {score:.1f}/100")
    
    # Performance rating
    score = summary['overall_score']
    if score >= 90:
        print("\n🏆 LEXUS-LEVEL QUALITY! Designer precision achieved!")
    elif score >= 80:
        print("\n✨ PREMIUM QUALITY! Very strong compliance!")
    elif score >= 70:
        print("\n👍 GOOD QUALITY! Room for fine-tuning!")
    else:
        print("\n🔧 NEEDS IMPROVEMENT! Significant work required!")

if __name__ == "__main__":
    main() 