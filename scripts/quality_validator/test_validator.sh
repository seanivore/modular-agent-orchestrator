#!/bin/bash

# MAO v4 Quality Validator Test Script
# Tests the validator itself to ensure it works correctly

echo "🧪 Testing MAO v4 Quality Validator..."

# Colors for output
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BLUE='\033[94m'
BOLD='\033[1m'
END='\033[0m'

# Test functions
test_validator_exists() {
    echo -e "${BLUE}Testing: Validator script exists...${END}"
    
    if [ -f "./mao-validate" ]; then
        echo -e "${GREEN}✅ mao-validate command found${END}"
        return 0
    else
        echo -e "${RED}❌ mao-validate command not found${END}"
        return 1
    fi
}

test_validator_runs() {
    echo -e "${BLUE}Testing: Validator runs without crashing...${END}"
    
    if ./mao-validate --help > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Validator runs successfully${END}"
        return 0
    else
        echo -e "${RED}❌ Validator failed to run${END}"
        return 1
    fi
}

test_project_structure() {
    echo -e "${BLUE}Testing: Project structure detection...${END}"
    
    # Check if tools directory exists
    if [ -d "tools" ]; then
        echo -e "${GREEN}✅ Tools directory found${END}"
    else
        echo -e "${YELLOW}⚠️  Tools directory not found (expected for testing)${END}"
    fi
    
    # Check if orchestrator directory exists
    if [ -d "orchestrator" ]; then
        echo -e "${GREEN}✅ Orchestrator directory found${END}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Orchestrator directory not found (expected for testing)${END}"
        return 0
    fi
}

run_sample_validation() {
    echo -e "${BLUE}Testing: Running sample validation...${END}"
    
    # Run validator with current project
    echo -e "${YELLOW}🔍 Running validator on current project...${END}"
    ./mao-validate
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ All validations passed!${END}"
    elif [ $exit_code -eq 1 ]; then
        echo -e "${YELLOW}⚠️  Validation found issues (expected during development)${END}"
    else
        echo -e "${RED}❌ Validator crashed or had unexpected error${END}"
        return 1
    fi
    
    return 0
}

test_specific_validators() {
    echo -e "${BLUE}Testing: Individual validator components...${END}"
    
    # Test if we can import the validator (basic syntax check)
    python3 -c "
import ast
import sys
try:
    with open('scripts/quality_validator/mao_validator.py', 'r') as f:
        content = f.read()
    ast.parse(content)
    print('✅ Validator Python syntax is valid')
except FileNotFoundError:
    print('⚠️  Validator script not found (run install script first)')
    sys.exit(1)
except SyntaxError as e:
    print(f'❌ Syntax error in validator: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error checking validator: {e}')
    sys.exit(1)
"
    
    return $?
}

create_test_environment() {
    echo -e "${BLUE}Testing: Creating test environment...${END}"
    
    # Create a minimal test structure
    mkdir -p test_project/tools/test_tool
    mkdir -p test_project/orchestrator
    
    # Create test files
    cat > test_project/tools/test_tool/test_tool.py << 'EOF'
from cache.cache_system import CacheManager
from error_handling import handle_errors

class TestTool:
    def __init__(self):
        self.cache = CacheManager()
    
    def estimate_cost(self, params):
        return 0.001
EOF

    cat > test_project/tools/test_tool/button_test_tool.py << 'EOF'
def create_button_snippet(params, model="claude-sonnet-4"):
    return "test button code"
EOF

    cat > test_project/tools/test_tool/ui_test_tool.py << 'EOF'
def display_test_tool_result(result):
    print(f"Result: {result}")
EOF

    cat > test_project/tools/test_tool/tool_test_tool.json << 'EOF'
{
    "name": "test_tool",
    "version": "1.0.0",
    "description": "Test tool for validation",
    "capabilities": ["testing"]
}
EOF

    echo -e "${GREEN}✅ Test environment created${END}"
}

cleanup_test_environment() {
    echo -e "${BLUE}Cleaning up test environment...${END}"
    
    if [ -d "test_project" ]; then
        rm -rf test_project
        echo -e "${GREEN}✅ Test environment cleaned up${END}"
    fi
}

# Main test execution
main() {
    echo -e "${BOLD}🧪 MAO v4 Quality Validator Test Suite${END}"
    echo "=" * 50
    
    local failed_tests=0
    local total_tests=0
    
    # Run tests
    tests=(
        "test_validator_exists"
        "test_project_structure" 
        "test_specific_validators"
        "create_test_environment"
        "run_sample_validation"
    )
    
    for test_func in "${tests[@]}"; do
        echo ""
        ((total_tests++))
        
        if $test_func; then
            echo -e "${GREEN}✅ $test_func PASSED${END}"
        else
            echo -e "${RED}❌ $test_func FAILED${END}"
            ((failed_tests++))
        fi
    done
    
    # Cleanup
    cleanup_test_environment
    
    # Results
    echo ""
    echo -e "${BOLD}📊 Test Results:${END}"
    echo "Tests passed: $((total_tests - failed_tests))/$total_tests"
    
    if [ $failed_tests -eq 0 ]; then
        echo -e "${GREEN}${BOLD}🎉 All tests passed! Validator is ready to use!${END}"
        echo ""
        echo -e "${BLUE}Next steps:${END}"
        echo "1. Copy the validator Python code to scripts/quality_validator/mao_validator.py"
        echo "2. Run: ./mao-validate to validate your MAO v4 project"
        echo "3. Add to your CI/CD pipeline for automated quality checks"
        return 0
    else
        echo -e "${RED}${BOLD}❌ $failed_tests test(s) failed. Please fix issues before using the validator.${END}"
        return 1
    fi
}

# Help function
show_help() {
    echo "MAO v4 Quality Validator Test Script"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --help, -h     Show this help message"
    echo "  --clean        Clean up test environment only"
    echo ""
    echo "This script tests the MAO Quality Validator to ensure it works correctly."
}

# Parse arguments
case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    --clean)
        cleanup_test_environment
        exit 0
        ;;
    *)
        main "$@"
        exit $?
        ;;
esac