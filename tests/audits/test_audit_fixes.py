#!/usr/bin/env python3
"""
Import Test Script - Verify All Audit Fixes Work
Test that all imports work correctly after the error handling fixes
"""

import sys
import os
from pathlib import Path

# Debug output
print("🔍 DEBUG INFO:")
print(f"Current working directory: {os.getcwd()}")
print(f"Script location: {__file__}")
print(f"Python path: {sys.path[:3]}...")  # Just first 3 entries
print(f"orchestrator directory exists: {os.path.exists('orchestrator')}")
print(f"orchestrator/__init__.py exists: {os.path.exists('orchestrator/__init__.py')}")

# Add project root to Python path (THIS GOES HERE - BEFORE THE FUNCTION)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
print(f"Added to Python path: {project_root}")
print("")

def test_imports():
    """Test all critical imports work correctly"""
    print("🧪 Testing Import Fixes...")
    print("=" * 50)
    
    # Test 1: Error Handling Classes
    try:
        from orchestrator.error_handling import (
            OrchestrationError,
            ValidationError, 
            ProcessingError,
            ResourceError,
            APIError,
            handle_errors,
            setup_orchestrator_logging
        )
        print("✅ Error handling imports: SUCCESS")
        print(f"   • OrchestrationError: {OrchestrationError}")
        print(f"   • ValidationError: {ValidationError}")
        print(f"   • setup_orchestrator_logging: {setup_orchestrator_logging}")
    except ImportError as e:
        print(f"❌ Error handling imports: FAILED - {e}")
        return False
    
    # Test 2: Cache System
    try:
        from orchestrator.cache import CacheManager, CacheEntry
        print("✅ Cache system imports: SUCCESS")
        print(f"   • CacheManager: {CacheManager}")
        print(f"   • CacheEntry: {CacheEntry}")
    except ImportError as e:
        print(f"❌ Cache system imports: FAILED - {e}")
        return False
    
    # Test 3: Terminal Interface
    try:
        from interfaces.ui_terminal import TerminalInterface, TerminalDisplay
        print("✅ Terminal interface imports: SUCCESS")
        print(f"   • TerminalInterface: {TerminalInterface}")
        print(f"   • TerminalDisplay: {TerminalDisplay}")
    except ImportError as e:
        print(f"❌ Terminal interface imports: FAILED - {e}")
        return False
    
    # Test 4: Sample Tool Imports (to verify error handling works)
    try:
        from tools.file_operations.file_operations import read_file
        from tools.web_search.web_search import perform_web_search
        print("✅ Tool imports: SUCCESS")
        print(f"   • file_operations.read_file: {read_file}")
        print(f"   • web_search.perform_web_search: {perform_web_search}")
    except ImportError as e:
        print(f"❌ Tool imports: FAILED - {e}")
        return False
    
    # Test 5: Error Class Instantiation
    try:
        # Test creating new error classes
        validation_error = ValidationError("Test validation error", "test_field", "test_value")
        processing_error = ProcessingError("Test processing error", "test_operation", "test_stage")
        
        print("✅ Error class instantiation: SUCCESS")
        print(f"   • ValidationError.error_code: {validation_error.error_code}")
        print(f"   • ProcessingError.message: {processing_error.message}")
    except Exception as e:
        print(f"❌ Error class instantiation: FAILED - {e}")
        return False
    
    # Test 6: Error Handling Decorator
    try:
        @handle_errors(operation_name="test_operation", return_dict=True)
        def test_function():
            return {"status": "success", "message": "Test completed"}
        
        result = test_function()
        print("✅ Error handling decorator: SUCCESS")
        print(f"   • Test function result: {result}")
    except Exception as e:
        print(f"❌ Error handling decorator: FAILED - {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL IMPORT TESTS PASSED!")
    print("✅ Audit fixes are working correctly")
    return True

def test_no_legacy_references():
    """Test that no old references remain"""
    print("\n🔍 Checking for Legacy References...")
    print("=" * 50)
    
    # Check if any old class names are still accessible
    legacy_issues = []
    
    try:
        from orchestrator.error_handling import SFAError
        legacy_issues.append("SFAError still exists")
    except ImportError:
        print("✅ SFAError properly removed")
    
    try:
        from orchestrator.error_handling import setup_sfa_logging
        legacy_issues.append("setup_sfa_logging still exists")
    except ImportError:
        print("✅ setup_sfa_logging properly removed")
    
    try:
        from interfaces.ui_terminal import OCTerminalInterface
        legacy_issues.append("OCTerminalInterface still exists")
    except ImportError:
        print("✅ OCTerminalInterface properly removed")
    
    if legacy_issues:
        print("\n❌ LEGACY REFERENCE ISSUES FOUND:")
        for issue in legacy_issues:
            print(f"   • {issue}")
        return False
    
    print("\n✅ No legacy references found")
    return True

if __name__ == "__main__":
    print("🧪 MAO AUDIT FIXES - IMPORT TEST")
    print("Testing that all error handling and interface fixes work correctly")
    print("")
    
    # Run tests
    imports_ok = test_imports()
    legacy_ok = test_no_legacy_references()
    
    if imports_ok and legacy_ok:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("The audit fixes have been successfully applied.")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Check the errors above and fix any remaining issues.")
        sys.exit(1)