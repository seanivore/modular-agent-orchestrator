#!/usr/bin/env python3
"""
MAO Quality Audit Suite
Master script that runs all quality audits and provides a comprehensive quality dashboard

This suite includes:
1. Import consistency audit
2. JSON configuration audit  
3. Function naming audit
4. Error handling patterns audit
5. Overall quality score calculation
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import importlib.util

class QualityAuditSuite:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.scripts_dir = self.project_root / "scripts" / "quality_validator"
        self.audit_results = {}
        self.quality_score = 0
        
        # Available audits
        self.audits = {
            "import_audit": {
                "script": "import_audit.py",
                "name": "Import Consistency Audit",
                "weight": 25,  # Percentage weight in overall score
                "description": "Analyzes import patterns and sys.path.append usage"
            },
            "json_config_audit": {
                "script": "json_config_audit.py", 
                "name": "JSON Configuration Audit",
                "weight": 30,
                "description": "Analyzes JSON config consistency and schema patterns"
            },
            "function_naming_audit": {
                "script": "function_naming_audit.py",
                "name": "Function Naming Audit", 
                "weight": 25,
                "description": "Analyzes function/method naming consistency"
            },
            "error_handling_audit": {
                "script": None,  # Will create this
                "name": "Error Handling Patterns Audit",
                "weight": 20,
                "description": "Analyzes error handling consistency across codebase"
            }
        }

    def run_audit_script(self, script_name: str) -> Optional[Dict]:
        """Run a specific audit script and return results"""
        script_path = self.scripts_dir / script_name
        
        if not script_path.exists():
            print(f"⚠️ Script {script_name} not found, skipping...")
            return None
        
        try:
            print(f"🔍 Running {script_name}...")
            
            # Import and run the audit script
            spec = importlib.util.spec_from_file_location("audit_module", script_path)
            audit_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(audit_module)
            
            # Get the main auditor class
            if hasattr(audit_module, 'ImportAuditor'):
                auditor = audit_module.ImportAuditor()
            elif hasattr(audit_module, 'JSONConfigAuditor'):
                auditor = audit_module.JSONConfigAuditor()
            elif hasattr(audit_module, 'FunctionNamingAuditor'):
                auditor = audit_module.FunctionNamingAuditor()
            else:
                print(f"❌ No auditor class found in {script_name}")
                return None
            
            # Run the audit
            results = auditor.run_audit()
            return results
            
        except Exception as e:
            print(f"❌ Error running {script_name}: {str(e)}")
            return None

    def calculate_audit_score(self, audit_key: str, results: Dict) -> float:
        """Calculate quality score for a specific audit (0-100)"""
        if not results:
            return 0
        
        try:
            if audit_key == "import_audit":
                # Score based on import issues
                summary = results.get('summary', {})
                total_issues = summary.get('sys_path_issues_found', 0) + summary.get('other_issues', 0)
                total_files = summary.get('total_files_analyzed', 1)
                
                # Score decreases with more issues per file
                issues_per_file = total_issues / total_files
                score = max(0, 100 - (issues_per_file * 30))  # 30 points off per issue per file
                
            elif audit_key == "json_config_audit":
                # Score based on config consistency
                summary = results.get('summary', {})
                total_files = summary.get('total_files', 1)
                inconsistencies = summary.get('schema_inconsistencies', 0)
                date_formats = summary.get('date_formats_found', 1)
                bool_formats = summary.get('boolean_formats_found', 1)
                
                # Penalties for inconsistencies
                schema_penalty = (inconsistencies / total_files) * 40
                format_penalty = max(0, (date_formats - 1) * 10) + max(0, (bool_formats - 1) * 10)
                
                score = max(0, 100 - schema_penalty - format_penalty)
                
            elif audit_key == "function_naming_audit":
                # Score based on naming consistency
                summary = results.get('summary', {})
                total_functions = summary.get('total_functions', 1) + summary.get('total_methods', 1)
                inconsistencies = summary.get('manager_inconsistencies', 0) + summary.get('parameter_inconsistencies', 0)
                
                # Score decreases with inconsistencies
                inconsistency_ratio = inconsistencies / max(1, total_functions / 10)  # Scale by function count
                score = max(0, 100 - (inconsistency_ratio * 50))
                
            else:
                score = 50  # Default score for unknown audits
                
            return min(100, max(0, score))  # Clamp between 0-100
            
        except Exception:
            return 50  # Default score on error

    def calculate_overall_score(self) -> float:
        """Calculate weighted overall quality score"""
        total_weight = 0
        weighted_score = 0
        
        for audit_key, audit_info in self.audits.items():
            if audit_key in self.audit_results and self.audit_results[audit_key]:
                weight = audit_info['weight'] / 100
                score = self.calculate_audit_score(audit_key, self.audit_results[audit_key])
                
                weighted_score += score * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0
        
        return weighted_score / total_weight

    def generate_quality_insights(self) -> List[str]:
        """Generate insights and recommendations based on all audit results"""
        insights = []
        
        # Analyze overall patterns
        total_issues = 0
        critical_areas = []
        
        for audit_key, results in self.audit_results.items():
            if not results:
                continue
                
            score = self.calculate_audit_score(audit_key, results)
            audit_name = self.audits[audit_key]['name']
            
            if score < 60:
                critical_areas.append(f"{audit_name} (Score: {score:.1f})")
            
            # Count total issues
            if 'summary' in results:
                summary = results['summary']
                if audit_key == "import_audit":
                    total_issues += summary.get('sys_path_issues_found', 0)
                elif audit_key == "json_config_audit":
                    total_issues += summary.get('schema_inconsistencies', 0)
        
        # Generate insights
        if self.quality_score >= 80:
            insights.append("🌟 Excellent code quality! Your codebase shows strong consistency patterns.")
        elif self.quality_score >= 60:
            insights.append("✅ Good code quality with some areas for improvement.")
        else:
            insights.append("⚠️ Significant quality issues detected. Systematic improvements needed.")
        
        if critical_areas:
            insights.append(f"🎯 Focus areas: {', '.join(critical_areas)}")
        
        if total_issues > 50:
            insights.append("🔧 Consider implementing automated quality checks in your CI/CD pipeline.")
        
        insights.append("📈 Regular quality audits help maintain code consistency as the project scales.")
        
        return insights

    def create_quality_dashboard(self) -> Dict[str, Any]:
        """Create comprehensive quality dashboard"""
        dashboard = {
            'metadata': {
                'audit_timestamp': datetime.now().isoformat(),
                'project_root': str(self.project_root),
                'audits_run': len([k for k, v in self.audit_results.items() if v is not None])
            },
            'overall_score': self.quality_score,
            'score_breakdown': {},
            'audit_results': self.audit_results,
            'insights': self.generate_quality_insights(),
            'recommendations': []
        }
        
        # Calculate individual scores
        for audit_key, audit_info in self.audits.items():
            if audit_key in self.audit_results and self.audit_results[audit_key]:
                score = self.calculate_audit_score(audit_key, self.audit_results[audit_key])
                dashboard['score_breakdown'][audit_key] = {
                    'name': audit_info['name'],
                    'score': score,
                    'weight': audit_info['weight'],
                    'status': 'excellent' if score >= 80 else 'good' if score >= 60 else 'needs_improvement'
                }
        
        # Collect all recommendations
        for results in self.audit_results.values():
            if results and 'recommendations' in results:
                dashboard['recommendations'].extend(results['recommendations'])
        
        # Remove duplicates
        dashboard['recommendations'] = list(set(dashboard['recommendations']))
        
        return dashboard

    def run_all_audits(self) -> Dict[str, Any]:
        """Run all available quality audits"""
        print("🚀 Starting MAO Quality Audit Suite...")
        print("=" * 60)
        
        # Run each audit
        for audit_key, audit_info in self.audits.items():
            if audit_info['script']:
                print(f"\n📊 {audit_info['name']}")
                print("-" * 40)
                results = self.run_audit_script(audit_info['script'])
                self.audit_results[audit_key] = results
                
                if results:
                    score = self.calculate_audit_score(audit_key, results)
                    print(f"✅ Completed - Score: {score:.1f}/100")
                else:
                    print("❌ Failed to complete")
            else:
                print(f"\n⏭️ Skipping {audit_info['name']} (not implemented)")
                self.audit_results[audit_key] = None
        
        # Calculate overall score
        self.quality_score = self.calculate_overall_score()
        
        # Create dashboard
        dashboard = self.create_quality_dashboard()
        
        return dashboard

    def generate_report(self, output_file: str = "quality_audit_dashboard.json") -> None:
        """Generate comprehensive quality report"""
        dashboard = self.run_all_audits()
        
        # Save dashboard
        with open(output_file, 'w') as f:
            json.dump(dashboard, f, indent=2)
        
        # Print summary dashboard
        print("\n" + "=" * 70)
        print("📊 MAO QUALITY AUDIT DASHBOARD")
        print("=" * 70)
        
        # Overall score with visual indicator
        score = dashboard['overall_score']
        if score >= 80:
            indicator = "🌟 EXCELLENT"
        elif score >= 60:
            indicator = "✅ GOOD"
        else:
            indicator = "⚠️ NEEDS IMPROVEMENT"
        
        print(f"\n🎯 OVERALL QUALITY SCORE: {score:.1f}/100 {indicator}")
        
        # Individual audit scores
        print(f"\n📈 AUDIT BREAKDOWN:")
        for audit_key, score_info in dashboard['score_breakdown'].items():
            status_icon = "🌟" if score_info['status'] == 'excellent' else "✅" if score_info['status'] == 'good' else "⚠️"
            print(f"  {status_icon} {score_info['name']}: {score_info['score']:.1f}/100 (weight: {score_info['weight']}%)")
        
        # Key insights
        print(f"\n💡 KEY INSIGHTS:")
        for insight in dashboard['insights']:
            print(f"  {insight}")
        
        # Top recommendations
        print(f"\n🔧 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(dashboard['recommendations'][:5], 1):
            print(f"  {i}. {rec}")
        
        # Summary stats
        total_audits = dashboard['metadata']['audits_run']
        print(f"\n📊 SUMMARY:")
        print(f"  🔍 Audits completed: {total_audits}")
        print(f"  📅 Report generated: {dashboard['metadata']['audit_timestamp']}")
        print(f"  📄 Full dashboard saved to: {output_file}")
        
        print("\n" + "=" * 70)

def main():
    """Run the complete quality audit suite"""
    suite = QualityAuditSuite()
    suite.generate_report()

if __name__ == "__main__":
    main() 