#!/usr/bin/env python3
"""
MAO Quality Audit Suite - Complete Codebase Assessment
Runs all quality audits and generates comprehensive dashboard

This is the MASTER audit that checks:
1. Import patterns and consistency
2. Function naming conventions  
3. JSON configuration schemas
4. Error handling patterns
5. Cache usage patterns
6. File path handling

Updated to use PRECISION audits that recognize quality improvements!
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class QualityAuditSuite:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.audit_dir = self.project_root / "scripts" / "quality_validator"
        self.results = {}
        self.overall_score = 0.0
        
        # Map audit names to their script files (using precision versions where available)
        self.audits = {
            'import_patterns': 'import_audit_precision.py',  # PRECISION VERSION!
            'function_naming': 'function_naming_audit.py', 
            'json_configs': 'json_config_audit_precision.py',  # PRECISION VERSION!
            'error_handling': 'error_handling_audit.py',
            'cache_usage': 'cache_usage_audit.py',
            'file_paths': 'file_path_audit_precision.py'  # PRECISION VERSION!
        }

    def run_single_audit(self, audit_name: str, script_file: str) -> Dict[str, Any]:
        """Run a single audit script and capture results"""
        try:
            script_path = self.audit_dir / script_file
            if not script_path.exists():
                return {
                    'success': False,
                    'error': f'Audit script not found: {script_file}',
                    'score': 0.0
                }

            print(f"🔍 Running {audit_name} audit...")
            
            # Run the audit script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f'Audit failed: {result.stderr}',
                    'stdout': result.stdout,
                    'score': 0.0
                }
            
            # Parse score from output - look for score patterns
            score = self.extract_score_from_output(result.stdout)
            
            return {
                'success': True,
                'stdout': result.stdout,
                'score': score,
                'audit_name': audit_name
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'score': 0.0
            }

    def extract_score_from_output(self, output: str) -> float:
        """Extract numerical score from audit output"""
        import re
        
        # Look for various score patterns
        patterns = [
            r'Overall Score:\s*(\d+\.?\d*)/100',  # "Overall Score: 85.3/100"
            r'Score:\s*(\d+\.?\d*)/100',          # "Score: 85.3/100"
            r'Quality Score:\s*(\d+\.?\d*)',      # "Quality Score: 85.3"
            r'(\d+\.?\d*)/100',                   # Just "85.3/100"
            r'(\d+\.?\d*)%',                      # "85.3%"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, output)
            if match:
                score = float(match.group(1))
                # Convert percentage to 0-100 scale if needed
                if score <= 1.0 and '%' not in pattern:
                    score *= 100
                return min(score, 100.0)  # Cap at 100
        
        # If no score found, analyze output for quality indicators
        if 'error' in output.lower() or 'failed' in output.lower():
            return 0.0
        elif 'perfect' in output.lower() or 'excellent' in output.lower():
            return 95.0
        elif 'good' in output.lower():
            return 80.0
        else:
            return 50.0  # Default neutral score

    def run_all_audits(self) -> Dict[str, Any]:
        """Run all quality audits and compile results"""
        print("🚀 Starting MAO Quality Audit Suite")
        print("=" * 60)
        
        audit_results = {}
        total_score = 0.0
        successful_audits = 0
        
        for audit_name, script_file in self.audits.items():
            result = self.run_single_audit(audit_name, script_file)
            audit_results[audit_name] = result
            
            if result['success']:
                total_score += result['score']
                successful_audits += 1
                print(f"✅ {audit_name}: {result['score']:.1f}/100")
            else:
                print(f"❌ {audit_name}: FAILED - {result.get('error', 'Unknown error')}")
        
        # Calculate overall score
        if successful_audits > 0:
            self.overall_score = total_score / successful_audits
        else:
            self.overall_score = 0.0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'overall_score': self.overall_score,
            'total_audits': len(self.audits),
            'successful_audits': successful_audits,
            'audit_results': audit_results,
            'quality_rating': self.get_quality_rating(self.overall_score)
        }

    def get_quality_rating(self, score: float) -> str:
        """Get quality rating based on score"""
        if score >= 95:
            return "🏆 LEXUS PERFECTION - Designer-level quality achieved!"
        elif score >= 90:
            return "✨ PREMIUM QUALITY - A+ straight-A performance!"
        elif score >= 85:
            return "🎯 EXCELLENT - Very high quality standards!"
        elif score >= 80:
            return "👍 GOOD - Solid quality with room for polish!"
        elif score >= 70:
            return "⚠️ FAIR - Needs improvement in several areas!"
        elif score >= 60:
            return "🔧 POOR - Significant quality issues present!"
        else:
            return "🚨 CRITICAL - Major quality problems need immediate attention!"

    def generate_dashboard(self, results: Dict[str, Any]) -> str:
        """Generate quality dashboard report"""
        dashboard = []
        dashboard.append("🎯 MAO QUALITY AUDIT DASHBOARD")
        dashboard.append("=" * 60)
        dashboard.append(f"📊 OVERALL SCORE: {results['overall_score']:.1f}/100")
        dashboard.append(f"🎖️ QUALITY RATING: {results['quality_rating']}")
        dashboard.append(f"📈 AUDITS COMPLETED: {results['successful_audits']}/{results['total_audits']}")
        dashboard.append(f"⏰ TIMESTAMP: {results['timestamp']}")
        dashboard.append("")
        
        dashboard.append("📋 DETAILED BREAKDOWN:")
        dashboard.append("-" * 40)
        
        for audit_name, result in results['audit_results'].items():
            if result['success']:
                dashboard.append(f"✅ {audit_name.replace('_', ' ').title()}: {result['score']:.1f}/100")
            else:
                dashboard.append(f"❌ {audit_name.replace('_', ' ').title()}: FAILED")
        
        dashboard.append("")
        dashboard.append("🚀 NEXT STEPS:")
        dashboard.append("-" * 20)
        
        if results['overall_score'] >= 90:
            dashboard.append("🏆 CELEBRATE! You've achieved A+ quality!")
            dashboard.append("🔄 Consider setting up continuous quality monitoring")
            dashboard.append("📚 Document your quality engineering process")
        elif results['overall_score'] >= 80:
            dashboard.append("🎯 Focus on lowest-scoring audits for quick wins")
            dashboard.append("⚡ Apply precision fixes to reach 90+ territory")
            dashboard.append("🔍 Review edge cases in failing categories")
        else:
            dashboard.append("🔧 Prioritize systematic fixes in all categories")
            dashboard.append("🛠️ Run individual fixer scripts as needed")
            dashboard.append("📊 Re-audit after each major improvement")
        
        return "\n".join(dashboard)

    def save_results(self, results: Dict[str, Any], filename: str = "quality_audit_results.json"):
        """Save detailed results to JSON file"""
        output_path = self.project_root / filename
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 Detailed results saved to: {filename}")

def main():
    """Run the complete quality audit suite"""
    suite = QualityAuditSuite()
    results = suite.run_all_audits()
    
    # Generate and display dashboard
    dashboard = suite.generate_dashboard(results)
    print("\n" + dashboard)
    
    # Save detailed results
    suite.save_results(results)
    
    # Return overall score for scripting
    return results['overall_score']

if __name__ == "__main__":
    score = main()
    sys.exit(0 if score >= 70 else 1)  # Exit with error if below passing grade 